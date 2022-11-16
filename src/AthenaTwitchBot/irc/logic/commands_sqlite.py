# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import pathlib
from typing import AsyncContextManager, Coroutine
import contextlib
import aiosqlite
import enum
import asyncio
from dataclasses import field, dataclass

# Athena Packages
from AthenaLib.constants.types import PATHLIKE

# Local Imports
from AthenaTwitchBot.irc.logic._logic import BaseLogic
from AthenaTwitchBot.irc.message_context import MessageCommandContext

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


class CommandTypes(enum.StrEnum):
    No_ARGS = enum.auto()
    WITH_ARGS = enum.auto()

class OutputTypes(enum.StrEnum):
    WRITE = enum.auto()
    REPLY = enum.auto()

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CommandLogicSqlite(BaseLogic):
    db_path:pathlib.Path

    def __new__(cls, *args, db_path:PATHLIKE, **kwargs):
        obj = super().__new__(cls, *args, *kwargs)
        obj.db_path = pathlib.Path(db_path)

        asyncio.get_running_loop().create_task(obj._db_create_tables())

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
        async with self._db_connect() as db:
            for sql in SQL_CREATE_TABLES:
                await db.execute(sql)

    async def get_command(self, context:MessageCommandContext) -> Coroutine|False:
        async with self._db_connect(auto_commit=False) as db:
            db: aiosqlite.Connection

            async with db.execute(f"SELECT * FROM commands WHERE `command_name` == '{context.command}'") as cursor:
                for row in await cursor.fetchall(): #type: aiosqlite.Row
                    data = CommandData(**dict(row))

                    match context, data:
                        case MessageCommandContext(args=['']), CommandData(command_arg=None):
                            print("no arg", data)
                        case MessageCommandContext(args=args), CommandData(command_arg=stored_arg) if args[0] == stored_arg:
                            print("with arg", data)
                        case _,_:
                            print("not found", data)



    async def execute_command(self, context:MessageCommandContext):
        if not (coroutine := await self.get_command(context)):
            return
        # if not (fnc := self._commands.get(context.command, False)):
        #     await self._logger.log_unknown_message(context.original_line)
        #     return
        #
        # match fnc._data, context:
        #
        #     # a command that all users can access
        #     case CommandData(allow_user=True), _:
        #         print("NORMAL")
        #         await fnc(context)
        #
        #     case CommandData(allow_broadcaster=True), MessageCommandContext(user=user, channel=channel) if user == f":{channel}!{channel}@{channel}.tmi.twitch.tv":
        #         print("BROADCASTER")
        #         await fnc(context)
        #
        #     case CommandData(allow_mod=True), MessageCommandContext(tags=TagsPRIVMSG(moderator=True)):
        #         print("MOD")
        #         await fnc(context)
        #
        #     case CommandData(allow_sub=True), MessageCommandContext(tags=TagsPRIVMSG(subscriber=True)):
        #         print("SUB")
        #         await fnc(context)
        #
        #     case CommandData(allow_vip=True), MessageCommandContext(tags=TagsPRIVMSG(vip=True)):
        #         print("VIP")
        #         await fnc(context)
        #
        #     # in any other cases
        #     #   This should never happen
        #     case _,_:
        #         await self._logger.log_unknown_message(context.original_line)