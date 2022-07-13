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
from AthenaTwitchBot.models.twitch_api_user import TwitchApiUser
from AthenaTwitchBot.data.twitch_api_urls import TwitchApiURL

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

    def __post_init__(self):
        self._loop = asyncio.get_running_loop()
        self._get_header = [
            ("Authorization", f"Bearer {self.broadcaster_token}"),
            ("Client-Id", self.broadcaster_client_id)
        ]

    # ------------------------------------------------------------------------------------------------------------------
    # - Methods that do all the magic -
    # ------------------------------------------------------------------------------------------------------------------
    async def _get_response(self, url:str, headers:list[tuple[str,str]]):
        try:
            response = await requests.get(url=url, headers=headers, loop=self._loop)
            return json.loads(response.read())
        except urllib.error.URLError as e:
            print(e)
            raise

    # ------------------------------------------------------------------------------------------------------------------
    # - API methods-
    # ------------------------------------------------------------------------------------------------------------------
    async def connect(self) -> dict:
        # Execute the request
        data: dict = await self._get_response(url=TwitchApiURL.login.value,headers=self._get_header)

        # store the user, as some user data is required in further api commands
        self.user = TwitchApiUser.new_from_dict(data["data"][0])
        self.is_connected = True

        # return the data dictionary back
        return data

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

        return await self._get_response(url=url, headers=self._get_header)