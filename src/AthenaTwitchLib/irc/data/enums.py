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
class CommandTypes(enum.StrEnum):
    """
    The type of commands that are stored within the database, that then need to be parsed in a specific way.
    Commonly used by `CommandLogicSqlite` class.
    ===

    - DEFAULT : No argument parsing needs to be done within the output text
    - ARGS : Special argument parsing needs to be handled
    - EXIT : command triggers the exit of the connection
    - RESTART : command triggers the restart of the connection
    """

    DEFAULT = enum.auto()
    ARGS = enum.auto()
    EXIT = enum.auto()
    RESTART = enum.auto()
