# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dataclasses
from typing import Callable

# Athena Packages
from AthenaColor import ForeNest as Fore

# Local Imports
from AthenaTwitchLib.irc.irc_line_handler import IrcLineHandler

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclasses.dataclass(slots=True)
class LineHandler_ServerCap(IrcLineHandler):
    """
    Class is called when the Twitch server sends a message that isn't related to any user or room messages
    """
    _console_color:Callable = Fore.Khaki
    _console_section:str = 'SERVER_CAP'

    async def _output_logger(self, *args, **kwargs):
        ...
