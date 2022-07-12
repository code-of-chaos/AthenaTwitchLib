# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio

# Custom Library

# Custom Packages
from AthenaTwitchBot.functions.message_handler import message_handler
import AthenaTwitchBot.data.global_vars as gbl

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TwitchBotProtocol(asyncio.Protocol):
    transport: asyncio.transports.BaseTransport
    __slots__ = ("transport",)

    # ------------------------------------------------------------------------------------------------------------------
    # - Incoming Data Parsing -
    # ------------------------------------------------------------------------------------------------------------------
    def data_received(self, data: bytearray) -> None:
        for line in data.split(b"\r\n"):
            if line == b"":
                continue
            asyncio.create_task(self._line_received(line))

    async def _line_received(self, line:bytearray):
        await gbl.bot_server.output_all(context=await message_handler(line))

    # ------------------------------------------------------------------------------------------------------------------
    # - Connection Lost -
    # ------------------------------------------------------------------------------------------------------------------
    def connection_lost(self, exc: Exception | None) -> None:
        print(exc)