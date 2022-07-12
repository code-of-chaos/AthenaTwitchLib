# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import  Callable,ClassVar

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotMentioned:
    callback:Callable
    channel:str|TwitchChannel=None


    registered:ClassVar[BotMentioned]=None

    def __post_init__(self):
        if isinstance(self.channel, str):
            self.channel = TwitchChannel(self.channel)

    @classmethod
    def register(cls):
        # make sure the register exists
        if cls.registered is not None:
            raise ValueError("Only one Mentioned Bot command can be allowed at the same time")
        def decorator(fnc):
            cls.registered = cls(callback=fnc)
        return decorator