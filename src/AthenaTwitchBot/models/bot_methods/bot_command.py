# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, ClassVar

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotCommand:
    name:str
    callback:Callable
    args:bool
    subscriber_only:bool

    registered:ClassVar[dict[str,BotCommand]]=None

    @classmethod
    def register(cls, name:str, *,args:bool=False,subscriber_only:bool=False):
        # make sure the register exists
        if cls.registered is None:
            cls.registered = {}
        def decorator(fnc):
            cls.registered[name] = cls(name=name, callback=fnc, args=args,subscriber_only=subscriber_only)
        return decorator