# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass,field
import datetime

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_method_inheritance.callback import BotMethodCallback
from AthenaTwitchBot.models.twitch_bot.twitch_bot import TwitchBot

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotMethodRateLimit(BotMethodCallback):
    rate_limit:datetime.timedelta=None
    rate_limit_old_time:datetime.datetime=field(init=False, default_factory=datetime.datetime.now)

    async def __call__(self, *args, callback_self:TwitchBot, **kwargs):
        # rate limiter
        #   set here as the rate limit can be applied to all commands and makes the match case statement much more easy
        if self.rate_limit:
            if not self.rate_limit_old_time <= ((new_time := datetime.datetime.now()) - self.rate_limit):
                return
            # set the new rate limit to the old one as we need it for the next incoming self
            self.rate_limit_old_time = new_time
        return await self.callback(self=callback_self,*args,**kwargs)