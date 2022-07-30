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
class TwitchUser:
    """
    Simple data class that holds a single user text

    Parameters:
    - name: name of the user
    """
    name:str

    def __post_init__(self):
        # :billy_ikanda!billy_ikanda@billy_ikanda.tmi.twitch.tv
        self.name = self.name.split("!")[0][1:]

    def __str__(self) -> str:
        return self.name