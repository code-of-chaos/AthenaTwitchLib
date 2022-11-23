# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import enum

# Athena Packages
from AthenaLib.logging import AthenaSqliteLogger

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class IrcLogger(AthenaSqliteLogger):

    class Sections(enum.StrEnum):
        CALLED_HANDLERS = enum.auto()
        UNKNOWN_TAG = enum.auto()
