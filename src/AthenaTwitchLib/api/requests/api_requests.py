# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Athena Packages

# Local Imports
from AthenaTwitchLib.api.data.urls import TwitchApiUrl
from AthenaTwitchLib.api._request_data import RequestData
from AthenaTwitchLib.api.data.enums import DataFromConnection, TokenScope

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
def _filter_none(obj:dict) -> dict:
    """
    Simple function that strips all key-value pairs from the dictionary where the value is None
    """
    return {k: v for k, v in obj.items() if v is not None}

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def start_commercial(length:int) -> RequestData:
    """
    https://dev.twitch.tv/docs/api/reference#start-commercial
    """
    return RequestData.POST(
        url=TwitchApiUrl.CHANNEL_COMMERCIAL,
        data={"length": length},
        data_from_connection=(DataFromConnection.BROADCASTER_ID,),
        scopes={TokenScope.CHANNEL_EDIT_COMMERCIAL}
    )

def get_extension_analytics(extension_id:str=None, type_:str=None, started_at:str=None,ended_at:str=None, first:int=None, after:str=None) -> RequestData:
    """
    https://dev.twitch.tv/docs/api/reference#get-extension-analytics
    """
    return RequestData.GET(
        url=TwitchApiUrl.ANALYTICS_EXTENSIONS,
        params=_filter_none({
            "extension_id":extension_id,
            "type":type_,
            "started_at":started_at,
            "ended_at":ended_at,
            "first":first,
            "after":after
        }),
        scopes={TokenScope.ANALYTICS_READ_EXTENSIONS}
    )

def get_game_analytics(game_id:str=None, type_:str=None, started_at:str=None,ended_at:str=None, first:int=None, after:str=None) -> RequestData:
    """
    https://dev.twitch.tv/docs/api/reference#get-game-analytics
    """
    return RequestData.GET(
        url=TwitchApiUrl.ANALYTICS_GAMES,
        params=_filter_none({
            "game_id":game_id,
            "type":type_,
            "started_at":started_at,
            "ended_at":ended_at,
            "first":first,
            "after":after
        }),
        scopes={TokenScope.ANALYTICS_READ_GAMES}
    )

def get_bits_leaderboard(count:int=None, period:str=None,started_at:str=None,user_id:str=None) -> RequestData:
    """
    https://dev.twitch.tv/docs/api/reference#get-bits-leaderboard
    """
    return RequestData.GET(
        url=TwitchApiUrl.BITS_LEADERBOARD,
        params=_filter_none({
            "count":count,
            "period":period,
            "started_at":started_at,
            "user_id":user_id
        }),
        scopes={TokenScope.BITS_READ}
    )

def get_cheermotes(broadcaster_id:str=None) -> RequestData:
    """
    https://dev.twitch.tv/docs/api/reference#get-cheermotes
    """
    return RequestData.GET(
        url=TwitchApiUrl.BITS_CHEERMOTES,
        params=_filter_none({"broadcaster_id":broadcaster_id})
    )

def get_extension_transactions(extension_id:str,*,id_:str=None, first:int=None, after:str=None) -> RequestData:
    """
    https://dev.twitch.tv/docs/api/reference#get-extension-transactions
    """
    return RequestData.GET(
        url=TwitchApiUrl.EXTENSIONS_TRANSACTIONS,
        params=_filter_none({
            "extension_id":extension_id,
            "id":id_,
            "first":first,
            "after":after
        })
    )

def get_channel_information(broadcaster_id:str=None) -> RequestData:
    """
    https://dev.twitch.tv/docs/api/reference#get-channel-information
    """
    if broadcaster_id is None:
        return RequestData.GET(
            url=TwitchApiUrl.CHANNELS,
            params_from_connection=(DataFromConnection.BROADCASTER_ID,),
        )
    else:
        return RequestData.GET(
            url=TwitchApiUrl.CHANNELS,
            params={"broadcaster_id": broadcaster_id},
        )

def modify_channel_information() -> RequestData:
    raise NotImplementedError

def get_channel_editors() -> RequestData:
    raise NotImplementedError

def create_custom_rewards() -> RequestData:
    raise NotImplementedError

def delete_custom_reward() -> RequestData:
    raise NotImplementedError

def get_custom_reward() -> RequestData:
    raise NotImplementedError

def get_custom_reward_redemption() -> RequestData:
    raise NotImplementedError

def update_custom_reward() -> RequestData:
    raise NotImplementedError

