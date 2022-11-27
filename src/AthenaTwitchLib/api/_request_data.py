# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import dataclasses
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

@dataclass(slots=True)
class RequestData_GET(RequestData):
    http_command:HttpCommand = HttpCommand.GET

@dataclass(slots=True)
class RequestData_POST(RequestData):
    http_command:HttpCommand = HttpCommand.POST

@dataclass(slots=True)
class RequestData_PATCH(RequestData):
    http_command:HttpCommand = HttpCommand.PATCH

@dataclass(slots=True)
class RequestData_PUT(RequestData):
    http_command:HttpCommand = HttpCommand.PUT

@dataclass(slots=True)
class RequestData_DELETE(RequestData):
    http_command:HttpCommand = HttpCommand.DELETE