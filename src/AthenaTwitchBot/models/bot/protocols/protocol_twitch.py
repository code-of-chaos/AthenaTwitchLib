# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
from dataclasses import dataclass

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.bot.protocols.protocol import Protocol
from AthenaTwitchBot.models.bot.data_handlers.data_handler_twitch import DataHandlerTwitch
from AthenaTwitchBot.models.bot.contexts.context import Context

# ----------------------------------------------------------------------------------------------------------------------
# - All -
# ----------------------------------------------------------------------------------------------------------------------
__all__ = ["ProtocolTwitch"]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, eq=False, order=False, match_args=False, kw_only=True)
class ProtocolTwitch(Protocol):
    data_handler:DataHandlerTwitch

    # ------------------------------------------------------------------------------------------------------------------
    # - asyncio.Protocol methods ( most are defined in AthenaTwitchBot.models.protocols.protocol.Protocol )-
    # ------------------------------------------------------------------------------------------------------------------
    def data_received(self, data: bytearray) -> None:
        context: Context = self.data_handler.handle(data)
        self.command_handler(context)
        self.output_handler(context)

    # ------------------------------------------------------------------------------------------------------------------
    # - Twitch authenticate and define outputs methods-
    # ------------------------------------------------------------------------------------------------------------------
    def authenticate(self, bot_name:str, bot_oath_token:str):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    # - content handlers -
    # ------------------------------------------------------------------------------------------------------------------
    def command_handler(self, context:Context) -> Context:
        return context

    def task_handler(self, context:Context) -> Context:
        return context

