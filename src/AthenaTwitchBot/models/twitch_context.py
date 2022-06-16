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

    #some non init stuff
    is_command:bool=field(init=False, default=False)
    command_str:str=field(init=False, default=None)
    is_reply:bool=field(init=False, default=False)
    output_text:str=field(init=False, default=None)

    def reply(self, text:str):
        self.is_reply = True
        self.output_text=self._cleanup_output_text(text)

    def write(self, text:str):
        self.output_text=self._cleanup_output_text(text)

    @staticmethod
    def _cleanup_output_text(text:str) -> str:
        return text.replace("\n", " ")