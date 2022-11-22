# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import asyncio
from typing import Any
# Custom Library

# Custom Packages
from AthenaTwitchBot.data.message_flags import MessageFlags
from AthenaTwitchBot.models.twitch_bot.outputs.output import Output
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class OutputConsole(Output):
    # noinspection PyMethodOverriding
    async def output(self, context:MessageContext, transport: asyncio.BaseTransport | None) -> None:
        if context.raw_input_decoded is not None:
            print(context.raw_input_decoded)
