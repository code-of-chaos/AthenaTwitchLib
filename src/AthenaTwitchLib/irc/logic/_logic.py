# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Coroutine, Callable
import asyncio
import inspect

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.message_context import MessageCommandContext

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
def register_callback_as_logical_component(fnc: Callable):
    assert inspect.iscoroutinefunction(fnc), f"{fnc} was not a asyncio coroutine"
    fnc._logic_component = True

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class BaseHardCodedLogic(ABC):
    """
    A class meant for hard coded tasks, commands and other logic systems handled by the bot

    Will store all functions marked as a `_logic_component` to the list of`_logic_components`
        This is useful for later parsing over these functions
    """
    _logic_components: list[Coroutine]

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)

        # Retrieve all items that are marked as a '_logic_component'
        obj._logic_components = list(
            filter(
                lambda i: hasattr(i, "_logic_component"),
                (getattr(obj, i) for i in obj.__dir__())
            )
        )

        return obj

# ----------------------------------------------------------------------------------------------------------------------
class BaseCommandLogic(ABC):
    """
    Logic system for commands that need to be executed.
    This is simply a base class and needs to be extended to fully work.
    """
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