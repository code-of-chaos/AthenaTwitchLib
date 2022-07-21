# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_api.twitch_api import TwitchAPI
from AthenaTwitchBot.models.twitch_bot.twitch_bot import TwitchBot
from AthenaTwitchBot.models.twitch_bot.bot_server import BotServer
import AthenaTwitchBot.data.global_vars as gbl


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Launcher:
    _loop:asyncio.AbstractEventLoop

    _api:TwitchAPI=None
    _bot:TwitchBot=None

    # ------------------------------------------------------------------------------------------------------------------
    # - Properties -
    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    @property
    def api(cls) -> TwitchAPI:
        if cls._api is None:
            raise ValueError("The API connector was never started")
        return cls._api

    @classmethod
    async def start_API_connector(cls,broadcaster_token:str,broadcaster_client_id:str):
        cls._api = TwitchAPI(
            broadcaster_token=broadcaster_token,
            broadcaster_client_id=broadcaster_client_id
        )
        # connect to the API
        await cls.api.connect()

    @classmethod
    async def start_Bot(cls, bot:TwitchBot,*,sll:bool=True,**kwargs):
        gbl.bot = cls.bot = bot
        gbl.bot_server = BotServer(ssl_enabled=sll, **kwargs)
        await gbl.bot_server.launch()


    @classmethod
    async def start_all(cls, bot:TwitchBot,broadcaster_token:str, broadcaster_client_id:str, *,sll:bool=True, **kwargs):
        await cls.start_API_connector(
            broadcaster_token=broadcaster_token,
            broadcaster_client_id=broadcaster_client_id
        )

        await cls.start_Bot(
            bot=bot,
            sll=sll,
            **kwargs
        )