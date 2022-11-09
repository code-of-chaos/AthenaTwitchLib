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
class TagsGLOBALUSERSTATE(Tags):
    badge_info:str=None
    badges:str=None
    color:str=None
    display_name:str=None
    emote_set:str=None
    turbo:bool=None
    user_id:str=None
    user_type:Literal["", "admin", "global_mod", "staff"]=None

    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.GLOBALUSERSTATE
    _CONVERSION_MAPPING:ClassVar[dict] = {
        "badge-info": Conversion("badge_info",str),
        "badges": Conversion("badges",lambda obj: obj.split(",")),
        "bits": Conversion("bits",str),
        "color": Conversion("color",str),
        "display-name": Conversion("display_name",str),
        "emote-set": Conversion("emote_set",str),
        "turbo": Conversion("turbo",bool),
        "user-id": Conversion("user_id",str),
        "user-type": Conversion("user_type",str)
    }