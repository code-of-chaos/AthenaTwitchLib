# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import inspect

# Custom Library
from AthenaLib.functions.class_from_method import get_class_from_method

# Custom Packages
from AthenaTwitchBot.models.twitch_bot_method import TwitchBotMethod

from AthenaTwitchBot.models.decorator_helpers.command import Command
from AthenaTwitchBot.data.unions import CHANNEL, CHANNELS

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def _command_define(name,case_sensitive,wrapper,args_enabled) -> Command:
    return Command(
        name=name,
        case_sensitive=case_sensitive,
        callback=wrapper,
        args_enabled=args_enabled
    )

def command_method(name:str|list[str], case_sensitive:bool=False, args_enabled:bool=True, channel:CHANNEL|CHANNELS=None):
    def decorator(fnc):
        def wrapper(*args_, **kwargs_):
            return fnc(*args_, **kwargs_)
        return wrapper

    return TwitchBotMethod(
        callback=decorator,
        channels=channel,
        is_command=True,
        command_str=[name] if isinstance(name, str) else [str(n) for n in name],
        command_args=args_enabled,
        command_case_sensitive=case_sensitive
    )