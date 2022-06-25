# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.bot.twitch_channel import TwitchChannel

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True,eq=False,order=False,kw_only=True)
class TwitchBot:
    nickname:str
    oauth_token:str
    channels:list[TwitchChannel]
    prefix:str

    commands:dict=field(default_factory=dict)
    scheduled_tasks:list=field(default_factory=list)

    # Twitch-specific capabilities : https://dev.twitch.tv/docs/irc/capabilities
    capability_commands: bool = False # enables the usage of /... chat commands by the bot
    capability_membership: bool = False # lets bot receive notifications fo
    capability_tags: bool = True  # only one that has the default set to true, as this is required to make reply's work
