# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import inspect

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
bot_commands = {}
bot_tasks = {}

def bot_command(name:str):
    def decorator(fnc):
        for cls in inspect.getmro(fnc.im_class):
            if hasattr(fnc.__name__, cls):
                print(cls)
                break
        else:
            print("ef")
        bot_commands[name] = fnc
        def wrapper(*args, **kwargs):
            return fnc(*args, **kwargs)
        return wrapper
    return decorator