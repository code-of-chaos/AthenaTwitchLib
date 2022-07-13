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

    twitch_capability_commands:bool=False
    twitch_capability_membership:bool=False
    twitch_capability_tags:bool=True # only one that has the default set to true, is required to make reply's work


    client_id:str=None # needed for the twitch API