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

    get_custom_rewards= "https://api.twitch.tv/helix/channel_points/custom_rewards"