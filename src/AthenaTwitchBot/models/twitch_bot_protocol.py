# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from typing import Callable

# Custom Library

# Custom Packages
import AthenaTwitchBot.functions.twitch_irc_messages as messages
from AthenaTwitchBot.functions.twitch_message_constructors import twitch_message_constructor_tags

from AthenaTwitchBot.models.twitch_message import TwitchMessage, TwitchMessagePing
from AthenaTwitchBot.models.twitch_bot import TwitchBot
from AthenaTwitchBot.models.twitch_message_context import TwitchMessageContext
from AthenaTwitchBot.models.wrapper_helpers.command import Command
from AthenaTwitchBot.models.wrapper_helpers.scheduled_task import ScheduledTask
from AthenaTwitchBot.models.outputs.output import Output

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True, eq=False, order=False)
class TwitchBotProtocol(asyncio.Protocol):
    bot:TwitchBot
    output:Output

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
        for tsk in self.bot.scheduled_tasks:
            coro = loop.create_task(self.frequent_output_call(tsk))
            asyncio.ensure_future(coro, loop=loop)

    async def frequent_output_call(self, tsk:ScheduledTask):
        context = TwitchMessageContext(
            message=TwitchMessage(channel=f"#{self.bot.channel}"),
            transport=self.transport
        )
        if tsk.before: # the before attribute handles if we sleep before or after the task has been called
            while True:
                await asyncio.sleep(tsk.delay)
                tsk.callback(
                    self=self.bot,
                    context=context)
        else:
            while True:
                tsk.callback(
                    self=self.bot,
                    context=context)
                await asyncio.sleep(tsk.delay)


    def data_received(self, data: bytearray) -> None:
        for message in data.split(b"\r\n"):
            # if the bytearray is empty, just skip to the next one
            if message == bytearray(b''):
                continue

            match (twitch_message := self.message_constructor(message, bot_name=self.bot.nickname)):
                # Keepalive messages : https://dev.twitch.tv/docs/irc#keepalive-messages
                case TwitchMessagePing():
                    self.output.message(twitch_message)
                    self.transport.write(messages.pong(message=twitch_message.text))
                    continue

                # catch a message which starts with a command:
                case TwitchMessage(text=str(user_message)) if user_message.startswith(f"{self.bot.prefix}"):
                    self.output.message(twitch_message)
                    user_message:str
                    try:
                        user_cmd_str = user_message.replace(self.bot.prefix, "")
                        twitch_command:Command = self.bot.commands[user_cmd_str.lower()]
                        if twitch_command.case_sensitive and user_cmd_str != twitch_command.name:
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
                    except KeyError:
                        pass
                    continue

            # if the message wasn't able to be handled by the parser above
            #   it will just be outputted as undefined
            self.output.undefined(message)

    def connection_lost(self, exc: Exception | None) -> None:
        loop = asyncio.get_running_loop()
        loop.stop()

        if exc is not None:
            raise exc

