# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, ClassVar
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
    _tag_type:TAG_TYPES = TAG_TYPES.UNKNOWN
    _CONVERSION_MAPPING:ClassVar[dict] = {}

    @classmethod
    def import_from_group(cls, tags:str) -> Tags:
        tags_privmsg:Tags = cls()

        # don't parse the `@` -> [1:]
        for tag in tags[1:].split(";"):
            attr_name, value = tag.split("=",1)

            if not (conversion := cls._CONVERSION_MAPPING.get(attr_name, False)):
                conversion:Conversion
                setattr(tags_privmsg, conversion.new_attr_name, conversion.callback(value))

            else:
                get_bot_logger().log_unknown_tag(attr_name, value)
                print(Fore.Maroon(f"TAG NAME NOT FOUND IN {cls.__name__}"))

        return tags_privmsg
