# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Athena Packages

# Local Imports
from AthenaTwitchLib.api.data.urls import TwitchApiUrl
from AthenaTwitchLib.api._request_data import RequestData
from AthenaTwitchLib.api.data.enums import DataFromConnection

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def get_user(username:str) -> RequestData:
    return RequestData.GET(
        url=TwitchApiUrl.USERS,
        params={"login": username}
    )

def validate_token(oath_token:str) -> RequestData:
    return RequestData.GET(
        url=TwitchApiUrl.TOKEN_VALIDATE,
        headers={"Authorization":f"OAuth {oath_token}"},
        header_include_oath = False
    )