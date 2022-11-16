# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class BotSettings:
    """
    Instance of this class is used as the global settings system
    """
    bot_name:str
    bot_oath_token:str
    bot_join_channel:list[str] = field(default_factory=list)
    bot_join_message:str = None
    bot_prefix:str = "!"

    bot_capability_tags:bool=True,
    bot_capability_commands:bool=False,
    bot_capability_membership:bool=False,

    ssl_enabled: bool = True
    irc_host: str = 'irc.chat.twitch.tv'
    irc_port: int = 6667
    irc_port_ssl: int = 6697
