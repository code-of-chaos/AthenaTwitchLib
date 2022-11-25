# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import aiosqlite
import asyncio
from dataclasses import dataclass, asdict
import json

# Athena Packages
from AthenaLib.constants.types import PATHLIKE
from AthenaLib.general.sql import sanitize_sql
from AthenaLib.database_connectors.async_sqlite import ConnectorAioSqlite

# Local Imports
from AthenaTwitchLib.irc.logic._logic import BaseCommandLogic
from AthenaTwitchLib.irc.message_context import MessageCommandContext
from AthenaTwitchLib.logger import IrcLogger, SectionIRC
from AthenaTwitchLib.irc.data.enums import BotEvent, OutputTypes, CommandTypes
from AthenaTwitchLib.irc.data.sql import TBL_LOGIC_COMMANDS

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class CommandData:
    """
    Dataclass to hold the command's parameters.
    The data is gathered from the database.
    """
    id:int
    channel:str
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
            section=SectionIRC.CMD_DATA,
            text=json.dumps(asdict(self))
        )
# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CommandLogicSqlite(BaseCommandLogic):
    """
    Logic system for commands that are retrieved from a database.
    The database in this case, is an SQLite db file.
    """
    _connector: ConnectorAioSqlite

    def __new__(cls, *args,path:PATHLIKE, **kwargs):
        obj = super().__new__(cls, *args, *kwargs)
        
        obj._connector = ConnectorAioSqlite(path=path)
        asyncio.get_running_loop().create_task(obj._connector.db_create(queries=TBL_LOGIC_COMMANDS))

        return obj

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
            IrcLogger.log_error()
            raise ValueError(data.output_type)

    async def get_command(self, context:MessageCommandContext) -> CommandData|False:
        """
        Method which retrieves the command from the database, if present.
        Otherwise, will  return False.
        """
        async with self._connector.connect(auto_commit=False) as db:

            channel = sanitize_sql(context.channel)
            cmd = sanitize_sql(context.command)
            arg = sanitize_sql(context.args[0]) if context.args else "*"

            async with db.execute(f"""
                SELECT * 
                FROM commands 
                WHERE (
                    (`channel`,`command_name`,`command_arg`) = ('{channel}', '{cmd}','{arg}')
                    OR (`channel`,`command_name`,`command_arg`) = ('{channel}','{cmd}','*')
                )
                ORDER BY `command_arg` DESC 
                LIMIT 1;
            """) as cursor: #type: aiosqlite.Cursor

                # Quit if nothing has been found
                if (row := await cursor.fetchone()) is None:
                    return False

                match context, data := CommandData(**dict(row)):
                    case MessageCommandContext(args=_), CommandData(command_arg=None|"*"):
                        return data

                    case MessageCommandContext(args=args), CommandData(command_arg=stored_arg) if stored_arg == args[0]:
                        return data

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
            case CommandData(command_type=CommandTypes.DEFAULT):
                await self.output(context, data, data.output_text)

            case CommandData(command_type=CommandTypes.ARGS) if context.args:
                await self.output( context, data, data.output_text, format_={f"args_{i}":a for i, a in enumerate(context.args)})

            case CommandData(command_type=CommandTypes.EXIT):
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
