# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
import asyncio

# Athena Packages

# Local Imports
from AthenaTwitchBot.tags import TagsPRIVMSG
from AthenaTwitchBot.string_formatting import twitch_output_format

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class MessageContext:
    """
    Frozen Dataclass which holds the context that will be used by the LogicBot to handle an incomming message
    """
    tags:TagsPRIVMSG
    user:str
    channel:str
    text:str

    transport:asyncio.Transport
    bot_event_future:asyncio.Future

    async def reply(self, reply_msg:str):
        """
        Replies to the given message of the channel where it came from:
        """
        self.transport.write(
            twitch_output_format(
                f"@reply-parent-msg-id={self.tags.id} PRIVMSG #{self.channel} :{reply_msg}"
            )
        )

    async def write(self, write_msg:str):
        """
        Writes a message to the channel it came from:
        """
        self.transport.write(
            twitch_output_format(
                f"PRIVMSG #{self.channel} :{write_msg}"
            )
        )
