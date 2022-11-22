# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import socket
import asyncio
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import NoReturn

# Custom Library
from AthenaColor import ForeNest

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.twitch_bot_protocol import TwitchBotProtocol
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext
from AthenaTwitchBot.models.twitch_bot.logic_output import LogicOutput
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_task import BotTask
from AthenaTwitchBot.data.output_types import OutputTypes
import AthenaTwitchBot.data.global_vars as gbl
from AthenaTwitchBot.data.message_flags import MessageFlags
import AthenaTwitchBot.data.irc_twitch as irc_twitch

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, eq=False, order=False, slots=True)
class BotServer:
    # optional kwargs
    ssl_enabled:bool=True
    irc_host:str='irc.chat.twitch.tv'
    irc_port:int=6667
    irc_port_ssl:int=6697

    # things that aren't normally customized, but you never know what a user might want
    chat_bot_protocol:Callable[[], asyncio.BaseProtocol]=lambda: TwitchBotProtocol()
    logic_output:LogicOutput=field(default_factory=LogicOutput)

    # non init stuff
    bot_transport:asyncio.BaseTransport=field(init=False, repr=False)
    bot_tasks:set[asyncio.Task[None]]=field(init=False, repr=False, default_factory=set)
    loop:asyncio.AbstractEventLoop=field(init=False, repr=False)

    async def launch(self) -> None:
        # self.loop.create_task(self.start_chat_bot(self.loop))
        await self.start_chat_bot()
        print(ForeNest.Gold("CONNECTED"))

        # login with the chatbot
        await self.login_chat_bot()
        print(ForeNest.Gold("LOGGED IN"))

        # start tasks
        await self.start_chat_bot_tasks()
        print(ForeNest.Gold("STARTED TASKS"))


    # ------------------------------------------------------------------------------------------------------------------
    # - Launch the chat bot -
    # ------------------------------------------------------------------------------------------------------------------
    async def start_chat_bot(self) -> None:
        sock = socket.socket()
        sock.settimeout(5.)
        sock.connect((self.irc_host,self.irc_port_ssl if self.ssl_enabled else self.irc_port))

        self.bot_transport, _ = await asyncio.get_running_loop().create_connection(
            protocol_factory=self.chat_bot_protocol,
            server_hostname=self.irc_host,
            ssl=self.ssl_enabled,
            sock=sock
        )

        if self.bot_transport is None:
            raise ConnectionRefusedError

    async def login_chat_bot(self) -> None:
        assert gbl.bot is not None
        await self.output_twitch(MessageContext(
            flag=MessageFlags.login,output=f"PASS oauth:{gbl.bot.oauth_token}")
        )
        await self.output_twitch(MessageContext(
            flag=MessageFlags.login,output=f"NICK {gbl.bot.nickname}")
        )
        await self.output_twitch(MessageContext(
            flag=MessageFlags.login,output=f"JOIN {str(gbl.bot.channel)}")
        )

        await asyncio.gather(
            self.set_twitch_capability_commands(),
            self.set_twitch_capability_membership(),
            self.set_twitch_capability_tags()
        )

    # ------------------------------------------------------------------------------------------------------------------
    # - Capabilities -
    # ------------------------------------------------------------------------------------------------------------------
    async def set_twitch_capability_commands(self) -> None:
        assert gbl.bot is not None
        if gbl.bot.twitch_capability_commands:
            await self.output_twitch(MessageContext(flag=MessageFlags.login,output=irc_twitch.REQUEST_COMMANDS))
    async def set_twitch_capability_membership(self) -> None:
        assert gbl.bot is not None
        if gbl.bot.twitch_capability_membership:
            await self.output_twitch(MessageContext(flag=MessageFlags.login,output=irc_twitch.REQUEST_COMMANDS))
    async def set_twitch_capability_tags(self) -> None:
        assert gbl.bot is not None
        if gbl.bot.twitch_capability_tags:
            await self.output_twitch(MessageContext(flag=MessageFlags.login,output=irc_twitch.REQUEST_TAGS))

    # ------------------------------------------------------------------------------------------------------------------
    # - Register and start up tasks to be run every interval -
    # ------------------------------------------------------------------------------------------------------------------
    async def schedule_chat_bot_task(self, task:BotTask) -> NoReturn:
        assert gbl.bot is not None
        while True:
            await asyncio.sleep(task.interval.to_int_as_seconds())
            context = MessageContext(_channel=gbl.bot.channel)
            await task.callback(gbl.bot, context)
            await self.output_all(context)
            del context

    async def start_chat_bot_tasks(self) -> None:
        for task in BotTask.registered:
            loop = asyncio.get_running_loop()
            coro = loop.create_task(self.schedule_chat_bot_task(task=task))
            asyncio.ensure_future(coro, loop=loop)
            self.bot_tasks.add(coro)

    # ------------------------------------------------------------------------------------------------------------------
    # - Outputs -
    # ------------------------------------------------------------------------------------------------------------------
    async def output_all(self, context:MessageContext) -> None:
        await asyncio.gather(
            *[self.output_direct(
                output_type=t,
                context=context
            ) for t in self.logic_output.types]
        )

    async def output_direct(self, output_type: OutputTypes, context:MessageContext) -> None:
        await self.logic_output[output_type].output(context, transport=self.bot_transport)

    async def output_twitch(self, context:MessageContext) -> None:
        await self.logic_output[self.logic_output.types.twitch].output(context, transport=self.bot_transport)


