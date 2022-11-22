# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import abc
import asyncio
from typing import Any
from typing import overload

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Output(abc.ABC):
    """
    An abstract class to define which structure the output classes should use
    """
    async def output(self, context:MessageContext, *, transport: asyncio.BaseTransport | None) -> None:
        """
        Output a context the correct end state
        """
