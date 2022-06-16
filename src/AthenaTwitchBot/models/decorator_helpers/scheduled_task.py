# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

# Custom Library
from AthenaLib.models.time import Second, Minute, Hour

# Custom Packages
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, match_args=True, slots=True)
class ScheduledTask:
    delay:int|Second|Minute|Hour
    wait_before:bool
    callback:Callable
    channels:list[TwitchChannel]=None #always set to a channel in the end