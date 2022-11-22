# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Athena Packages

# Local Imports
from AthenaTwitchBot.irc.data.enums import BotEvent

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class BotEventException(Exception):
    """
    Simple exception to be raised by a bot, and caught by the constructor.
    """
    def __init__(self, event:BotEvent):
        self.event = event