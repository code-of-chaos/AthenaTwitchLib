# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, asdict
import json

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.data.enums import OutputTypes, CommandTypes
from AthenaTwitchLib.logger import IrcLogger, SectionIRC

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class CommandSqliteData:
    """
    Dataclass to hold the command's parameters.
    The data is gathered from the database.
    """
    id:int
    channel:str
    command_name:str
    command_arg:str|None
    command_type:str|CommandTypes
    allow_user:bool|int
    allow_sub:bool|int
    allow_vip:bool|int
    allow_mod:bool|int
    allow_broadcaster:bool
    output_text:str
    output_type:str|OutputTypes

    def __post_init__(self):
        self.command_type = CommandTypes(self.command_type)
        self.allow_user = bool(self.allow_user)
        self.allow_sub = bool(self.allow_sub)
        self.allow_vip = bool(self.allow_vip)
        self.allow_mod = bool(self.allow_mod)
        self.output_type = OutputTypes(self.output_type)

        # Log to db
        IrcLogger.log_debug(section=SectionIRC.CMD_DATA, data=json.dumps(asdict(self)))