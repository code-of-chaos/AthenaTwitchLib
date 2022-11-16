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
class TagsNOTICE(Tags):
    """
    Class for Twitch IRC Tags, that are from the NOTICE message
    """
    msg_id:str=None
    target_user_id:str=None

    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.NOTICE
    _CONVERSION_MAPPING:ClassVar[dict] = {
        "msg-id": Conversion("room_id",int),
        "target-user-id": Conversion("target_user_id",str)
    }