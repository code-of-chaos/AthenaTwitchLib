# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import re

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
server_ping = re.compile(r"PING :tmi\.twitch\.tv")

server_message = re.compile(r"^:tmi.twitch.tv \d\d\d ([^ ]*) :")
server_353 = re.compile(r"^:([^ ]*)\.tmi\.twitch\.tv 353 \1 = #([^ ]*) :")
server_366 = re.compile(r"^:([^ ]*)\.tmi\.twitch\.tv 366 \1 #([^ ]*) :End of /NAMES list$")
server_cap = re.compile(r":tmi\.twitch\.tv CAP \* ACK :.*")

join = re.compile(r"^:([^ ]*)!\1@\1\.tmi\.twitch\.tv JOIN (#.*)")
part = re.compile(r"^:([^ ]*)!\1@\1\.tmi\.twitch\.tv PART (#.*)")

message = re.compile(r"^@([^ ]*) ([^ ]*) PRIVMSG #([^:]*) :([^ ]*)(.*)")

user_notice = re.compile(r"^([^ ]*) ([^ ]*) USERNOTICE #([^:]*) :(.*)")
user_state = re.compile(r"^@([^ ]*) :tmi\.twitch\.tv USERSTATE #([^:]*)")
username = re.compile(r":([^!]*)!\1@\1\.tmi\.twitch\.tv")