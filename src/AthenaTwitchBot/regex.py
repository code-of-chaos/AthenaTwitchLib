# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import re
from dataclasses import dataclass

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, init=False)
class RegexPatterns:
    server_message:re.Pattern
    server_353:re.Pattern
    server_366:re.Pattern
    server_cap:re.Pattern

    join:re.Pattern
    part:re.Pattern

    message_command_with_args:re.Pattern
    message_command_without_args:re.Pattern
    message:re.Pattern
    user_notice:re.Pattern
    user_state:re.Pattern

    def __init__(self, bot_name:str, bot_prefix:str):
        self.server_message = re.compile(fr"^((:tmi.twitch.tv) \d\d\d ({bot_name}) :)")
        self.server_353 = re.compile(fr"^:{bot_name}\.tmi\.twitch\.tv 353 {bot_name} = #.*:")
        self.server_366 = re.compile(fr"^:{bot_name}\.tmi\.twitch\.tv 366 {bot_name} #.*:End of /NAMES list")
        self.server_cap = re.compile(fr":tmi\.twitch\.tv CAP \* ACK :.*")

        self.join = re.compile(fr"^:([^ ]*)!\1@\1\.tmi\.twitch\.tv JOIN (#.*)")
        self.part = re.compile(fr"^:([^ ]*)!\1@\1\.tmi\.twitch\.tv PART (#.*)")

        self.message = re.compile(fr"^@([^ ]*) ([^ ]*) PRIVMSG #([^:]*) :(.*)")
        self.message_command_with_args = re.compile(fr"^{bot_prefix}([^ ]*) (.*)")
        self.message_command_without_args = re.compile(fr"^{bot_prefix}([^ ]*)")
        self.user_notice = re.compile(r"^([^ ]*) ([^ ]*) USERNOTICE #([^:]*) :(.*)")
        self.user_state = re.compile(r"^@([^ ]*) :tmi\.twitch\.tv USERSTATE #([^:]*)")