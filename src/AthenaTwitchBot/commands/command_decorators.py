# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Callable

# Athena Packages

# Local Imports
from AthenaTwitchBot.commands.command_logic import CommandLogic

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def chat_command(**kwargs):
    def decorator(fnc:Callable):
        assert (channels := kwargs.get("channels", False)), "For a default chat command, you have to define at least one channel"
        assert isinstance(channels, set)
        fnc._command_logic_kwargs = kwargs
        return fnc
    return decorator

def global_command(**kwargs):
    def decorator(fnc:Callable):
        kwargs.pop("channels", None) # global command cannot have a channels kwargs
        fnc._command_logic_kwargs = kwargs
        return fnc
    return decorator

def mod_only_command(**kwargs):
    def decorator(fnc:Callable):
        # Overwrites if the kwarg was already set
        kwargs["user"] = False
        kwargs["vip"] = False
        kwargs["sub"] = False
        kwargs["mod"] = True
        fnc._command_logic_kwargs = kwargs
        return fnc
    return decorator

def vip_only_command(**kwargs):
    def decorator(fnc:Callable):
        # Overwrites if the kwarg was already set
        kwargs["user"] = False
        kwargs["vip"] = True
        kwargs["sub"] = False
        kwargs["mod"] = True
        fnc._command_logic_kwargs = kwargs
        return fnc
    return decorator

def sub_only_command(**kwargs):
    def decorator(fnc:Callable):
        # Overwrites if the kwarg was already set
        kwargs["user"] = False
        kwargs["vip"] = False
        kwargs["sub"] = True
        kwargs["mod"] = True
        fnc._command_logic_kwargs = kwargs
        return fnc
    return decorator
