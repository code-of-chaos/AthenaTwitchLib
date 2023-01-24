# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.message_context import MessageCommandContext
from AthenaTwitchLib.api.api_connection import ApiConnection

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class BaseCommandLogic(ABC):
    """
    Logic system for commands that need to be executed.
    This is simply a base class and needs to be extended to fully work.
    """
    api_connection: ApiConnection

    def __init__(self,api_connection:ApiConnection):
        self.api_connection = api_connection

    @abstractmethod
    async def execute_command(self, context: MessageCommandContext):
        """
        Main entry point from the Async Protocol, will first try and find a corresponding command.
        Afterwards it needs to execute the given command, with the correct context.
        """

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