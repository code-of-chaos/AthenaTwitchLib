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

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class OutputConsole(Output):
    # noinspection PyMethodOverriding
    async def output(self, context:MessageContext,**_):
        print(context.raw_input_decoded)