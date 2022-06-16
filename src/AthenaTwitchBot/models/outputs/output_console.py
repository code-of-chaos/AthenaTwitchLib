# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaColor import ForeNest

# Custom Packages
from AthenaTwitchBot.models.outputs.output import Output
from AthenaTwitchBot._info._v import VERSION

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class OutputConsole(Output):
    async def connection_made(self,**kwargs):
        print(
            ForeNest.SlateGray(
                f"- AthenaTwitchBot {ForeNest.HotPink('v', VERSION, sep='')} -",
                f"   made by Andreas Sas",
                "",
                f"Connection established to {ForeNest.MediumPurple('Twitch')}",
                sep="\n"
            ),
        )

    async def connection_ping(self,**kwargs):
        print(ForeNest.ForestGreen("PING RECEIVED"))

    async def undefined(self,text:str,**kwargs):
        print(ForeNest.SlateGray(text),)

    async def command(self,context, **kwargs):
        pass