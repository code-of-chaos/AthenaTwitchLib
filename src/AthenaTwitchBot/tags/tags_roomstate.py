# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
import datetime
from typing import Literal

# Athena Packages

# Local Imports
from AthenaTwitchBot.tags._tags import Conversion, Tags, TAG_TYPES

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class TagsROOMSTATE(Tags):
    emote_only:bool=None
    followers_only:bool=None
    r9k:bool=None
    room_id:int=None
    slow:int=None
    subs_only:bool=None

    _tag_type:TAG_TYPES = TAG_TYPES.ROOMSTATE
    _CONVERSION_MAPPING = {
        "emote-only": Conversion("emote_only",bool),
        "followers-only": Conversion("followers_only",bool),
        "r9k": Conversion("r9k",bool),
        "room-id": Conversion("room_id",int),
        "slow": Conversion("slow",int),
        "subs-only": Conversion("subs_only",bool),
    }