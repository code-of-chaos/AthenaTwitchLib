# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar

# Athena Packages

# Local Imports
from AthenaTwitchBot.irc.tags._tags import Conversion, Tags, TAG_TYPES

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class TagsROOMSTATE(Tags):
    """
    Class for Twitch IRC Tags, that are from the ROOMSTATE message
    """
    emote_only:bool=None
    followers_only:bool=None
    r9k:bool=None
    room_id:int=None
    slow:int=None
    subs_only:bool=None

    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.ROOMSTATE
    _CONVERSION_MAPPING:ClassVar[dict] = {
        "emote-only": Conversion("emote_only",lambda obj: bool(int(obj))),
        "followers-only": Conversion("followers_only",lambda obj: bool(int(obj))),
        "r9k": Conversion("r9k",lambda obj: bool(int(obj))),
        "room-id": Conversion("room_id",int),
        "slow": Conversion("slow",int),
        "subs-only": Conversion("subs_only",lambda obj: bool(int(obj))),
    }