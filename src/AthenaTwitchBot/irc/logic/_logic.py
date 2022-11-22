# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import inspect
from typing import Coroutine, Callable
from abc import ABC, abstractmethod

# Athena Packages

# Local Imports
from AthenaTwitchBot.logger import IrcLogger, TwitchLoggerType
from AthenaTwitchBot.irc.message_context import MessageCommandContext

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
def register_callback_as_logical_component(fnc: Callable):
    assert inspect.iscoroutinefunction(fnc), f"{fnc} was not a asyncio coroutine"
    fnc._logic_component = True

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class BaseLogic(ABC):
    """
    Logic system for commands that need to be executed.
    This is simply a base class and needs to be extended to fully work.
    """
    _logic_components: list[Coroutine]
    _logger:IrcLogger

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)

        # Retrieve all items that are marked as a '_logic_component'
        obj._logic_components = list(
            filter(
                lambda i : hasattr(i, "_logic_component"),
                (getattr(obj, i) for i in obj.__dir__())
            )
        )
        obj._logger = IrcLogger.get_logger(TwitchLoggerType.IRC)

        return obj

    @abstractmethod
    async def execute_command(self, context: MessageCommandContext):
        """
        Main entry point from the Async Protocol, will first try and find a corresponding command.
        Afterwards it needs to execute the given command, with the correct context.
        """