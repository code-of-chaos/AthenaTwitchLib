# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import aiohttp

# Athena Packages

# Local Imports
from AthenaTwitchLib.api.data.urls import TwitchApiUrl
from AthenaTwitchLib.logger import ApiLogger
from AthenaTwitchLib.api._request_data import RequestData

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class ApiConnection:
    username:str
    oath_token:str
    client_id:str

    # init False
    _headers_auth:dict = field(init=False)

    def __post_init__(self):
        self._headers_auth = {
            "Authorization": f"Bearer {self.oath_token}",
            "Client-Id": self.client_id,
        }

    # ------------------------------------------------------------------------------------------------------------------
    # - Context managed -
    # ------------------------------------------------------------------------------------------------------------------
    async def __aenter__(self):
        # make sure that the user has at least logged in once to the api
        #   to get correct information
        await self.get(RequestData(url=TwitchApiUrl.USERS, params={"login": self.username}))

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    # - Http commands -
    # ------------------------------------------------------------------------------------------------------------------
    async def get(self, request_data:RequestData) -> dict:

        # make a union of both dictionaries
        #   Don't store them to the request_data, as this is a frozen dataclass
        headers = request_data.headers | self._headers_auth

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(request_data.url,data=request_data.data, params=request_data.params) as response:
                return await response.json()


