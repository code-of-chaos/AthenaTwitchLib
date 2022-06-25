# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from abc import ABC, abstractmethod

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.bot.contexts.context import Context

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class DataHandler(ABC):
    @abstractmethod
    def handle(self, data:bytearray) -> Context:
        """handles the data in a proper manner"""