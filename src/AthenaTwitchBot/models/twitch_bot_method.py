# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable

# Custom Library
from AthenaLib.models import Second, Minute, Hour
from AthenaLib.functions.time import convert_time_to_seconds

# Custom Packages
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

from AthenaTwitchBot.functions.general import channel_list_to_TwitchChannels

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True, match_args=True)
class TwitchBotMethod:
    channels:list[TwitchChannel|str] = field(default_factory=list)

    # command related attributes
    is_command:bool = False
    command_names:list[str] = field(default_factory=list)
    command_args:bool = False
    command_args_skip_emotes:bool = False
    command_case_sensitive:bool = False

    # scheduled task related attributes
    is_scheduled_task:bool = False
    task_interval:int = 3600 # default is every hour
    task_call_on_startup:bool = False

    # non init stuff
    callback:Callable = field(init=False)
    owner:object = field(init=False, default=None) # defined by TwitchBot

    def __post_init__(self):
        self.channels = channel_list_to_TwitchChannels(self.channels)

    def __call__(self, fnc:Callable):
        self.callback = lambda *args, **kwargs: fnc(self.owner, *args, **kwargs)
        return self # needs to return self to be assigned to the function's call

    # ------------------------------------------------------------------------------------------------------------------
    # - Command Method -
    # ------------------------------------------------------------------------------------------------------------------
    def command(
            self=None,
            *,
            names:str|list[str],
            args_enabled:bool=False,
            args_skip_emotes:bool=False,
            case_sensitive:bool = False
    ) -> TwitchBotMethod:
        # if the method is used on the TwitchBotMethod class and not an instance of it
        kwargs:dict = {
            "is_command" : True,
            "command_names" : [names] if isinstance(names, str) else [str(n) for n in names],
            "command_args" : args_enabled,
            "command_case_sensitive" : case_sensitive,
            "command_args_skip_emotes":args_skip_emotes
        }

        # if the method is used on a TwitchBotMethod instance
        return TwitchBotMethod(
            channels = self.channels,
            **kwargs
        ) if self is not None else TwitchBotMethod(
            **kwargs
        )

    # ------------------------------------------------------------------------------------------------------------------
    # - Scheduled Task Method -
    # ------------------------------------------------------------------------------------------------------------------
    def scheduled_task(
            self=None,
            *,
            interval:int|Second|Minute|Hour=Hour(1),
            call_on_startup:bool=False
    ) -> TwitchBotMethod:
        kwargs: dict = {
            "is_scheduled_task": True,
            "task_interval": convert_time_to_seconds(interval, to_int=True),
            "task_call_on_startup": call_on_startup
        }

        # if the method is used on a TwitchBotMethod instance
        return TwitchBotMethod(
            channels=self.channels,
            **kwargs
        ) if self is not None else TwitchBotMethod(
            **kwargs
        )
