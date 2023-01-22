# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import pathlib

# Athena Packages
from AthenaLib.logging.logger_sqlite import AthenaSqliteLogger

# Local Imports
from AthenaTwitchLib.logger._cast_to_str import api_cast_to_str

# ----------------------------------------------------------------------------------------------------------------------
# - Loggers -
# ----------------------------------------------------------------------------------------------------------------------
IrcLogger = AthenaSqliteLogger(
    sqlite_path=pathlib.Path("data/logger.sqlite"),
    table_to_use="logger_twitch_irc"
)

ApiLogger = AthenaSqliteLogger(
    sqlite_path=pathlib.Path("data/logger.sqlite"),
    table_to_use="logger_twitch_api",
    cast_to_str=api_cast_to_str
)
