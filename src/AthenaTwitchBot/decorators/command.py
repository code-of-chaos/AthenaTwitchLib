# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def commandmethod(name:str):
    def decorator(fnc):
        fnc.is_command = True
        fnc.command_name = name
        def wrapper(*args, **kwargs):
            return fnc(*args, **kwargs)
        return wrapper
    return decorator