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
class TwitchUser:
    """
    Simple data class that holds a single user text

    Parameters:
    - name: name of the user
    """
    name:str

    def __post_init__(self) -> None:
        # :billy_ikanda!billy_ikanda@billy_ikanda.tmi.twitch.tv
        self.name = self.name.split("!")[0][1:]

    def __str__(self) -> str:
        return self.name
