# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import contextlib
import os
import pathlib

# Athena Packages
from AthenaLib.parsers import AthenaDotEnv
from AthenaTwitchLib.api.api_connection import ApiConnection
from AthenaTwitchLib.logger import ApiLogger

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@contextlib.asynccontextmanager
async def connection() -> ApiConnection:
    AthenaDotEnv(filepath=".secrets/secrets.env", auto_run=True)
    # ApiLogger.sqlite_path = pathlib.Path(r"D:\directive_athena\applications\neptune\twitch_bot\data\logger.sqlite")
    # with ApiLogger:
    async with ApiConnection(oath_token="xs749y7if7d4dxyui9dmgtkdt00dvt") as api_connection:
    # async with ApiConnection(oath_token=os.getenv("TWITCH_ACCESS_TOKEN")) as api_connection:
        yield api_connection