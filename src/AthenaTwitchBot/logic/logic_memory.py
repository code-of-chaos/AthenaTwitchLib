# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Callable, Coroutine, Optional

# Athena Packages

# Local Imports
from AthenaTwitchBot.logic.logic_types import CommandLogic, MessageLogic

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class _LogicMemory:
    """
    Class that holds all logic containing command access and assignment
    """
    msg_command: dict[tuple[str, str]:CommandLogic]
    msg_normal:dict[str:MessageLogic]

    def __init__(self):
        self.msg_command = {}
        self.msg_normal = {}

    # ------------------------------------------------------------------------------------------------------------------
    # - Logic for user commands -
    # ------------------------------------------------------------------------------------------------------------------
    def assign_as_command(self,logic:CommandLogic, channel:str):
        """
        Method to assign a coroutine as to a specific command that is run on a specific channel
        """
        if known_coroutine:=(self.msg_command.get(cmd_key:=(channel, logic.cmd_name), False)):
            raise KeyError(
                f"The combination of `{cmd_key}` already existed in the mapping,\nwith callback: `{known_coroutine}`"
            )
        # Else:
        self.msg_command[cmd_key] = logic

    def get_command_logic(self, channel:str, cmd_name:str) -> CommandLogic|None:
        return self.msg_command.get((channel, cmd_name), None)

    # ------------------------------------------------------------------------------------------------------------------
    # - Logic for normal user messages -
    # ------------------------------------------------------------------------------------------------------------------
    def assign_as_normal_message(self,logic:MessageLogic, channel:str):
        if known_coroutine := self.msg_normal.get(channel, False):
            raise KeyError(
                f"The key `{channel}` already existed in the mapping,\nwith callback: `{known_coroutine}`"
            )
        # Else:
        self.msg_normal[channel] = logic

    def get_normal_message_logic(self, channel: str) -> MessageLogic | None:
        return self.msg_normal.get(channel, None)


# ----------------------------------------------------------------------------------------------------------------------
# Basically a glorified singleton
LogicMemory = _LogicMemory()