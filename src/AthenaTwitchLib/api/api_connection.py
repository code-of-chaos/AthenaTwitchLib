# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dataclasses
from dataclasses import dataclass, field
import aiohttp
from typing import Callable, AsyncGenerator
import uuid

from AthenaTwitchLib.api._token_data import TokenData
# Athena Packages

# Local Imports
from AthenaTwitchLib.api.data.urls import TwitchApiUrl
from AthenaTwitchLib.api.data.enums import DataFromConnection, HttpCommand
from AthenaTwitchLib.logger import ApiLogger, SectionAPI
from AthenaTwitchLib.api._request_data import RequestData
from AthenaTwitchLib.api._user_data import UserData
from AthenaTwitchLib.api.requests import ConnectionRequests

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
    token:TokenData = field(init=False, default=None)

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
            self.user = await self.get_user_data()

        if self.token is None:
            self.token = await self.validate_token()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_from_connection(self, data_connection:tuple[DataFromConnection]) -> dict:
        return {
            str(d_enum): _mapping_data_from_connection.get(d_enum)(self)
            for d_enum in data_connection
        }

    # ------------------------------------------------------------------------------------------------------------------
    # - Special Http commands -
    # ------------------------------------------------------------------------------------------------------------------
    async def validate_token(self) -> TokenData:
        token_data = await self.get(
            ConnectionRequests.validate_token(self.oath_token),
            check_scope=False
        )
        ApiLogger.log_debug(section=SectionAPI.USER_DATA, data=token_data)
        return TokenData(**token_data)

    async def get_user_data(self) -> UserData:
        user_data = await self.get(
            ConnectionRequests.get_user(username=self.username),
            check_scope=False
        )
        ApiLogger.log_debug(section=SectionAPI.USER_DATA, data=user_data)
        return UserData(**user_data["data"][0])

    # ------------------------------------------------------------------------------------------------------------------
    # - Http commands -
    # ------------------------------------------------------------------------------------------------------------------
    async def _http_switch(self,request_data:RequestData) -> dict:
        ApiLogger.log_debug(section=SectionAPI.REQUEST_SEND, data=request_data)
        match request_data:

            case RequestData(http_command=HttpCommand.GET):
                result = await self.get(request_data)

            case RequestData(http_command=HttpCommand.POST):
                result = await self.post(request_data)

            case _:
                raise ValueError

        ApiLogger.log_debug(section=SectionAPI.REQUEST_RESULT, data=result)
        return result

    async def request(self,request_data:RequestData,*,limit:int=None) -> AsyncGenerator[dict, None]:
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
            match (result := await self._http_switch(request_data)):
                # Normal flow of data
                case {"data": data,}:
                    #   Go over items
                    for item in data:
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


                # Error thrown by the API
                case {"error":_, "status":_, "message": _}:
                    yield result
                    return

                # Something unexpected came back
                case _:
                    raise ValueError(result)

    async def get(self, request_data:RequestData, check_scope:bool=True) -> dict:
        # Check if all scopes are present
        if check_scope and not (token_scopes := self.token.scopes) >= (request_scopes := request_data.scopes):
            raise PermissionError(
                f"Token did not have required scopes:\nToken Scopes: {token_scopes}\nScopes required: {request_scopes}"
            )

        # make a union of both dictionaries
        #   Don't store them to the request_data, as this is a frozen dataclass
        headers = request_data.headers
        if request_data.header_include_oath:
             headers |= self._headers_auth

        params = request_data.params | self.get_from_connection(request_data.params_from_connection)

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(request_data.url, params=params) as response:
                return await response.json()

    async def post(self, request_data:RequestData, check_scope:bool=True) -> dict:
        # Check if all scopes are present
        if check_scope and not (token_scopes := self.token.scopes) >= (request_scopes := request_data.scopes):
            raise PermissionError(
                f"Token did not have required scopes:\nToken Scopes: {token_scopes}\nScopes required: {request_scopes}"
            )

        # make a union of both dictionaries
        #   Don't store them to the request_data, as this is a frozen dataclass
        headers = request_data.headers | self._headers_auth
        data = request_data.data | self.get_from_connection(request_data.data_from_connection)
        params = request_data.params | self.get_from_connection(request_data.params_from_connection)

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(request_data.url, data=data, params=params) as response:
                return await response.json()

