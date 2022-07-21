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
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotMethodRateLimit(BotMethodCallback):
    rate_limit:datetime.timedelta=None
    rate_limit_old_time:datetime.datetime=field(init=False)

    def __post_init__(self):
        # if there is a rate limit in placer
        #   make the command available at the bot start, which is done by subtracting the time delta from the
        #   current time, which places the "virtually last call to the command" far enough away in the past
        if self.rate_limit:
            self.rate_limit_old_time = datetime.datetime.now()-self.rate_limit

    async def __call__(self, *args, callback_self:TwitchBot, context:MessageContext, **kwargs):
        # rate limiter
        #   set here as the rate limit can be applied to all commands and makes the match case statement much more easy
        if self.rate_limit:
            if not self.rate_limit_old_time <= ((new_time := datetime.datetime.now()) - self.rate_limit):
                context.rate_limited = True
                return
            # set the new rate limit to the old one as we need it for the next incoming self
            self.rate_limit_old_time = new_time
        return await self.callback(*args,self=callback_self,context=context,**kwargs)