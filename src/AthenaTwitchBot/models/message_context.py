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
    raw_input_decoded:str=None
    _output:list[str]=None

    def __post_init__(self):
        if self.raw_input is not None:
            self.raw_input_decoded = self.raw_input.decode("utf_8")

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

