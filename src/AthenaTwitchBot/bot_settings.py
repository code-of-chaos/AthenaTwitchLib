# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class BotSettings:
    bot_name:str
    bot_oath_token:str
    bot_join_channel:str
    bot_join_message:str = None

    ssl_enabled: bool = True
    irc_host: str = 'irc.chat.twitch.tv'
    irc_port: int = 6667
    irc_port_ssl: int = 6697