# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from typing import Callable

# Custom Library
from AthenaColor import ForeNest

# Custom Packages
import AthenaTwitchBot.functions.twitch_irc_messages as messages
from AthenaTwitchBot.functions.twitch_message_constructors import twitch_message_constructor_tags

from AthenaTwitchBot.models.twitch_message import TwitchMessage, TwitchMessagePing
from AthenaTwitchBot.models.twitch_bot import TwitchBot
from AthenaTwitchBot.models.twitch_message_context import TwitchMessageContext

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True, eq=False, order=False)
class TwitchBotProtocol(asyncio.Protocol):
    bot:TwitchBot
    main_loop:asyncio.AbstractEventLoop

    # non init slots
    transport:asyncio.transports.Transport = field(init=False)
    message_constructor:Callable = field(init=False)

    def __post_init__(self):
        if self.bot.twitch_capibility_tags:
            self.message_constructor = twitch_message_constructor_tags
        else:
            raise NotImplementedError("This needs to be created")

    def connection_made(self, transport: asyncio.transports.Transport) -> None:
        self.transport = transport
        # first write the password then the nickname else the connection will fail
        self.transport.write(messages.password(oauth_token=self.bot.oauth_token))
        self.transport.write(messages.nick(nickname=self.bot.nickname))
        self.transport.write(messages.join(channel=self.bot.channel))
        self.transport.write(messages.request_tags)

    def data_received(self, data: bytearray) -> None:
        for message in data.split(b"\r\n"):
            match (twitch_message := self.message_constructor(message, bot_name=self.bot.nickname)):
                # Keepalive messages : https://dev.twitch.tv/docs/irc#keepalive-messages
                case TwitchMessagePing():
                    print(ForeNest.ForestGreen("PINGED BY TWITCH"))
                    self.transport.write(pong_message := messages.pong(message=twitch_message.text))
                    print(pong_message)

                # catch a message which starts with a command:
                case TwitchMessage(text=user_message) if user_message.startswith(f"{self.bot.prefix}"):
                    user_message:str
                    print(ForeNest.ForestGreen("COMMAND CAUGHT"))
                    try:
                        user_cmd = user_message.replace(f"{self.bot.prefix}", "")
                        # tuple unpacking because we have a callback
                        #   and the object instance where the command is placed in
                        callback, orign_obj = self.bot.commands[user_cmd]
                        callback(
                            self=orign_obj,
                            # Assign a context so the user doesn't need to write the transport messages themselves
                            #   A user opnly has to write the text
                            context=TwitchMessageContext(
                                message=twitch_message,
                                transport=self.transport
                            )
                        )
                    except KeyError:
                        pass

    def connection_lost(self, exc: Exception | None) -> None:
        self.main_loop.stop()

