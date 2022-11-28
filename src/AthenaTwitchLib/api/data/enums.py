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
class HttpCommand(enum.Enum):
    GET = enum.auto()
    POST = enum.auto()
    PUT = enum.auto()
    PATCH = enum.auto()
    DELETE = enum.auto()

class DataFromConnection(enum.StrEnum):
    BROADCASTER_ID = enum.auto()
    MODERATOR_ID = enum.auto()
    OATH_TOKEN = enum.auto()

class TokenScope(enum.StrEnum):
    ANALYTICS_READ_EXTENSIONS = "analytics:read:extensions"
    ANALYTICS_READ_GAMES = "analytics:read:games"
    BITS_READ = "bits:read"
    CHANNEL_EDIT_COMMERCIAL = "channel:edit:commercial"
    CHANNEL_MANAGE_BROADCAST = "channel:manage:broadcast"
    CHANNEL_MANAGE_EXTENSIONS = "channel:manage:extensions"
    CHANNEL_MANAGE_MODERATORS = "channel:manage:moderators"
    CHANNEL_MANAGE_POLLS = "channel:manage:polls"
    CHANNEL_MANAGE_PREDICTIONS = "channel:manage:predictions"
    CHANNEL_MANAGE_RAIDS = "channel:manage:raids"
    CHANNEL_MANAGE_REDEMPTIONS = "channel:manage:redemptions"
    CHANNEL_MANAGE_SCHEDULE = "channel:manage:schedule"
    CHANNEL_MANAGE_VIDEOS = "channel:manage:videos"
    CHANNEL_MANAGE_VIPS = "channel:manage:vips"
    CHANNEL_MODERATE = "channel:moderate"
    CHANNEL_READ_CHARITY = "channel:read:charity"
    CHANNEL_READ_EDITORS = "channel:read:editors"
    CHANNEL_READ_GOALS = "channel:read:goals"
    CHANNEL_READ_HYPE_TRAIN = "channel:read:hype_train"
    CHANNEL_READ_POLLS = "channel:read:polls"
    CHANNEL_READ_PREDICTIONS = "channel:read:predictions"
    CHANNEL_READ_REDEMPTIONS = "channel:read:redemptions"
    CHANNEL_READ_STREAM_KEY = "channel:read:stream_key"
    CHANNEL_READ_SUBSCRIPTIONS = "channel:read:subscriptions"
    CHANNEL_READ_VIPS = "channel:read:vips"
    CHAT_EDIT = "chat:edit"
    CHAT_READ = "chat:read"
    CLIPS_EDIT = "clips:edit"
    MODERATION_READ = "moderation:read"
    MODERATOR_MANAGE_ANNOUNCEMENTS = "moderator:manage:announcements"
    MODERATOR_MANAGE_AUTOMOD = "moderator:manage:automod"
    MODERATOR_MANAGE_AUTOMOD_SETTINGS = "moderator:manage:automod_settings"
    MODERATOR_MANAGE_BANNED_USERS = "moderator:manage:banned_users"
    MODERATOR_MANAGE_BLOCKED_TERMS = "moderator:manage:blocked_terms"
    MODERATOR_MANAGE_CHAT_MESSAGES = "moderator:manage:chat_messages"
    MODERATOR_MANAGE_CHAT_SETTINGS = "moderator:manage:chat_settings"
    MODERATOR_READ_AUTOMOD_SETTINGS = "moderator:read:automod_settings"
    MODERATOR_READ_BLOCKED_TERMS = "moderator:read:blocked_terms"
    MODERATOR_READ_CHAT_SETTINGS = "moderator:read:chat_settings"
    MODERATOR_READ_CHATTERS = "moderator:read:chatters"
    USER_EDIT = "user:edit"
    USER_EDIT_BROADCAST = "user:edit:broadcast"
    USER_EDIT_FOLLOWS = "user:edit:follows"
    USER_MANAGE_BLOCKED_USERS = "user:manage:blocked_users"
    USER_MANAGE_CHAT_COLOR = "user:manage:chat_color"
    USER_MANAGE_WHISPERS = "user:manage:whispers"
    USER_READ_BLOCKED_USERS = "user:read:blocked_users"
    USER_READ_BROADCAST = "user:read:broadcast"
    USER_READ_EMAIL = "user:read:email"
    USER_READ_FOLLOWS = "user:read:follows"
    USER_READ_SUBSCRIPTIONS = "user:read:subscriptions"
    WHISPERS_EDIT = "whispers:edit"
    WHISPERS_READ = "whispers:read"