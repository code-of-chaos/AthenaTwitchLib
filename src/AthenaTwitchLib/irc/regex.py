# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import re
from dataclasses import dataclass, field

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class RegexPatterns:
    server_message:re.Pattern = field(default_factory=lambda:re.compile(r"^:tmi.twitch.tv \d\d\d ([^ ]*) :"))
    server_353:re.Pattern = field(default_factory=lambda:re.compile(r"^:([^ ]*)\.tmi\.twitch\.tv 353 \1 = #([^ ]*) :"))
    server_366:re.Pattern = field(default_factory=lambda:re.compile(r"^:([^ ]*)\.tmi\.twitch\.tv 366 \1 #([^ ]*) :End of /NAMES list$"))
    server_cap:re.Pattern = field(default_factory=lambda:re.compile(r":tmi\.twitch\.tv CAP \* ACK :.*"))

    join:re.Pattern = field(default_factory=lambda:re.compile(r"^:([^ ]*)!\1@\1\.tmi\.twitch\.tv JOIN (#.*)"))
    part:re.Pattern = field(default_factory=lambda:re.compile(r"^:([^ ]*)!\1@\1\.tmi\.twitch\.tv PART (#.*)"))

    message:re.Pattern = field(default_factory=lambda:re.compile(r"^@([^ ]*) ([^ ]*) PRIVMSG #([^:]*) :(.*)"))
    message_command: re.Pattern = field(default_factory=lambda: re.compile(r"^([!.?#])([^ ]*)(.*)"))

    user_notice:re.Pattern = field(default_factory=lambda:re.compile(r"^([^ ]*) ([^ ]*) USERNOTICE #([^:]*) :(.*)"))
    user_notice_raid:re.Pattern = field(default_factory=lambda:re.compile(r"^([^ ]*msg-id=raid[^ ]*) :tmi.twitch.tv USERNOTICE #([^ ]*)$"))
    user_state:re.Pattern = field(default_factory=lambda:re.compile(r"^@([^ ]*) :tmi\.twitch\.tv USERSTATE #([^:]*)"))
    username:re.Pattern = field(default_factory=lambda:re.compile(r":([^!]*)!\1@\1\.tmi\.twitch\.tv"))