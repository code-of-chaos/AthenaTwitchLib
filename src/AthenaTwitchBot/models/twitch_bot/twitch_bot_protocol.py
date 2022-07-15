# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio

# Custom Library
from AthenaColor import ForeNest

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.line_handler import LineHandler
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
            if line:
                asyncio.create_task(LineHandler.handle(line))

    def connection_lost(self, exc: Exception | None) -> None:
        if exc is not None:
            print(exc)