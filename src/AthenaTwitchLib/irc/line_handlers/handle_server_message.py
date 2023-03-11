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
class LineHandler_ServerMessage(IrcLineHandler):
    """
    Class is called when the Twitch server sends a message that isn't related to any user or room messages
    """
    _section:IrcSections = IrcSections.SERVER_MESSAGE

