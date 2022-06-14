# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(init=False, slots=True, eq=True, match_args=True)
class TwitchMessage:
    message:list[str]

    def __init__(self, message_bytes:bytearray):
        self.message = message_bytes.decode("utf_8").replace("\r\n", "").split(" ")