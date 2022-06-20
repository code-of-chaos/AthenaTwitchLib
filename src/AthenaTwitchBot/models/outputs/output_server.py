# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.outputs.output import Output

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class OutputServer(Output):
    transport:asyncio.Transport
    def __init__(self, transport:asyncio.Transport, **kwargs):
        self.transport = transport

    def undefined(self, data):
        pass