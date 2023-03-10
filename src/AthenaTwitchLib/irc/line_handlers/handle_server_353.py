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
class LineHandler_Server353(IrcLineHandler):
    """
    Class is called when twitch sends a 353 message
    """
    _console_color:Callable = Fore.AliceBlue
    _console_section:str = 'SERVER_353'

    async def _output_logger(self, *args, **kwargs):
        ...
