# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
from dataclasses import dataclass, field

# Custom Library
from AthenaColor import ForeNest

# Custom Packages
import AthenaTwitchBot.functions.twitch_irc_messages as messages
from AthenaTwitchBot.models.twitch_message import TwitchMessage

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True, eq=False, order=False)
class TwitchBotProtocol(asyncio.Protocol):
    bot_nickname:str
    bot_oauth_token:str
    bot_channel:str
    command_prefix:str
    main_loop:asyncio.AbstractEventLoop

    # non init slots
    transport:asyncio.transports.Transport = field(init=False)

    def connection_made(self, transport: asyncio.transports.Transport) -> None:
        # todo make some sort of connector to make t
        self.transport = transport
        # first write the password then the nickname else the connection will fail
        self.transport.write(messages.password(oauth_token=self.bot_oauth_token))
        self.transport.write(messages.nick(nickname=self.bot_nickname))
        self.transport.write(messages.join(channel=self.bot_channel))

    def data_received(self, data: bytearray) -> None:
        match (twitch_message := TwitchMessage(data)):
            # Keepalive messages : https://dev.twitch.tv/docs/irc#keepalive-messages
            case TwitchMessage(message=["PING", *_]):
                print(ForeNest.ForestGreen("PINGED BY TWITCH"))
                self.transport.write(pong_message := messages.pong(
                    message=twitch_message.message[1:-1]
                ))
                print(data, pong_message)

            # catch a message which starts with a command:
            case TwitchMessage(message=[_,_,_,str(user_message),*user_message_other]) if user_message.startswith(f":{self.command_prefix}"):
                user_message:str
                print(ForeNest.ForestGreen("COMMAND CAUGHT"))
                print(user_message, user_message_other)

            # catch a message which has a command within it:
            case TwitchMessage(message=[_,_,_,*messages_parts]):
                print(messages_parts)
                for message in messages_parts:
                    if message.startswith(self.command_prefix):
                        print(ForeNest.ForestGreen("COMMAND CAUGHT"))
                        print(messages_parts)
                print(data)
            case _:
                print(data)

    def connection_lost(self, exc: Exception | None) -> None:
        self.main_loop.stop()

