# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import aiosqlite
import asyncio

# Athena Packages
from AthenaLib.constants.types import PATHLIKE
from AthenaLib.database_connectors.async_sqlite import ConnectorAioSqlite
from AthenaLib.general.sql import sanitize_sql

# Local Imports
from AthenaTwitchLib.api.api_connection import ApiConnection
from AthenaTwitchLib.irc.data.enums import ConnectionEvent, OutputTypes, CommandTypes
from AthenaTwitchLib.irc.data.sql import TBL_LOGIC_COMMANDS
from AthenaTwitchLib.irc.logic.types import BaseCommandLogic
from AthenaTwitchLib.irc.message_context import MessageCommandContext
from AthenaTwitchLib.logger import IrcLogger
from AthenaTwitchLib.irc_ext.commands_sqlite.command_data import CommandSqliteData

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CommandLogicSqlite(BaseCommandLogic):
    """
    Logic system for commands that are retrieved from a database.
    The database in this case, is an SQLite db file.
    """
    _connector: ConnectorAioSqlite
    _special_event_mapping: dict[CommandTypes:ConnectionEvent] = {
        CommandTypes.EXIT : ConnectionEvent.EXIT,
        CommandTypes.RESTART: ConnectionEvent.RESTART
    }

    def __init__(self, path:PATHLIKE ,api_connection:ApiConnection):
        # Run the init of BaseCommandLogic
        super(CommandLogicSqlite, self).__init__(api_connection=api_connection)

        # Assemble the connector
        #   Create the database as soon as possible (async function)
        self._connector = ConnectorAioSqlite(path=path)
        asyncio.get_running_loop().create_task(self._connector.db_create(queries=TBL_LOGIC_COMMANDS))


    # ------------------------------------------------------------------------------------------------------------------
    # - Helper Methods -
    # ------------------------------------------------------------------------------------------------------------------
    async def first_arg_wait(self, context:MessageCommandContext, data:CommandSqliteData):
        """
        Simple method that requires the first argument fo a command to be an integer
        Will wait this amount of seconds
        """
        try:
            await asyncio.gather(
                self.output(context, data, data.output_text.format(delay=(delay := int(context.args[0])))),
                asyncio.sleep(delay)
            )
        # delay couldn't be cast into a string
        except ValueError:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    # - Command execution -
    # ------------------------------------------------------------------------------------------------------------------
    async def execute_command(self, context:MessageCommandContext) -> None:
        """
        Main entry point from the Async Protocol, will first try and find a corresponding command within the database
        Afterwards it executes the command, following the correct format
        """
        # stage 1: Retrieve command
        if not (data := await self.get_command(context)): #type: CommandSqliteData
            return

        # stage 2: Validate command
        if not self.validate_user(context, data):
            return

        # stage 3: Execute command
        await self.parse_command_type(context, data)


    @staticmethod
    async def output(context: MessageCommandContext, data: CommandSqliteData, msg: str, format_:dict=None):
        """
        General output function for the Logic class to write to chat.
        """
        # Assemble the msg,
        #   as 99,99% of the time it will not fail
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

    async def get_command(self, context:MessageCommandContext) -> CommandSqliteData | False:
        """
        Method which retrieves the command from the database, if present.
        Otherwise, will  return False.
        """
        async with self._connector.connect(commit=False) as db:

            # Prep some data so the sql query is a little easier to real
            channel = sanitize_sql(context.channel)
            cmd = sanitize_sql(context.command)
            arg = sanitize_sql(context.args[0]) if context.args else "*"

            # SQL query, might need some optimization
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

                # If something has been found
                #   There are two possible states of success:
                #       - no strict args of that kind were defined
                #       - a strict arg was found and will be applied
                #   If all fails,
                #       it'll eventually return the function as false and not execute any further
                match context, data := CommandSqliteData(**dict(row)):
                    case MessageCommandContext(args=_), CommandSqliteData(command_arg=None | "*"):
                        return data

                    case MessageCommandContext(args=args), CommandSqliteData(command_arg=stored_arg) if stored_arg == args[0]:
                        return data

        # Nothing matched
        return False

    @staticmethod
    def validate_user(context:MessageCommandContext, data:CommandSqliteData) -> bool:
        """
        Method checks if the user can use the command
        """
        # Any will return false if nothing checks
        #   True if at least one is successful
        return any((
            data.allow_user,
            data.allow_broadcaster and context.user == f":{context.channel}!{context.channel}@{context.channel}.tmi.twitch.tv",
            data.allow_mod and context.tags.moderator,
            data.allow_sub and context.tags.subscriber,
            data.allow_vip and context.tags.vip,
        ))

    async def parse_command_type(self, context:MessageCommandContext, data:CommandSqliteData) -> None:
        """
        If a command has been found, parse it's args and text corresponding to the CommandType
        """
        match data:
            case CommandSqliteData(command_type=CommandTypes.DEFAULT):
                await self.output(context, data, data.output_text)

            case CommandSqliteData(command_type=CommandTypes.ARGS) if context.args:
                await self.output( context, data, data.output_text, format_={f"args_{i}":a for i, a in enumerate(context.args)})

            # Special type of command
            #   Like the exit or restart commands
            case CommandSqliteData(command_type=cmd_type) if cmd_type in (CommandTypes.EXIT, CommandTypes.RESTART):
                if context.args:
                    await self.first_arg_wait(context=context,data=data)

                # Set the event future to the correct event
                #   constructor will handle the rest
                context.bot_event_future.set_result(self._special_event_mapping.get(cmd_type, None))
