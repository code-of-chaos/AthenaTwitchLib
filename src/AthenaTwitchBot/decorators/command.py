# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_command import TwitchCommand

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def command_method(*args, name:str, force_capitalization:bool=False, **kwargs):
    def decorator(fnc):
        def wrapper(*args_, **kwargs_):
            return fnc(*args_, **kwargs_)

        # store attributes for later use by the bot
        wrapper.is_command = True
        # store some information
        wrapper.cmd = TwitchCommand(
            name=name,
            force_capitalization=force_capitalization,
            callback=wrapper,
            args=args,
            kwargs = kwargs,
        )

        return wrapper
    return decorator