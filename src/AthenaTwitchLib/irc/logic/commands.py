# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Callable
import json

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.logic._logic import BaseHardCodedLogic, BaseCommandLogic,register_callback_as_logical_component
from AthenaTwitchLib.irc.message_context import MessageCommandContext
from AthenaTwitchLib.irc.tags import TagsPRIVMSG
from AthenaTwitchLib.logger import SectionIRC, IrcLogger

from AthenaTwitchLib.api.api_connection import ApiConnection

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class CommandData:
    """
    Simple dataclass to hold basic information about the hard coded command.
    Meant for the `CommandLogic` class to differentiate what to do when it receives a command from chat
    ===

    - cmd_names:             All possible command Names
    - allow_user:            Boolean option to allow all users to use this command
    - allow_sub:             Boolean option to allow subscribers to use this command
    - allow_vip:             Boolean option to allow VIP's to use this command
    - allow_mod:             Boolean option to allow moderators to use this command
    - allow_broadcaster:     Boolean option to allow broadcasters to use this command

    """
    cmd_names:list[str]|str
    allow_user:bool=field(kw_only=True, default=True)
    allow_sub:bool=field(kw_only=True, default=False)
    allow_vip:bool=field(kw_only=True, default=False)
    allow_mod:bool=field(kw_only=True, default=False)
    allow_broadcaster:bool=field(kw_only=True, default=False)

    def __post_init__(self):
        if isinstance(self.cmd_names, str):
            self.cmd_names = [self.cmd_names]
        elif not isinstance(self.cmd_names, list):
            raise ValueError

        # Log to db
        IrcLogger.log_debug(section=SectionIRC.CMD_DATA, data=json.dumps(asdict(self)))

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CommandLogic(BaseHardCodedLogic,BaseCommandLogic):
    """
    Logic system behind hard coded commands.
    """
    _commands: dict[str: Callable]

    def __init__(self, api_connection: ApiConnection):
        # Run the init of BaseCommandLogic
        super(CommandLogic, self).__init__(api_connection=api_connection)

        # Gather all commands
        self._commands = {
            name:fnc
            for fnc in self._logic_components
            for name in fnc._data.cmd_names
        }

    async def execute_command(self, context:MessageCommandContext):
        """
        Main entry point from the Async Protocol, will try and find a corresponding command within the Bot.
        """
        # Get the command from the stored bot's method.
        #   If it can't be found, skip the entire function
        if not (fnc := self._commands.get(context.command, False)):
            IrcLogger.log_debug(section=SectionIRC.CMD_UNKNOWN, data=context.original_line)
            return

        # When a callback is found
        #   Execute command
        match fnc._data, context:

            # a command that all users can access
            case CommandData(allow_user=True), _:
                await fnc(context)

            case CommandData(allow_broadcaster=True), MessageCommandContext(user=user, channel=channel) if user == f":{channel}!{channel}@{channel}.tmi.twitch.tv":
                await fnc(context)

            case CommandData(allow_mod=True), MessageCommandContext(tags=TagsPRIVMSG(moderator=True)):
                await fnc(context)

            case CommandData(allow_sub=True), MessageCommandContext(tags=TagsPRIVMSG(subscriber=True)):
                await fnc(context)

            case CommandData(allow_vip=True), MessageCommandContext(tags=TagsPRIVMSG(vip=True)):
                await fnc(context)

            # in any other cases
            #   This should never happen
            case _,_:
                IrcLogger.log_warning(section=SectionIRC.CMD_NOT_PARSABLE, data=context.original_line)

    @staticmethod
    def command(command_data:CommandData):
        """
        Decorator to be used by the Bot, to assign a method as a command.
        """
        def decorator(fnc):
            register_callback_as_logical_component(fnc)
            fnc._data = command_data

            return fnc
        return decorator

    @staticmethod
    def command_subscriber(command_data:CommandData):
        """
        Decorator to be used by the Bot, to assign a method as a command only to be used by a Subscriber.
        The command will also be able to be used by Mods and Broadcasters
        """
        command_data.allow_user = False
        command_data.allow_sub = True
        command_data.allow_vip = False
        command_data.allow_mod = True
        command_data.allow_broadcaster = True

        def decorator(fnc):
            register_callback_as_logical_component(fnc)
            fnc._data = command_data

            return fnc
        return decorator

    @staticmethod
    def command_vip(command_data:CommandData):
        """
        Decorator to be used by the Bot, to assign a method as a command only to be used by a VIP.
        The command will also be able to be used by Mods and Broadcasters
        """
        command_data.allow_user = False
        command_data.allow_sub = False
        command_data.allow_vip = True
        command_data.allow_mod = True
        command_data.allow_broadcaster = True

        def decorator(fnc):
            register_callback_as_logical_component(fnc)
            fnc._data = command_data

            return fnc
        return decorator

    @staticmethod
    def command_moderator(command_data:CommandData):
        """
        Decorator to be used by the Bot, to assign a method as a command only to be used by a Moderator.
        The command will also be able to be used by Broadcasters
        """
        command_data.allow_user = False
        command_data.allow_sub = False
        command_data.allow_vip = True
        command_data.allow_mod = True
        command_data.allow_broadcaster = True

        def decorator(fnc):
            register_callback_as_logical_component(fnc)
            fnc._data = command_data

            return fnc
        return decorator

    @staticmethod
    def command_broadcaster(command_data:CommandData):
        """
        Decorator to be used by the Bot, to assign a method as a command only to be used by a Broadcasters.
        """
        command_data.allow_user = False
        command_data.allow_sub = False
        command_data.allow_vip = False
        command_data.allow_mod = False
        command_data.allow_broadcaster = True

        def decorator(fnc):
            register_callback_as_logical_component(fnc)
            fnc._data = command_data

            return fnc
        return decorator