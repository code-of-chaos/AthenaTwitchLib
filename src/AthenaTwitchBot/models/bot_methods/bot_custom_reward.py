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
class BotCustomReward:
    callback:Callable
    args:bool
    custom_reward_id:str

    registered:ClassVar[dict[str,BotCustomReward]]=None

    @classmethod
    def register(cls,custom_reward_id:str, *,args:bool=False,):
        # make sure the register exists
        if cls.registered is None:
            cls.registered = {}
        def decorator(fnc):
            cls.registered[custom_reward_id] = cls(custom_reward_id=custom_reward_id, callback=fnc, args=args,)
        return decorator