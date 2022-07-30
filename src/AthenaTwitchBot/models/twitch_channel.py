# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.functions.athena_dataclass import _dataclass

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@_dataclass(slots=True)
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