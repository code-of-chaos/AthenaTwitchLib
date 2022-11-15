# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import functools
import socket
import asyncio
import pathlib
from dataclasses import dataclass, field, KW_ONLY
from typing import Callable

# Athena Packages
from AthenaLib.constants.text import NEW_LINE

# Local Imports
from AthenaTwitchBot.string_formatting import twitch_output_format
from AthenaTwitchBot.bot_protocol import BotConnectionProtocol
from AthenaTwitchBot.regex import RegexPatterns
from AthenaTwitchBot.bot_settings import BotSettings
from AthenaTwitchBot.bot_logger import BotLogger
from AthenaTwitchBot.bot_event_types import BotEvent

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class BotConstructor:
    settings: BotSettings
    protocol_cls:type[BotConnectionProtocol]=BotConnectionProtocol

    logging_enabled:bool=False
    restart_attempts:int=5 # if set to -1, will run forever
    current_restart_attempt:int=0

    # Non init
    loop: asyncio.AbstractEventLoop = field(init=False,default_factory=asyncio.get_running_loop)
    bot_event_future: asyncio.Future = field(init=False)

    def __post_init__(self):
        # Define the logger as soon as possible,
        #   As it is called by a lot of different systems
        #   Will create tables if need be
        BotLogger.set_logger(
            path=pathlib.Path("data/logger.sqlite"),
            logging_enabled=self.logging_enabled,
            log_all_messages=True,
        )

        self.loop.create_task(BotLogger.logger.create_tables())

    async def construct(self):
        """
        Constructor function for the Bot and all its logical systems like the asyncio.Protocol handler.
        It also logs the bot in onto the Twitch IRC server
        """
        while self.restart_attempts != 0:

            # Assemble the asyncio.Protocol
            #   The custom protocol_type needs a constructor to known which patterns to use, settings, etc...
            bot_event:asyncio.Future = self.loop.create_future()

            bot_transport, protocol_obj = await self.loop.create_connection( # type: asyncio.BaseTransport, object
                protocol_factory=self._protocol_constructor(bot_event),
                server_hostname=self.settings.irc_host,
                ssl=self.settings.ssl_enabled,
                sock=self._assemble_socket()
            )
            if bot_transport is None:
                raise ConnectionRefusedError

            # Give the protocol the transporter,
            #   so it can easily create write calls to the connection
            # bot_transport: asyncio.Transport
            protocol_obj.transport = bot_transport

            # Log the bot in on the IRC server
            await self._login_bot(bot_transport)

            # Waiting portion of the BotConstructor,
            #   This regulates the bot starting back up and restarting
            match result := await bot_event :
                case BotEvent.RESTART:
                    self.current_restart_attempt +=1
                    print(f"{NEW_LINE*25}{'-'*25}RESTART ATTEMPT {self.current_restart_attempt}{'-'*25}")
                    bot_transport.close()
                    self.restart_attempts -= 1
                    continue # restarts it all

                case BotEvent.EXIT | _:
                    print(result)
                    self.loop.stop()
                    break

    def _assemble_socket(self) -> socket.socket:
        """
        Simple method that creates the required socket for the asyncio.Protocol factory
        """
        sock = socket.socket()
        sock.settimeout(5.)
        sock.connect(
            (
                self.settings.irc_host,
                self.settings.irc_port_ssl if self.settings.ssl_enabled else self.settings.irc_port
            )
        )
        return sock

    def _protocol_constructor(self, bot_event:asyncio.Future) -> Callable:
        """
        Simple construction for the custom asyncio.Protocol class
        Seperated into its own function for better programming common sense
        """
        return functools.partial(
            self.protocol_cls,

            # Creates a new regex pattern
            #   in the event that it's matches must change during a restart
            regex_patterns=RegexPatterns(
                bot_name=self.settings.bot_name,
                bot_prefix=self.settings.bot_prefix
            ),

            # Assign the logic
            #   If this isn't defined, the protocol can't handle anything correctly
            bot_logic=self.logic_bot,

            # For restarts, exits and other special events
            bot_event_future=bot_event
        )

    async def _login_bot(self, bot_transport:asyncio.BaseTransport|asyncio.Transport):
        """
        Steps that need to be taken for the Bot to be logged into the Twitch IRC chat
        """
        # Login into the irc chat
        #   Not handled by the protocol,
        #   as it is a direct write only feature and doesn't need to respond to anything
        bot_transport.write(twitch_output_format(f"PASS oauth:{self.settings.bot_oath_token}"))
        bot_transport.write(twitch_output_format(f"NICK {self.settings.bot_name}"))
        for channel in self.settings.bot_join_channel:
            bot_transport.write(twitch_output_format(f"JOIN #{channel}"))

        # Request correct capabilities
        if self.settings.bot_capability_tags:  # this should always be requested, else answering to chat is not possible
            bot_transport.write(twitch_output_format(f"CAP REQ :twitch.tv/tags"))
        if self.settings.bot_capability_commands:
            bot_transport.write(twitch_output_format(f"CAP REQ :twitch.tv/commands"))
        if self.settings.bot_capability_membership:
            bot_transport.write(twitch_output_format(f"CAP REQ :twitch.tv/membership"))

        # will catch all those that are Truthy (not: "", None, False, ...)
        if self.settings.bot_join_message:
            for channel in self.settings.bot_join_channel:
                bot_transport.write(twitch_output_format(f"PRIVMSG #{channel} :{self.settings.bot_join_message}"))
