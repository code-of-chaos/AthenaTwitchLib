# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.outputs.output import Output
from AthenaTwitchBot.models.message_context import MessageContext
from AthenaTwitchBot.functions.output_twitch_prep import output_twitch_prep

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class OutputTwitch(Output):
    # noinspection PyMethodOverriding
    async def output(self, context:MessageContext,*,transport:asyncio.Transport):
        # if no output has been defined, just exit here
        if context.output is None:
            return
        # context.output should always be a list of strings, where every string is a line to return to twitch
        for text in context.output:
            transport.write(output_twitch_prep(text))