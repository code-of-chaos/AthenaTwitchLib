# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
import pathlib
import json
from typing import Callable, Any
import functools

# Athena Packages

# Local Imports
from AthenaTwitchBot.bot_logger import get_bot_logger

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def track_handler(fnc:Callable) -> Any:
    """
    Simple decorator to keep track of how many calls are made to handlers
    """

    @functools.wraps(fnc)
    async def wrapper(*args, **kwargs):
        result, _ = await asyncio.gather(
            fnc(*args, **kwargs),
            get_bot_logger().log_handler_called(fnc.__name__)
        )
        return result

    return wrapper

