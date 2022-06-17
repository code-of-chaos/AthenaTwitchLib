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
MESSAGE_TAG_MAPPING:dict[str:Callable] = {
    "@badge-info":                  "badge_info",
    "badges":                       "badges",
    "client-nonce":                 "client_nonce",
    "color":                        "color",
    "display-name":                 "display_name",
    "emotes":                       "emotes",
    "first-msg":                    "first_msg",
    "flags":                        "flags",
    "id":                           "message_id",
    "mod":                          "mod",
    "room-id":                      "room_id",
    "subscriber":                   "subscriber",
    "tmi-sent-ts":                  "tmi_sent_ts",
    "turbo":                        "turbo",
    "user-id":                      "user_id",
    "user-type":                    "user_type",
    "reply-parent-display-name":    "reply_parent_display_name",
    "reply-parent-msg-body":        "reply_parent_msg_body",
    "reply-parent-msg-id":          "reply_parent_msg_id",
    "reply-parent-user-id":         "reply_parent_user_id",
    "reply-parent-user-login":      "reply_parent_user_login",
    "emote-only":                   "emote_only",
    "returning-chatter":            "returning_chatter"
}

MESSAGE_TAG_CONVERSION_MAPPING:dict[str:Callable] = {
    "@badge-info":              lambda value: value,
    "badges":                   lambda value: value,
    "client-nonce":             lambda value: value,
    "color":                    lambda value: HEX(value) if value else HEX(),
    "display-name":             lambda value: value,
    "emotes":                   lambda value: value,
    "first-msg":                lambda value: bool(int(value)),
    "flags":                    lambda value: value,
    "id":                       lambda value: value,
    "mod":                      lambda value: bool(int(value)),
    "room-id":                  lambda value: value,
    "subscriber":               lambda value: bool(int(value)),
    "tmi-sent-ts":              lambda value: int(value),
    "turbo":                    lambda value: bool(int(value)),
    "user-id":                  lambda value: int(value),
    "user-type":                lambda value: value,
    "reply-parent-display-name":lambda value: value,
    "reply-parent-msg-body":    lambda value: value,
    "reply-parent-msg-id":      lambda value: int(value),
    "reply-parent-user-id":     lambda value: int(value),
    "reply-parent-user-login":  lambda value: value,
    "emote-only":               lambda value: bool(int(value)),
    "returning-chatter":        lambda value: bool(int(value)),
}