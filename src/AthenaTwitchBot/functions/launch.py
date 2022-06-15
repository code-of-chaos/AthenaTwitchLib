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
from AthenaTwitchBot.models.outputs.output import Output
from AthenaTwitchBot.models.outputs.output_console import OutputConsole

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def launch(
        *, # after this, keywords only
        bot:TwitchBot=None,
        protocol_factory:Callable=None,
        output:Output=None,
        host:str='irc.chat.twitch.tv',
        port:int=6667, #todo make this into the ssl port

        auto_restart:bool=False
):

    if output is None:
        output=OutputConsole()
    output.pre_launch()

    while True:
        try:
            # a bot always has to be defined
            if bot is None or not isinstance(bot, TwitchBot):
                raise SyntaxError("a proper bot has not been defined")

            loop = asyncio.get_event_loop()

            # assemble the protocol if a custom hasn't been defined
            if protocol_factory is None:
                protocol_factory = lambda: TwitchBotProtocol(bot=bot,output=output)

            loop.run_until_complete(
                loop.create_connection(
                    protocol_factory=protocol_factory,
                    host=host,
                    port=port,
                )
            )
            loop.run_forever()
            loop.close()
        except ConnectionResetError:
            print("not connection")
            if auto_restart:
                loop = asyncio.get_running_loop()
                loop.stop()
                continue
            else:
                break

        except : # make sure everything else is caught else the loop will continue indefinitely
            raise

