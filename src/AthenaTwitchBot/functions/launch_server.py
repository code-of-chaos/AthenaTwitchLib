# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import tracemalloc

# Custom Library

# Custom Packages
import AthenaTwitchBot.functions.global_vars as gbl
from AthenaTwitchBot.models.twitch_bot import TwitchBot
from AthenaTwitchBot.models.bot_server import BotServer

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def launch_server(
        *,
        twitch_bot:TwitchBot,
        **kwargs
) -> None:

    """
    Simplified function which starts the server.
    Passes all arguments directly to the BotServer class.
    For correct parameters, go to the BotServer class.
    """
    tracemalloc.start()
    gbl.bot = twitch_bot
    gbl.bot_server = BotServer(**kwargs)
    gbl.bot_server.launch()