# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import pathlib

# Athena Packages
from AthenaLib.logging.logger_sqlite import AthenaSqliteLogger

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
IrcLogger = AthenaSqliteLogger(
    sqlite_path=pathlib.Path("data/logger.sqlite"),
    table_to_use="logger_twitch_irc"
)

ApiLogger = AthenaSqliteLogger(
    sqlite_path=pathlib.Path("data/logger.sqlite"),
    table_to_use="logger_twitch_api"
)
