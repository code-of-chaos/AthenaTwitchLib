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
    "NICK", "PASS", "JOIN", "PONG", "REQUEST_COMMANDS", "REQUEST_MEMBERSHIP", "REQUEST_TAGS", "PING", "PRIVMSG",
    "TMI_TWITCH_TV", "CAP", "ACK", "ASTERISK", "TWITCH_TAGS", "EQUALS"
]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
NICK = "NICK"
PASS = "PASS oauth:"
JOIN = "JOIN"
PONG = "PONG"
REQUEST_COMMANDS = "CAP REQ :twitch.tv/commands"
REQUEST_MEMBERSHIP = "CAP REQ :twitch.tv/membership"
REQUEST_TAGS = "CAP REQ :twitch.tv/tags"
PING = "PING"
PRIVMSG = "PRIVMSG"
TMI_TWITCH_TV = ":tmi.twitch.tv"
CAP = "CAP"
ASTERISK = "*"
ACK = "ACK"
TWITCH_TAGS = ":twitch.tv/tags"
EQUALS = "="