def update_redemption_status() -> RequestData:
    raise NotImplementedError

def get_charity_campaign() -> RequestData:
    raise NotImplementedError

def get_charity_campaign_donations() -> RequestData:
    raise NotImplementedError

def get_chatters(broadcaster_id:str=None, *, first:int=None, after:str=None) -> RequestData:
    """
    https://dev.twitch.tv/docs/api/reference#get-chatters
    """
    # Assemble optional parameters
    params = _filter_none({
        "after":after,
        "first":first
    })

    # Return the completed object
    if broadcaster_id is None:
        return RequestData.GET(
            url=TwitchApiUrl.CHAT_USERS,
            params=params,
            params_from_connection=(DataFromConnection.MODERATOR_ID,DataFromConnection.BROADCASTER_ID),
            scopes={TokenScope.MODERATOR_READ_CHATTERS}
        )
    else:
        return RequestData.GET(
            url=TwitchApiUrl.CHAT_USERS,
            params={"broadcaster_id": broadcaster_id} | params,
            params_from_connection=(DataFromConnection.MODERATOR_ID,),
            scopes={TokenScope.MODERATOR_READ_CHATTERS}
        )

def get_channel_emotes(broadcaster_id:str=None) -> RequestData:
    """
    https://dev.twitch.tv/docs/api/reference#get-channel-emotes
    """
    if broadcaster_id is None:
        return RequestData.GET(
            url=TwitchApiUrl.CHAT_EMOTES,
            params_from_connection=(DataFromConnection.BROADCASTER_ID,)
        )
    else:
        return RequestData.GET(
            url=TwitchApiUrl.CHAT_EMOTES,
            params={"broadcaster_id": broadcaster_id}
        )


def get_global_emotes() -> RequestData:
    """
    https://dev.twitch.tv/docs/api/reference#get-global-emotes
    """
    return RequestData.GET(
        url=TwitchApiUrl.CHAT_EMOTES_GLOBAL
    )

def get_emote_sets() -> RequestData:
    raise NotImplementedError

def get_channel_chat_badges() -> RequestData:
    raise NotImplementedError

def get_global_chat_badges() -> RequestData:
    raise NotImplementedError

def get_chat_settings() -> RequestData:
    raise NotImplementedError

def update_chat_settings() -> RequestData:
    raise NotImplementedError

def send_chat_announcement() -> RequestData:
    raise NotImplementedError

def get_user_chat_color() -> RequestData:
    raise NotImplementedError

def update_user_chat_color() -> RequestData:
    raise NotImplementedError

def create_clip() -> RequestData:
    raise NotImplementedError

def get_clips() -> RequestData:
    raise NotImplementedError

def get_code_status() -> RequestData:
    raise NotImplementedError

def get_drops_entitlements() -> RequestData:
    raise NotImplementedError

def update_drops_entitlements() -> RequestData:
    raise NotImplementedError

def redeem_code() -> RequestData:
    raise NotImplementedError

def get_extension_configuration_segment() -> RequestData:
    raise NotImplementedError

def set_extension_configuration_segment() -> RequestData:
    raise NotImplementedError

def set_extension_required_configuration() -> RequestData:
    raise NotImplementedError

def send_extension_pubsub_message() -> RequestData:
    raise NotImplementedError

def get_extension_live_channels() -> RequestData:
    raise NotImplementedError

def get_extension_secrets() -> RequestData:
    raise NotImplementedError

def create_extension_secret() -> RequestData:
    raise NotImplementedError

def send_extension_chat_message() -> RequestData:
    raise NotImplementedError

def get_extensions() -> RequestData:
    raise NotImplementedError

def get_released_extensions() -> RequestData:
    raise NotImplementedError

def get_extension_bits_products() -> RequestData:
    raise NotImplementedError

def update_extension_bits_product() -> RequestData:
    raise NotImplementedError

def create_eventsub_subscription() -> RequestData:
    raise NotImplementedError

def delete_eventsub_subscription() -> RequestData:
    raise NotImplementedError

def get_eventsub_subscriptions() -> RequestData:
    raise NotImplementedError

def get_top_games() -> RequestData:
    raise NotImplementedError

def get_games() -> RequestData:
    raise NotImplementedError

def get_creator_goals() -> RequestData:
    raise NotImplementedError

def get_hype_train_events() -> RequestData:
    raise NotImplementedError

def check_automod_status() -> RequestData:
    raise NotImplementedError

def manage_held_automod_messages() -> RequestData:
    raise NotImplementedError

