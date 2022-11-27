# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dataclasses
from dataclasses import dataclass, field
import aiohttp
from typing import Callable, Generator
import contextlib

# Athena Packages

# Local Imports
from AthenaTwitchLib.api.data.urls import TwitchApiUrl
from AthenaTwitchLib.api.data.enums import DataFromConnection, HttpCommand
from AthenaTwitchLib.logger import ApiLogger
from AthenaTwitchLib.api._request_data import RequestData
from AthenaTwitchLib.api._user_data import UserData

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
_mapping_data_from_connection: dict[DataFromConnection:Callable] = {
    DataFromConnection.BROADCASTER_ID : lambda api_conn: api_conn.user.id,
    DataFromConnection.MODERATOR_ID : lambda api_conn: api_conn.user.id,
}
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
    user:UserData = field(init=False, default=None)

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
        if self.user is None:
            data = await self.get(RequestData(
                url=TwitchApiUrl.USERS,
                http_command=HttpCommand.GET,
                params={"login": self.username}
            ))
            self.user = UserData(**data["data"][0])

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_from_connection(self, data_connection:tuple[DataFromConnection]) -> dict:
        return {
            str(d_enum): _mapping_data_from_connection.get(d_enum)(self)
            for d_enum in data_connection
        }

    # ------------------------------------------------------------------------------------------------------------------
    # - Http commands -
    # ------------------------------------------------------------------------------------------------------------------
    async def _http_switch(self,request_data:RequestData) -> dict:
        match request_data:

            case RequestData(http_command=HttpCommand.GET):
                return await self.get(request_data)

            case RequestData(http_command=HttpCommand.POST):
                return await self.post(request_data)

            case _:
                raise ValueError

    async def request(self,request_data:RequestData,*,limit:int=None) -> Generator[dict, None, None]:
        """
        Creates a request to the Twitch API.
        Returns a Generator object that goes over all items in the "Data" key of the json response.
        Will automatically process pagination, and continue request data to the Twitch API if need be.
        """
        # Assign pagination to begin with a TRUE value
        #   Ensures we at least enter the while loop once
        pagination:bool|dict = True
        processed_items:int = 0

        # the Pagination key will most likely always exists, but won't always have some data.
        #   This allows for Truthy checks
        while pagination:

            # Get the result from the new request
            #   Go over items
            for item in (result := await self._http_switch(request_data))["data"]:
                yield item
                processed_items += 1

                # If the limit has been reached
                #   Quit out of the generator
                if limit is not None and processed_items >= limit:
                    return

            # Assign pagination again
            #   Overwrites, so we can keep using the same variable name
            #   Ensures our while statement will quit out at some point
            pagination = result.get("pagination", False)

            # Update the request data with the new cursor as a parameters for the query
            #   The only thing that needs to be altered is the "after" parameter
            #   Keep all other values as is
            #   Only get the cursor if pagination still exists, else causes error
            if pagination and (cursor := pagination.get("cursor", False)):
                request_data.params["after"] = cursor

    async def get(self, request_data:RequestData) -> dict:
        # make a union of both dictionaries
        #   Don't store them to the request_data, as this is a frozen dataclass
        headers = request_data.headers | self._headers_auth
        params = request_data.params | self.get_from_connection(request_data.params_from_connection)

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(request_data.url, params=params) as response:
                return await response.json()

    async def post(self, request_data:RequestData) -> dict:
        # make a union of both dictionaries
        #   Don't store them to the request_data, as this is a frozen dataclass
        headers = request_data.headers | self._headers_auth
        data = request_data.data | self.get_from_connection(request_data.data_from_connection)
        params = request_data.params | self.get_from_connection(request_data.params_from_connection)

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(request_data.url, data=data, params=params) as response:
                return await response.json()

