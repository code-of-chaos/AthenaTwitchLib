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
    _console_color:Callable = Fore.SlateGray
    _console_section:str = 'UNKNOWN'

    async def _output_logger(self, *args, **kwargs):
        IrcLogger.log_warning(section=SectionIRC.HANDLER_UNKNOWN, data=line)
