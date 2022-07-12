# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

# Custom Library
from AthenaLib.data.text import NOTHING
from AthenaColor import ForeNest, HEX

# Custom Packages
from AthenaTwitchBot.data.message_tag_mapping import MESSAGE_TAG_CONVERSION_MAPPING, MESSAGE_TAG_MAPPING

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

    @classmethod
    def new_from_tags_str(cls, tags_str:str) -> MessageTags:
        attr_value:dict[str:Any] = {}
        for tag_value in tags_str.split(";"):
            tag,value = tag_value.split("=")
            try:
                attr_value[MESSAGE_TAG_MAPPING[tag]] = MESSAGE_TAG_CONVERSION_MAPPING[tag](value=value)
            except KeyError:
                # don't make this crash the bot !
                print(ForeNest.Maroon(f"{tag} not found in mapping"))

        return cls(**attr_value)