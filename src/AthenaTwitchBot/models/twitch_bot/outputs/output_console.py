# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaColor import ForeNest

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.outputs.output import Output
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class OutputConsole(Output):
    # noinspection PyMethodOverriding
    async def output(self, context:MessageContext,**_):
        print(context.raw_input_decoded)
        if context.rate_limited:
            print(ForeNest.IndianRed("the user was rate_limited"))