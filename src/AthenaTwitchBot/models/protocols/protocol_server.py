# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.protocols.protocol import Protocol
from AthenaTwitchBot.models.data_handlers.data_handler_server import DataHandlerServer

# ----------------------------------------------------------------------------------------------------------------------
# - All -
# ----------------------------------------------------------------------------------------------------------------------
__all__ = ["ProtocolServer"]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, eq=False, order=False, match_args=False, kw_only=True)
class ProtocolServer(Protocol):
    data_handler:DataHandlerServer