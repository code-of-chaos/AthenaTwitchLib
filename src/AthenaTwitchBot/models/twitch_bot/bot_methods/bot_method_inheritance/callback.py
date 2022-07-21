# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.twitch_bot import TwitchBot
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotMethodCallback:
    callback:Callable=None
    args:bool=None
    async def __call__(self, *args, callback_self:TwitchBot, context:MessageContext, **kwargs):
        return await self.callback(*args,self=callback_self,context=context,**kwargs)