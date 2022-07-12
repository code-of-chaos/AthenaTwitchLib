# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.message_context import MessageContext
from AthenaTwitchBot.data.message_flags import MessageFlags

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
async def handle_ping(context:MessageContext, ping_response:tuple[str]) -> None:
    context.flag = MessageFlags.ping
    context.output = " ".join(ping_response)