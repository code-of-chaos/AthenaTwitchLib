# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
import datetime
from typing import Literal

# Athena Packages

# Local Imports
from AthenaTwitchBot.tags._tags import Conversion, Tags, TAG_TYPES

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class TagsPRIVMSG(Tags):
    badge_info:str=None
    badges:str=None
    bits:int=None
    color:str=None
    display_name:str=None
    emotes:str=None
    emote_only:bool=None
    first_msg:bool=None,
    flags:str=None
    id:str=None
    mod:bool=None
    returning_chatter:bool=None
    reply_parent_msg_id:str=None
    reply_parent_user_id:str=None
    reply_parent_user_login:str=None
    reply_parent_display_name:str=None
    reply_parent_msg_body:str=None
    room_id:str=None
    subscriber:bool=None
    tmi_sent_ts: datetime.datetime=None
    turbo:bool=None
    user_id:str=None
    user_type:Literal["", "admin", "global_mod", "staff"]=None
    vip:bool=None


    _tag_type:TAG_TYPES = TAG_TYPES.PRIVMSG
    _CONVERSION_MAPPING = {
        "badge-info": Conversion("badge_info", str),
        "badges": Conversion( "badges", lambda obj: obj.split(",")),
        "bits": Conversion( "bits", str),
        "color": Conversion( "color", str),
        "display-name": Conversion( "display_name", str),
        "emotes": Conversion( "emotes", str),
        "emote-only": Conversion( "emote_only", bool),
        "first-msg": Conversion( "first_msg", bool),
        "flags": Conversion( "flags", str),
        "id": Conversion( "id", str),
        "mod": Conversion( "mod", bool),
        "returning-chatter": Conversion( "returning_chatter", bool),
        "reply-parent-msg-id": Conversion( "reply_parent_msg_id", str),
        "reply-parent-user-id": Conversion( "reply_parent_user_id", str),
        "reply-parent-user-login": Conversion( "reply_parent_user_login", str),
        "reply-parent-display-name": Conversion( "reply_parent_display_name", str),
        "reply-parent-msg-body": Conversion( "reply_parent_msg_body", str),
        "room-id": Conversion( "room_id", str),
        "subscriber": Conversion( "subscriber", bool),
        "tmi-sent-ts": Conversion( "tmi_sent_ts", datetime.datetime.fromtimestamp),
        "turbo": Conversion( "turbo", bool),
        "user-id": Conversion( "user_id", str),
        "user-type": Conversion( "user_type", str),
        "vip": Conversion( "vip", bool),
    }