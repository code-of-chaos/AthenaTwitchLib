# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import unittest
import os

# Athena Packages
from AthenaTwitchLib.api.api_connection import ApiConnection
from AthenaTwitchLib.api.requests import ConnectionRequests

from AthenaLib.parsers.dot_env import AthenaDotEnv

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TestApiReference(unittest.IsolatedAsyncioTestCase):

    # ------------------------------------------------------------------------------------------------------------------
    # - Support Methods -
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _connection() -> ApiConnection:
        AthenaDotEnv(filepath="../.secrets/secrets.env", auto_run=True)

        return ApiConnection(
            username=os.getenv("TWITCH_BROADCASTER_NAME"),
            oath_token=os.getenv("TWITCH_BROADCASTER_OATH"),
            client_id=os.getenv("TWITCH_BROADCASTER_CLIENT_ID")
        )

    # ------------------------------------------------------------------------------------------------------------------
    # - Tests -
    # ------------------------------------------------------------------------------------------------------------------
    async def test_get_user(self):
        async with self._connection() as api_connection:
            data = await api_connection.get_user_data()
            print(data)

    async def test_validate_token(self):
        async with self._connection() as api_connection:
            data = await api_connection.validate_token()
            print(data)
