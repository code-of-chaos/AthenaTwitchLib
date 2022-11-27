# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Athena Packages

# Local Imports
from AthenaTwitchLib.api.data.urls import TwitchApiUrl

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class RequestData:
    url:TwitchApiUrl
    data:dict = field(default_factory=dict)
    params: dict[str:str] = field(default_factory=dict)
    headers:dict = field(default_factory=dict)