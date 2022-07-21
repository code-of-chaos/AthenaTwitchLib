# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import enum

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class MessageFlags(enum.Enum):
    """
    Collection of all Flags that can be set on a message.
    This is purely for the output handlers and doesn't affect the MessageContext
    """
    undefined="undefined"
    ping="ping"
    write="write"
    reply="reply"
    login="login"
    no_output="no_output"
    command_notice="command_notice"

