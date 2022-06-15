# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
import socket

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot import TwitchBot

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True,eq=False,order=False,kw_only=True)
class Server:
    bot: TwitchBot
    socket:socket.socket=field(default_factory=socket.socket)

    # non init slots
    server:asyncio.AbstractServer = field(init=False)

    def launch(self):
        pass