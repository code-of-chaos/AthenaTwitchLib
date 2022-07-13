# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import json
import urllib.request
import urllib.error
import asyncio
from dataclasses import dataclass, field
from functools import wraps

# Custom Library
import AthenaLib.HTTP.functions.requests as requests

# Custom Packages
from AthenaTwitchBot.models.twitch_api.twitch_api_user import TwitchApiUser
from AthenaTwitchBot.data.twitch_api_urls import TwitchApiURL
from AthenaTwitchBot.data.twitch_api_scopes import TwitchApiScopes

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
def connected_to_twitch(fnc):
    @wraps(fnc)
    async def wrapper(*args,**kwargs):
        self,  *_ = args #type: TwitchAPI
        if not self.is_connected:
            raise ValueError(f"TwitchAPI.connect() has to be run before the {fnc} can be used")
        return await fnc(*args, **kwargs)
    return wrapper

def user_has_scope(scope:TwitchApiScopes):
    def decorator(fnc):
        async def wrapper(*args,**kwargs):
            self, *_ = args  # type: TwitchAPI
            if scope not in self.user.scopes:
                raise ValueError(f"The scope of '{scope.value}' was not defined on the user")
            return await fnc(*args, **kwargs)
        return wrapper
    return decorator


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True,kw_only=True)
class TwitchAPI:
    broadcaster_token:str
    broadcaster_client_id:str

    # set after init
    user:TwitchApiUser=None

    # non init stuff
    is_connected:bool=field(init=False, default=False)
    _loop:asyncio.AbstractEventLoop = field(init=False)
    _header:dict=field(init=False, default=None)
    _header_json:dict=field(init=False, default=None)

    def __post_init__(self):
        self._loop = asyncio.get_running_loop()
        self._header = {
            "Authorization":f"Bearer {self.broadcaster_token}",
            "Client-Id":self.broadcaster_client_id
        }
        self._header_json = {
            "Authorization":f"Bearer {self.broadcaster_token}",
            "Client-Id":self.broadcaster_client_id,
            "Content-Type":"application/json"
        }
    # ------------------------------------------------------------------------------------------------------------------
    # - Methods that do all the magic -
    # ------------------------------------------------------------------------------------------------------------------
    async def _get(self, url:str, headers:dict,query_parameters:dict=None):
        try:
            response = await requests.get(
                url=url,
                headers=headers,
                loop=self._loop,
                query_parameters=query_parameters
            )
            try:
                return json.loads(response.read())
            except json.JSONDecodeError:
                return response.read()
        except urllib.error.URLError as e:
            print(e)
            raise

    async def _post(self,url:str, headers:dict,data:dict,query_parameters:dict=None):
        try:
            response = await requests.post(
                url=url,
                headers=headers,
                data=json.dumps(data).encode("utf_8"),
                loop=self._loop,
                query_parameters=query_parameters
            )
            if response is None:
                return {}
            try:
                return json.loads(response.read())
            except json.JSONDecodeError:
                return response.read()
        except urllib.error.URLError as e:
            print(e)
            raise

    async def _patch(self,url:str, headers:dict,data:dict,query_parameters:dict=None):
        try:
            response = await requests.patch(
                url=url,
                headers=headers,
                data=json.dumps(data).encode("utf_8"),
                loop=self._loop,
                query_parameters=query_parameters
            )
            if response is None:
                return {}
            try:
                return json.loads(response.read())
            except json.JSONDecodeError:
                return response.read()
        except urllib.error.URLError as e:
            print(e)
            raise

    # ------------------------------------------------------------------------------------------------------------------
    # - API methods-
    # ------------------------------------------------------------------------------------------------------------------
    async def connect(self) -> dict:
        # Execute the request
        login_data, scope_data = await asyncio.gather(
            self.login(),
            self.get_scopes()
        )

        # store the user, as some user data is required in further api commands
        self.user = TwitchApiUser.new_from_dict(login_data["data"][0]).set_scopes(scope_data["scopes"])
        self.is_connected = True

        # return the data dictionary back
        return login_data

    async def login(self) -> dict:
        return await self._get(
            url=TwitchApiURL.login.value,
            headers=self._header
        )

    async def get_scopes(self) -> dict:
        return await self._get(
            url=TwitchApiURL.scopes.value,
            headers={"Authorization": f"OAuth {self.broadcaster_token}"}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_custom_reward(self, *, reward_id:str=None, only_manageable_rewards:bool=False) -> dict:
        query = {"broadcaster_id":self.user.id}

        # assemble arguments
        if reward_id is not None:
            query["reward_id"] = reward_id
        if only_manageable_rewards:
            query["only_manageable_rewards"] = only_manageable_rewards

        return await self._get(
            url=TwitchApiURL.custom_rewards.value,
            headers=self._header,
            query_parameters=query
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelEditCommercial)
    @connected_to_twitch
    async def start_commercial(self, *, length:int):
        return await self._post(
            url=TwitchApiURL.commercial.value,
            headers=self._header_json,
            data={
                "broadcaster_id": self.user.id,
                "length": length
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.AnalyticsReadExtensions)
    @connected_to_twitch
    async def get_extension_analytics(
            self, *, after:str=None, ended_at:str=None, extension_id:str=None, first:int=None, started_at:str=None,
            type_:str=None
    ):
        query = {}

        # assemble query
        if after is not None:
            query["after"] = after
        if ended_at is not None:
            query["ended_at"] = ended_at
        if extension_id is not None:
            query["extension_id"] = extension_id
        if first is not None:
            query["first"] = first
        if started_at is not None:
            query["started_at"] = started_at
        if type_ is not None:
            query["type"] = type_

        return await self._get(
            url=TwitchApiURL.analytics_extension.value,
            headers=self._header,
            query_parameters=query
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.AnalyticsReadGames)
    @connected_to_twitch
    async def get_game_analytics(
            self, *, after:str=None, ended_at:str=None, game_id:str=None, first:int=None, started_at:str=None,
            type_:str=None
    ):
        query = {}

        # assemble query
        if after is not None:
            query["after"] = after
        if ended_at is not None:
            query["ended_at"] = ended_at
        if game_id is not None:
            query["game_id"] = game_id
        if first is not None:
            query["first"] = first
        if started_at is not None:
            query["started_at"] = started_at
        if type_ is not None:
            query["type"] = type_

        return await self._get(
            url=TwitchApiURL.analytics_extension.value,
            headers=self._header,
            query_parameters=query
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.BitsRead)
    @connected_to_twitch
    async def get_bits_leaderboard(
            self, *, count:int = None, period:str = None, started_at:str=None, user_id:str=None
    ):
        # assemble query
        query = {}
        if count is not None:
            query["count"] = count
        if period is not None:
            query["period"] = period
        if started_at is not None:
            query["started_at"] = started_at
        if user_id is not None:
            query["user_id"] = user_id


        return await self._get(
            url=TwitchApiURL.bits_leaderboard.value,
            headers=self._header,
            query_parameters=query
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_cheermotes(self, broadcaster_id:str=None):
        return await self._get(
            url=TwitchApiURL.cheermotes.value,
            headers=self._header,
            query_parameters={"broadcaster_id": broadcaster_id if broadcaster_id is not None else self.user.id}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_extension_transactions(self, extension_id:str, id_:str=None, after:str=None, first:int=None):
        # assemble query
        query = {"extension_id": extension_id}
        if id_ is not None:
            query["id_"] = id_
        if after is not None:
            query["after"] = after
        if first is not None:
            query["first"] = first

        return await self._get(
            url=TwitchApiURL.cheermotes.value,
            headers=self._header,
            query_parameters=query
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_channel_information(self, broadcaster_id:str=None):
        return await self._get(
            url=TwitchApiURL.channel_information.value,
            headers=self._header,
            query_parameters={"broadcaster_id": broadcaster_id if broadcaster_id is not None else self.user.id}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelManageBroadcast)
    @connected_to_twitch
    async def modify_channel_information(
            self, broadcaster_id:str=None, game_id:str=None, broadcaster_language:str=None, title:str=None,
            delay:int=None
    ):
        data={}
        if game_id is not None:
            data["game_id"] = game_id
        if broadcaster_language is not None:
            data["broadcaster_language"] = broadcaster_language
        if title is not None:
            data["title"] = title
        if delay is not None:
            data["delay"] = delay

        return await self._patch(
            url=TwitchApiURL.channel_information.value,
            headers=self._header_json,
            query_parameters={"broadcaster_id": broadcaster_id if broadcaster_id is not None else self.user.id},
            data=data
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelManageBroadcast)
    @connected_to_twitch
    async def get_channel_editors(self, broadcaster_id:str=None):
        return await self._get(
            url=TwitchApiURL.channel_editors.value,
            headers=self._header,
            query_parameters={"broadcaster_id": broadcaster_id if broadcaster_id is not None else self.user.id},
        )



