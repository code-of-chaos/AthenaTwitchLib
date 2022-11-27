# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import enum

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TwitchApiUrl(enum.StrEnum):
    USERS = "https://api.twitch.tv/helix/users"

    CHAT_USERS = "https://api.twitch.tv/helix/chat/chatters"
    CHAT_EMOTES = "https://api.twitch.tv/helix/chat/emotes"

    CHANNEL_COMMERCIAL = "https://api.twitch.tv/helix/channels/commercial"