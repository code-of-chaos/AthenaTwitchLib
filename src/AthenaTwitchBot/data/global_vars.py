# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.bot_server import BotServer
from AthenaTwitchBot.models.twitch_bot.twitch_bot import TwitchBot

# ----------------------------------------------------------------------------------------------------------------------
# - Bot Server -
# ----------------------------------------------------------------------------------------------------------------------

# the variables stored here are to be set when the BotServer is created
#   These variables are used by various functions and classes to call back to

bot_server: BotServer | None = None # stands for the BotServer
bot: TwitchBot | None = None     # stands for the TwitchBot