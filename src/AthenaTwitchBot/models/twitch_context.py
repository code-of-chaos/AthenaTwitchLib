# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_user import TwitchUser
from AthenaTwitchBot.models.twitch_channel import TwitchChannel
from AthenaTwitchBot.models.twitch_message_tags import TwitchMessageTags

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, eq=False, order=False, match_args=True, repr=True)
class TwitchContext:
    message_tags:TwitchMessageTags
    user:TwitchUser
    channel:TwitchChannel
    raw_text:tuple[str]
    raw_irc:list[str]

    #some non init stuff
    command_str:str=field(init=False, default=None)
    command_args:tuple[str]=field(init=False, default_factory=tuple)
    is_reply:bool=field(init=False, default=False)
    is_write:bool=field(init=False, default=False)
    output_text:str=field(init=False, default=None)

    def reply(self, text:str):
        self.is_reply = True
        self.output_text = text

    def write(self, text:str):
        self.is_write = True
        self.output_text = text