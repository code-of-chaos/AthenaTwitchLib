# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field, KW_ONLY
from typing import Coroutine

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True, unsafe_hash=True)
class CommandLogic:
    name:str # without the prefix (!,?,...)

    # All below this are keyword only
    _: KW_ONLY
    coroutine: Coroutine
    user:bool=True
    vip:bool=False
    sub:bool=False
    mod:bool=False

    channels:set[str] = field(default_factory=set)