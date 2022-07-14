# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.data.output_types import OutputTypes
from AthenaTwitchBot.models.twitch_bot.outputs.output import Output
from AthenaTwitchBot.models.twitch_bot.outputs.output_twitch import OutputTwitch
from AthenaTwitchBot.models.twitch_bot.outputs.output_console import OutputConsole

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class LogicOutput:
    mapping:dict[OutputTypes:Output]
    __slots__ = ("mapping",)

    def __init__(self):
        self.mapping = {
            self.types.twitch:OutputTwitch(),
            self.types.console:OutputConsole()
        }

    @property
    def types(self) -> type[OutputTypes]:
        return OutputTypes

    def __getitem__(self, item:OutputTypes):
        return self.mapping[item]

    def register_mapping(self, item:OutputTypes, output:Output):
        if item in self.mapping:
            raise ValueError(f"No same item ({item.value}) can be used in the output system")
        # noinspection PyTypeChecker
        self.mapping[item] = output

