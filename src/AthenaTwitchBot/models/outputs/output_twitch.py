# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.outputs.abstract_output import AbstractOutput
from AthenaTwitchBot.models.twitch_bot import TwitchBot
from AthenaTwitchBot.models.twitch_context import TwitchContext

from AthenaTwitchBot.functions.twitch_irc_messages import format_message
from AthenaTwitchBot.data.twitch_irc_messages import *
from AthenaTwitchBot.data.general import EMPTY_STR

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class OutputTwitch(AbstractOutput):
    def __init__(self, transport: asyncio.transports.Transport):
        self.transport = transport

    async def connection_made(self, bot:TwitchBot,**kwargs):
        self.transport.write(format_message(f"{PASS}{bot.oauth_token}"))
        self.transport.write(format_message(f"{NICK} {bot.nickname}"))
        self.transport.write(format_message(f"{JOIN} {','.join(str(c) for c in bot.channels)}"))
        self.transport.write(format_message(REQUEST_TAGS))

    async def connection_ping(self, ping_response:list[str], **kwargs):
        self.transport.write(format_message(f"{PONG} {' '.join(ping_response)}"))

    async def undefined(self,**kwargs):
        pass # don't answer to something that is undefined

    async def write(self, context:TwitchContext, **kwargs):
        if context.output_text is not None:
            self.transport.write(
                format_message(
                    f"{PRIVMSG} {context.channel} :{context.output_text}"
            ))

    async def reply(self, context:TwitchContext, **kwargs):
        if context.output_text is not None and context.message_tags.message_id != EMPTY_STR:
            self.transport.write(
                format_message(
                    f"@reply-parent-msg-id={context.message_tags.message_id} {PRIVMSG} {context.channel} :{context.output_text}"
            ))

    async def scheduled_task(self, context:TwitchContext, **kwargs):
        pass
