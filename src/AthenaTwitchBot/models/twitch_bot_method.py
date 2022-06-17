# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class TwitchBotMethod:
    callback:Callable
    channels:list[str] = field(default_factory=list)

    # command related attributes
    is_command:bool = False
    command_str:list[str] = field(default_factory=list)
    command_args:bool = False
    command_case_sensitive:bool = False


    # scheduled task related attributes
    is_task:bool = False

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)