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
TAG_MAPPING:dict[str:Callable] = {
    "@badge-info":              lambda tmtags, tag_value: setattr(tmtags, "badge_info",                 tag_value),
    "badges":                   lambda tmtags, tag_value: setattr(tmtags, "badges",                     tag_value),
    "client-nonce":             lambda tmtags, tag_value: setattr(tmtags, "client_nonce",               tag_value),
    "color":                    lambda tmtags, tag_value: setattr(tmtags, "color",                      HEX(tag_value) if tag_value else HEX()),
    "display-name":             lambda tmtags, tag_value: setattr(tmtags, "display_name",               tag_value),
    "emotes":                   lambda tmtags, tag_value: setattr(tmtags, "emotes",                     tag_value),
    "first-msg":                lambda tmtags, tag_value: setattr(tmtags, "first_msg",                  bool(int(tag_value))),
    "flags":                    lambda tmtags, tag_value: setattr(tmtags, "flags",                      tag_value),
    "id":                       lambda tmtags, tag_value: setattr(tmtags, "message_id",                 tag_value),
    "mod":                      lambda tmtags, tag_value: setattr(tmtags, "mod",                        bool(int(tag_value))),
    "room-id":                  lambda tmtags, tag_value: setattr(tmtags, "room_id",                    tag_value),
    "subscriber":               lambda tmtags, tag_value: setattr(tmtags, "subscriber",                 bool(int(tag_value))),
    "tmi-sent-ts":              lambda tmtags, tag_value: setattr(tmtags, "tmi_sent_ts",                int(tag_value)),
    "turbo":                    lambda tmtags, tag_value: setattr(tmtags, "turbo",                      bool(int(tag_value))),
    "user-id":                  lambda tmtags, tag_value: setattr(tmtags, "user_id",                    int(tag_value)),
    "user-type":                lambda tmtags, tag_value: setattr(tmtags, "user_type",                  tag_value),
    "reply-parent-display-name":lambda tmtags, tag_value: setattr(tmtags, "reply_parent_display_name",  tag_value),
    "reply-parent-msg-body":    lambda tmtags, tag_value: setattr(tmtags, "reply_parent_msg_body",      tag_value),
    "reply-parent-msg-id":      lambda tmtags, tag_value: setattr(tmtags, "reply_parent_msg_id",        int(tag_value)),
    "reply-parent-user-id":     lambda tmtags, tag_value: setattr(tmtags, "reply_parent_user_id",       int(tag_value)),
    "reply-parent-user-login":  lambda tmtags, tag_value: setattr(tmtags, "reply_parent_user_login",    tag_value),
    "emote-only":               lambda tmtags, tag_value: setattr(tmtags, "emote_only",                 bool(int(tag_value))),
}