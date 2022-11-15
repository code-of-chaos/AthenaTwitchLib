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