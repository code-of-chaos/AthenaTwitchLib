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
class BotEvent(enum.Enum):
    """
    Types of Events that can be raised inside the Bot
    """
    RESTART = enum.auto()
    EXIT = enum.auto()


# ----------------------------------------------------------------------------------------------------------------------
class OutputTypes(enum.StrEnum):
    """
    Simple Enum for the Output Type of the Bot
    ===

    - Write : Means the bot will simply write the message to chat
    - Reply : Means the bot will write the message as a response to a previous message
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
    - EXIT : command triggers the exit of the bot
    - RESTART : command triggers the restart of the bot
    """

    DEFAULT = enum.auto()
    ARGS = enum.auto()
    EXIT = enum.auto()
    RESTART = enum.auto()
