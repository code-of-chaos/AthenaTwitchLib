# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass

# Custom Library
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class TwitchBot:
    """
    Simple data class that holds all data meant to create the bot

    Parameters:
    - nickname: the name your bot has on twitch
    - oauth_token: the token used to connect the twitch IRC
    - channel: list of channels to connect to
    - command_prefix: the piece of text the bot will look for to catch commands
    """
    nickname:str
    oauth_token:str
    channels:list[TwitchChannel]
    command_prefix:str