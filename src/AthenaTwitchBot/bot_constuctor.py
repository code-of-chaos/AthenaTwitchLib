# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import socket
import asyncio
import pathlib

# Athena Packages

# Local Imports
from AthenaTwitchBot.string_formatting import twitch_output_format
from AthenaTwitchBot.bot_protocol import BotConnectionProtocol
from AthenaTwitchBot.regex import RegexPatterns
from AthenaTwitchBot.bot_settings import BotSettings
from AthenaTwitchBot.logic.logic_bot import LogicBot
from AthenaTwitchBot.bot_logger import BotLogger
from AthenaTwitchBot.bot_event_types import BotEvent

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
async def bot_constructor(
    settings:BotSettings,
    logic_bot:LogicBot=None,
    protocol_type:type[BotConnectionProtocol]=BotConnectionProtocol,
    logging_enabled:bool=False,
    loop:asyncio.AbstractEventLoop=None
):
    """
    Constructor function for the Bot and all its logical systems like the asyncio.Protocol handler.
    It also logs the bot in onto the Twitch IRC server
    """
    if loop is None:
        loop = asyncio.get_running_loop()

    # Define the logger as soon as possible,
    #   As it is called by a lot of different systems
    BotLogger.set_logger(
        path=pathlib.Path("data/logger.sqlite"),
        logging_enabled=logging_enabled,
        log_all_messages=True,
    )
    await BotLogger.logger.create_tables()

    _keep_restarting:bool=True

    while _keep_restarting:
        # Assemble the asyncio.Protocol
        #   The custom protocol_type needs a constructor to known which patterns to use, settings, etc...
        bot_event_future: asyncio.Future = loop.create_future()

        # Create a custom socket object
        sock = socket.socket()
        sock.settimeout(5.)
        sock.connect(
            (
                settings.irc_host,
                settings.irc_port_ssl if settings.ssl_enabled else settings.irc_port
            )
        )

        # noinspection PyArgumentList
        bot_transport, protocol_obj = await asyncio.get_running_loop().create_connection(
            protocol_factory=lambda: protocol_type(
                settings=settings,
                regex_patterns=RegexPatterns(
                    bot_name=settings.bot_name,
                    bot_prefix=settings.bot_prefix
                ),
                bot_logic=logic_bot,
                bot_event_future=bot_event_future
            ),
            server_hostname=settings.irc_host,
            ssl=settings.ssl_enabled,
            sock=sock
        )
        if bot_transport is None:
            raise ConnectionRefusedError

        # Give the protocol the transporter,
        #   so it can easily create write calls to the connection
        bot_transport: asyncio.Transport
        protocol_obj.transport = bot_transport

        # Login into the irc chat
        #   Not handled by the protocol,
        #   as it is a direct write only feature and doesn't need to respond to anything
        bot_transport.write(twitch_output_format(f"PASS oauth:{settings.bot_oath_token}"))
        bot_transport.write(twitch_output_format(f"NICK {settings.bot_name}"))
        for channel in settings.bot_join_channel:
            bot_transport.write(twitch_output_format(f"JOIN #{channel}"))

        # Request correct capabilities
        if settings.bot_capability_tags:  # this should always be requested, else answering to chat is not possible
            bot_transport.write(twitch_output_format(f"CAP REQ :twitch.tv/tags"))
        if settings.bot_capability_commands:
            bot_transport.write(twitch_output_format(f"CAP REQ :twitch.tv/commands"))
        if settings.bot_capability_membership:
            bot_transport.write(twitch_output_format(f"CAP REQ :twitch.tv/membership"))

        # will catch all those that are Truthy (not: "", None, False, ...)
        if settings.bot_join_message:
            for channel in settings.bot_join_channel:
                bot_transport.write(twitch_output_format(f"PRIVMSG #{channel} :{settings.bot_join_message}"))

        try:
            match result := await bot_event_future :
                case BotEvent.RESTART:
                    print("RESTART")
                    bot_transport.close()
                    continue # restarts it all

                case BotEvent.EXIT:
                    print("EXIT")
                    bot_transport.close()
                    _keep_restarting = False

                case _ :
                    print(result)

        except asyncio.InvalidStateError:
            raise

    # NOTHING AFTER THIS !
