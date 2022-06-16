# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaColor import StyleNest, ForeNest, BackNest

# Custom Packages
from AthenaTwitchBot.models.outputs.output import Output
from AthenaTwitchBot.models.twitch_message import TwitchMessage, TwitchMessagePing, TwitchMessageOnlyForBot
# noinspection PyProtectedMember
from AthenaTwitchBot._info._v import VERSION

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class OutputConsole(Output):

    def pre_launch(self):
        print(
            ForeNest.SlateGray(
                f"- AthenaTwitchBot {ForeNest.HotPink('v', VERSION, sep='')} -",
                f"   made by Andreas Sas",
                "",
                sep="\n"
            ),
        )

    def message(self, message:TwitchMessage):
        match message:
            case TwitchMessagePing():
                print(ForeNest.SlateGray(message.text), ForeNest.ForestGreen("PING RECEIVED"))
            case TwitchMessageOnlyForBot():
                print(ForeNest.SlateGray(message.text))
            case TwitchMessage(first_msg=True):
                print(ForeNest.BlueViolet(message.username), ForeNest.SlateGray(":"),ForeNest.White(message.text))
            case TwitchMessage():
                print(ForeNest.SlateGray(message.username, ":"),ForeNest.White(message.text))

    def undefined(self,message=None):
        print(ForeNest.SlateGray(message))
