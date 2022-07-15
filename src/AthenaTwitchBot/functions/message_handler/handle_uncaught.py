# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaColor import ForeNest

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
async def handle_uncaught(context:MessageContext):
    """
    Currently unused function to parse uncaught messages

    Parameters:
    - context:
    """
    print(f"NOT CAUGHT : {ForeNest.Maroon(context.raw_input_decoded)}")