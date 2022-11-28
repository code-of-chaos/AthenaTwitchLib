# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

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
class TagsROOMSTATE(Tags):
    """
    Class for Twitch IRC Tags, that are from the ROOMSTATE message
    """
    emote_only:bool=False
    followers_only:bool=False
    r9k:bool=False
    room_id:int|None=None
    slow:int|None=None
    subs_only:bool=False

    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.ROOMSTATE
    _CONVERSION_MAPPING:ClassVar[Mapping[str, Conversion]] = {
        "emote-only": Conversion("emote_only",lambda obj: bool(int(obj))),
        "followers-only": Conversion("followers_only",lambda obj: bool(int(obj))),
        "r9k": Conversion("r9k",lambda obj: bool(int(obj))),
        "room-id": Conversion("room_id",int),
        "slow": Conversion("slow",int),
        "subs-only": Conversion("subs_only",lambda obj: bool(int(obj))),
    }
