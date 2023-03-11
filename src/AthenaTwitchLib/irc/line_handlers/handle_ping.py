# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
import re
import dataclasses

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.irc_line_handler import IrcLineHandler
from AthenaTwitchLib.logger import IrcSections


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclasses.dataclass(slots=True)
class LineHandler_Ping(IrcLineHandler):
    """
    Class is called when the Twitch server sends a keep alive PING message
    Needs to have the reply: `"PONG :tmi.twitch.tv` for the connection to remain alive
    """
    _section:IrcSections = IrcSections.PING

    async def handle_line(self, conn_event:asyncio.Future, transport: asyncio.Transport, matched_content: re.Match,
                          original_line: str):
        # Executes the default output and log when the data is first given.
        await super(LineHandler_Ping, self).handle_line(conn_event, transport, matched_content, original_line)

        # Need this to keep connection alive
        transport.write("PONG :tmi.twitch.tv\r\n".encode())