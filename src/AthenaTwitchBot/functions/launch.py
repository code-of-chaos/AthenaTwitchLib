# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
from typing import Callable

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot import TwitchBot
from AthenaTwitchBot.models.twitch_bot_protocol import TwitchBotProtocol

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def launch(
        bot:TwitchBot=None,
        protocol_factory:Callable=None,
        *,
        host:str='irc.chat.twitch.tv',
        port:int=6667 #todo make this into the ssl port
):
    # a bot always has to be defined
    if bot is None or not isinstance(bot, TwitchBot):
        raise SyntaxError("a proper bot has not been defined")

    loop = asyncio.get_event_loop()

    # assemble the protocol if a custom hasn't been defined
    if protocol_factory is None:
        protocol_factory = lambda: TwitchBotProtocol(
            bot=bot,
            main_loop=loop,
        )

    loop.run_until_complete(
        loop.create_connection(
            protocol_factory=protocol_factory,
            host=host,
            port=port,
        )
    )
    loop.run_forever()
    loop.close()

