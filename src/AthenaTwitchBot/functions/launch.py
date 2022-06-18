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
from AthenaTwitchBot.models.outputs.abstract_output import AbstractOutput
from AthenaTwitchBot.models.outputs.output_twitch import OutputTwitch
from AthenaTwitchBot.models.outputs.output_console import OutputConsole

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def launch(
        *, # after this, keywords only
        bot:TwitchBot=None,
        protocol_factory:Callable=None,
        outputs:list[type[AbstractOutput]]=None,
        console_enabled:bool=True,
        irc_connection:bool=True,
        irc_host:str='irc.chat.twitch.tv',
        irc_port:int=6667,
        irc_port_ssl:int=6697,
        ssl:bool=False
):
    if irc_connection:
        if outputs is None:
            outputs=[OutputTwitch]
        # thanks for fikotta for pointing me to use isinstance here
        if not any(issubclass(o, OutputTwitch) for o in outputs):
            # always make sure OutputTwitch callbacks are the first to be made
            outputs.insert(0,OutputTwitch)
        if not any(issubclass(o, OutputConsole) for o in outputs) and console_enabled:
            # placement of the Console does not matter
            outputs.append(OutputConsole)

        # a bot always has to be defined
        if bot is None or not isinstance(bot, TwitchBot):
            raise SyntaxError("a proper bot has not been defined")

        loop = asyncio.get_event_loop()

        # assemble the protocol if a custom hasn't been defined
        if protocol_factory is None:
            protocol_factory = lambda: TwitchBotProtocol(bot=bot,outputs=outputs)

        loop.run_until_complete(
            loop.create_connection(
                protocol_factory=protocol_factory,
                host=irc_host,
                port=irc_port if not ssl else irc_port_ssl,
                ssl=ssl
            )
        )
        loop.run_forever()
        loop.close()

    else:
        # todo do this maybe?
        return NotImplemented(irc_connection)
