# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio
import re
import dataclasses
from typing import Callable

# Athena Packages

# Local Imports
from AthenaTwitchLib.logger import IrcLogger, IrcSections

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclasses.dataclass(slots=True)
class IrcLineHandler(ABC):
    regex_pattern:re.Pattern|None
    _section:IrcSections

    async def handle_line(
        self,
        conn_event:asyncio.Future,
        transport:asyncio.Transport,
        matched_content: re.Match|None,
        original_line: str
    ):
        IrcLogger.debug(msg=original_line, section=self._section)
