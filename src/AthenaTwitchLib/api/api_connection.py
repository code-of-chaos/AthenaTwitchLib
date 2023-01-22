# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import aiohttp
from typing import Callable, AsyncGenerator

from AthenaTwitchLib.api._token_data import TokenData
# Athena Packages

# Local Imports
from AthenaTwitchLib.api.data.enums import DataFromConnection, HttpMethod
from AthenaTwitchLib.logger import ApiLogger, SectionAPI
from AthenaTwitchLib.api._request_data import RequestData
from AthenaTwitchLib.api._user_data import UserData
from AthenaTwitchLib.api.requests import ConnectionRequests, ApiRequests

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
_mapping_data_from_connection: dict[DataFromConnection:Callable] = {
    DataFromConnection.BROADCASTER_ID : lambda api_conn: api_conn.user.id,
    DataFromConnection.MODERATOR_ID : lambda api_conn: api_conn.user.id,
    DataFromConnection.OATH_TOKEN : lambda api_conn: api_conn.oath_token
}

# Create the simple Hash switch for the `ApiConnection._http_execute`
_http_execute_switch = {
    HttpMethod.GET:     lambda *,session,url,params,     **_:   session.get(url, params=params),
    HttpMethod.POST:    lambda *,session,url,params,data,**_:   session.post(url, data=data, params=params),
    HttpMethod.PUT:     lambda *,session,url,params,data,**_:   session.put(url, data=data, params=params),
    HttpMethod.PATCH:   lambda *,session,url,params,data,**_:   session.patch(url, data=data, params=params),
    HttpMethod.DELETE:  lambda *,session,url,params,data,**_:   session.delete(url, data=data, params=params),
}

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class ApiConnection:
    oath_token:str

    # Non init
    user:UserData = field(init=False, default=None)
    token:TokenData = field(init=False, default=None)

    # Extra data needed for special cases
    _headers_auth:dict = field(init=False, default=None)

    # ------------------------------------------------------------------------------------------------------------------
    # - Properties -
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def headers_auth(self):
        if self._headers_auth is None:
            if self.token is None:
                raise PermissionError(
                    "Token has never been validated and stored to connection. "
                    "This can easily be resolved by using async with"
                )

            # Define if it hasn't been defined yet
            self._headers_auth = {
                "Authorization": f"Bearer {self.oath_token}",
                "Client-Id": self.token.client_id,
            }

        return self._headers_auth

    # ------------------------------------------------------------------------------------------------------------------
    # - Context managed -
    # ------------------------------------------------------------------------------------------------------------------
    async def __aenter__(self):
        # make sure that the user has at least logged in once to the api
        #   to get correct information
        if self.token is None:
            self.token = await self.validate_token()

        if self.user is None:
            user_data = await self._http_execute(ApiRequests.get_users(client_id=self.token.user_id))
            ApiLogger.log_debug(section=SectionAPI.USER_DATA, data=user_data)
            self.user = UserData(**user_data["data"][0])

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
        # Check if the token is valid
        #   When no longer valid, the API will throw an error
        token_data = await self._http_execute(
            ConnectionRequests.validate_token(self.oath_token),
            check_scopes=False
        )

        match token_data:
            # Normal flow of data
            case {"client_id":client_id,"login": login,"scopes": scopes, "user_id": user_id, "expires_in": expires_in}:
                ApiLogger.log_debug(section=SectionAPI.TOKEN_DATA, data=token_data)
                return TokenData(
                    client_id=client_id,
                    login=login, scopes=scopes,
                    user_id=user_id,
                    expires_in=expires_in
                )

            # Token has an error
            case {"status":_, "message":_}:
                raise PermissionError(token_data)

    # ------------------------------------------------------------------------------------------------------------------
    # - Http commands -
    # ------------------------------------------------------------------------------------------------------------------
    async def request_simple(self,request_data:RequestData) -> dict:
        """
        Creates a request to the Twitch API.
        Returns the result as is. Won't process pagination or go over the "data" items.
        """
        return await self._http_execute(request_data)

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
            match (result := await self._http_execute(request_data)):
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

    async def _http_execute(self,request_data:RequestData, check_scopes:bool=True) -> dict:
        ApiLogger.log_debug(section=SectionAPI.REQUEST_SEND, data=request_data)

        # Check if all scopes are present on the Oath Token
        #   This shouldn't be skipped, except for the original request of token validation
        #   Checks if all `request_scopes` is in `token_scopes`
        if check_scopes and not (token_scopes := self.token.scopes) >= (request_scopes := request_data.scopes):
            ApiLogger.log_warning(section=SectionAPI.TOKEN_INVALID, data=token_scopes)
            raise PermissionError(
                f"Token did not have required scopes:\nToken Scopes: {token_scopes}\nScopes required: {request_scopes}"
            )

        # Assemble all components with extra data
        #   Don't update the already set request_data as this with pagination the original data might be needed
        headers = request_data.headers | (self.headers_auth if request_data.header_include_oath else {})
        params = request_data.params | self.get_from_connection(request_data.params_from_connection)
        data = request_data.data | self.get_from_connection(request_data.data_from_connection)

        # Enter the session,
        #   so it will be closed correctly
        async with aiohttp.ClientSession(headers=headers) as session:
            async with _http_execute_switch[request_data.http_method](
                    session=session,
                    url=request_data.url,
                    params=params,
                    data=data
            ) as response:
                result = await response.json()

        # Log output
        ApiLogger.log_debug(section=SectionAPI.REQUEST_RESULT, data=result)
        return result