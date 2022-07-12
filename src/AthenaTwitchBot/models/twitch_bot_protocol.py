# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio

# Custom Library

# Custom Packages
from AthenaTwitchBot.functions.message_handler import line_received_handler
# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TwitchBotProtocol(asyncio.Protocol):
    transport: asyncio.transports.BaseTransport
    __slots__ = ("transport",)

    # ------------------------------------------------------------------------------------------------------------------
    # - asyncio.Protocol methods-
    # ------------------------------------------------------------------------------------------------------------------
    def data_received(self, data: bytearray) -> None:
        for line in data.split(b"\r\n"):
            if line == b"":
                continue
            asyncio.create_task(line_received_handler(line))

    def connection_lost(self, exc: Exception | None) -> None:
        if exc is not None:
            print(exc)