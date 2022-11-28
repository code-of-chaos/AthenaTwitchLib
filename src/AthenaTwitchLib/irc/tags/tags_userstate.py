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
class TagsUSERSTATE(Tags):
    """
    Class for Twitch IRC Tags, that are from the USERSTATE message
    """
    badge_info:str|None=None
    badges:str|None=None
    color:str|None=None
    display_name:str|None=None
    emote_sets: str|None = None
    id:str|None=None
    mod:bool=False
    subscriber:bool=False
    turbo:bool=False
    user_type:Literal["", "admin", "global_mod", "staff"] | None=None

    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.USERSTATE
    _CONVERSION_MAPPING:ClassVar[Mapping[str, Conversion]] = {
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
