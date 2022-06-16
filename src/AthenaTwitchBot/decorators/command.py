# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.decorator_helpers.command import Command

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

def command_method(name:str|list[str], case_sensitive:bool=False, args_enabled:bool=True):
    def decorator(fnc):
        def wrapper(*args_, **kwargs_):
            return fnc(*args_, **kwargs_)

        # store attributes for later use by the bot
        wrapper.is_command = True
        # store some information
        wrapper.cmd = []
        if isinstance(name, list):
            for n in name:
                wrapper.cmd.append(_command_define(n,case_sensitive,wrapper,args_enabled))
        else:
            wrapper.cmd.append(_command_define(name,case_sensitive,wrapper,args_enabled))

        return wrapper
    return decorator