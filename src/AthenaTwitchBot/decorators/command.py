# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.wrapper_helpers.command import Command

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def command_method(name:str|list[str], case_sensitive:bool=False):
    def decorator(fnc):
        def wrapper(*args_, **kwargs_):
            return fnc(*args_, **kwargs_)

        # store attributes for later use by the bot
        wrapper.is_command = True
        # store some information
        wrapper.cmd = []
        if isinstance(name, list):
            for n in name:
                wrapper.cmd.append(Command(
                    name=n,
                    case_sensitive=case_sensitive,
                    callback=wrapper,
                ))
        else:
            wrapper.cmd.append(Command(
                name=name,
                case_sensitive=case_sensitive,
                callback=wrapper,
            ))

        return wrapper
    return decorator