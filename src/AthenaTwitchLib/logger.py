# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import pathlib
import enum

# Athena Packages
from AthenaLib.logging.logger_sqlite import AthenaSqliteLogger

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Section Enums -
# ----------------------------------------------------------------------------------------------------------------------
class SectionIRC(enum.StrEnum):
    """
    Enum which holds all possible section types for the IrcLogger
    """
    HANDLER_CALLED = enum.auto()
    HANDLER_UNKNOWN = enum.auto()

    MSG = enum.auto()
    MSG_CONTEXT = enum.auto()
    MSG_TAGS = enum.auto()
    MSG_TAGS_UNKNOWN = enum.auto()

    CONNECTION_REFUSED = enum.auto()
    CONNECTION_MADE = enum.auto()
    CONNECTION_RESTART = enum.auto()
    CONNECTION_EXIT = enum.auto()

    LOGIN = enum.auto()
    LOGIN_MSG = enum.auto()
    LOGIN_CAPABILITY = enum.auto()

    JOIN = enum.auto()
    CMD_DATA = enum.auto()
    CMD_UNKNOWN = enum.auto()
    CMD_NOT_PARSABLE = enum.auto()

# ----------------------------------------------------------------------------------------------------------------------
class SectionAPI(enum.StrEnum):
    """
    Enum which holds all possible section types for the ApiLogger
    """

# ----------------------------------------------------------------------------------------------------------------------
# - Loggers -
# ----------------------------------------------------------------------------------------------------------------------
IrcLogger = AthenaSqliteLogger(
    sqlite_path=pathlib.Path("data/logger.sqlite"),
    table_to_use="logger_twitch_irc"
)

ApiLogger = AthenaSqliteLogger(
    sqlite_path=pathlib.Path("data/logger.sqlite"),
    table_to_use="logger_twitch_api"
)
