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
        # todo make some sort of connector to make t
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
                case TwitchMessage(message=[_,_,_,str(user_message),*user_message_other]) if user_message.startswith(f":{self.bot.prefix}"):
                    user_message:str
                    print(ForeNest.ForestGreen("COMMAND CAUGHT"))
                    try:
                        user_cmd = user_message.replace(f":{self.bot.prefix}", "")
                        result = self.bot.commands[user_cmd](self=self.bot,transport=self.transport)
                        print(result)
                    except KeyError:
                        pass

                # catch a message which has a command within it:
                case TwitchMessage(message=[_,_,_,*messages_parts]):
                    for message in messages_parts:
                        if message.startswith(self.bot.prefix):
                            print(ForeNest.ForestGreen("COMMAND CAUGHT"))

    def connection_lost(self, exc: Exception | None) -> None:
        self.main_loop.stop()

