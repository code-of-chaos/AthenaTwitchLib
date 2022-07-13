# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import json
import urllib.request
import urllib.error
import asyncio
from dataclasses import dataclass, field
from typing import ClassVar

# Custom Library

# Custom Packages
import AthenaTwitchBot.data.twitch_api_urls as UrlLib

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True,kw_only=True)
class TwitchAPI:
    broadcaster_token:str
    broadcaster_client_id:str

    # non init stuff
    loop:asyncio.AbstractEventLoop = field(init=False)

    def __post_init__(self):
        self.loop = asyncio.get_running_loop()

    # ------------------------------------------------------------------------------------------------------------------
    # - Methods that do all the magic -
    # ------------------------------------------------------------------------------------------------------------------
    async def _get_response(self, req:urllib.request.Request):
        try:
            response = await self.loop.run_in_executor(
                executor=None,
                func=lambda : urllib.request.urlopen(req)
            )
            return json.loads(response.read())
        except urllib.error.URLError as e:
            print(e)

    async def connect(self) -> dict:
        req = urllib.request.Request(UrlLib.LOGIN)
        req.add_header("Authorization",f"Bearer {self.broadcaster_token}")
        req.add_header("Client-Id",self.broadcaster_client_id)

        return await self._get_response(req)
            raise