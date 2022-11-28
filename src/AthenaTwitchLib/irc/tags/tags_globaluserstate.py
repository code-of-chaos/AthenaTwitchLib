# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar
from typing import Literal

from AthenaTwitchLib.irc.tags._tags import Conversion
from AthenaTwitchLib.irc.tags._tags import TAG_TYPES
from AthenaTwitchLib.irc.tags._tags import Tags
# Athena Packages
# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class TagsGLOBALUSERSTATE(Tags):
    """
    Class for Twitch IRC Tags, that are from the GLOBALUSERSTATE message
    """
    badge_info:str|None=None
    badges:str|None=None
    color:str|None=None
    display_name:str|None=None
    emote_set:str|None=None
    turbo:bool=False
    user_id:str|None=None
    user_type:Literal["", "admin", "global_mod", "staff"] | None=None

    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.GLOBALUSERSTATE
    _CONVERSION_MAPPING:ClassVar[Mapping[str, Conversion]] = {
        "badge-info": Conversion("badge_info",str),
        "badges": Conversion("badges",lambda obj: obj.split(",")),
        "bits": Conversion("bits",str),
        "color": Conversion("color",str),
        "display-name": Conversion("display_name",str),
        "emote-set": Conversion("emote_set",str),
        "turbo": Conversion("turbo",lambda obj: bool(int(obj))),
        "user-id": Conversion("user_id",str),
        "user-type": Conversion("user_type",str)
    }
