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
    user:TwitchApiUser|None=None

    # non init stuff
    is_connected:bool=field(init=False, default=False)
    _loop:asyncio.AbstractEventLoop = field(init=False)
    _header:dict=field(init=False, default=None)
    _header_json:dict=field(init=False, default=None)

    def __post_init__(self):
        self._loop = asyncio.get_event_loop()
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
    async def _request(self, callback:Callable, url:str, headers:dict,data:dict|None=None,query_parameters:dict|None=None):
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
            self, *, after:str|None=None, ended_at:str|None=None, extension_id:str|None=None, first:int|None=None, started_at:str|None=None,
            type_:str|None=None
    ):
        query = {"after": after, "ended_at": ended_at, "extension_id": extension_id, "first": first,
                 "started_at": started_at, "type": type_}

        # assemble query

        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.analytics_extension.value,
            headers=self._header,
            query_parameters={k:v for k,v in query.items() if v is not None}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.AnalyticsReadGames)
    @connected_to_twitch
    async def get_game_analytics(
            self, *, after:str|None=None, ended_at:str|None=None, game_id:str|None=None, first:int|None=None, started_at:str|None=None,
            type_:str|None=None
    ):
        query = {"after": after, "ended_at": ended_at, "game_id": game_id, "first": first, "started_at": started_at,
                 "type": type_}

        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.analytics_extension.value,
            headers=self._header,
            query_parameters={k:v for k,v in query.items() if v is not None}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.BitsRead)
    @connected_to_twitch
    async def get_bits_leaderboard(
            self, *, count:int = None, period:str = None, started_at:str|None=None, user_id:str|None=None
    ):
        query = {"count": count, "period": period, "started_at": started_at, "user_id": user_id}

        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.bits_leaderboard.value,
            headers=self._header,
            query_parameters={k:v for k,v in query.items() if v is not None}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_cheermotes(self, broadcaster_id:str|None=None):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.cheermotes.value,
            headers=self._header,
            query_parameters={"broadcaster_id": broadcaster_id if broadcaster_id is not None else self.user.id}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_extension_transactions(self, extension_id:str, id_:str|None=None, after:str|None=None, first:int|None=None):
        # assemble query
        query = {"extension_id": extension_id, "id_": id_, "after": after, "first": first}

        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.cheermotes.value,
            headers=self._header,
            query_parameters={k:v for k,v in query.items() if v is not None}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_channel_information(self, broadcaster_id:str|None=None):
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
            self, broadcaster_id:str|None=None, game_id:str|None=None, broadcaster_language:str|None=None, title:str|None=None,
            delay:int|None=None
    ):
        data= {"game_id": game_id, "broadcaster_language": broadcaster_language, "title": title, "delay": delay}

        return await self._request(
            callback=requests.patch,
            url=TwitchApiURL.channel_information.value,
            headers=self._header_json,
            query_parameters={"broadcaster_id": broadcaster_id if broadcaster_id is not None else self.user.id},
            data={k:v for k,v in data.items() if v is not None}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelReadEditors)
    @connected_to_twitch
    async def get_channel_editors(self, broadcaster_id:str|None=None):
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
            self, title:str, cost:int, prompt:str|None=None,is_enabled:bool|None=None,background_color:str|None=None,
            is_user_input_required:bool|None=None, is_max_per_stream_enabled:bool|None=None,max_per_stream:int|None=None,
            is_max_per_user_per_stream_enabled:bool|None=None, max_per_user_per_stream:int|None=None,
            is_global_cooldown_enabled:bool|None=None, global_cooldown_seconds:int|None=None,
            should_redemptions_skip_request_queue:bool|None=None
    ):
        data= {"title": title, "cost": cost, "prompt": prompt, "is_enabled": is_enabled,
               "background_color": background_color, "is_user_input_required": is_user_input_required,
               "is_max_per_stream_enabled": is_max_per_stream_enabled, "max_per_stream": max_per_stream,
               "is_max_per_user_per_stream_enabled": is_max_per_user_per_stream_enabled,
               "max_per_user_per_stream": max_per_user_per_stream,
               "is_global_cooldown_enabled": is_global_cooldown_enabled,
               "global_cooldown_seconds": global_cooldown_seconds,
               "should_redemptions_skip_request_queue": should_redemptions_skip_request_queue}

        return await self._request(
            callback=requests.post,
            url=TwitchApiURL.custom_rewards.value,
            headers=self._header_json,
            query_parameters={"broadcaster_id": self.user.id},
            data={k:v for k,v in data.items() if v is not None}
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
    async def get_custom_reward(self, *, reward_id: str = None, only_manageable_rewards: bool = None) -> dict:
        query = {"broadcaster_id": self.user.id, "reward_id":reward_id,
                 "only_manageable_rewards":only_manageable_rewards}

        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.custom_rewards.value,
            headers=self._header,
            query_parameters={k:v for k,v in query.items() if v is not None}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelReadRedemptions)
    @connected_to_twitch
    async def get_custom_reward_redemption(
            self,reward_id:str,*,id_:str|None=None, status:str|None=None, sort:str|None=None, after:str|None=None, first:int|None=None
    ):
        query = {"broadcaster_id": self.user.id, "reward_id": reward_id, "id": id_, "status": status, "sort": sort,
                 "after": after, "first": first}
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.custom_reward_redemptions.value,
            headers=self._header,
            query_parameters={k:v for k,v in query.items() if v is not None}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelManageRedemptions)
    @connected_to_twitch
    async def update_custom_reward(
            self, id_:str,*,title:str|None=None, cost:int, prompt:str|None=None,is_enabled:bool|None=None,background_color:str|None=None,
            is_user_input_required:bool|None=None, is_max_per_stream_enabled:bool|None=None,max_per_stream:int|None=None,
            is_max_per_user_per_stream_enabled:bool|None=None, max_per_user_per_stream:int|None=None,
            is_global_cooldown_enabled:bool|None=None, global_cooldown_seconds:int|None=None,
            should_redemptions_skip_request_queue:bool|None=None
    ):
        query = {
            "broadcaster_id": self.user.id,
            "id":id_
        }
        data= {
            "title": title,
            "cost": cost,
            "prompt": prompt,
            "is_enabled": is_enabled,
            "background_color": background_color,
            "is_user_input_required": is_user_input_required,
            "is_max_per_stream_enabled": is_max_per_stream_enabled,
            "max_per_stream": max_per_stream,
            "is_max_per_user_per_stream_enabled": is_max_per_user_per_stream_enabled,
            "max_per_user_per_stream": max_per_user_per_stream,
            "is_global_cooldown_enabled": is_global_cooldown_enabled,
            "global_cooldown_seconds": global_cooldown_seconds,
            "should_redemptions_skip_request_queue": should_redemptions_skip_request_queue
        }

        # assemble arguments

        return await self._request(
            callback=requests.patch,
            url=TwitchApiURL.custom_rewards.value,
            headers=self._header_json,
            query_parameters=query,
            data={k:v for k,v in data.items() if v is not None}
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
    async def get_chat_settings(self, *, moderator_id:str|None=None):
        query = {
            "broadcaster_id": self.user.id,
            "moderator_id":moderator_id
        }

        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.chat_settings.value,
            headers=self._header,
            query_parameters={k:v for k,v in query.items() if v is not None}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ModeratorManageChatSettings)
    @connected_to_twitch
    async def update_chat_settings(
            self,*, moderator_id:str|None=None,emote_mode:bool|None=None, follower_mode:bool|None=None,
            follower_mode_duration:int|None=None,non_moderator_chat_delay:bool|None=None,
            non_moderator_chat_delay_duration:int|None=None,slow_mode:bool|None=None, slow_mode_wait_time:int|None=None,
            subscriber_mode:bool|None=None,unique_chat_mode:bool|None=None

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
            query_parameters={k:v for k,v in query.items() if v is not None},
            data={k:v for k,v in data.items() if v is not None}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ClipsEdit)
    @connected_to_twitch
    async def create_clip(self, *, hash_delay:bool|None=None):
        query = {
            "broadcaster_id": self.user.id,
            "hash_delay": hash_delay
        }

        return await self._request(
            callback=requests.post,
            url=TwitchApiURL.clips.value,
            headers=self._header,
            query_parameters={k:v for k,v in query.items() if v is not None}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_clips(self, game_id:str, id_:str):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.clips.value,
            headers=self._header,
            query_parameters={
                "broadcaster_id": self.user.id,
                "game_id": game_id,
                "id_": id_,
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_code_status(self, code:str, user_id:int):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.entitlements_code.value,
            headers=self._header,
            query_parameters={
                "code": code,
                "user_id": user_id,
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_drop_entitlements(
            self, id_:str|None=None, user_id:str|None=None, game_id:str|None=None, fulfillment_status:str|None=None,
            after:str|None = None, first:int|None=None
    ):
        query = {
            "id_":id_,
            "user_id":user_id,
            "game_id":game_id,
            "fulfillment_status":fulfillment_status,
            "after":after,
            "first":first
        }

        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.entitlements_drops.value,
            headers=self._header,
            query_parameters={k:v for k,v in query.items() if v is not None}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def update_drops_entitlements(self, entitlement_ids:list[str]|None=None, fulfillment_status:str|None=None):
        return await self._request(
            callback=requests.patch,
            url=TwitchApiURL.entitlements_drops.value,
            headers=self._header_json,
            data={
                k:v for k,v in
                {"entitlement_ids":entitlement_ids,"fulfillment_status":fulfillment_status }.items()
                if v is not None
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def redeem_code(self, code:str):
        return await self._request(
            callback=requests.patch,
            url=TwitchApiURL.entitlements_code.value,
            headers=self._header_json,
            data={"code":code,"user_id":self.user.id}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_extension_configuration_segment(self, extension_id:str,segment:str):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.extension_configurations.value,
            headers=self._header,
            query_parameters={"broadcaster_id":self.user.id,"extension_id":extension_id,"segment":segment}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def set_extension_configuration_segment(
            self, extension_id:str,segment:str,
            *, content:str=None,version:str=None
    ):
        return await self._request(
            callback=requests.put,
            url=TwitchApiURL.extension_configurations.value,
            headers=self._header_json,
            query_parameters={"extension_id":extension_id,"segment":segment},
            data={
                k:v for k,v in
                {"broadcaster_id":self.user.id,"content":content,"version":version}.items()
                if v is not None
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def set_extension_required_configuration(
            self, extension_id:str,required_configuration:str,extension_version:str
    ):
        return await self._request(
            callback=requests.put,
            url=TwitchApiURL.extension_configurations.value,
            headers=self._header_json,
            query_parameters={"broadcaster_id": self.user.id},
            data={
                "broadcaster_id":self.user.id,
                "required_configuration":required_configuration,
                "extension_version":extension_version,
                "extension_id":extension_id
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def send_extension_pubsub_message(
            self, target:list,is_global_broadcast:bool,message:str
    ):
        return await self._request(
            callback=requests.post,
            url=TwitchApiURL.extension_pubsub.value,
            headers=self._header_json,
            data={
                "broadcaster_id":self.user.id,
                "is_global_broadcast":is_global_broadcast,
                "message":message,
                "target":target
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_extension_live_channels(
            self, extension_id:str,*,first:int=None,after:str
    ):
        return await self._request(
            callback=requests.post,
            url=TwitchApiURL.extension_live.value,
            headers=self._header,
            query_parameters={
                k:v
                for k, v in {
                    "extension_id": extension_id,
                    "first":first,
                    "after":after
                }.items()
                if v is not None
            },
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_extension_secrets(self):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.extension_configurations.value,
            headers=self._header,
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def create_extension_secret(
            self, extension_id:str,*,delay:int=None
    ):
        return await self._request(
            callback=requests.post,
            url=TwitchApiURL.extension_jwt_secrets.value,
            headers=self._header,
            query_parameters={
                k:v
                for k, v in {
                    "extension_id": extension_id,
                    "delay":delay
                }.items()
                if v is not None
            },
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def send_extension_chat_message(
            self, text:str,extension_id:str,extension_version:str
    ):
        return await self._request(
            callback=requests.post,
            url=TwitchApiURL.extension_chat.value,
            headers=self._header_json,
            query_parameters={
                "broadcaster_id":self.user.id
            },
            data={
                "text":text,
                "extension_id":extension_id,
                "extension_version":extension_version
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_extensions(
            self, extension_id:str,*,extension_version:str=None
    ):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.extension.value,
            headers=self._header,
            query_parameters={
                k:v
                for k, v in
                {"extension_id": extension_id,
                 "extension_version": extension_version}.items()
                if v is not None
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_released_extensions(
            self, extension_id:str,*,extension_version:str=None
    ):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.extension_released.value,
            headers=self._header,
            query_parameters={
                k:v
                for k, v in
                {"extension_id": extension_id,
                 "extension_version": extension_version}.items()
                if v is not None
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_extension_bits_products(
            self, *,should_include_all:bool=None
    ):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.extension.value,
            headers=self._header,
            query_parameters={
                k:v
                for k, v in
                {"should_include_all": should_include_all}.items()
                if v is not None
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def update_extension_bits_product(
            self, sku:str,cost_amount:int, cost_type:str,display_name:str,
            *,in_development:bool=None,expiration:str=None,is_broadcast:bool=None
    ):
        return await self._request(
            callback=requests.put,
            url=TwitchApiURL.extension_chat.value,
            headers=self._header_json,
            data={
                k:v
                for k,v in
                {
                    "sku": sku,
                    "cost": {
                        "amount": cost_amount,
                        "type": cost_type
                    },
                    "display_name": display_name,
                    "in_development":in_development,
                    "expiration":expiration,
                    "is_broadcast":is_broadcast
                 }.items()
                if v is not None
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def create_eventsub_subscription(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def delete_eventsub_subscription(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_eventsub_subscriptions(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_top_games(self,*,after:str|None=None, before:str|None=None, first:str|None=None):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.games_top.value,
            headers=self._header,
            query_parameters={
                k:v for k,v in
                {"after":after,"before":before,"first":first}.items()
                if v is not None
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_games(self, id_:str, name:str):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.games.value,
            headers=self._header,
            query_parameters={"id":id_,"name":name}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_creator_goals(self, broadcaster_id:str|None=None):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.goals.value,
            headers=self._header,
            query_parameters={"broadcaster_id":broadcaster_id if broadcaster_id is not None else self.user.id}
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ChannelReadHypeTrain)
    @connected_to_twitch
    async def get_hype_train_events(self, first:int|None=None, cursor:str|None=None):
        return await self._request(
            callback=requests.get,
            url=TwitchApiURL.hypetrain.value,
            headers=self._header,
            query_parameters={
                k:v for k,v in
                {"broadcaster_id": self.user.id, "first": first, "cursor": cursor}.items()
                if v is not None
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @user_has_scope(scope=TwitchApiScopes.ModerationRead)
    @connected_to_twitch
    async def check_automod_status(self,msg_id:str, msg_text:str):
        return await self._request(
            callback=requests.post,
            url=TwitchApiURL.enforcements_status.value,
            headers=self._header_json,
            query_parameters={
                k:v for k,v in
                {"broadcaster_id": self.user.id, "msg_id": msg_id, "msg_text": msg_text}.items()
                if v is not None
            }
        )

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def manage_held_automod_messages(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_automod_settings(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def update_automod_settings(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_banned_users(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def ban_user(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def unban_user(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_blocked_terms(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def add_blocked_term(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def remove_blocked_term(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_moderators(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_polls(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def create_poll(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def end_poll(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_predictions(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def create_prediction(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def end_prediction(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def start_a_raid(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def cancel_a_raid(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_channel_stream_schedule(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_channel_icalendar(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def update_channel_stream_schedule(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def create_channel_stream_schedule_segment(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def update_channel_stream_schedule_segment(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def delete_channel_stream_schedule_segment(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def search_categories(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def search_channels(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_soundtrack_current_track(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_soundtrack_playlist(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_soundtrack_playlists(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_stream_key(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_streams(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_followed_streams(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def create_stream_marker(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_stream_markers(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_broadcaster_subscriptions(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def check_user_subscription(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_all_stream_tags(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_stream_tags(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def replace_stream_tags(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_channel_teams(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_teams(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_users(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def update_user(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_users_follows(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_user_block_list(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def block_user(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def unblock_user(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_user_extensions(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_user_active_extensions(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def update_user_extensions(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def get_videos(self):
        return NotImplemented

    # ------------------------------------------------------------------------------------------------------------------
    @connected_to_twitch
    async def delete_videos(self):
        return NotImplemented





