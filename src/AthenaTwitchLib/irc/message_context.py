# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, asdict
import asyncio

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.tags import TagsPRIVMSG
from AthenaTwitchLib.string_formatting import twitch_irc_output_format

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True, frozen=True)
class MessageContext:
    """
    Frozen Dataclass which holds the context that will be used by the LogicBot to handle an incoming message
    """
    tags:TagsPRIVMSG
    user:str
    username:str
    channel:str
    text:str

    transport:asyncio.Transport
    bot_event_future:asyncio.Future
    original_line:str

    def as_dict(self) -> dict:
        """
        Casts the object to a dict that is usable in a JSON format
        """
        return {
            "tags": asdict(self.tags),
            "user": self.user,
            "username": self.username,
            "channel": self.channel,
            "text": self.text
        }

    async def reply(self, reply_msg:str):
        """
        Replies to the given message of the channel where it came from:
        """
        self.transport.write(
            twitch_irc_output_format(f"@reply-parent-msg-id={self.tags.id} PRIVMSG #{self.channel} :{reply_msg}")
        )

    async def write(self, write_msg:str):
        """
        Writes a message to the channel it came from:
        """
        self.transport.write(
            twitch_irc_output_format(f"PRIVMSG #{self.channel} :{write_msg}")
        )

# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True,kw_only=True, frozen=True)
class MessageCommandContext(MessageContext):
    """
    Frozen Dataclass which holds the context that will be used by the LogicBot to handle an incoming message
    The message in question should be a command
    """
    command:str
    args:list[str]

    def __post_init__(self):
        if self.args == ['']:
            self.args.clear()
