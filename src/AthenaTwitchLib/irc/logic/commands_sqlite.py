# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import pathlib
from typing import AsyncContextManager
import contextlib
import aiosqlite
import enum
import asyncio
from dataclasses import dataclass, asdict
import json

# Athena Packages
from AthenaLib.constants.types import PATHLIKE

from AthenaTwitchLib.irc.data.enums import BotEvent
# Local Imports
from AthenaTwitchLib.irc.logic._logic import BaseCommandLogic
from AthenaTwitchLib.irc.message_context import MessageCommandContext
from AthenaTwitchLib.logger import IrcSection, IrcLogger

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
SQL_CREATE_TABLES:list[str] = [
f"""
CREATE TABLE IF NOT EXISTS `commands`  (
    `id` INTEGER PRIMARY KEY,                               -- internal id
    `command_name` TEXT NOT NULL,                           -- ![command_name]
    `command_arg` TEXT DEFAULT NULL,                        -- if this specific arg is present, execute this record
    `command_type` TEXT NOT NULL,                           -- Type of command, means it has extra logic attached to it
    `allow_user` INTEGER NOT NULL DEFAULT TRUE,
    `allow_sub` INTEGER NOT NULL DEFAULT FALSE,
    `allow_vip` INTEGER NOT NULL DEFAULT FALSE,
    `allow_mod` INTEGER NOT NULL DEFAULT FALSE,
    `allow_broadcaster` INTEGER NOT NULL DEFAULT FALSE,
    `output_text` TEXT NOT NULL DEFAULT 'NO OUTPUT SET',    -- text to output in chat
    `output_type` TEXT NOT NULL DEFAULT 'reply'             -- reply or write output
);
"""
]

@dataclass(slots=True, kw_only=True)
class CommandData:
    id:int
    command_name:str
    command_arg:str|None
    command_type:str|CommandTypes
    allow_user:bool|int
    allow_sub:bool|int
    allow_vip:bool|int
    allow_mod:bool|int
    allow_broadcaster:bool
    output_text:str
    output_type:str|OutputTypes

    def __post_init__(self):
        self.command_type = CommandTypes(self.command_type)
        self.allow_user = bool(self.allow_user)
        self.allow_sub = bool(self.allow_sub)
        self.allow_vip = bool(self.allow_vip)
        self.allow_mod = bool(self.allow_mod)
        self.output_type = OutputTypes(self.output_type)

        # Log to db
        IrcLogger.log_debug(
            section=IrcSection.CMD_DATA,
            text=json.dumps(asdict(self))
        )


class CommandTypes(enum.StrEnum):
    """
    The type of commands that are stored within the database, that then need to be parsed in a specific way
    ---

    - PLAIN : No argument parsing needs to be done within the output text
    - EXIT : command triggers the exit of the bot
    - RESTART : command triggers the restart of the bot
    """

    PLAIN = enum.auto()
    FORMAT = enum.auto()
    EXIT = enum.auto()
    RESTART = enum.auto()

