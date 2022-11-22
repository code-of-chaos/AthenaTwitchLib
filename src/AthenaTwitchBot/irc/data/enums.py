# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import enum

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class LineHandlerType(enum.StrEnum):
    """
    Types of calls that are caught by the Protocol system.
    Used for logging.
    """
    PING : enum.auto()
    SERVER_MESSAGE : enum.auto()
    SERVER_353 : enum.auto()
    SERVER_366 : enum.auto()
    SERVER_CAP : enum.auto()
    JOIN : enum.auto()
    PART : enum.auto()
    MESSAGE : enum.auto()
    MESSAGE_COMMAND : enum.auto()
    MESSAGE_COMMAND_WITHOUT_ARGS : enum.auto()
    USER_NOTICE : enum.auto()
    USER_STATE : enum.auto()
    UNKNOWN : enum.auto()

class BotEvent(enum.Enum):
    """
    Types of Events that can be raised inside the Bot
    """
    RESTART = enum.auto()
    EXIT = enum.auto()
