# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import asyncio

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.protocols.protocol_twitch import ProtocolTwitch
from AthenaTwitchBot.models.twitch_data_handler import TwitchDataHandler

from AthenaTwitchBot.data.connections import *

# ----------------------------------------------------------------------------------------------------------------------
# - All -
# ----------------------------------------------------------------------------------------------------------------------
__all__ = ["Launcher"]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Launcher:
    protocol_twitch_type:type[ProtocolTwitch]=ProtocolTwitch
    loop:asyncio.AbstractEventLoop=field(default_factory=asyncio.get_event_loop)

    ssl_enabled:bool=True

    # non init
    protocol_twitch:ProtocolTwitch=field(init=False, default=None)

    def launch(self):
        # create the connection to twitch and handle basic setup
        self.loop.run_until_complete(
            self.create_connection_twitch()
        )

        # run everything that is in the loop forever
        self.loop.run_forever()
        self.loop.close()

    async def create_connection_twitch(self):
        _, self.protocol_twitch = await self.loop.create_connection(
            protocol_factory=self.protocol_twitch_type.factory(
                data_handler=TwitchDataHandler()
            ),
            host=TWITCH_IRC_HOST if not self.ssl_enabled else TWITCH_IRC_HOST_SSL,
            port=TWITCH_IRC_PORT if not self.ssl_enabled else TWITCH_IRC_PORT_SSL,
            ssl=self.ssl_enabled
        )
        self.protocol_twitch.authenticate(

        )