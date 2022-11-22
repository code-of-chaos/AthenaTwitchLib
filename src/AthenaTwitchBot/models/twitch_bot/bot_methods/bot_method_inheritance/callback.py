# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Callable
from collections.abc import Awaitable
from typing import Any
from typing import Protocol

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.twitch_bot import TwitchBot
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
#TODO hard to find types that nicely fit, further investigation needed
class TBMCCallback(Protocol):
    def __call__(self, *args: Any, callback_self: TwitchBot, context: MessageContext, **kwargs: Any) -> Awaitable[Any]: ...


@dataclass(slots=True)
class BotMethodCallback:
    callback: TBMCCallback | None = None
    args:bool=False

    async def __call__(self, *args: Any, callback_self:TwitchBot, context:MessageContext, **kwargs: Any) -> Any:
        if self.callback is None:
            raise ValueError("callback can't be `None`")
        return await self.callback(*args,self=callback_self,context=context,**kwargs)