class OutputTypes(enum.StrEnum):
    WRITE = enum.auto()
    REPLY = enum.auto()


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CommandLogicSqlite(BaseCommandLogic):
    """
    Logic system for commands that are retrieved from a database.
    The database in this case, is an SQLite db file.
    """
    db_path:pathlib.Path

    def __new__(cls, *args, db_path:PATHLIKE, **kwargs):
        obj = super().__new__(cls, *args, *kwargs)
        obj.db_path = pathlib.Path(db_path)

        asyncio.get_running_loop().create_task(cls._db_create_tables(obj))

        return obj

    # ------------------------------------------------------------------------------------------------------------------
    # - DB connection -
    # ------------------------------------------------------------------------------------------------------------------
    @contextlib.asynccontextmanager
    async def _db_connect(self, auto_commit: bool = True) -> AsyncContextManager[aiosqlite.Connection]:
        """
        Async Context manager to easily connect to the database
        Commits all changes to the db, before closing the connection
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            yield db

            if auto_commit:
                await db.commit()

    async def _db_create_tables(self):
        """
        Method which is run at the start of the bot.
        Executes SQL lines, which need to ensure that the correct tables are present on the Database, without overriding
        them if they are already present.
        """
        async with self._db_connect() as db:
            for sql in SQL_CREATE_TABLES:
                await db.execute(sql)

    # ------------------------------------------------------------------------------------------------------------------
    # - Command execution -
    # ------------------------------------------------------------------------------------------------------------------
    async def execute_command(self, context:MessageCommandContext) -> None:
        """
        Main entry point from the Async Protocol, will first try and find a corresponding command within the database
        Afterwards it executes the command, following the correct format
        """
        # stage 1: Retrieve command
        if not (data := await self.get_command(context)): #type: CommandData
            return

        # stage 2: Validate command
        if not self.validate_user(context, data):
            return

        # stage 3: Execute command
        await self.parse_command_type(context, data)


    @staticmethod
    async def output(context: MessageCommandContext, data: CommandData, msg: str, format_:dict=None):

        msg_formatted = msg.format(
            username=context.username,
            channel=context.channel,
            **format_ if format_ is not None else {}
        )

        if data.output_type == OutputTypes.WRITE:
            await context.write(msg_formatted)
        elif data.output_type == OutputTypes.REPLY:
            await context.reply(msg_formatted)
        else:
            raise ValueError(data.output_type)

    async def get_command(self, context:MessageCommandContext) -> CommandData|False:
        """
        Method which retrieves the command from the database, if present.
        Otherwise, will  return False.
        """
        async with self._db_connect(auto_commit=False) as db:
            db: aiosqlite.Connection

            # noinspection SqlType
            async with db.execute(f"SELECT * FROM commands WHERE `command_name` == '{context.command}'") as cursor:
                for row in await cursor.fetchall(): #type: aiosqlite.Row
                    match context, data := CommandData(**dict(row)):
                        case MessageCommandContext(args=_), CommandData(command_arg=None|"*"):
                            return data

                        case MessageCommandContext(args=args), CommandData(command_arg=stored_arg) if stored_arg == args[0]:
                            return data

                        case _,_:
                            continue
        return False


    @staticmethod
    def validate_user(context:MessageCommandContext, data:CommandData) -> bool:
        """
        Method checks if the user can use the command
        """
        if data.allow_user:
            return True
        elif data.allow_broadcaster and context.user == f":{context.channel}!{context.channel}@{context.channel}.tmi.twitch.tv":
            return True
        elif data.allow_mod and context.tags.moderator:
            return True
        elif data.allow_sub and context.tags.subscriber:
            return True
        elif data.allow_vip and context.tags.vip:
            return True

        return False

    async def parse_command_type(self, context:MessageCommandContext, data:CommandData) -> None:
        """
        If a command has been found, parse it's args and text corresponding to the CommandType
        """
        match data:
            case CommandData(command_type=CommandTypes.PLAIN):
                await self.output(context, data, data.output_text)

            case CommandData(command_type=CommandTypes.FORMAT) if context.args:
                await self.output( context, data, data.output_text, format_={f"args_{i}":a for i, a in enumerate(context.args)})

            case CommandData(command_type=CommandTypes.EXIT):
                context.bot_event_future.set_result(BotEvent.EXIT)

            case CommandData(command_type=CommandTypes.RESTART):
                # restart has a deferred argument parsing
                #   Meaning that the first argument can be interpreted as a delay integer, in seconds
                if context.args:
                    try:
                        await asyncio.gather(
                            self.output(context, data, data.output_text.format(delay=(delay:=int(context.args[0])))),
                            asyncio.sleep(delay)
                        )
                    # delay couldn't be cast into a string
                    except ValueError:
                        pass

                # Even if there are args, we still need to trigger the restart
                context.bot_event_future.set_result(BotEvent.RESTART)
