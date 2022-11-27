# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Athena Packages

# Local Imports
from AthenaTwitchLib.api.data.urls import TwitchApiUrl
from AthenaTwitchLib.api._request_data import RequestData

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def start_commercial(broadcaster_id:int, length:int) -> RequestData:
    return RequestData(
        url=TwitchApiUrl.CHANNEL_COMMERCIAL,
        data={
            "broadcaster_id": broadcaster_id,
            "length": length
        }
    )