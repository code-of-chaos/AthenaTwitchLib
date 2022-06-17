# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

# Custom Library
from AthenaColor import HEX, ForeNest

# Custom Packages
from AthenaTwitchBot.data.general import EMPTY_STR
from AthenaTwitchBot.data.dict_mapping_logic import MESSAGE_TAG_MAPPING,MESSAGE_TAG_CONVERSION_MAPPING

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, eq=False, order=False, match_args=True, repr=True)
class TwitchMessageTags:
    badge_info: str = EMPTY_STR
    badges: list[str] = field(default_factory=list)
    client_nonce: str = EMPTY_STR
    color: HEX = field(default_factory=HEX)
    display_name: str = EMPTY_STR
    first_msg: bool = False
    message_id: str = EMPTY_STR
    mod: bool = False
    room_id: str = EMPTY_STR
    subscriber: bool = False
    tmi_sent_ts: int = 0
    turbo: bool = False
    user_id: int = 0
    emotes: str = EMPTY_STR
    flags: str = EMPTY_STR
    user_type: str = EMPTY_STR
    emote_only: bool = False
    reply_parent_display_name: str = EMPTY_STR
    reply_parent_msg_body: str = EMPTY_STR
    reply_parent_msg_id: int = 0
    reply_parent_user_id: int = 0
    reply_parent_user_login: str = EMPTY_STR
    returning_chatter:bool = False

    @classmethod
    def new_from_tags_str(cls, tags_str:str) -> TwitchMessageTags:
        attr_value:dict[str:Any] = {}
        for tag_value in tags_str.split(";"):
            tag,value = tag_value.split("=")
            try:
                attr_value[MESSAGE_TAG_MAPPING[tag]] = MESSAGE_TAG_CONVERSION_MAPPING[tag](value=value)
            except KeyError:
                # don't make this crash the bot !
                print(ForeNest.Maroon(f"{tag} not found in mapping"))

        return cls(**attr_value)



