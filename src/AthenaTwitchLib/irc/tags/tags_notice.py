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
class TagsNOTICE(Tags):
    """
    Class for Twitch IRC Tags, that are from the NOTICE message
    """
    msg_id:str | None=None
    target_user_id:str|None=None

    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.NOTICE
    _CONVERSION_MAPPING:ClassVar[Mapping[str, Conversion]] = {
        "msg-id": Conversion("room_id",int),
        "target-user-id": Conversion("target_user_id",str)
    }
