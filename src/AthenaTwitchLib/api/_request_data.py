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
from AthenaTwitchLib.api.data.enums import DataFromConnection, HttpMethod, TokenScope

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class RequestData:
    url:TwitchApiUrl
    http_method:HttpMethod
    data:dict = field(default_factory=dict)
    data_from_connection:tuple[DataFromConnection] = field(default_factory=tuple)
    params: dict = field(default_factory=dict)
    params_from_connection:tuple[DataFromConnection] = field(default_factory=tuple)
    headers:dict = field(default_factory=dict)
    header_include_oath:bool = True
    scopes:set[TokenScope] = field(default_factory=set)

    @classmethod
    def GET(cls,*args, **kwargs) -> Self:
        return cls(*args, http_method= HttpMethod.GET, **kwargs)

    @classmethod
    def POST(cls,*args, **kwargs) -> Self:
        return cls(*args, http_method= HttpMethod.POST, **kwargs)

    @classmethod
    def PATCH(cls,*args, **kwargs) -> Self:
        return cls(*args, http_method= HttpMethod.PATCH, **kwargs)

    @classmethod
    def PUT(cls,*args, **kwargs) -> Self:
        return cls(*args, http_method= HttpMethod.PUT, **kwargs)

    @classmethod
    def DELETE(cls,*args, **kwargs) -> Self:
        return cls(*args, http_method= HttpMethod.DELETE, **kwargs)
