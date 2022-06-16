# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaColor import ForeNest

# Custom Packages
from AthenaTwitchBot.models.outputs.abstract_output import AbstractOutput
from AthenaTwitchBot._info._v import VERSION

from AthenaTwitchBot.data.output_console import PING_RECEIVED

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class OutputConsole(AbstractOutput):
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
        print(ForeNest.ForestGreen(PING_RECEIVED))

    async def undefined(self,text:str,**kwargs):
        print(ForeNest.SlateGray(text),)

    async def write(self, context, **kwargs):
        await self.undefined(text=" ".join(context.raw_irc))
        if context.is_command:
            print(ForeNest.SlateGray(context.user, ":", ForeNest.Gold("!", context.command_str, sep="")),)
            print(ForeNest.SlateGray(context.output_text))

    async def reply(self, context, **kwargs):
        await self.undefined(text=" ".join(context.raw_irc))
        if context.is_command:
            print(ForeNest.SlateGray(context.user, ":", ForeNest.Gold("!", context.command_str, sep="")),)
            print(ForeNest.SlateGray(context.output_text))


    async def scheduled_task(self, context, **kwargs):
        await self.undefined(text=" ".join(context.raw_irc))