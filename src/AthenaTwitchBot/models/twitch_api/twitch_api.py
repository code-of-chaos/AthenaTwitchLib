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

def has_scope(scope:TwitchApiScopes):
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
    _get_header:list[tuple[str,str]]=field(init=False, default=None)
    _post_header_json:list[tuple[str,str]]=field(init=False, default=None)

    def __post_init__(self):
        self._loop = asyncio.get_running_loop()
        self._get_header = [
            ("Authorization", f"Bearer {self.broadcaster_token}"),
            ("Client-Id", self.broadcaster_client_id)
        ]
        self._post_header_json = [
            *self._get_header,
            ("Content-Type", "application/json")
        ]

    # ------------------------------------------------------------------------------------------------------------------
    # - Methods that do all the magic -
    # ------------------------------------------------------------------------------------------------------------------
    async def _get(self, url:str, headers:list[tuple[str,str]]):
        try:
            response = await requests.get(url=url, headers=headers, loop=self._loop)
            return json.loads(response.read())
        except urllib.error.URLError as e:
            print(e)
            raise

    async def _post(self,url:str, headers:list[tuple[str,str]],data:dict):

        data_encoded = json.dumps(data).encode("utf_8")

        try:
            response = await requests.post(url=url, headers=headers, data=data_encoded, loop=self._loop)
            if response is None:
                return {}
            return json.loads(response.read())
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
        return await self._get(url=TwitchApiURL.login.value, headers=self._get_header)

    async def get_scopes(self) -> dict:
        return await self._get(url=TwitchApiURL.get_scopes.value,
                               headers=[("Authorization", f"OAuth {self.broadcaster_token}")])

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_custom_reward(self, *, reward_id:str=None, only_manageable_rewards:bool=False) -> dict:
        # assemble base url
        #   the TwitchAPI.connect() has to be run before this method can be used as it relies on TwitchAPI.user.id
        url = f"{TwitchApiURL.get_custom_rewards.value}?broadcaster_id={self.user.id}"

        # assemble arguments
        if reward_id is not None:
            url += f"&id={reward_id}"
        if only_manageable_rewards:
            url += f"&only_manageable_rewards=true"

        return await self._get(url=url, headers=self._get_header)

    @has_scope(scope=TwitchApiScopes.ChannelEditCommercial)
    @connected_to_twitch
    async def start_commercial(self, *, length:int):
        return await self._post(
            url=TwitchApiURL.start_commercial.value,
            headers=self._post_header_json,
            data={
                "broadcaster_id": self.user.id,
                "length": length
            }
        )

