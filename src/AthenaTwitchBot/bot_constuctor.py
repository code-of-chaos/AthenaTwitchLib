# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import socket
import asyncio

# Athena Packages

# Local Imports
from AthenaTwitchBot.string_formatting import twitch_output_format
from AthenaTwitchBot.bot_protocol import BotConnectionProtocol
from AthenaTwitchBot.regex import RegexPatterns
from AthenaTwitchBot.bot_settings import BotSettings

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
async def bot_constructor(settings:BotSettings, protocol_type:type[BotConnectionProtocol]=BotConnectionProtocol):
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
        protocol_factory=lambda:protocol_type(
            settings=settings,
            regex_patterns = RegexPatterns(
                bot_name=settings.bot_name
            )
        ),
        server_hostname=settings.irc_host,
        ssl=settings.ssl_enabled,
        sock=sock
    )
    # Give the protocol the
    bot_transport:asyncio.Transport
    protocol_obj.transport = bot_transport

    if bot_transport is None:
        raise ConnectionRefusedError

    bot_transport.write(twitch_output_format(f"PASS oauth:{settings.bot_oath_token}"))
    bot_transport.write(twitch_output_format(f"NICK {settings.bot_name}"))
    bot_transport.write(twitch_output_format(f"JOIN #{settings.bot_join_channel}"))
    bot_transport.write(twitch_output_format(f"CAP REQ :twitch.tv/commands"))
    bot_transport.write(twitch_output_format(f"CAP REQ :twitch.tv/membership"))
    bot_transport.write(twitch_output_format(f"CAP REQ :twitch.tv/tags"))

    if settings.bot_join_message is not None:
        bot_transport.write(
            twitch_output_format(
                f":{settings.bot_name}!{settings.bot_name}@{settings.bot_name}.tmi.twitch.tv PRIVMSG #{settings.bot_join_channel} :{settings.bot_join_message}"
            )
        )



