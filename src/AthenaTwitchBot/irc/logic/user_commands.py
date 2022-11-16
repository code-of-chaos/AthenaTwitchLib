# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

# Athena Packages

# Local Imports
from AthenaTwitchBot.logic._logic import BaseLogic
from AthenaTwitchBot.message_context import MessageContext
from AthenaTwitchBot.tags import TagsPRIVMSG
from AthenaTwitchBot.bot_logger import BotLogger

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class UserCommandData:
    cmd_names:list[str]|str
    broadcaster_only:bool=False
    mod_only:bool=False
    sub_only:bool=False
    vip_only:bool=False
    all_users:bool=True

    def __post_init__(self):
        if isinstance(self.cmd_names, str):
            self.cmd_names = [self.cmd_names]
        elif not isinstance(self.cmd_names, list):
            raise ValueError

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class UserCommandLogic(BaseLogic):
    _commands: dict[str: Callable]

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, *kwargs)
        obj._commands = {
            name:fnc
            for fnc in obj._logic_components
            for name in fnc._data.cmd_names
        }
        return obj

    def execute_command(self, cmd_name:str, message_context:MessageContext):
        if not (fnc := self._commands.get(cmd_name, False)):
            return

        match fnc._data, message_context:
            case UserCommandData(broadcaster_only=True), MessageContext(user=user, channel=channel) if user == f":{channel}!{channel}@{channel}].tmi.twitch.tv":
                print("BROADCASTER")
                await fnc(message_context)

            case UserCommandData(mod_only=True), MessageContext(tags=TagsPRIVMSG(moderator=True)):
                print("MOD")
                await fnc(message_context)

            case UserCommandData(sub_only=True), MessageContext(tags=TagsPRIVMSG(subscriber=True)):
                print("SUB")
                await fnc(message_context)

            case UserCommandData(vip_only=True), MessageContext(tags=TagsPRIVMSG(vip=True)):
                print("VIP")
                await fnc(message_context)

            # a command that all users can access
            case UserCommandData(all_users=True), _:
                print("NORMAL")
                await fnc(message_context)

            # in any other cases
            #   This should never happen
            case _,_:
                print("UNKNOWN")
                await BotLogger.logger.log_unknown_message(message_context.text)



    @classmethod
    def command(cls, command_data:UserCommandData):
        def decorator(fnc):
            cls.register_callback_as_logical_component(fnc)
            fnc._data = command_data

            return fnc
        return decorator

    @classmethod
    def command_for_mods(cls, command_data:UserCommandData):
        command_data.mod_only = True

        def decorator(fnc):
            cls.register_callback_as_logical_component(fnc)
            fnc._data = command_data

            return fnc
        return decorator