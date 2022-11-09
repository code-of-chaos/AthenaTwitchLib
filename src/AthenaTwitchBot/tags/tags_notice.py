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
class TagsNOTICE(Tags):
    msg_id:str=None
    target_user_id:str=None

    _tag_type:TAG_TYPES = TAG_TYPES.NOTICE
    _CONVERSION_MAPPING = {
        "msg-id": Conversion("room_id",int),
        "target-user-id": Conversion("target_user_id",str)
    }