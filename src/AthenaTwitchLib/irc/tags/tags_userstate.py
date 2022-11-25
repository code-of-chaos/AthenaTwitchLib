# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, ClassVar

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.tags._tags import Conversion, Tags, TAG_TYPES

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class TagsUSERSTATE(Tags):
    """
    Class for Twitch IRC Tags, that are from the USERSTATE message
    """
    badge_info:str=None
    badges:str=None
    color:str=None
    display_name:str=None
    emote_sets: str = None
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
        "emote-sets": Conversion("emote_sets",str),
        "id": Conversion("id",str),
        "mod": Conversion("mod",lambda obj: bool(int(obj))),
        "subscriber":Conversion("subscriber", lambda obj: bool(int(obj))),
        "turbo": Conversion("turbo",lambda obj: bool(int(obj))),
        "user-type": Conversion("user_type",str),
    }