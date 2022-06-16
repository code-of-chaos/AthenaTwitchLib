# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot import TwitchBot

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Output(ABC):

    @abstractmethod
    async def connection_made(self, bot:TwitchBot, transport: asyncio.transports.Transport,**kwargs):
        """Output of data when the connection to the Twitch servers is established"""

    @abstractmethod
    async def connection_ping(self, transport: asyncio.transports.Transport, ping_response:list[str],**kwargs):
        """Output response to a ping sent by the Twitch servers"""

    @abstractmethod
    async def undefined(self,text:str, **kwargs):
        """Output response to anything that wasn't caught correctly"""

    @abstractmethod
    async def command(self,context, **kwargs):
        """Output response to a command that was given to the bot by a viewer"""