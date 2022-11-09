# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Callable, ClassVar
import functools
from dataclasses import dataclass, field

# Athena Packages

# Local Imports
from AthenaTwitchBot.tags import TagsPRIVMSG

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class CommandSettings:
    name:str
    channels:list[str] = field(default_factory=list)

    # non init
    callback:Callable = field(init=False)

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class BotLogic:
    mapped_commands:ClassVar[dict] = {}

    async def handle(self, tags:TagsPRIVMSG,user,channel:str,text:str):
        cmd_with_prefix, *args = text.split(" ")
        cmd = cmd_with_prefix[1:] # removes the prefix

        print(self.mapped_commands, cmd)

        if cmd in self.mapped_commands and (not (channels := self.mapped_commands[cmd].channels) or channel in channels):
            await self.mapped_commands[cmd].callback(self)

    @classmethod
    def command(cls, settings:CommandSettings):
        def decorator(fnc:Callable):
            settings.callback = fnc
            cls.mapped_commands[settings.name] = settings

            @functools.wraps(fnc)
            async def wrapper(*args, **kwargs):
                return await fnc(*args, **kwargs)
            return wrapper
        return decorator
