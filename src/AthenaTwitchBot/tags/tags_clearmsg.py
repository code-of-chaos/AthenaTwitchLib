# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
import datetime
from typing import ClassVar

# Athena Packages

# Local Imports
from AthenaTwitchBot.tags._tags import Conversion, Tags, TAG_TYPES

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class TagsCLEARMSG(Tags):
    """
    Class for Twitch IRC Tags, that are from the CLEARMSG message
    """
    login:str=None
    room_id:str=None
    target_user_id:str=None
    tmi_sent_ts: datetime.datetime=None

    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.CLEARMSG
    _CONVERSION_MAPPING:ClassVar[dict] = {
        "login": Conversion("login",str),
        "room-id": Conversion("room_id",int),
        "target-user-id": Conversion("target_user_id",str),
        "tmi-sent-ts": Conversion("tmi_sent_ts",datetime.datetime.fromtimestamp),
    }