# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaTwitchBot.models.twitch_bot import TwitchBot

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
class EmptyBot(TwitchBot):
    def __init__(self):
        super(EmptyBot, self).__init__(
            nickname="empty_bot",
            oauth_token="...",
            channels=["directiveathena"],
            prefix="!",
        )