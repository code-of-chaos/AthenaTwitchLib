# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext
from AthenaTwitchBot.data.message_flags import MessageFlags

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
async def handle_capabilities(context:MessageContext):
    """
    Currently unused function to parse CAP messages

    Parameters:
    - context:
    """
    context.flag = MessageFlags.no_output