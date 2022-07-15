# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from typing import Callable

# Custom Library
from AthenaLib.data.text import NOTHING
from AthenaColor import ForeNest, HEX

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
# Dictionary used to map the tags found in the twitch IRC message
#   The key is the string stored in the irc but because it used characters that can't be used as class attributes names,
#       the key has to be mapped to the corresponding attr name and any conversion that needs to be done

MESSAGE_TAG_MAPPING:dict[str:tuple[str,Callable]] = {
    "badge-info":                   ("badge_info",                  (_return_as_is := lambda value: value),),
    "badges":                       ("badges",                      _return_as_is,),
    "client-nonce":                 ("client_nonce",                _return_as_is,),
    "color":                        ("color",                       lambda value: HEX(value) if value else HEX(),),
    "display-name":                 ("display_name",                _return_as_is,),
    "emotes":                       ("emotes",                      _return_as_is,),
    "first-msg":                    ("first_msg",                   (_return_as_bool:=lambda value: bool(int(value))),),
    "flag":                         ("flag",                        _return_as_is,),
    "flags":                        ("flags",                       _return_as_is,),
    "id":                           ("message_id",                  _return_as_is,),
    "mod":                          ("mod",                         _return_as_bool,),
    "room-id":                      ("room_id",                     _return_as_is,),
    "subscriber":                   ("subscriber",                  _return_as_bool,),
    "tmi-sent-ts":                  ("tmi_sent_ts",                 (_return_as_int := lambda value: int(value)),),
    "turbo":                        ("turbo",                       _return_as_bool,),
    "user-id":                      ("user_id",                     _return_as_int,),
    "user-type":                    ("user_type",                   _return_as_is,),
    "reply-parent-display-name":    ("reply_parent_display_name",   _return_as_is,),
    "reply-parent-msg-body":        ("reply_parent_msg_body",       _return_as_is,),
    "reply-parent-msg-id":          ("reply_parent_msg_id",         _return_as_is,),
    "reply-parent-user-id":         ("reply_parent_user_id",        _return_as_int,),
    "reply-parent-user-login":      ("reply_parent_user_login",     _return_as_is,),
    "emote-only":                   ("emote_only",                  _return_as_bool,),
    "returning-chatter":            ("returning_chatter",           _return_as_bool,),
    "custom-reward-id":             ("custom_reward_id",            _return_as_is),
    "emote-sets":                   ("emote_sets",                  _return_as_is),
    "msg-id":                       ("msg_id",                      _return_as_is),
}

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, eq=False, order=False, match_args=True, repr=True)
class MessageTags:
    badge_info: str = NOTHING
    badges: list[str] = field(default_factory=list)
    client_nonce: str = NOTHING
    color: HEX = field(default_factory=HEX)
    display_name: str = NOTHING
    first_msg: bool = False
    message_id: str = NOTHING
    mod: bool = False
    room_id: str = NOTHING
    subscriber: bool = False
    tmi_sent_ts: int = 0
    turbo: bool = False
    user_id: int = 0
    emotes: str = NOTHING
    flag: str = NOTHING
    flags: str = NOTHING
    user_type: str = NOTHING
    emote_only: bool = False
    reply_parent_display_name: str = NOTHING
    reply_parent_msg_body: str = NOTHING
    reply_parent_msg_id: str = NOTHING
    reply_parent_user_id: int = 0
    reply_parent_user_login: str = NOTHING
    returning_chatter:bool = False
    custom_reward_id:str = NOTHING
    emote_sets:str =NOTHING
    msg_id:str=NOTHING

    @classmethod
    def new_from_tags_str(cls, tags_str:str) -> MessageTags:
        attr_value:dict[str:Any] = {}
        for tag_value in tags_str.split(";"):
            tag,value = tag_value.split("=")
            try:
                attr_name, callback = MESSAGE_TAG_MAPPING[tag.replace("@", "")]
                attr_value[attr_name] = callback(value=value)
            except KeyError:
                # don't make this crash the bot !
                print(ForeNest.Maroon(f"{tag} not found in mapping"))
        return cls(**attr_value)