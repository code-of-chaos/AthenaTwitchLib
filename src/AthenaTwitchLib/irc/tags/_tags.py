# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, ClassVar, Any
import enum

# Athena Packages
from AthenaColor import ForeNest as Fore
from AthenaLib.logging import AthenaSqliteLogger

# Local Imports
from AthenaTwitchLib.logger import SectionIRC, IrcLogger

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class Conversion:
    """
    Simple dataclass to easily hold the new attr name and type casting callback for Twitch IRC Tags
    """
    new_attr_name:str
    callback:Callable

class TAG_TYPES(enum.StrEnum):
    """
    StrEnum that holds all possible categories of Twitch IRC Tags
    """
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
    """
    Base class for all twitch IRC tag classes
    Holds some basic logic to import a tags group string, and create the correct Tags object from it
    """
    # Has to be a ClassVar,
    #   for the dataclass to know that it is a ClassVar
    _tag_type:ClassVar[TAG_TYPES] = TAG_TYPES.UNKNOWN
    _CONVERSION_MAPPING:ClassVar[dict[str:Conversion]] = {}

    @classmethod
    async def import_from_group_as_str(cls, tags:str) -> Tags:
        """
        Splits up a given tags string (eg: `badge-info=;badges=premium/1;color=#00AAAA`) into its separate tags.
        It will then cast the tags into the correct type, provided by the `cls._CONVERSION_MAPPING`
        """
        converted_tags:dict[str:Any] = {}

        for tag in tags.split(";"):
            attr_name, value = tag.split("=",1)

            if not (conversion := cls._CONVERSION_MAPPING.get(attr_name, False)):
                # If it fails, log and continue to the next one
                print(Fore.Maroon(f"TAG NAME '{attr_name}={value}' NOT FOUND IN {cls.__name__}"))
                IrcLogger.log_warning(section=SectionIRC.MSG_TAGS_UNKNOWN, text=f"{attr_name, value}")
                continue

            # When everything goes as normal
            converted_tags[conversion.new_attr_name] = conversion.callback(value)

        # noinspection PyArgumentList
        return cls(**converted_tags)
