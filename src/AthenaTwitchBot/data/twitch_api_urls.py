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
    analytics_extension = "https://api.twitch.tv/helix/analytics/extensions"
    analytics_game = "https://api.twitch.tv/helix/analytics/games"
    badges_chat = "https://api.twitch.tv/helix/chat/badges"
    badges_global = "https://api.twitch.tv/helix/chat/badges/global"
    bits_leaderboard = "https://api.twitch.tv/helix/bits/leaderboard"
    channel_editors = "https://api.twitch.tv/helix/channels/editors"
    channel_information = "https://api.twitch.tv/helix/channels"
    chat_settings = "https://api.twitch.tv/helix/chat/settings"
    cheermotes = "https://api.twitch.tv/helix/bits/cheermotes"
    clips= "https://api.twitch.tv/helix/clips"
    commercial = "https://api.twitch.tv/helix/channels/commercial"
    custom_reward_redemptions = "https://api.twitch.tv/helix/channel_points/custom_rewards/redemptions"
    custom_rewards = "https://api.twitch.tv/helix/channel_points/custom_rewards"
    emotes_chat = "https://api.twitch.tv/helix/chat/emotes"
    emotes_global = "https://api.twitch.tv/helix/chat/emotes/global"
    emotes_set = "https://api.twitch.tv/helix/chat/emotes/set"
    enforcements_status = "https://api.twitch.tv/helix/moderation/enforcements/status"
    entitlements_code = "https://api.twitch.tv/helix/entitlements/codes"
    entitlements_drops = "https://api.twitch.tv/helix/entitlements/drops"
    extension_chat = "https://api.twitch.tv/helix/extensions/chat"
    extension_configurations = "https://api.twitch.tv/helix/extensions/configurations"
    extension_jwt_secrets = "https://api.twitch.tv/helix/extensions/jwt/secrets"
    extension_live = "https://api.twitch.tv/helix/extensions/live"
    extension_pubsub = "https://api.twitch.tv/helix/extensions/pubsub"
    extension_transactions = "https://api.twitch.tv/helix/extensions/transactions"
    games = "https://api.twitch.tv/helix/games"
    games_top = "https://api.twitch.tv/helix/games/top"
    goals = "https://api.twitch.tv/helix/goals"
    hypetrain = "https://api.twitch.tv/helix/hypetrain/events"
    scopes = "https://id.twitch.tv/oauth2/validate"
    users = "https://api.twitch.tv/helix/users"
