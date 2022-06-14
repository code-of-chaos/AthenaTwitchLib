# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
import socket
from typing import Callable

# Custom Library
import AthenaLib
import AthenaColor

# Custom Packages
from AthenaTwitchBot.models.twitch_bot_protocol import TwitchBotProtocol

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True,eq=False,order=False,kw_only=True)
class TwitchBot:
    nickname:str
    oauth_token:str
    channel:str
    prefix:str

    commands:dict[str: Callable]=field(default_factory=dict) # made part of init if someone wants to feel the pain of adding commands manually

    # non init slots

    # ------------------------------------------------------------------------------------------------------------------
    # - Code -
    # ------------------------------------------------------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        # don't set self.commands to a new dictionary
        #   as this might have been defined due to the field default factory
        # Loop over own functions to see if any is decorated with the command setup

        # surpressed because of pycharm being an ass
        # noinspection PyTypeChecker
        return type.__new__(cls, *args, **kwargs)

    def launch(self):
        loop = asyncio.get_event_loop()
        coro = loop.create_connection(
            protocol_factory = lambda: TwitchBotProtocol(
                bot_nickname=self.nickname,
                bot_oauth_token=self.oauth_token,
                bot_channel=self.channel,
                main_loop=loop,
                command_prefix=self.prefix
            ),
            host='irc.chat.twitch.tv',
            port=6667,
        )
        loop.run_until_complete(coro)
        loop.run_forever()
        loop.close()



