# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - All -
# ----------------------------------------------------------------------------------------------------------------------
__all__ = [
    "REQUEST_COMMANDS", "REQUEST_MEMBERSHIP", "REQUEST_TAGS",
    "TMI_TWITCH_TV", "TWITCH_TAGS", "TAGS"
]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
REQUEST_COMMANDS = "CAP REQ :twitch.tv/commands"
REQUEST_MEMBERSHIP = "CAP REQ :twitch.tv/membership"
REQUEST_TAGS = "CAP REQ :twitch.tv/tags"
TMI_TWITCH_TV = ":tmi.twitch.tv"
TWITCH_TAGS = ":twitch.tv/tags"
TWITCH_COMMANDS = ":twitch.tv/commands"
TWITCH_MEMBERSHIP = ":twitch.tv/membership"

TAGS = {TWITCH_COMMANDS, TWITCH_TAGS, TWITCH_MEMBERSHIP}