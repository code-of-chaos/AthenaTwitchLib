# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotData:
    """
    Data class for a Twitch Bot
    The bot_data itself shouldn't have special methods for commands and tasks,
        these are controlled by classes which inherit from `CommandLogic` and `TaskLogic` respectively
    """
    name:str
    oath_token:str
    join_channel:list[str] = field(default_factory=list)
    join_message:str = None
    prefix:str = "!"

    capability_tags:bool=True,
    capability_commands:bool=False,
    capability_membership:bool=False,