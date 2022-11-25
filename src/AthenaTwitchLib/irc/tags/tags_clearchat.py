# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
import datetime

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.tags._tags import Conversion, Tags, TAG_TYPES

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class TagsCLEARCHAT(Tags):
    """
    Class for Twitch IRC Tags, that are from the CLEARCHAT message
    """
    ban_duration:int=None
    room_id:str=None
    target_user_id:str=None
    tmi_sent_ts: datetime.datetime=None

    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.CLEARCHAT
    _CONVERSION_MAPPING:ClassVar[dict] = {
        "ban-duration": Conversion("ban_duration",int),
        "room-id": Conversion("room_id",int),
        "target-user-id": Conversion("target_user_id",str),
        "tmi-sent-ts": Conversion("tmi_sent_ts",datetime.datetime.fromtimestamp),
    }