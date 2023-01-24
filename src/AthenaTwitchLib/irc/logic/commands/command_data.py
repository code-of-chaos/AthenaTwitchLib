# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field, asdict
import json
from typing import Self

# Athena Packages

# Local Imports
from AthenaTwitchLib.logger import SectionIRC, IrcLogger

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class CommandData:
    """
    Simple dataclass to hold basic information about the hard coded command.
    Meant for the `CommandLogic` class to differentiate what to do when it receives a command from chat
    ===

    - cmd_names:             All possible command Names
    - allow_user:            Boolean option to allow all users to use this command
    - allow_sub:             Boolean option to allow subscribers to use this command
    - allow_vip:             Boolean option to allow VIP's to use this command
    - allow_mod:             Boolean option to allow moderators to use this command
    - allow_broadcaster:     Boolean option to allow broadcasters to use this command

    """
    cmd_names:list[str]|str
    allow_user:bool=field(kw_only=True, default=True)
    allow_sub:bool=field(kw_only=True, default=False)
    allow_vip:bool=field(kw_only=True, default=False)
    allow_mod:bool=field(kw_only=True, default=False)
    allow_broadcaster:bool=field(kw_only=True, default=False)

    def __post_init__(self):
        if isinstance(self.cmd_names, str):
            self.cmd_names = [self.cmd_names]
        elif not isinstance(self.cmd_names, list):
            raise ValueError

        # Log to db
        IrcLogger.log_debug(section=SectionIRC.CMD_DATA, data=json.dumps(asdict(self)))

    # ------------------------------------------------------------------------------------------------------------------
    # - Constructors for Role only commands -
    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def for_subscriber(cls, cmd_names:list[str]|str) -> Self:
        return cls(
            cmd_names=cmd_names,
            allow_user = False,
            allow_sub = True,
            allow_vip = False,
            allow_mod = True,
            allow_broadcaster = True,
        )

    @classmethod
    def for_vip(cls, cmd_names:list[str]|str) -> Self:
        return cls(
            cmd_names=cmd_names,
            allow_user = False,
            allow_sub = False,
            allow_vip = True,
            allow_mod = True,
            allow_broadcaster = True,
        )

    @classmethod
    def for_moderator(cls, cmd_names:list[str]|str) -> Self:
        return cls(
            cmd_names=cmd_names,
            allow_user = False,
            allow_sub = False,
            allow_vip = False,
            allow_mod = True,
            allow_broadcaster = True,
        )

    @classmethod
    def for_broadcaster(cls, cmd_names:list[str]|str) -> Self:
        return cls(
            cmd_names=cmd_names,
            allow_user = False,
            allow_sub = False,
            allow_vip = False,
            allow_mod = False,
            allow_broadcaster = True,
        )