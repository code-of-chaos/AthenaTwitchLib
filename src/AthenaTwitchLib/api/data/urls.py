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

    TOKEN_VALIDATE = "https://id.twitch.tv/oauth2/validate"

    CHAT_USERS = "https://api.twitch.tv/helix/chat/chatters"
    CHAT_EMOTES = "https://api.twitch.tv/helix/chat/emotes"
    CHAT_EMOTES_GLOBAL = "https://api.twitch.tv/helix/chat/emotes/global"

    CHANNEL_COMMERCIAL = "https://api.twitch.tv/helix/channels/commercial"

    ANALYTICS_EXTENSIONS = "https://api.twitch.tv/helix/analytics/extensions"
    ANALYTICS_GAMES = "https://api.twitch.tv/helix/analytics/games"