# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Coroutine
import enum

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True, unsafe_hash=True)
class MessageLogic:
    coroutine: Coroutine
    user:bool=True
    vip:bool=False
    sub:bool=False
    mod:bool=False

    channels:set[str] = field(default_factory=set)

# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True, unsafe_hash=True)
class CommandLogic(MessageLogic):
    cmd_name:str=None # without the prefix (!,?,...)

# ----------------------------------------------------------------------------------------------------------------------
class LogicTypes(enum.Enum):
    MESSAGE = enum.auto()
    COMMAND = enum.auto()