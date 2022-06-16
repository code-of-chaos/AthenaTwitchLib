# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.outputs.output import Output
from AthenaTwitchBot.models.twitch_bot import TwitchBot

from AthenaTwitchBot.functions.twitch_irc_messages import format_message
from AthenaTwitchBot.data.twitch_irc_messages import *

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class OutputTwitch(Output):
    async def connection_made(self, bot:TwitchBot, transport: asyncio.transports.Transport,**kwargs):
        transport.write(format_message(f"{PASS}{bot.oauth_token}"))
        transport.write(format_message(f"{NICK} {bot.nickname}"))
        transport.write(format_message(f"{JOIN} {','.join(str(c) for c in bot.channels)}"))
        transport.write(format_message(REQUEST_TAGS))

    async def connection_ping(self, transport: asyncio.transports.Transport, ping_response:list[str], **kwargs):
        transport.write(format_message(f"{PONG} {' '.join(ping_response)}"))

    async def undefined(self,**kwargs):
        pass # don't answer to something that is undefined

    async def command(self,context, **kwargs):
        pass