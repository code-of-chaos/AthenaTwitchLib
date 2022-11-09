# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, ClassVar

# Athena Packages

# Local Imports
from AthenaTwitchBot.tags._tags import Conversion, Tags, TAG_TYPES

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class TagsUSERSTATE(Tags):
    badge_info:str=None
    badges:str=None
    color:str=None
    display_name:str=None
    emote_set: str = None
    id:str=None
    mod:bool=None
    subscriber:bool=None
    turbo:bool=None
    user_type:Literal["", "admin", "global_mod", "staff"]=None

    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.USERSTATE
    _CONVERSION_MAPPING:ClassVar[dict] = {
        "badge-info": Conversion("badge_info",str),
        "badges": Conversion("badges",lambda obj: obj.split(",")),
        "bits": Conversion("bits",str),
        "color": Conversion("color",str),
        "display-name": Conversion("display_name",str),
        "emote-set": Conversion("emote_set",str),
        "id": Conversion("id",str),
        "mod": Conversion("mod",bool),
        "subscriber":Conversion("subscriber", bool),
        "turbo": Conversion("turbo",bool),
        "user-type": Conversion("user_type",str),
    }