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
    get_scopes = "https://id.twitch.tv/oauth2/validate"

    start_commercial = "https://api.twitch.tv/helix/channels/commercial"
    get_extension_analytics = "https://api.twitch.tv/helix/analytics/extensions"
    get_game_analytics = "https://api.twitch.tv/helix/analytics/games"
    get_bits_leaderboard = "https://api.twitch.tv/helix/bits/leaderboard"
    get_cheermotes = "https://api.twitch.tv/helix/bits/cheermotes"
    get_extension_transactions = "https://api.twitch.tv/helix/extensions/transactions"
    channel_information = "https://api.twitch.tv/helix/channels"

    get_custom_rewards= "https://api.twitch.tv/helix/channel_points/custom_rewards"