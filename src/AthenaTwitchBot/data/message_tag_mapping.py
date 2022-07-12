# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Callable

# Custom Library
from AthenaColor import HEX

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------

# Dictionary used to map the tags found in the twitch IRC message
#   The key is the string stored in the irc but because it used characters that can't be used as class attributes names,
#       the key has to be mapped to the corresponding attr name and any conversion that needs to be done

MESSAGE_TAG_MAPPING:dict[str:tuple[str,Callable]] = {
    "@badge-info":                  ("badge_info",                  (_return_as_is := lambda value: value),),
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
}