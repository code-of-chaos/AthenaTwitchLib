# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.bot.outputs.output import Output

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class OutputTwitch(Output):
    transport:asyncio.Transport
    def __init__(self, transport:asyncio.Transport, **_):
        self.transport = transport

    def undefined(self, data):
        pass