# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
import re
import dataclasses

# Athena Packages
from AthenaColor import ForeNest as Fore

# Local Imports
from AthenaTwitchLib.irc.irc_line_handler import IrcLineHandler

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclasses.dataclass(slots=True)
class LineHandler_Ping(IrcLineHandler):
    """
    Class is called when the Twitch server sends a keep alive PING message
    Needs to have the reply: `"PONG :tmi.twitch.tv` for the connection to remain alive
    """

    async def _output_on_ingest_console(self, matched_content: re.Match, original_line: str):
        print(f"{Fore.Peru('PONG')} | {original_line}")

    async def _output_on_ingest_logger(self, matched_content: re.Match, original_line: str):
        ...

    async def _handle_line(self, transport:asyncio.Transport, matched_content: re.Match, original_line: str):
        # Need this to keep connection alive
        transport.write("PONG :tmi.twitch.tv\r\n".encode())