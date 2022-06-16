# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library
from AthenaColor import HEX

# Custom Packages
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

from AthenaTwitchBot.data.general import EMPTY_STR, ZERO

# ----------------------------------------------------------------------------------------------------------------------
# - Support code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, eq=True, match_args=True)
class TwitchMessageTags:
    # optional info if tags is enabled
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
    tmi_sent_ts: int = ZERO
    turbo: bool = False
    user_id: int = ZERO
    emotes: str = EMPTY_STR
    flags: str = EMPTY_STR
    user_type: str = EMPTY_STR
    emote_only: bool = False
    reply_parent_display_name: str = EMPTY_STR
    reply_parent_msg_body: str = EMPTY_STR
    reply_parent_msg_id: int = ZERO
    reply_parent_user_id: int = ZERO
    reply_parent_user_login: str = EMPTY_STR

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, eq=True, match_args=True)
class TwitchMessage:
    message:list=field(default_factory=list)
    message_type:str=EMPTY_STR
    channel:TwitchChannel=field(default_factory=lambda: TwitchChannel(EMPTY_STR))
    text:str=EMPTY_STR
    user:str=EMPTY_STR
    username:str=field(init=False) # decoupled after init

    tags_enabled:bool=False
    tags:TwitchMessageTags=field(default_factory=TwitchMessageTags)

    def __post_init__(self):
        self.username = self.user.split("!")[0][1:]

# ----------------------------------------------------------------------------------------------------------------------
# - Special message types -
# ----------------------------------------------------------------------------------------------------------------------
class TwitchMessagePing(TwitchMessage):
    pass

class TwitchMessageOnlyForBot(TwitchMessage):
    pass