# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, ClassVar, Any
import enum

# Athena Packages
from AthenaColor import ForeNest as Fore

# Local Imports
from AthenaTwitchBot.bot_logger import get_bot_logger

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class Conversion:
    new_attr_name:str
    callback:Callable

class TAG_TYPES(enum.StrEnum):
    CLEARCHAT = enum.auto()
    CLEARMSG = enum.auto()
    GLOBALUSERSTATE = enum.auto()
    NOTICE = enum.auto()
    PRIVMSG = enum.auto()
    ROOMSTATE = enum.auto()
    USERNOTICE = enum.auto()
    USERSTATE = enum.auto()
    WHISPER = enum.auto()

    UNKNOWN = enum.auto()

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class Tags:
    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.UNKNOWN
    _CONVERSION_MAPPING:ClassVar[dict[str:Conversion]] = {}

    @classmethod
    async def import_from_group_as_str(cls, tags:str) -> Tags:
        bot_logger = get_bot_logger()
        converted_tags:dict[str:Any] = {}

        for tag in tags.split(";"):
            attr_name, value = tag.split("=",1)

            if conversion := cls._CONVERSION_MAPPING.get(attr_name, False):
                converted_tags[conversion.new_attr_name] = conversion.callback(value)

            else:
                print(Fore.Maroon(f"TAG NAME '{attr_name}={value}' NOT FOUND IN {cls.__name__}"))
                await bot_logger.log_unknown_tag(cls._tag_type, attr_name, value)

        # noinspection PyArgumentList
        return cls(**converted_tags)
