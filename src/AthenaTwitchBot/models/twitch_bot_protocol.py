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
from AthenaTwitchBot.models.twitch_message import TwitchMessage
from AthenaTwitchBot.models.twitch_bot import TwitchBot
from AthenaTwitchBot.models.twitch_message_context import TwitchMessageContext
from AthenaTwitchBot.models.wrapper_helpers.scheduled_task import ScheduledTask
from AthenaTwitchBot.models.outputs.output import Output
from AthenaTwitchBot.models.outputs.output_twitch import OutputTwitch
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

from AthenaTwitchBot.functions.output import *

from AthenaTwitchBot.data.unions import OUTPUT_CALLBACKS
from AthenaTwitchBot.data.twitch_irc_messages import (
    PING, PRIVMSG, TMI_TWITCH_TV, JOIN, ACK, ASTERISK, CAP, TWITCH_TAGS, EQUALS
)

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True, eq=False, order=False)
class TwitchBotProtocol(asyncio.Protocol):
    bot:TwitchBot
    outputs:list[Output]

    # non init slots
    transport:asyncio.transports.Transport = field(init=False)
    message_constructor:Callable = field(init=False)
    loop:asyncio.AbstractEventLoop = field(init=False)

    def __post_init__(self):
        self.loop = asyncio.get_running_loop()

    # ------------------------------------------------------------------------------------------------------------------
    # - Support Methods  -
    # ------------------------------------------------------------------------------------------------------------------
    async def scheduled_task_coro(self, tsk:ScheduledTask, channel:TwitchChannel):
        context = TwitchMessageContext(
            message=TwitchMessage(channel=channel),
            transport=self.transport
        )
        if tsk.wait_before: # the wait_before attribute handles if we sleep wait_before or after the task has been called
            while True:
                await asyncio.sleep(tsk.delay)
                tsk.callback(self=self.bot,context=context)
        else:
            while True:
                tsk.callback(self=self.bot,context=context)
                await asyncio.sleep(tsk.delay)

    def output_handler(self,callback:OUTPUT_CALLBACKS, **kwargs):
        # TODO test code below with asyncio.gather
        for output in self.outputs:
            # schedule the coro
            asyncio.ensure_future(
                # only the twitch bots need the transport object
                self.loop.create_task(callback(output=output,transport=self.transport,**kwargs))
                if isinstance(output, OutputTwitch) else
                self.loop.create_task(callback(output=output, **kwargs))
                ,
                loop=self.loop)

    # ------------------------------------------------------------------------------------------------------------------
    # - Protocol necessary  -
    # ------------------------------------------------------------------------------------------------------------------
    def connection_made(self, transport: asyncio.transports.Transport) -> None:
        self.transport = transport
        # first write the password then the nickname else the connection will fail
        self.output_handler(
            callback=output_connection_made,
            # below this point is all **kwargs
            bot = self.bot
        )

        # add frequent_output methods to the coroutine loop
        for tsk in self.bot.scheduled_tasks:
            if tsk.channels: # the list is populated with channels
                for channel in tsk.channels:
                    coro = self.loop.create_task(self.scheduled_task_coro(tsk, channel=channel))
                    asyncio.ensure_future(coro, loop=self.loop)
            else: # a channel has not been defined, and the task will run on all the bot channels
                for channel in self.bot.channels:
                    coro = self.loop.create_task(self.scheduled_task_coro(tsk, channel=channel))
                    asyncio.ensure_future(coro, loop=self.loop)


    def data_received(self, data: bytearray) -> None:
        self.data_parser(data)

    def connection_lost(self, exc: Exception | None) -> None:
        self.loop.stop()

        if exc is not None:
            raise exc

        # ------------------------------------------------------------------------------------------------------------------
        # - MESSAGE PARSING  -
        # ------------------------------------------------------------------------------------------------------------------

    def data_parser(self, data: bytearray):
        """Actual message parsing, which parses viewer's messages"""
        # decode and split to handle every message by itself
        for d in data.decode("utf_8").split("\r\n"):
            # catch some patterns early to be either ignored or parsed
            match d_split:= d.split(" "):
                case _ping, *ping_response \
                    if _ping == PING:
                    # CATCHES the following pattern:
                    # PING
                    # :tmi.twitch.tv
                    self.output_handler(
                        callback=output_connection_ping,
                        # below this point is all **kwargs
                        ping_response=ping_response # same response has to be given back
                    )
                    continue # go to next piece of data

                case _tmi_twitch_tv, str(int_id), self.bot.nickname, *text \
                    if _tmi_twitch_tv == TMI_TWITCH_TV:
                    # CATCHES the following pattern:
                    # :tmi.twitch.tv
                    # 001
                    # eva_athenabot
                    # :Welcome, GLHF!
                    pass # todo functionality
                    self.output_handler(
                        callback=output_undefined,
                        # below this point is all **kwargs
                        text=" ".join(d_split)
                    )


                case str(info), str(user_name), _privmsg, str(channel), *text \
                    if _privmsg == PRIVMSG:
                    # CATCHES the following pattern:
                    # @badge-info=;badges=;client-nonce=4ac36d90556713038f596be25cc698a2;color=#1E90FF;display-name=badcop_;emotes=;first-msg=0;flags=;id=8b506bf0-517d-4ae7-9dcb-bce5c2145412;mod=0;room-id=600187263;subscriber=0;tmi-sent-ts=1655367514927;turbo=0;user-id=56931496;user-type=
                    # :badcop_!badcop_@badcop_.tmi.twitch.tv
                    # PRIVMSG
                    # #directiveathena
                    # :that sentence was poggers
                    pass # todo functionality
                    self.output_handler(
                        callback=output_undefined,
                        # below this point is all **kwargs
                        text=" ".join(d_split)
                    )

                case str(bot_name_long), _join, str(channel) \
                    if _join == JOIN \
                       and bot_name_long == f":{self.bot.nickname}!{self.bot.nickname}@{self.bot.nickname}.tmi.twitch.tv":
                    # CATCHES the following pattern:
                    # :eva_athenabot!eva_athenabot@eva_athenabot.tmi.twitch.tv
                    # JOIN
                    # #directiveathena
                    pass # todo functionality
                    self.output_handler(
                        callback=output_undefined,
                        # below this point is all **kwargs
                        text=" ".join(d_split)
                    )

                case _list if _list == [TMI_TWITCH_TV, CAP, ASTERISK, ACK, TWITCH_TAGS]:
                    # CATCHES the following pattern:
                    # :tmi.twitch.tv
                    # CAP
                    # *
                    # ACK
                    # :twitch.tv/tags
                    pass # todo functionality
                    self.output_handler(
                        callback=output_undefined,
                        # below this point is all **kwargs
                        text=" ".join(d_split)
                    )

                case str(bot_name_long), str(int_id), self.bot.nickname, _equals, str(channel), str(bot_name_short) \
                    if _equals == EQUALS \
                       and bot_name_long == f":{self.bot.nickname}.tmi.twitch.tv" \
                       and bot_name_short == f":{self.bot.nickname}":
                    # CATCHES the following pattern:
                    # :eva_athenabot.tmi.twitch.tv
                    # 353
                    # eva_athenabot
                    # =
                    # #directiveathena
                    # :eva_athenabot
                    pass # todo functionality
                    self.output_handler(
                        callback=output_undefined,
                        # below this point is all **kwargs
                        text=" ".join(d_split)
                    )

                case str(bot_name_long), str(int_id), self.bot.nickname, str(channel), *text \
                    if  bot_name_long == f":{self.bot.nickname}.tmi.twitch.tv":
                    # CATCHES the following pattern:
                    # :eva_athenabot.tmi.twitch.tv
                    # 353
                    # eva_athenabot
                    # =
                    # #directiveathena
                    # :eva_athenabot
                    pass  # todo functionality
                    self.output_handler(
                        callback=output_undefined,
                        # below this point is all **kwargs
                        text=" ".join(d_split)
                    )

                case _:
                    self.output_handler(
                        callback=output_undefined,
                        # below this point is all **kwargs
                        text=ForeNest.Maroon("UNDEFINED : '",ForeNest.SlateGray(" ".join(d_split)), "'", sep="")
                    )


