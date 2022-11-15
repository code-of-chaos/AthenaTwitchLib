# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Callable

# Athena Packages

# Local Imports
from AthenaTwitchBot.logic.logic_types import LogicTypes

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def chat_command(**kwargs):
    def decorator(fnc:Callable):
        fnc._type = LogicTypes.COMMAND
        fnc._kwargs = kwargs
        return fnc
    return decorator

def broadcaster_only_command(**kwargs):
    def decorator(fnc:Callable):
        # Overwrites if the kwarg was already set
        kwargs["user"] = False
        kwargs["vip"] = False
        kwargs["sub"] = False
        kwargs["mod"] = False
        kwargs["broadcaster"] = True
        fnc._type = LogicTypes.COMMAND
        fnc._kwargs = kwargs
        return fnc
    return decorator

def mod_only_command(**kwargs):
    def decorator(fnc:Callable):
        # Overwrites if the kwarg was already set
        kwargs["user"] = False
        kwargs["vip"] = False
        kwargs["sub"] = False
        kwargs["mod"] = True
        fnc._type = LogicTypes.COMMAND
        fnc._kwargs = kwargs
        return fnc
    return decorator

def vip_only_command(**kwargs):
    def decorator(fnc:Callable):
        # Overwrites if the kwarg was already set
        kwargs["user"] = False
        kwargs["vip"] = True
        kwargs["sub"] = False
        kwargs["mod"] = True
        fnc._type = LogicTypes.COMMAND
        fnc._kwargs = kwargs
        return fnc
    return decorator

def sub_only_command(**kwargs):
    def decorator(fnc:Callable):
        # Overwrites if the kwarg was already set
        kwargs["user"] = False
        kwargs["vip"] = False
        kwargs["sub"] = True
        kwargs["mod"] = True
        fnc._type = LogicTypes.COMMAND
        fnc._kwargs = kwargs
        return fnc
    return decorator

def chat_message(**kwargs):
    """
    Assigns the function to be called when a message is sent in a specific chat
    :return:
    """
    def decorator(fnc:Callable):
        fnc._type = LogicTypes.MESSAGE
        fnc._kwargs = kwargs
        return fnc
    return decorator