# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import tracemalloc
import asyncio
import os

# Athena Packages
from AthenaLib.parsers import AthenaDotEnv
from AthenaTwitchLib.irc.irc_connection import IrcConnection
from AthenaTwitchLib.irc.bot_data import BotData

# Local Imports
from tests._connection import connection

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
async def main():

    AthenaDotEnv(filepath=".secrets/secrets.env", auto_run=True)

    bot_data = BotData(
        name=os.getenv("TWITCH_ACCOUNT"),
        oath_token=os.getenv("TWITCH_ACCESS_TOKEN"),
        join_channel=[os.getenv("TWITCH_ACCOUNT")]
    )

    await IrcConnection(bot_data=bot_data).connect()

if __name__ == '__main__':
    asyncio.run(main())