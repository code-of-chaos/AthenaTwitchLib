# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import enum

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TwitchApiURL(enum.Enum):
    login = "https://api.twitch.tv/helix/users"
    scopes = "https://id.twitch.tv/oauth2/validate"

    commercial = "https://api.twitch.tv/helix/channels/commercial"
    analytics_extension = "https://api.twitch.tv/helix/analytics/extensions"
    analytics_game = "https://api.twitch.tv/helix/analytics/games"
    bits_leaderboard = "https://api.twitch.tv/helix/bits/leaderboard"
    cheermotes = "https://api.twitch.tv/helix/bits/cheermotes"
    extension_transactions = "https://api.twitch.tv/helix/extensions/transactions"
    channel_information = "https://api.twitch.tv/helix/channels"
    channel_editors = "https://api.twitch.tv/helix/channels/editors"

    custom_rewards= "https://api.twitch.tv/helix/channel_points/custom_rewards"