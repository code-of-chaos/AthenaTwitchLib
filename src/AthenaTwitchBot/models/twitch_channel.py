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
@dataclass(slots=True)
class TwitchChannel:
    """
    Simple data class that holds a single channel

    Parameters:
    - name: name of the channel
    """
    name:str

    def __post_init__(self):
        if self.name[0] != "#":
            self.name = f"#{self.name}"

    def __str__(self) -> str:
        return self.name