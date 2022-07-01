# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from typing import Callable

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.bot.twitch_bot_handler import TwitchBotHandler
from AthenaTwitchBot.models.bot.twitch_message_context import TwitchMessageContext

# ----------------------------------------------------------------------------------------------------------------------
# - All -
# ----------------------------------------------------------------------------------------------------------------------
__all__ = ["TwitchProtocol"]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, eq=False, order=False, match_args=False, kw_only=True)
class TwitchProtocol:
    data_handler: TwitchBotHandler

    # non init values
    transport: asyncio.transports.Transport = field(init=False, default=None)

    # ------------------------------------------------------------------------------------------------------------------
    # - factory, needed for asyncio.AbstractEventLoop.create_connection protocol_factory kwarg used in Launcher -
    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def factory(cls, **kwargs) -> Callable[[], TwitchProtocol]:
        def factory_wrapper():
            # noinspection PyArgumentList
            return cls(**kwargs)

        return factory_wrapper

    # ------------------------------------------------------------------------------------------------------------------
    # - asyncio.Protocol methods ( most are defined in AthenaTwitchBot.models.protocols.protocol.Protocol )-
    # ------------------------------------------------------------------------------------------------------------------
    def connection_made(self, transport: asyncio.transports.Transport) -> None:
        self.transport = transport

    def connection_lost(self, exc: Exception | None) -> None:
        raise exc

    def data_received(self, data: bytearray) -> None:
        context: TwitchMessageContext = TwitchMessageContext(data)
        self.data_handler.handle(context)
        self.command_handler(context)
        self.output_handler(context)

    # ------------------------------------------------------------------------------------------------------------------
    # - Twitch authenticate -
    # ------------------------------------------------------------------------------------------------------------------
    def authenticate(self, bot_name:str, bot_oath_token:str):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    # - Outputs -
    # ------------------------------------------------------------------------------------------------------------------
    def output_handler(self, context: TwitchMessageContext):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    # - content handlers -
    # ------------------------------------------------------------------------------------------------------------------
    def command_handler(self, context:TwitchMessageContext) -> TwitchMessageContext:
        pass

    def task_handler(self, context:TwitchMessageContext) -> TwitchMessageContext:
        pass

