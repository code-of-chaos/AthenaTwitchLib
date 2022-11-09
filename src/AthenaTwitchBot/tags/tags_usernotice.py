# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, ClassVar

# Athena Packages

# Local Imports
from AthenaTwitchBot.tags._tags import Conversion, Tags, TAG_TYPES

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class TagsUSERNOTICE(Tags):
    badge_info:str=None
    badges:str=None
    color:str=None
    display_name:str=None
    emotes:str=None
    id:str=None
    login:str=None
    mod:bool=None
    msg_id:str=None
    room_id:str=None
    system_msg:str=None
    turbo:bool=None
    user_id:str=None
    user_type:Literal["", "admin", "global_mod", "staff"]=None

    msg_param_cumulative_months:str=None
    msg_param_displayName:str=None
    msg_param_login:str=None
    msg_param_months:str=None
    msg_param_promo_gift_total:str=None
    msg_param_promo_name:str=None
    msg_param_recipient_display_name:str=None
    msg_param_recipient_id:str=None
    msg_param_recipient_user_name:str=None
    msg_param_sender_login:str=None
    msg_param_sender_name:str=None
    msg_param_should_share_streak:str=None
    msg_param_streak_months:str=None
    msg_param_sub_plan:str=None
    msg_param_sub_plan_name:str=None
    msg_param_viewerCount:str=None
    msg_param_ritual_name:str=None
    msg_param_threshold:str=None
    msg_param_gift_months:str=None


    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.USERNOTICE
    _CONVERSION_MAPPING:ClassVar[dict] = {
        "badge-info": Conversion("badge_info",str),
        "badges": Conversion("badges",lambda obj: obj.split(",")),
        "bits": Conversion("bits",str),
        "color": Conversion("color",str),
        "display-name": Conversion("display_name",str),
        "emotes": Conversion("emotes",str),
        "id": Conversion("id",str),
        "login": Conversion("login",str),
        "mod": Conversion("mod",bool),
        "msg-id": Conversion("msg_id",str),
        "room-id": Conversion("room_id",str),
        "system-msg": Conversion("system_msg",str),
        "turbo": Conversion("turbo",bool),
        "user-id": Conversion("user_id",str),
        "user-type": Conversion("user_type",str),

        "msg-param-cumulative-months":Conversion("msg_param_cumulative_months",str),
        "msg-param-displayName":Conversion("msg_param_displayName",str),
        "msg-param-login":Conversion("msg_param_login",str),
        "msg-param-months":Conversion("msg_param_months",str),
        "msg-param-promo-gift-total":Conversion("msg_param_promo_gift_total",str),
        "msg-param-promo-name":Conversion("msg_param_promo_name",str),
        "msg-param-recipient-display-name":Conversion("msg_param_recipient_display_name",str),
        "msg-param-recipient-id":Conversion("msg_param_recipient_id",str),
        "msg-param-recipient-user-name":Conversion("msg_param_recipient_user_name",str),
        "msg-param-sender-login":Conversion("msg_param_sender_login",str),
        "msg-param-sender-name":Conversion("msg_param_sender_name",str),
        "msg-param-should-share-streak":Conversion("msg_param_should_share_streak",str),
        "msg-param-streak-months":Conversion("msg_param_streak_months",str),
        "msg-param-sub-plan":Conversion("msg_param_sub_plan",str),
        "msg-param-sub-plan-name":Conversion("msg_param_sub_plan_name",str),
        "msg-param-viewerCount":Conversion("msg_param_viewerCount",str),
        "msg-param-ritual-name":Conversion("msg_param_ritual_name",str),
        "msg-param-threshold":Conversion("msg_param_threshold",str),
        "msg-param-gift-months":Conversion("msg_param_gift_months",str),
    }