# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio
import re
import dataclasses

# Athena Packages

# Local Imports


# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclasses.dataclass(slots=True)
class IrcLineHandler(ABC):
    regex_pattern:re.Pattern|None

    async def __call__(self, transport:asyncio.Transport, matched_content: re.Match|None, original_line: str) -> None:
        await asyncio.gather(
            self._output_on_ingest_console(
                matched_content=matched_content,
                original_line=original_line
            ),
            self._output_on_ingest_logger(
                matched_content=matched_content,
                original_line=original_line
            ),
            self._handle_line(
                transport=transport,
                matched_content=matched_content,
                original_line=original_line
            ),
        )

    @abstractmethod
    async def _output_on_ingest_console(self, matched_content: re.Match|None, original_line: str): ...

    @abstractmethod
    async def _output_on_ingest_logger(self, matched_content: re.Match|None, original_line: str): ...

    @abstractmethod
    async def _handle_line(self, transport:asyncio.Transport, matched_content: re.Match|None, original_line: str): ...