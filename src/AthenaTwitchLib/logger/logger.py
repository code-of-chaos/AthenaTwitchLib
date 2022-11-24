# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Athena Packages
from AthenaLib.logging.logger_sqlite import AthenaSqliteLogger

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
IrcLogger = AthenaSqliteLogger(table_to_use="logger_twitch_irc")
ApiLogger = AthenaSqliteLogger(table_to_use="logger_twitch_api")