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
from AthenaTwitchBot.models.twitch_bot import TwitchBot
from AthenaTwitchBot.models.outputs.abstract_output import AbstractOutput
from AthenaTwitchBot.models.twitch_channel import TwitchChannel
from AthenaTwitchBot.models.twitch_message_tags import TwitchMessageTags
from AthenaTwitchBot.models.twitch_user import TwitchUser
from AthenaTwitchBot.models.twitch_context import TwitchContext
from AthenaTwitchBot.models.twitch_bot_method import TwitchBotMethod

from AthenaTwitchBot.functions.output import *

from AthenaTwitchBot.data.unions import OUTPUT_CALLBACKS
from AthenaTwitchBot.data.twitch_irc_messages import (
    PING, PRIVMSG, TMI_TWITCH_TV, JOIN, ACK, ASTERISK, CAP, TWITCH_TAGS, EQUALS
)
from AthenaTwitchBot.data.emotes import emotes_set

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True, eq=False, order=False)
class TwitchBotProtocol(asyncio.Protocol):
    bot:TwitchBot
    outputs:list[type[AbstractOutput]]

    # non init slots
    outputs_initialized:list[AbstractOutput] =field(init=False)
    message_constructor:Callable = field(init=False)
    loop:asyncio.AbstractEventLoop = field(init=False)
    PREFIX_FULL:str = field(init=False)

    def __post_init__(self):
        self.loop = asyncio.get_running_loop()
        self.PREFIX_FULL = f":{self.bot.prefix}"

    # ------------------------------------------------------------------------------------------------------------------
    # - Support Methods  -
    # ------------------------------------------------------------------------------------------------------------------
    async def scheduled_task_coro(self, tsk:TwitchBotMethod, channel:TwitchChannel):
        context_create = lambda : TwitchContext(
            message_tags=TwitchMessageTags(),
            user=TwitchUser(self.bot.nickname),
            channel=channel,
            raw_text=tuple(),
            raw_irc=[""]
        )
        callback = lambda context_: tsk.callback(context=context_)

        if tsk.task_call_on_startup:
            callback(context:=context_create())
            self.parse_context_output(context)

        while True:
            await asyncio.sleep(tsk.task_interval)
            tsk.callback(context=(context:=context_create()))
            self.parse_context_output(context)

    def output_handler(self,callback:OUTPUT_CALLBACKS, **kwargs):
        asyncio.ensure_future(
            asyncio.gather(
                *(callback(output=output, **kwargs)
                for output in self.outputs_initialized)
            ),
            loop=self.loop
        )

    # ------------------------------------------------------------------------------------------------------------------
    # - Protocol necessary  -
    # ------------------------------------------------------------------------------------------------------------------
    def connection_made(self, transport: asyncio.transports.Transport) -> None:
        self.outputs_initialized = [output(transport=transport) for output in self.outputs]

        # first write the password then the nickname else the connection will fail
        self.output_handler(
            callback=output_connection_made,
            # below this point is all **kwargs
            bot = self.bot
        )

        # add frequent_output methods to the coroutine loop
        for tsk in self.bot.scheduled_tasks:
            if tsk.channels is not None and tsk.channels: # the list is populated with channels
                for channel in tsk.channels:
                    coro = self.loop.create_task(self.scheduled_task_coro(tsk, channel=channel))
                    asyncio.ensure_future(coro, loop=self.loop)
            else: # a channel has not been defined, and the task will run on all the bot channels
                for channel in self.bot.channels:
                    coro = self.loop.create_task(self.scheduled_task_coro(tsk, channel=channel))
                    asyncio.ensure_future(coro, loop=self.loop)

    def data_received(self, data: bytearray) -> None:
        self.parse_data(data)

    def connection_lost(self, exc: Exception | None) -> None:
        if exc is not None:
            raise exc

    # ------------------------------------------------------------------------------------------------------------------
    # - MESSAGE PARSING  -
    # ------------------------------------------------------------------------------------------------------------------
    def parse_data(self, data: bytearray):
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

                case _tmi_twitch_tv, str(_), self.bot.nickname, *_ \
                    if _tmi_twitch_tv == TMI_TWITCH_TV:
                    # CATCHES the following pattern:
                    # :tmi.twitch.tv
                    # 001
                    # eva_athenabot
                    # :Welcome, GLHF!
                    self.output_handler(
                        callback=output_undefined,
                        # below this point is all **kwargs
                        text=" ".join(d_split)
                    )

                case str(tags), str(user_name_str), _privmsg, str(channel_str), *text if (
                    _privmsg == PRIVMSG
                    and self.bot.twitch_capability_tags
                ):
                    # CATCHES the following pattern:
                    # @badge-info=;badges=;client-nonce=4ac36d90556713038f596be25cc698a2;color=#1E90FF;display-name=badcop_;emotes=;first-msg=0;flags=;id=8b506bf0-517d-4ae7-9dcb-bce5c2145412;mod=0;room-id=600187263;subscriber=0;tmi-sent-ts=1655367514927;turbo=0;user-id=56931496;user-type=
                    # :badcop_!badcop_@badcop_.tmi.twitch.tv
                    # PRIVMSG
                    # #directiveathena
                    # :that sentence was poggers
                    self.parse_context_output(
                        self.parse_user_message(
                            context=TwitchContext(
                                message_tags=TwitchMessageTags.new_from_tags_str(tags),
                                user=TwitchUser(user_name_str),
                                channel=TwitchChannel(channel_str),
                                raw_text=text,
                                raw_irc=d_split
                            )
                        )
                    )

                case str(user_name_str), _privmsg, str(channel_str), *text if (
                    _privmsg == PRIVMSG
                    and not self.bot.twitch_capability_tags
                ):
                    # CATCHES the following pattern:
                    # :badcop_!badcop_@badcop_.tmi.twitch.tv
                    # PRIVMSG
                    # #directiveathena
                    # :that sentence was poggers
                    self.parse_context_output(
                        self.parse_user_message(
                            context=TwitchContext(
                                message_tags=TwitchMessageTags(),
                                user=TwitchUser(user_name_str),
                                channel=TwitchChannel(channel_str),
                                raw_text=text,
                                raw_irc=d_split
                            )
                        )
                    )

                case str(bot_name_long), _join, str(_) if (
                    _join == JOIN
                    and bot_name_long == f":{self.bot.nickname}!{self.bot.nickname}@{self.bot.nickname}.tmi.twitch.tv"
                ):
                    # CATCHES the following pattern:
                    # :eva_athenabot!eva_athenabot@eva_athenabot.tmi.twitch.tv
                    # JOIN
                    # #directiveathena
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
                    self.output_handler(
                        callback=output_undefined,
                        # below this point is all **kwargs
                        text=" ".join(d_split)
                    )

                case str(bot_name_long), str(_), self.bot.nickname, _equals, str(_), str(bot_name_short) if (
                    _equals == EQUALS
                    and bot_name_long == f":{self.bot.nickname}.tmi.twitch.tv"
                    and bot_name_short == f":{self.bot.nickname}"
                ):
                    # CATCHES the following pattern:
                    # :eva_athenabot.tmi.twitch.tv
                    # 353
                    # eva_athenabot
                    # =
                    # #directiveathena
                    # :eva_athenabot
                    self.output_handler(
                        callback=output_undefined,
                        # below this point is all **kwargs
                        text=" ".join(d_split)
                    )

                case str(bot_name_long), str(_), self.bot.nickname, str(_), *_ \
                    if  bot_name_long == f":{self.bot.nickname}.tmi.twitch.tv":
                    # CATCHES the following pattern:
                    # :eva_athenabot.tmi.twitch.tv
                    # 353
                    # eva_athenabot
                    # =
                    # #directiveathena
                    # :eva_athenabot
                    self.output_handler(
                        callback=output_undefined,
                        # below this point is all **kwargs
                        text=" ".join(d_split)
                    )

                case str(a), if not a:
                    # skip empty lines
                    continue

                case _:
                    self.output_handler(
                        callback=output_undefined,
                        # below this point is all **kwargs
                        text=ForeNest.Maroon("UNDEFINED : '",ForeNest.SlateGray(" ".join(d_split)), "'", sep="")
                    )

    # ------------------------------------------------------------------------------------------------------------------
    # - Message Parsing  -
    # ------------------------------------------------------------------------------------------------------------------
    def parse_user_message(self, context:TwitchContext) -> TwitchContext:
        if (cmd_str := context.raw_text[0]).startswith(self.PREFIX_FULL) and cmd_str != self.PREFIX_FULL:

            context.command_str = cmd_str.replace(self.PREFIX_FULL, "")
            cmd_str_lower = context.command_str.lower()

            try:
                method:TwitchBotMethod = self.bot.commands[cmd_str_lower]
            except KeyError:
                return context

            match method:
                case TwitchBotMethod(command_case_sensitive=True) if context.command_str != cmd_str_lower:
                    return context # checks if the command was case-sensitive and break if it is
                case TwitchBotMethod(command_args=True, command_args_skip_emotes=True):
                    # use set logic to filter out the emotes
                    context.command_args = tuple(set(context.raw_text[1:]).difference(emotes_set))
                case TwitchBotMethod(command_args=True, command_args_skip_emotes=False):
                    context.command_args = context.raw_text[1:]

            method.callback(context=context)

        return context

    def parse_context_output(self, context:TwitchContext):
        match context:
            case TwitchContext(is_write=True):
                self.output_handler(
                    callback=output_write,
                    context=context
                )
            case TwitchContext(is_reply=True):
                self.output_handler(
                    callback=output_reply,
                    context=context
                )
            case _:
                self.output_handler(
                    callback=output_undefined,
                    text=" ".join(context.raw_irc)
                )
