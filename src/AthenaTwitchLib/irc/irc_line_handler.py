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


# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclasses.dataclass(slots=True)
class IrcLineHandler(ABC):
    regex_pattern:re.Pattern|None
    _console_color:Callable
    _console_section:str

    @abstractmethod
    async def _output_logger(self, *args,**kwargs): ...

    async def _output_console(self, txt:str):
        print(f"{self._console_color(self._console_section)} | {txt}")

    async def handle_line(
        self,
        conn_event:asyncio.Future,
        transport:asyncio.Transport,
        matched_content: re.Match|None,
        original_line: str
    ):
        await asyncio.gather(
            self._output_console(txt=original_line),
            self._output_logger(conn_event,transport,matched_content,original_line)
        )

