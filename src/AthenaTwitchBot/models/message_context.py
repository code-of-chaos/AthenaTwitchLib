# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class MessageContext:
    raw_input:bytearray=None
    _output:list[str]=None

    @property
    def output(self) -> list[str]:
        return self._output

    @output.setter
    def output(self, value:list[str]):
        if isinstance(value, str):
            self._output = [value]
        elif isinstance(value, list):
            self._output = value
        else:
            raise ValueError("text was not defined as a list of string(s)")

