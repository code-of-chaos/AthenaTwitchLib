# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Self
from dataclasses import dataclass, field

# Athena Packages

# Local Imports
from AthenaTwitchLib.api.data.urls import TwitchApiUrl
from AthenaTwitchLib.api.data.enums import DataFromConnection, HttpCommand

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class RequestData:
    url:TwitchApiUrl
    http_command:HttpCommand
    data:dict = field(default_factory=dict)
    data_from_connection:tuple[DataFromConnection] = field(default_factory=tuple)
    params: dict = field(default_factory=dict)
    params_from_connection:tuple[DataFromConnection] = field(default_factory=tuple)
    headers:dict = field(default_factory=dict)

    @classmethod
    def get(cls,*args, **kwargs) -> Self:
        return cls(*args, http_command = HttpCommand.GET, **kwargs)

    @classmethod
    def post(cls,*args, **kwargs) -> Self:
        return cls(*args, http_command = HttpCommand.POST, **kwargs)

    @classmethod
    def patch(cls,*args, **kwargs) -> Self:
        return cls(*args, http_command = HttpCommand.PATCH, **kwargs)

    @classmethod
    def put(cls,*args, **kwargs) -> Self:
        return cls(*args, http_command = HttpCommand.PUT, **kwargs)

    @classmethod
    def delete(cls,*args, **kwargs) -> Self:
        return cls(*args, http_command = HttpCommand.DELETE, **kwargs)
