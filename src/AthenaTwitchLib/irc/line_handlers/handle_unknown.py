# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dataclasses

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.irc_line_handler import IrcLineHandler
from AthenaTwitchLib.logger import IrcSections


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclasses.dataclass(slots=True)
class LineHandler_Unknown(IrcLineHandler):
    """
    Class is called when the Twitch server sends a keep alive PING message
    Needs to have the reply: `"PONG :tmi.twitch.tv` for the connection to remain alive
    """
    _section:IrcSections = IrcSections.UNKNOWN
