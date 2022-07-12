# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, ClassVar

# Custom Library
from AthenaLib.models.time import TimeValue, Minute

# Custom Packages
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotTask:
    callback:Callable
    interval:TimeValue=field(default_factory=lambda: Minute(10))
    channel:str|TwitchChannel=None

    registered:ClassVar[list[BotTask]]=None

    def __post_init__(self):
        if isinstance(self.channel, str):
            self.channel = TwitchChannel(self.channel)

    @classmethod
    def register(cls, *,interval:TimeValue=Minute(10)):
        # make sure the register exists
        if cls.registered is None:
            cls.registered = []
        def decorator(fnc):
            cls.registered.append(
                cls(callback=fnc, interval=interval)
            )
        return decorator