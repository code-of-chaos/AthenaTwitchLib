# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import datetime
from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar

from AthenaTwitchLib.irc.tags._tags import Conversion
from AthenaTwitchLib.irc.tags._tags import TAG_TYPES
from AthenaTwitchLib.irc.tags._tags import Tags
# Athena Packages
# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class TagsCLEARCHAT(Tags):
    """
    Class for Twitch IRC Tags, that are from the CLEARCHAT message
    """
    ban_duration:int|None=None
    room_id:str|None=None
    target_user_id:str|None=None
    tmi_sent_ts: datetime.datetime|None=None

    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.CLEARCHAT
    _CONVERSION_MAPPING:ClassVar[Mapping[str, Conversion]] = {
        "ban-duration": Conversion("ban_duration",int),
        "room-id": Conversion("room_id",int),
        "target-user-id": Conversion("target_user_id",str),
        "tmi-sent-ts": Conversion("tmi_sent_ts",datetime.datetime.fromtimestamp),
    }
