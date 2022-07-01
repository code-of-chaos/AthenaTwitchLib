# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.bot.twitch_bot import TwitchBot

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True, eq=False, order=False)
class TwitchBotHandler:
    bot:TwitchBot

    def handle(self, data:bytearray):
        pass