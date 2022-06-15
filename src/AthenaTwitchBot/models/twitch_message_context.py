# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import asyncio

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_message import TwitchMessage

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True,eq=False,order=False,match_args=True)
class TwitchMessageContext:
    message:TwitchMessage
    transport:asyncio.Transport

    # things not to be defined on init
    username:str=field(init=False)

    def __post_init__(self):
        self.username = f"@{self.message.username}"

    def reply(self, text:str):
        """
        a "reply" method does reply to the user's message that invoked the command
        """
        self.transport.write(
            f"@reply-parent-msg-id={self.message.message_id} PRIVMSG {self.message.channel} :{text}\r\n".encode("UTF_8")
        )

    def write(self, text:str):
        """
        a "write" method does not reply to the message that invoked the command, but simply writes the text to the channel
        """
        self.transport.write(
            f"PRIVMSG {self.message.channel} :{text}\r\n".encode("UTF_8")
        )