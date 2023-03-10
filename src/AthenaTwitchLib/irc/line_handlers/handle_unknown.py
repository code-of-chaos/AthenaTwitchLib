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
from AthenaTwitchLib.logger import IrcLogger, SectionIRC


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclasses.dataclass(slots=True)
class LineHandler_Unknown(IrcLineHandler):
    """
    Class is called when the Twitch server sends a keep alive PING message
    Needs to have the reply: `"PONG :tmi.twitch.tv` for the connection to remain alive
    """

    async def _output_on_ingest_console(self, matched_content: re.Match, original_line: str):
        print(Fore.SlateGray(f"NOT CAUGHT | {original_line}"))

    async def _output_on_ingest_logger(self, matched_content: re.Match, original_line: str):
        IrcLogger.log_warning(section=SectionIRC.HANDLER_UNKNOWN, data=line)

    async def _handle_line(self, transport:asyncio.Transport, matched_content: re.Match, original_line: str):
        ...