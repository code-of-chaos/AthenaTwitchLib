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
class OutputTwitch(Output):
    async def output(self, context:MessageContext,*,transport:asyncio.Transport):
        for text in context.output:
            transport.write(f"{text}\r\n".encode("utf_8"))