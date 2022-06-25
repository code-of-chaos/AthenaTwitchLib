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
@dataclass(slots=True, init=False)
class TwitchChannel:
    name:str

    def __init__(self, name:str):
        # remove any "#" if they exist, so that all the __str__ casting happens the same way
        if " " in name:
            raise ValueError
        elif "#" != name[0]:
            self.name = f"#{name}"
        else:
            self.name = name

    def __str__(self) -> str:
        return self.name