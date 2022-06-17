# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Any

# Custom Library
from AthenaLib.models import Second, Minute, Hour
from AthenaLib.functions.time import convert_time_to_seconds

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class TwitchBotMethod:
    channels:list[str] = field(default_factory=list)

    # command related attributes
    is_command:bool = False
    command_names:list[str] = field(default_factory=list)
    command_args:bool = False
    command_case_sensitive:bool = False

    # scheduled task related attributes
    is_scheduled_task:bool = False
    task_delay:Second = field(default=lambda : Second(60))

    # non init stuff
    callback:Callable = field(init=False)
    owner:object = field(init=False, default=None) # defined by TwitchBot

    def __call__(self, fnc:Callable):
        self.callback = lambda *args, **kwargs: fnc(self.owner, *args, **kwargs)
        return self # needs to return self to be assigned to the function's call

    def command(self=None, *, names:str|list[str], args_enabled:bool=False, case_sensitive:bool = False) -> TwitchBotMethod:
        # if the method is used on the TwitchBotMethod class and not an instance of it
        kwargs:dict = {
            "is_command" : True,
            "command_names" : [names] if isinstance(names, str) else [str(n) for n in names],
            "command_args" : args_enabled,
            "command_case_sensitive" : case_sensitive,
        }

        # if the method is used on a TwitchBotMethod instance
        obj:TwitchBotMethod = TwitchBotMethod(
            channels = self.channels,
            **kwargs
        ) if self is not None else TwitchBotMethod(
            **kwargs
        )

        # set the command to true and return
        obj.is_command = True
        return obj

    def scheduled_task(self=None, *, delay:int=Hour(1)):
        kwargs: dict = {
            "is_scheduled_task": True,
            "task_delay": convert_time_to_seconds(delay),
        }

        # if the method is used on a TwitchBotMethod instance
        obj: TwitchBotMethod = TwitchBotMethod(
            channels=self.channels,
            **kwargs
        ) if self is not None else TwitchBotMethod(
            **kwargs
        )

        # set the command to true and return
        obj.is_scheduled_task = True
        return obj
