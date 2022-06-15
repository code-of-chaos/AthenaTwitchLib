# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime

# Custom Library
from AthenaColor import HEX

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, eq=True, match_args=True)
class TwitchMessage:
    message:str="" # complete message without the sufix: "\r\n"
    message_type:str=""
    channel:str=""
    text:str=""

    # optional info if tags is enabled
    badge_info:str=""
    badges:list[str]=field(default_factory=list)
    client_nonce:str=""
    color:HEX=field(default_factory=HEX)
    display_name:str=""
    first_msg:bool=False
    message_id:str=""
    mod:bool=False
    room_id:str=""
    subscriber:bool=False
    tmi_sent_ts:int=0
    turbo:bool=False
    user_id:int=0
    emotes:str=""
    flags:str=""
    user_type:str=""
# ----------------------------------------------------------------------------------------------------------------------
# - Special message types -
# ----------------------------------------------------------------------------------------------------------------------
class TwitchMessagePing(TwitchMessage):
    pass

class TwitchMessageOnlyForBot(TwitchMessage):
    pass