def get_automod_settings() -> RequestData:
    raise NotImplementedError

def update_automod_settings() -> RequestData:
    raise NotImplementedError

def get_banned_users() -> RequestData:
    raise NotImplementedError

def ban_user() -> RequestData:
    raise NotImplementedError

def unban_user() -> RequestData:
    raise NotImplementedError

def get_blocked_terms() -> RequestData:
    raise NotImplementedError

def add_blocked_term() -> RequestData:
    raise NotImplementedError

def remove_blocked_term() -> RequestData:
    raise NotImplementedError

def delete_chat_messages() -> RequestData:
    raise NotImplementedError

def get_moderators() -> RequestData:
    raise NotImplementedError

def add_channel_moderator() -> RequestData:
    raise NotImplementedError

def remove_channel_moderator() -> RequestData:
    raise NotImplementedError

def get_vips() -> RequestData:
    raise NotImplementedError

def add_channel_vip() -> RequestData:
    raise NotImplementedError

def remove_channel_vip() -> RequestData:
    raise NotImplementedError

def get_polls() -> RequestData:
    raise NotImplementedError

def create_poll() -> RequestData:
    raise NotImplementedError

def end_poll() -> RequestData:
    raise NotImplementedError

def get_predictions() -> RequestData:
    raise NotImplementedError

def create_prediction() -> RequestData:
    raise NotImplementedError

def end_prediction() -> RequestData:
    raise NotImplementedError

def start_a_raid() -> RequestData:
    raise NotImplementedError

def cancel_a_raid() -> RequestData:
    raise NotImplementedError

def get_channel_stream_schedule() -> RequestData:
    raise NotImplementedError

def get_channel_icalendar() -> RequestData:
    raise NotImplementedError

def update_channel_stream_schedule() -> RequestData:
    raise NotImplementedError

def create_channel_stream_schedule_segment() -> RequestData:
    raise NotImplementedError

def update_channel_stream_schedule_segment() -> RequestData:
    raise NotImplementedError

def delete_channel_stream_schedule_segment() -> RequestData:
    raise NotImplementedError

def search_categories() -> RequestData:
    raise NotImplementedError

def search_channels() -> RequestData:
    raise NotImplementedError

def get_soundtrack_current_track() -> RequestData:
    raise NotImplementedError

def get_soundtrack_playlist() -> RequestData:
    raise NotImplementedError

def get_soundtrack_playlists() -> RequestData:
    raise NotImplementedError

def get_stream_key() -> RequestData:
    raise NotImplementedError

def get_streams() -> RequestData:
    raise NotImplementedError

def get_followed_streams() -> RequestData:
    raise NotImplementedError

def create_stream_marker() -> RequestData:
    raise NotImplementedError

def get_stream_markers() -> RequestData:
    raise NotImplementedError

def get_broadcaster_subscriptions() -> RequestData:
    raise NotImplementedError

def check_user_subscription() -> RequestData:
    raise NotImplementedError

def get_all_stream_tags() -> RequestData:
    raise NotImplementedError

def get_stream_tags() -> RequestData:
    raise NotImplementedError

def replace_stream_tags() -> RequestData:
    raise NotImplementedError

def get_channel_teams() -> RequestData:
    raise NotImplementedError

def get_teams() -> RequestData:
    raise NotImplementedError

def get_users(client_id:str|list[str]=None, username:str|list[str]=None) -> RequestData:
    """
    https://dev.twitch.tv/docs/api/reference#get-users
    """

    if client_id is None and username is None:
        raise ValueError("At least one client id or username has to be given")

    params = {
        "id":client_id,
        "login":username
    }

    return RequestData.GET(url=TwitchApiUrl.USERS,params={k:v for k,v in params.items() if v is not None})


def update_user() -> RequestData:
    raise NotImplementedError

def get_users_follows() -> RequestData:
    raise NotImplementedError

def get_user_block_list() -> RequestData:
    raise NotImplementedError

def block_user() -> RequestData:
    raise NotImplementedError

def unblock_user() -> RequestData:
    raise NotImplementedError

def get_user_extensions() -> RequestData:
    raise NotImplementedError

def get_user_active_extensions() -> RequestData:
    raise NotImplementedError

def update_user_extensions() -> RequestData:
    raise NotImplementedError

def get_videos() -> RequestData:
    raise NotImplementedError

def delete_videos() -> RequestData:
    raise NotImplementedError

def send_whisper() -> RequestData:
    raise NotImplementedError

