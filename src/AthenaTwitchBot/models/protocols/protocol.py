# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Callable

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.data_handlers.data_handler import DataHandler
from AthenaTwitchBot.models.contexts.context import Context

# ----------------------------------------------------------------------------------------------------------------------
# - All -
# ----------------------------------------------------------------------------------------------------------------------
__all__ = ["Protocol"]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------

@dataclass(slots=True, eq=False, order=False, match_args=False, kw_only=True)
class Protocol(asyncio.Protocol, ABC):
    data_handler:DataHandler

    # non init values
    transport: asyncio.transports.Transport = field(init=False, default=None)

    # ------------------------------------------------------------------------------------------------------------------
    # - factory, needed for asyncio.AbstractEventLoop.create_connection protocol_factory kwarg used in Launcher -
    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def factory(cls, **kwargs) -> Callable[[], Protocol]:
        def factory_wrapper():
            # noinspection PyArgumentList
            return cls(**kwargs)
        return factory_wrapper

    # ------------------------------------------------------------------------------------------------------------------
    # - asyncio.Protocol methods -
    # ------------------------------------------------------------------------------------------------------------------
    def connection_made(self, transport: asyncio.transports.Transport) -> None:
        self.transport = transport

    def data_received(self, data: bytearray) -> None:
        context: Context = self.data_handler.handle(data)
        self.output_handler(context)

    def connection_lost(self, exc: Exception | None) -> None:
        raise exc

    # ------------------------------------------------------------------------------------------------------------------
    # - Outputs -
    # ------------------------------------------------------------------------------------------------------------------
    def output_handler(self, context:Context):
        pass