# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.data.output_types import OutputTypes
from AthenaTwitchBot.models.outputs.output import Output
from AthenaTwitchBot.models.outputs.output_twitch import OutputTwitch

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class OutputSystem:
    mapping:dict[OutputTypes:Output]

    def __init__(self):
        self.mapping = {
            OutputTypes.twitch:OutputTwitch()
        }

    def __getitem__(self, item:OutputTypes):
        return self.mapping[item]

    def register_mapping(self, item:OutputTypes, output:Output):
        if item in self.mapping:
            raise ValueError(f"No same item ({item.value}) can be used in the output system")
        # noinspection PyTypeChecker
        self.mapping[item] = output

