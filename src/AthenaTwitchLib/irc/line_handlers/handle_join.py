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
class LineHandler_Join(IrcLineHandler):
    """
    Class is called when any user (irc or viewer) joins the channel
    """
    _console_color:Callable = Fore.Red
    _console_section:str = 'JOIN'

    async def _output_logger(self, *args, **kwargs):
        ...