# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.message_context import MessageContext

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def output_twitch_prep(text:str) -> bytes:
    if text.endswith("\r\n"):
        return text.encode("utf_8")
    else:
        return f"{text}\r\n".encode("utf_8")