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
from typing import Callable

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
    async def _request(self, callback:Callable, url:str, headers:dict,data:dict=None,query_parameters:dict=None):
        try:
            response = await (callback(
                url=url,
                headers=headers,
                loop=self._loop,
                data=data,
                query_parameters=query_parameters
            ))
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
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.users.value,
            headers=self._header
        )

    async def get_scopes(self) -> dict:
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.scopes.value,
            headers={"Authorization": f"OAuth {self.broadcaster_token}"}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelEditCommercial)
    @connected_to_twitch
    async def start_commercial(self, *, length:int):
        return await self._request(
            callback=requests.post,
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

        return await self._request(
            callback=requests.get,
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

        return await self._request(
            callback=requests.get,
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


        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.bits_leaderboard.value,
            headers=self._header,
            query_parameters=query
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_cheermotes(self, broadcaster_id:str=None):
        return await self._request(
            callback=requests.get,
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

        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.cheermotes.value,
            headers=self._header,
            query_parameters=query
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_channel_information(self, broadcaster_id:str=None):
        return await self._request(
            callback=requests.get,
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

        return await self._request(
            callback=requests.patch,
            url=TwitchApiURL.channel_information.value,
            headers=self._header_json,
            query_parameters={"broadcaster_id": broadcaster_id if broadcaster_id is not None else self.user.id},
            data=data
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelReadEditors)
    @connected_to_twitch
    async def get_channel_editors(self, broadcaster_id:str=None):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.channel_editors.value,
            headers=self._header,
            query_parameters={"broadcaster_id": broadcaster_id if broadcaster_id is not None else self.user.id},
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelManageRedemptions)
    @connected_to_twitch
    async def create_custom_reward(
            self, title:str, cost:int, prompt:str=None,is_enabled:bool=None,background_color:str=None,
            is_user_input_required:bool=None, is_max_per_stream_enabled:bool=None,max_per_stream:int=None,
            is_max_per_user_per_stream_enabled:bool=None, max_per_user_per_stream:int=None,
            is_global_cooldown_enabled:bool=None, global_cooldown_seconds:int=None,
            should_redemptions_skip_request_queue:bool=None
    ):
        data={"title":title, "cost":cost}
        if prompt is not None:
            data["prompt"] = prompt
        if is_enabled is not None:
            data["is_enabled"] = is_enabled
        if background_color is not None:
            data["background_color"] = background_color
        if is_user_input_required is not None:
            data["is_user_input_required"] = is_user_input_required
        if is_max_per_stream_enabled is not None:
            data["is_max_per_stream_enabled"] = is_max_per_stream_enabled
        if max_per_stream is not None:
            data["max_per_stream"] = max_per_stream
        if is_max_per_user_per_stream_enabled is not None:
            data["is_max_per_user_per_stream_enabled"] = is_max_per_user_per_stream_enabled
        if max_per_user_per_stream is not None:
            data["max_per_user_per_stream"] = max_per_user_per_stream
        if is_global_cooldown_enabled is not None:
            data["is_global_cooldown_enabled"] = is_global_cooldown_enabled
        if global_cooldown_seconds is not None:
            data["global_cooldown_seconds"] = global_cooldown_seconds
        if should_redemptions_skip_request_queue is not None:
            data["should_redemptions_skip_request_queue"] = should_redemptions_skip_request_queue

        return await self._request(
            callback=requests.post,
            url=TwitchApiURL.custom_rewards.value,
            headers=self._header_json,
            query_parameters={"broadcaster_id": self.user.id},
            data=data
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelManageRedemptions)
    @connected_to_twitch
    async def delete_custom_reward(self, id_:str):
        return await self._request(
            callback=requests.delete,
            url=TwitchApiURL.custom_rewards.value,
            headers=self._header_json,
            query_parameters={"broadcaster_id": self.user.id, "id":id_},
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_custom_reward(self, *, reward_id: str = None, only_manageable_rewards: bool = False) -> dict:
        query = {"broadcaster_id": self.user.id}

        # assemble arguments
        if reward_id is not None:
            query["reward_id"] = reward_id
        if only_manageable_rewards is not None:
            query["only_manageable_rewards"] = only_manageable_rewards

        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.custom_rewards.value,
            headers=self._header,
            query_parameters=query
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelReadRedemptions)
    @connected_to_twitch
    async def get_custom_reward_redemption(
            self,reward_id:str,*,id_:str=None, status:str=None, sort:str=None, after:str=None, first:int=None
    ):
        query = {"broadcaster_id": self.user.id, "reward_id":reward_id}

        # assemble arguments
        if id_ is not None:
            query["id"] = id_
        if status is not None:
            query["status"] = status
        if sort is not None:
            query["sort"] = sort
        if after is not None:
            query["after"] = after
        if first is not None:
            query["first"] = first

        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.custom_reward_redemptions.value,
            headers=self._header,
            query_parameters=query
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelManageRedemptions)
    @connected_to_twitch
    async def update_custom_reward(
            self, id_:str,*,title:str=None, cost:int, prompt:str=None,is_enabled:bool=None,background_color:str=None,
            is_user_input_required:bool=None, is_max_per_stream_enabled:bool=None,max_per_stream:int=None,
            is_max_per_user_per_stream_enabled:bool=None, max_per_user_per_stream:int=None,
            is_global_cooldown_enabled:bool=None, global_cooldown_seconds:int=None,
            should_redemptions_skip_request_queue:bool=None
    ):
        query = {"broadcaster_id": self.user.id, "id":id_}
        data={}

        # assemble arguments
        if title is not None:
            data["title"] = title
        if cost is not None:
            data["cost"] = cost
        if prompt is not None:
            data["prompt"] = prompt
        if is_enabled is not None:
            data["is_enabled"] = is_enabled
        if background_color is not None:
            data["background_color"] = background_color
        if is_user_input_required is not None:
            data["is_user_input_required"] = is_user_input_required
        if is_max_per_stream_enabled is not None:
            data["is_max_per_stream_enabled"] = is_max_per_stream_enabled
        if max_per_stream is not None:
            data["max_per_stream"] = max_per_stream
        if is_max_per_user_per_stream_enabled is not None:
            data["is_max_per_user_per_stream_enabled"] = is_max_per_user_per_stream_enabled
        if max_per_user_per_stream is not None:
            data["max_per_user_per_stream"] = max_per_user_per_stream
        if is_global_cooldown_enabled is not None:
            data["is_global_cooldown_enabled"] = is_global_cooldown_enabled
        if global_cooldown_seconds is not None:
            data["global_cooldown_seconds"] = global_cooldown_seconds
        if should_redemptions_skip_request_queue is not None:
            data["should_redemptions_skip_request_queue"] = should_redemptions_skip_request_queue

        return await self._request(
            callback=requests.patch,
            url=TwitchApiURL.custom_rewards.value,
            headers=self._header_json,
            query_parameters=query,
            data=data
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelManageRedemptions)
    @connected_to_twitch
    async def update_custom_reward_redemption(self,id_:str,reward_id:str, status:str):
        return await self._request(
            callback=requests.patch,
            url=TwitchApiURL.custom_reward_redemptions.value,
            headers=self._header_json,
            query_parameters={"id":id_,"reward_id":reward_id,"broadcaster_id": self.user.id},
            data={"status":status}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_channel_emotes(self):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.emotes_chat.value,
            headers=self._header,
            query_parameters={"broadcaster_id": self.user.id},
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_global_emotes(self):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.emotes_global.value,
            headers=self._header,
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_emote_sets(self, emote_set_id:str):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.emotes_set.value,
            headers=self._header,
            query_parameters={"emote_set_id":emote_set_id}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_channel_chat_badges(self):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.badges_chat.value,
            headers=self._header,
            query_parameters={"broadcaster_id": self.user.id}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_global_chat_badges(self):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.badges_global.value,
            headers=self._header
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_chat_settings(self, *, moderator_id:str=None):
        query = {"broadcaster_id": self.user.id}
        if moderator_id is not None:
            query["moderator_id"] = moderator_id

        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.chat_settings.value,
            headers=self._header,
            query_parameters=query
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def update_chat_settings(
            self, moderator_id:str=None,*,emote_mode:bool=None, follower_mode:bool=None,
            follower_mode_duration:int=None,non_moderator_chat_delay:bool=None,
            non_moderator_chat_delay_duration:int=None,slow_mode:bool=None, slow_mode_wait_time:int=None,
            subscriber_mode:bool=None,unique_chat_mode:bool=None

    ):
        query = {
            "broadcaster_id": self.user.id,
            "moderator_id": moderator_id
        }
        data={
            "emote_mode":emote_mode,
            "follower_mode":follower_mode,
            "follower_mode_duration":follower_mode_duration,
            "non_moderator_chat_delay":non_moderator_chat_delay,
            "non_moderator_chat_delay_duration":non_moderator_chat_delay_duration,
            "slow_mode":slow_mode,
            "slow_mode_wait_time":slow_mode_wait_time,
            "subscriber_mode":subscriber_mode,
            "unique_chat_mode":unique_chat_mode
        }

        return await self._request(
            callback=requests.patch,
            url=TwitchApiURL.chat_settings.value,
            headers=self._header,
            query_parameters={k:v for k,v in query if v is not None},
            data={k:v for k,v in data if v is not None}
        )





