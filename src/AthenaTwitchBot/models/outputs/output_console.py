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
class OutputConsole(Output):
    # noinspection PyMethodOverriding
    async def output(self, context:MessageContext,**_):
        print(context.raw_input_decoded)