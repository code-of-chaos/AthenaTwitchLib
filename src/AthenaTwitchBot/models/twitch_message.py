# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library
from AthenaColor import HEX

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
EMPTY_STR = ""

@dataclass(slots=True, eq=True, match_args=True)
class TwitchMessage:
    message:str=EMPTY_STR # complete message without the suffix: "\r\n"
    message_type:str=EMPTY_STR
    channel:str=EMPTY_STR
    text:str=EMPTY_STR
    user:str=EMPTY_STR
    username:str=field(init=False) # decoupled after init

    # optional info if tags is enabled
    badge_info:str=EMPTY_STR
    badges:list[str]=field(default_factory=list)
    client_nonce:str=EMPTY_STR
    color:HEX=field(default_factory=HEX)
    display_name:str=EMPTY_STR
    first_msg:bool=False
    message_id:str=EMPTY_STR
    mod:bool=False
    room_id:str=EMPTY_STR
    subscriber:bool=False
    tmi_sent_ts:int=0
    turbo:bool=False
    user_id:int=0
    emotes:str=EMPTY_STR
    flags:str=EMPTY_STR
    user_type:str=EMPTY_STR
    emote_only:bool=False

    def __post_init__(self):
        self.username = self.user.split("!")[0][1:]

# ----------------------------------------------------------------------------------------------------------------------
# - Special message types -
# ----------------------------------------------------------------------------------------------------------------------
class TwitchMessagePing(TwitchMessage):
    pass

class TwitchMessageOnlyForBot(TwitchMessage):
    pass