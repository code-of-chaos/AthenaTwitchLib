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
from AthenaTwitchBot.models.twitch_command import TwitchCommand

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
        if self.bot.twitch_capability_tags:
            self.message_constructor = twitch_message_constructor_tags
        else:
            raise NotImplementedError("This needs to be created")

    # ----------------------------------------------------------------------------------------------------------------------
    # - Protocol necessary  -
    # ----------------------------------------------------------------------------------------------------------------------
    def connection_made(self, transport: asyncio.transports.Transport) -> None:
        self.transport = transport
        # first write the password then the nickname else the connection will fail
        self.transport.write(messages.password(oauth_token=self.bot.oauth_token))
        self.transport.write(messages.nick(nickname=self.bot.nickname))
        self.transport.write(messages.join(channel=self.bot.channel))
        self.transport.write(messages.request_tags)

        # add frequent_output methods to the coroutine loop
        loop = asyncio.get_running_loop()
        for callback, delay in self.bot.frequent_outputs:
            coro = loop.create_task(self.frequent_output_call(callback,delay))
            asyncio.ensure_future(coro, loop=loop)

    async def frequent_output_call(self, callback,delay:int):
        context = TwitchMessageContext(
            message=TwitchMessage(channel=f"#{self.bot.channel}"),
            transport=self.transport
        )
        while True:
            await asyncio.sleep(delay)
            callback(
                self=self.bot,
                context=context)

    def data_received(self, data: bytearray) -> None:
        for message in data.split(b"\r\n"):
            if message == bytearray(b''): # if the bytearray is empty, just skip to the next one
                continue
            match (twitch_message := self.message_constructor(message, bot_name=self.bot.nickname)):
                # Keepalive messages : https://dev.twitch.tv/docs/irc#keepalive-messages
                case TwitchMessagePing():
                    print(ForeNest.ForestGreen("PINGED BY TWITCH"))
                    self.transport.write(messages.pong(message=twitch_message.text))

                # catch a message which starts with a command:
                case TwitchMessage(text=str(user_message)) if user_message.startswith(f"{self.bot.prefix}"):
                    user_message:str
                    print(ForeNest.ForestGreen("POSSIBLE COMMAND CAUGHT"))
                    try:
                        user_cmd_str = user_message.replace(f"{self.bot.prefix}", "")
                        twitch_command:TwitchCommand = self.bot.commands[user_cmd_str.lower()]
                        if twitch_command.force_capitalization and user_cmd_str != twitch_command.name:
                            raise KeyError # the check to make the force capitalization work

                        twitch_command.callback(
                            self=self.bot,
                            # Assign a context so the user doesn't need to write the transport messages themselves
                            #   A user only has to write the text
                            context=TwitchMessageContext(
                                message=twitch_message,
                                transport=self.transport
                            )
                        )
                        print(ForeNest.ForestGreen("COMMAND EXECUTED"))
                    except KeyError:
                        print(ForeNest.Crimson("COMMAND COULD NOT BE PARSED"))
                        pass

    def connection_lost(self, exc: Exception | None) -> None:
        self.main_loop.stop()

