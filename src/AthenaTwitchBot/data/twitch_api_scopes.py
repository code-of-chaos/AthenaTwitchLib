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
class TwitchApiScopes(enum.Enum):
    AnalyticsReadExtensions = "analytics:read:extensions"
    AnalyticsReadGames = "analytics:read:games"
    BitsRead = "bits:read"
    ChannelEditCommercial = "channel:edit:commercial"
    ChannelManageBroadcast = "channel:manage:broadcast"
    ChannelManageExtensions = "channel:manage:extensions"
    ChannelManagePolls = "channel:manage:polls"
    ChannelManagePredictions = "channel:manage:predictions"
    ChannelManageRaids = "channel:manage:raids"
    ChannelManageRedemptions = "channel:manage:redemptions"
    ChannelManageSchedule = "channel:manage:schedule"
    ChannelManageVideos = "channel:manage:videos"
    ChannelReadEditors = "channel:read:editors"
    ChannelReadGoals = "channel:read:goals"
    ChannelReadHype_train = "channel:read:hype_train"
    ChannelReadPolls = "channel:read:polls"
    ChannelReadPredictions = "channel:read:predictions"
    ChannelReadRedemptions = "channel:read:redemptions"
    ChannelReadStream_key = "channel:read:stream_key"
    ChannelReadSubscriptions = "channel:read:subscriptions"
    ClipsEdit = "clips:edit"
    ModerationRead = "moderation:read"
    ModeratorManageBanned_users = "moderator:manage:banned_users"
    ModeratorReadBlocked_terms = "moderator:read:blocked_terms"
    ModeratorManageBlocked_terms = "moderator:manage:blocked_terms"
    ModeratorManageAutomod = "moderator:manage:automod"
    ModeratorReadAutomod_settings = "moderator:read:automod_settings"
    ModeratorManageAutomod_settings = "moderator:manage:automod_settings"
    ModeratorReadChat_settings = "moderator:read:chat_settings"
    ModeratorManageChat_settings = "moderator:manage:chat_settings"
    UserEdit = "user:edit"
    UserEditFollows = "user:edit:follows"
    UserEditBroadcast = "user:edit:broadcast"
    UserManageBlocked_users = "user:manage:blocked_users"
    UserReadBlocked_users = "user:read:blocked_users"
    UserReadBroadcast = "user:read:broadcast"
    UserReadEmail = "user:read:email"
    UserReadFollows = "user:read:follows"
    UserReadSubscriptions = "user:read:subscriptions"
    ChannelModerate = "channel:moderate"
    ChatEdit = "chat:edit"
    ChatRead = "chat:read"
    WhispersRead = "whispers:read"
    WhispersEdit = "whispers:edit"

    @classmethod
    def string_mapping(cls) -> dict[str:enum.Enum]:
        return {v.value:v for v in cls._member_map_.values()}