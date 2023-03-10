# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class BaseTaskLogic(ABC):
    """
    Logic system for commands that need to be executed.
    This is simply a base class and needs to be extended to fully work.
    """
    @abstractmethod
    def start_all_tasks(self, transport:asyncio.Transport, loop:asyncio.AbstractEventLoop):
        """
        Main Entry point for the constructor to start all tasks
        """

    @abstractmethod
    def stop_all_tasks(self):
        """
        Main Entry point for the constructor to stop all tasks when needed
        """