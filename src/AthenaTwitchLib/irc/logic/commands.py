# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.logic._logic import BaseLogic,register_callback_as_logical_component
from AthenaTwitchLib.irc.message_context import MessageCommandContext
from AthenaTwitchLib.irc.tags import TagsPRIVMSG

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class CommandData:
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

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CommandLogic(BaseLogic):
    _commands: dict[str: Callable]

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, *kwargs)
        obj._commands = {
            name:fnc
            for fnc in obj._logic_components
            for name in fnc._data.cmd_names
        }

        return obj

    async def execute_command(self, context:MessageCommandContext):
        """
        Main entry point from the Async Protocol, will try and find a corresponding command within the Bot.
        """
        # Get the command from the stored bot's method.
        #   If it can't be found, skip the entire function
        if not (fnc := self._commands.get(context.command, False)):
            await self._logger.log_unknown_message(context.original_line)
            return

        # When a callback is found
        #   Execute command
        match fnc._data, context:

            # a command that all users can access
            case CommandData(allow_user=True), _:
                print("NORMAL")
                await fnc(context)

            case CommandData(allow_broadcaster=True), MessageCommandContext(user=user, channel=channel) if user == f":{channel}!{channel}@{channel}.tmi.twitch.tv":
                print("BROADCASTER")
                await fnc(context)

            case CommandData(allow_mod=True), MessageCommandContext(tags=TagsPRIVMSG(moderator=True)):
                print("MOD")
                await fnc(context)

            case CommandData(allow_sub=True), MessageCommandContext(tags=TagsPRIVMSG(subscriber=True)):
                print("SUB")
                await fnc(context)

            case CommandData(allow_vip=True), MessageCommandContext(tags=TagsPRIVMSG(vip=True)):
                print("VIP")
                await fnc(context)

            # in any other cases
            #   This should never happen
            case _,_:
                await self._logger.log_unknown_message(context.original_line)



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