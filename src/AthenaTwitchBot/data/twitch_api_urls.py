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
    users = "https://api.twitch.tv/helix/users"
    scopes = "https://id.twitch.tv/oauth2/validate"

    commercial = "https://api.twitch.tv/helix/channels/commercial"
    analytics_extension = "https://api.twitch.tv/helix/analytics/extensions"
    analytics_game = "https://api.twitch.tv/helix/analytics/games"
    bits_leaderboard = "https://api.twitch.tv/helix/bits/leaderboard"
    cheermotes = "https://api.twitch.tv/helix/bits/cheermotes"
    extension_transactions = "https://api.twitch.tv/helix/extensions/transactions"
    channel_information = "https://api.twitch.tv/helix/channels"
    channel_editors = "https://api.twitch.tv/helix/channels/editors"
    custom_rewards = "https://api.twitch.tv/helix/channel_points/custom_rewards"
    custom_reward_redemptions = "https://api.twitch.tv/helix/channel_points/custom_rewards/redemptions"
    emotes_chat = "https://api.twitch.tv/helix/chat/emotes"
    emotes_global = "https://api.twitch.tv/helix/chat/emotes/global"
    emotes_set = "https://api.twitch.tv/helix/chat/emotes/set"
    badges_chat = "https://api.twitch.tv/helix/chat/badges"
    badges_global = "https://api.twitch.tv/helix/chat/badges/global"
    chat_settings = "https://api.twitch.tv/helix/chat/settings"
    clips= "https://api.twitch.tv/helix/clips"
    entitlements_code = "https://api.twitch.tv/helix/entitlements/codes"
    entitlements_drops = "https://api.twitch.tv/helix/entitlements/drops"
    extension_configurations = "https://api.twitch.tv/helix/extensions/configurations"
    games_top = "https://api.twitch.tv/helix/games/top"
    games = "https://api.twitch.tv/helix/games"
    goals = "https://api.twitch.tv/helix/goals"
    hypetrain = "https://api.twitch.tv/helix/hypetrain/events"
    enforcements_status = "https://api.twitch.tv/helix/moderation/enforcements/status"