# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import asyncio

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.twitch_bot_protocol import TwitchBotProtocol
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext
from AthenaTwitchBot.models.twitch_bot.logic_output import LogicOutput
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_task import BotTask
from AthenaTwitchBot.data.output_types import OutputTypes
import AthenaTwitchBot.data.global_vars as gbl
from AthenaTwitchBot.data.message_flags import MessageFlags

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
    chat_bot_protocol:type[TwitchBotProtocol]=TwitchBotProtocol
    logic_output:LogicOutput=LogicOutput()

    # non init stuff
    bot_transport:asyncio.Transport=field(init=False, repr=False)
    bot_tasks:set[asyncio.Task]=field(init=False, repr=False, default_factory=set)
    loop:asyncio.AbstractEventLoop=field(init=False, repr=False)

    def launch(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.start_chat_bot(self.loop))
        # login with the chatbot
        self.loop.create_task(self.login_chat_bot())
        # start tasks
        self.loop.create_task(self.start_chat_bot_tasks())

    # ------------------------------------------------------------------------------------------------------------------
    # - Launch the chat bot -
    # ------------------------------------------------------------------------------------------------------------------
    async def start_chat_bot(self, loop:asyncio.AbstractEventLoop):
        self.bot_transport,_ = await loop.create_connection(
            protocol_factory=self.chat_bot_protocol,
            host=self.irc_host,
            port=self.irc_port_ssl if self.ssl_enabled else self.irc_port,
            ssl=self.ssl_enabled
        )

    async def login_chat_bot(self):
        await self.output_twitch(MessageContext(
            flag=MessageFlags.login,output=f"PASS oauth:{gbl.bot.oauth_token}")
        )
        await self.output_twitch(MessageContext(
            flag=MessageFlags.login,output=f"NICK {gbl.bot.nickname}")
        )
        await self.output_twitch(MessageContext(
            flag=MessageFlags.login,output=f"JOIN {','.join(str(c) for c in gbl.bot.channels)}")
        )
        await self.output_twitch(MessageContext(
            flag=MessageFlags.login,output="CAP REQ :twitch.tv/tags")
        )

    # ------------------------------------------------------------------------------------------------------------------
    # - Register and start up tasks to be run every interval -
    # ------------------------------------------------------------------------------------------------------------------
    async def start_chat_bot_tasks(self):
        if BotTask.registered is not None:
            for task in BotTask.registered: #type:BotTask
                if task.channel is None:
                    task.channel = gbl.bot.channels
                loop = asyncio.get_running_loop()
                coro = loop.create_task(self.schedule_chat_bot_task(task=task))
                asyncio.ensure_future(coro, loop=loop)
                self.bot_tasks.add(coro)

    async def schedule_chat_bot_task(self, task:BotTask):
        while True:
            for channel in task.channel:
                await asyncio.sleep(task.interval.to_int_as_seconds())
                context = MessageContext(_channel=channel)
                await task.callback(self=gbl.bot, context=context)
                await self.output_all(context)
                del context

    # ------------------------------------------------------------------------------------------------------------------
    # - Outputs -
    # ------------------------------------------------------------------------------------------------------------------
    async def output_all(self, context:MessageContext):
        await asyncio.gather(
            *[self.output_direct(
                output_type=t,
                context=context
            ) for t in OutputTypes]
        )

    async def output_direct(self, output_type: OutputTypes, context:MessageContext):
        await self.logic_output[output_type].output(context, transport=self.bot_transport)

    async def output_twitch(self, context:MessageContext):
        await self.logic_output[OutputTypes.twitch].output(context, transport=self.bot_transport)


