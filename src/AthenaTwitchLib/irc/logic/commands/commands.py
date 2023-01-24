# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Callable,ClassVar
import inspect

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.logic.types import BaseCommandLogic
from AthenaTwitchLib.irc.message_context import MessageCommandContext
from AthenaTwitchLib.irc.tags import TagsPRIVMSG
from AthenaTwitchLib.logger import SectionIRC, IrcLogger
from AthenaTwitchLib.irc.logic.commands.command_data import CommandData

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CommandLogic(BaseCommandLogic):
    """
    Logic system behind hard coded commands.
    """
    _logic_components: ClassVar[dict[str: tuple[Callable,CommandData]]] = {}

    async def execute_command(self, context:MessageCommandContext):
        """
        Main entry point from the Async Protocol, will try and find a corresponding command within the connection.
        """
        # Get the command from the stored connection's method.
        #   If it can't be found, skip the entire function
        if not (fnc_and_command_data := CommandLogic._logic_components.get(context.command, False)):
            IrcLogger.log_debug(section=SectionIRC.CMD_UNKNOWN, data=context.original_line)
            return

        # When a callback is found
        #   Execute command
        fnc:Callable = fnc_and_command_data[0]
        command_data:CommandData = fnc_and_command_data[1]

        match command_data, context:
            # a command that all users can access
            case CommandData(allow_user=True), _:
                await fnc(self, context)

            case CommandData(allow_broadcaster=True), MessageCommandContext(user=user, channel=channel) if user == f":{channel}!{channel}@{channel}.tmi.twitch.tv":
                await fnc(self, context)

            case CommandData(allow_mod=True), MessageCommandContext(tags=TagsPRIVMSG(moderator=True)):
                await fnc(self, context)

            case CommandData(allow_sub=True), MessageCommandContext(tags=TagsPRIVMSG(subscriber=True)):
                await fnc(self, context)

            case CommandData(allow_vip=True), MessageCommandContext(tags=TagsPRIVMSG(vip=True)):
                await fnc(self, context)

            # in any other cases
            #   This should never happen
            case _,_:
                IrcLogger.log_warning(section=SectionIRC.CMD_NOT_PARSABLE, data=context.original_line)

    @staticmethod
    def command(command_data:CommandData):
        """
        Decorator to be used by the BotData, to assign a method as a command.
        """
        def decorator(fnc):
            if not inspect.iscoroutinefunction(fnc):
                raise ValueError(f"{fnc} was not a asyncio coroutine")
            # For every possible given name,
            #   assign to logic components
            for name in command_data.cmd_names:
                CommandLogic._logic_components[name]=(fnc, command_data)

            return fnc
        return decorator