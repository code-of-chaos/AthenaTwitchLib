# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
from dataclasses import dataclass

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.protocols.protocol import Protocol
from AthenaTwitchBot.models.twitch_data_handler import TwitchDataHandler

# ----------------------------------------------------------------------------------------------------------------------
# - All -
# ----------------------------------------------------------------------------------------------------------------------
__all__ = ["ProtocolTwitch"]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, eq=False, order=False, match_args=False, kw_only=True)
class ProtocolTwitch(Protocol):
    data_handler:TwitchDataHandler

    # ------------------------------------------------------------------------------------------------------------------
    # - asyncio.Protocol methods ( most are defined in AthenaTwitchBot.models.protocols.protocol.Protocol )-
    # ------------------------------------------------------------------------------------------------------------------
    def data_received(self, data: bytearray) -> None:
        result = self.data_handler.handle(data)

    # ------------------------------------------------------------------------------------------------------------------
    # - Twitch authenticate and define outputs methods-
    # ------------------------------------------------------------------------------------------------------------------
    def authenticate(self, bot_name:str, bot_oath_token:str):
        pass