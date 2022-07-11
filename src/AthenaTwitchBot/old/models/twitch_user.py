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
@dataclass(init=False,slots=True)
class TwitchUser:
    name:str
    raw_str:str

    def __init__(self, raw_str:str):
        self.raw_str = raw_str
        self.name = raw_str.split("!")[0][1:]

    def __str__(self) -> str:
        return self.name
