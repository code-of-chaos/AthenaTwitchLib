# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import ClassVar

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_method_inheritance.callback import BotMethodCallback
from AthenaTwitchBot.functions.athena_dataclass import _dataclass

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@_dataclass(slots=True)
class BotChatMessage(BotMethodCallback):
    registered: ClassVar[BotChatMessage] = None

    @classmethod
    def register(
            cls,
            *,
            args:bool=False
    ):
        """Registers the function to the class"""
        if cls.registered is not None:
            raise ValueError("Only one First-Time-Chatter command can be allowed at the same time")
        def decorator(fnc):
            cls.registered = cls(
                callback=fnc,
                args=args
            )
        return decorator