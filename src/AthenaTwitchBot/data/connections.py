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
    "TWITCH_WS_PORT", "TWITCH_WS_PORT_SSL", "TWITCH_WS_HOST_SSL", "TWITCH_IRC_PORT_SSL", "TWITCH_WS_HOST",
    "TWITCH_IRC_HOST", "TWITCH_IRC_HOST_SSL", "TWITCH_IRC_PORT"
]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
TWITCH_IRC_HOST = "irc.chat.twitch.tv"
TWITCH_IRC_HOST_SSL = TWITCH_IRC_HOST
TWITCH_IRC_PORT = 6667
TWITCH_IRC_PORT_SSL = 6697

TWITCH_WS_HOST = "irc-ws.chat.twitch.tv"
TWITCH_WS_HOST_SSL = TWITCH_WS_HOST
TWITCH_WS_PORT =80
TWITCH_WS_PORT_SSL =443