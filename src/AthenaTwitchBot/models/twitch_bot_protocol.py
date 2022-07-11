# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.message_context import MessageContext
from AthenaTwitchBot.functions.message_handler import message_handler
from AthenaTwitchBot.data.output_types import OutputTypes
import AthenaTwitchBot.functions.global_vars as gbl

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TwitchBotProtocol(asyncio.Protocol):
    transport: asyncio.transports.BaseTransport
    __slots__ = ("transport",)

    def connection_made(self, transport: asyncio.transports.BaseTransport) -> None:
        # store the transport to be used in every
        self.transport = transport

    def data_received(self, data: bytearray) -> None:
        for line in data.split(b"\r\n"):
            print(line)
        # asyncio.create_task(
        #     gbl.get_bot_server().output_direct(
        #         output_type=OutputTypes.twitch,
        #         context=await message_handler(data)
        #     )
        # )

    def connection_lost(self, exc: Exception | None) -> None:
        print(exc)