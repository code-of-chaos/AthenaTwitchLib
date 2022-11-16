# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import inspect
import asyncio
import functools
from typing import Coroutine, Callable, Tuple, Any, Dict

# Athena Packages

# Local Imports
from AthenaTwitchBot.line_handler_type import LineHandlerType
from AthenaTwitchBot.bot_logger import BotLogger

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class BaseLogic:
    _logic_components: list[Coroutine]

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj._logic_components = []

        for item_name in obj.__dir__():
            # Get the item all items from the system that are logical components
            if not hasattr(item := getattr(obj, item_name), "_logic_component"):
                continue

            obj._logic_components.append(item)

        return obj

    @classmethod
    def register_callback_as_logical_component(cls, fnc:Callable):
        assert inspect.iscoroutinefunction(fnc), f"{fnc} was not a asyncio coroutine"
        fnc._logic_component = True


    async def _logging(self, line:str, line_handler_type:LineHandlerType):
        logger = BotLogger.logger
        await asyncio.gather(
            logger.log_handler_called(str(line_handler_type)),
            logger.log_handled_message(line)
        )