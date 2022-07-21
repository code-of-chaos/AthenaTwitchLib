# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def output_twitch_prep(text:str) -> bytes:
    """
    Formats the string into the correct byte structure expected by the Twitch IRC

    Parameters:
    - text:
    """
    text_flat = text.replace('\n',' ')
    return f"{text_flat}\r\n".encode("utf_8")
