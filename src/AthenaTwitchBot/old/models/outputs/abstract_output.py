# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from abc import ABC, abstractmethod

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot import TwitchBot
from AthenaTwitchBot.models.twitch_context import TwitchContext

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class AbstractOutput(ABC):

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    async def connection_made(self, bot:TwitchBot, **kwargs):
        """Output of data when the connection to the Twitch servers is established"""

    @abstractmethod
    async def connection_ping(self, ping_response:list[str],**kwargs):
        """Output response to a ping sent by the Twitch servers"""

    @abstractmethod
    async def undefined(self,text:str, **kwargs):
        """Output response to anything that wasn't caught correctly"""

    @abstractmethod
    async def write(self, context:TwitchContext, **kwargs):
        """Output which context is not a reply, but simply write out to the chat"""

    @abstractmethod
    async def reply(self, context:TwitchContext, **kwargs):
        """Output which context is a reply to a user"""

    @abstractmethod
    async def scheduled_task(self, context:TwitchContext, **kwargs):
        """Automated output after a task has been run"""