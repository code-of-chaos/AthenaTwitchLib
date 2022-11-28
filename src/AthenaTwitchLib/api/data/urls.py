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
    ANALYTICS_EXTENSIONS = "https://api.twitch.tv/helix/analytics/extensions"
    ANALYTICS_GAMES = "https://api.twitch.tv/helix/analytics/games"
    CHANNEL_COMMERCIAL = "https://api.twitch.tv/helix/channels/commercial"
    CHAT_EMOTES = "https://api.twitch.tv/helix/chat/emotes"
    CHAT_EMOTES_GLOBAL = "https://api.twitch.tv/helix/chat/emotes/global"
    CHAT_USERS = "https://api.twitch.tv/helix/chat/chatters"
    TOKEN_VALIDATE = "https://id.twitch.tv/oauth2/validate"
    USERS = "https://api.twitch.tv/helix/users"
    BITS_LEADERBOARD = "https://api.twitch.tv/helix/bits/leaderboard"
    BITS_CHEERMOTES = "https://api.twitch.tv/helix/bits/cheermotes"
    EXTENSIONS_TRANSACTIONS = "https://api.twitch.tv/helix/extensions/transactions"