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
class LineHandler_Part(IrcLineHandler):
    """
    Class is called when any user (irc or viewer) joins the channel
    """

    async def _output_on_ingest_console(self, matched_content: re.Match, original_line: str):
        print(f"{Fore.DeepPink('Part')} | {original_line}")

    async def _output_on_ingest_logger(self, matched_content: re.Match, original_line: str):
        ...

    async def _handle_line(self, transport:asyncio.Transport, matched_content: re.Match, original_line: str):
        ...