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
class ConnectionEvent(enum.Enum):
    """
    Types of Events that can be raised inside the IRC Connection
    """
    RESTART = enum.auto()
    EXIT = enum.auto()


# ----------------------------------------------------------------------------------------------------------------------
class OutputTypes(enum.StrEnum):
    """
    Simple Enum for the Output Type of the IRC Connection Transport
    ===

    - Write : Means the connection will simply write the message to chat
    - Reply : Means the connection will write the message as a response to a previous message
    """
    WRITE = enum.auto()
    REPLY = enum.auto()

# ----------------------------------------------------------------------------------------------------------------------
class LineHandlers(enum.StrEnum):
    JOIN = enum.auto()
    MESSAGE = enum.auto()
    PART = enum.auto()
    PING = enum.auto()
    SERVER353 = enum.auto()
    SERVER366 = enum.auto()
    SERVERCAP = enum.auto()
    SERVERMESSAGE = enum.auto()
    UNKNOWN = enum.auto()
    USERNOTICE = enum.auto()
    USERSTATE = enum.auto()