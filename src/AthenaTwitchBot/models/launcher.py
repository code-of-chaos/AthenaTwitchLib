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
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_command import BotCommand
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_mentioned import BotMentioned
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_mentioned_start import BotMentionedStart
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_custom_reward import BotCustomReward
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_first_time_chatter import BotFirstTimeChatter
import AthenaTwitchBot.data.global_vars as gbl


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Launcher:
    _loop:asyncio.AbstractEventLoop
    started_from_all: bool = False

    _api:TwitchAPI=None
    _bot:TwitchBot=None

    # ------------------------------------------------------------------------------------------------------------------
    # - Properties -
    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    @property
    def api(cls) -> TwitchAPI:
        if cls._api is None:
            raise ValueError("The APi connector was never started")
        return cls._api

    @classmethod
    def get_loop(cls):
        cls._loop = asyncio.get_event_loop()

    @classmethod
    def start_API_connector(cls,broadcaster_token:str,broadcaster_client_id:str):
        cls.get_loop()
        cls._api = TwitchAPI(
            broadcaster_token=broadcaster_token,
            broadcaster_client_id=broadcaster_client_id
        )
        # connect to the API
        cls._loop.run_until_complete(cls.api.connect())

        if not cls.started_from_all:
            cls._loop.run_forever()

    @classmethod
    def start_Bot(cls, bot:TwitchBot,*,sll:bool=True,**kwargs):
        cls.get_loop()
        gbl.bot = cls.bot = bot

        gbl.bot_command_enabled = BotCommand.registered is not None
        gbl.bot_mentioned_start_enabled = BotMentionedStart.registered is not None
        gbl.bot_mentioned_enabled = BotMentioned.registered is not None
        gbl.bot_custom_reward_enabled = BotCustomReward.registered is not None
        gbl.bot_first_time_chatter_enabled = BotFirstTimeChatter.registered is not None

        gbl.bot_server = BotServer(ssl_enabled=sll, **kwargs)
        gbl.bot_server.launch()

        if not cls.started_from_all:
            cls._loop.run_forever()


    @classmethod
    def start_all(cls, bot:TwitchBot,broadcaster_token:str, broadcaster_client_id:str, *,sll:bool=True, **kwargs):
        cls.started_from_all = True
        cls.get_loop()
        cls.start_API_connector(
            broadcaster_token=broadcaster_token,
            broadcaster_client_id=broadcaster_client_id
        )
        cls.start_Bot(
            bot=bot,
            sll=sll,
            **kwargs
        )

        # run the loop forever
        cls._loop.run_forever()