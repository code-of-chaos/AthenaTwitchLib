# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable
import asyncio
import json
import re

# Athena Packages
from AthenaColor import ForeNest as Fore
from AthenaLib.general.json import GeneralCustomJsonEncoder

# Local Imports
from AthenaTwitchLib.irc.bot_data import BotData
from AthenaTwitchLib.irc.data.enums import ConnectionEvent
from AthenaTwitchLib.irc.logic import BaseCommandLogic
from AthenaTwitchLib.irc.message_context import MessageContext,MessageCommandContext
from AthenaTwitchLib.irc.tags import TagsPRIVMSG, TagsUSERSTATE, TagsUSERNOTICE
from AthenaTwitchLib.logger import SectionIRC, IrcLogger
import AthenaTwitchLib.irc.data.regex as RegexPatterns
from AthenaTwitchLib.string_formatting import twitch_irc_output_format

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class IrcConnectionProtocol(asyncio.Protocol):
    """
    Asyncio.Protocol child class,
    Holds all logic to convert the incoming Twitch IRC messages to useful calls/data
    """
    bot_data:BotData = field(kw_only=True)
    conn_event: asyncio.Future = field(kw_only=True)
    logic_commands:BaseCommandLogic = field(kw_only=True)

    # Non init
    transport: asyncio.transports.Transport = field(init=False)  # delayed as it has to be set after the connection has been made
    _loop :asyncio.AbstractEventLoop = field(init=False)
    _map_pattern_callbacks:list[tuple[re.Pattern, Callable]] = field(default_factory=list, init=False)

    def __post_init__(self):
        self._loop = asyncio.get_running_loop()

        # Populate the map of matched to callback
        #   with the proper combinations of regex to awaitable callback
        self._map_pattern_callbacks.extend([
            (re.compile(fr"^@([^ ]*) ([^ ]*) PRIVMSG #([^:]*) :{self.bot_data.prefix}([^ ]*)(.*)"), self.handle_message_command),
            (RegexPatterns.message, self.handle_message),
            (RegexPatterns.server_ping, self.handle_ping),
            (RegexPatterns.server_message, self.handle_server_message),
            (RegexPatterns.join, self.handle_join),
            (RegexPatterns.part, self.handle_part),
            (RegexPatterns.server_353, self.handle_server_353),
            (RegexPatterns.server_366, self.handle_server_366),
            (RegexPatterns.server_cap, self.handle_server_cap),
            (RegexPatterns.user_notice, self.handle_user_notice),
            (RegexPatterns.user_notice_raid, self.handle_user_notice_raid),
            (RegexPatterns.user_state, self.handle_user_state),
        ])

    # ------------------------------------------------------------------------------------------------------------------
    # - Protocol Calls (aka, calls made by asyncio.Protocol) -
    # ------------------------------------------------------------------------------------------------------------------
    def connection_made(self, transport: asyncio.transports.Transport) -> None:
        # store transport in self
        self.transport = transport

        # Login into the irc chat
        #   Not handled by the protocol,
        #   as it is a direct write only feature and doesn't need to respond to anything
        self.transport.write(twitch_irc_output_format(f"PASS oauth:{self.bot_data.oath_token}"))
        self.transport.write(twitch_irc_output_format(f"NICK {self.bot_data.name}"))

        IrcLogger.log_debug(
            section=SectionIRC.LOGIN,
            data=f"[{self.bot_data.name=}, {self.bot_data.join_channel=}, {self.bot_data.join_message=}, {self.bot_data.prefix=}]"
        )

        # Join all channels and don't wait for the logger to finish
        for channel in self.bot_data.join_channel:
            self.transport.write(twitch_irc_output_format(f"JOIN #{channel}"))

        # Request correct capabilities
        if self.bot_data.capability_tags:
            self.transport.write(twitch_irc_output_format("CAP REQ :twitch.tv/tags"))
        if self.bot_data.capability_commands:
            self.transport.write(twitch_irc_output_format("CAP REQ :twitch.tv/commands"))
        if self.bot_data.capability_membership:
            self.transport.write(twitch_irc_output_format("CAP REQ :twitch.tv/membership"))

        IrcLogger.log_debug(
            section=SectionIRC.LOGIN_CAPABILITY,
            data=f"tags={self.bot_data.capability_tags};commands={self.bot_data.capability_commands};membership{self.bot_data.capability_membership}"
        )

        # will catch all those that are Truthy (not: "", None, False, ...)
        if self.bot_data.join_message:
            for channel in self.bot_data.join_channel:
                self.transport.write(twitch_irc_output_format(f"PRIVMSG #{channel} :{self.bot_data.join_message}"))

            IrcLogger.log_debug(section=SectionIRC.LOGIN_MSG, data=f"Sent Join Message : {self.bot_data.join_message}")

    def data_received(self, data: bytearray) -> None:
        """
        First hit of the protocol when it receives data from Twitch IRC
        Because twitch sends in this data in bytes, and sometimes multiple different message,
        the function has to decode and split the data on every new line
        """

        # Goes over all non-empty lines
        for line in filter(None,data.decode().split("\r\n")):
            # Log the unparsed line
            IrcLogger.log_debug(section=SectionIRC.MSG_ORIGINAL, data=line)

            # Uses filter to get the correct pattern matched group and callback to the corresponding async function
            for callback,group in filter(None, (
                (call,output) if (output := pattern.match(line)) else False
                for pattern, call in self._map_pattern_callbacks
            )):
                # Log which handler we've used
                IrcLogger.log_track(section=SectionIRC.HANDLER_CALLED, data=callback.__name__),

                # Create the coroutine's task
                self._loop.create_task(callback(group, line=line))
                break # breaks from the second for _loop, so it doesn't call the 'no break' else clause

            # No break was called,
            #   meaning nothing could be mapped to a re pattern
            else:
                # Log which handler we've used
                IrcLogger.log_track(section=SectionIRC.HANDLER_CALLED, data=self.handle_UNKNOWN.__name__),
                self._loop.create_task(self.handle_UNKNOWN(None, line))


    def connection_lost(self, exc: Exception | None) -> None:
        if exc is not None:
            print(exc)

        if not self.conn_event.done():
            self.conn_event.set_result(ConnectionEvent.RESTART)

    # ------------------------------------------------------------------------------------------------------------------
    # - Line handlers -
    # ------------------------------------------------------------------------------------------------------------------
    async def handle_ping(self,_:re.Match, *, line):
        """
        Method is called when the Twitch server sends a keep alive PING message
        Needs to have the reply: `"PONG :tmi.twitch.tv` for the connection to remain alive
        """
        print(f"{Fore.Peru('PONG')} | {line}")

        # Need to keep alive
        self.transport.write("PONG :tmi.twitch.tv\r\n".encode())

    # ------------------------------------------------------------------------------------------------------------------
    async def handle_server_message(self, server_message:re.Match, *, line:str):
        """
        Method is called when the Twitch server sends a message that isn't related to any user or room messages
        """
        print(f"{Fore.Blue('SERVER_MESSAGE')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    async def handle_server_353(self, server_353: re.Match, *, line: str):
        """
        Method is called when twitch sends a 353 message
        """
        print(f"{Fore.AliceBlue('SERVER_353')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    async def handle_server_366(self, server_366: re.Match, *, line: str):
        """
        Method is called when twitch sends a 353 message
        """
        print(f"{Fore.Ivory('SERVER_366')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    async def handle_server_cap(self, server_cap: re.Match, *, line: str):
        """
        Method is called when twitch sends a CAP message
        """
        print(f"{Fore.Khaki('SERVER_CAP')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    async def handle_join(self, join:re.Match,*, line:str):
        """
        Method is called when any user (irc or viewer) joins the channel
        """
        print(f"{Fore.Red('JOIN')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    async def handle_part(self, part:re.Match, *, line:str):
        """
        Method is called when any user (irc or viewer) parts the channel
        """
        print(f"{Fore.DeepPink('PART')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    async def handle_message(self, message:re.Match, *, line:str):
        """
        Method is called when any user (irc or viewer) sends a regular message in the channel
        """
        print(f"{Fore.Orchid('MESSAGE')} | {message.groups()[-1]} | {Fore.SlateGray(line)}")

        # Extract data from matched message
        #   Easily done due to regex groups
        tags_group_str,user,channel,text = message.groups()

        # Create the context and run more checks
        message_context = MessageContext(
            tags=await TagsPRIVMSG.import_from_group_as_str(tags_group_str),
            user=user,
            username=RegexPatterns.username.findall(user)[0],
            channel=channel,
            text=text,
            transport=self.transport,
            bot_event_future=self.conn_event,
            original_line=line
        )
        IrcLogger.log_debug(section=SectionIRC.MSG_CONTEXT,
                            data=json.dumps(message_context.as_dict(), cls=GeneralCustomJsonEncoder))

    # ------------------------------------------------------------------------------------------------------------------
    async def handle_message_command(self, message:re.Match, *, line:str):
        """
        Method is called when any user (irc or viewer) sends a message in the channel,
        which is presumed to be an irc command
        """
        print(f"{Fore.Orchid('MESSAGE_COMMAND')} | {message.groups()[-1]} | {Fore.SlateGray(line)}")

        # Extract data from matched message
        #   Easily done due to regex groups
        tags_group_str,user,channel,command,args = message.groups()

        message_context = MessageCommandContext(
            tags=await TagsPRIVMSG.import_from_group_as_str(tags_group_str),
            user=user,
            username=RegexPatterns.username.findall(user)[0],
            channel=channel,
            text=f"!{command}",
            transport=self.transport,
            bot_event_future=self.conn_event,
            original_line=line,
            command=command,
            args=args.strip().split(" ")
        )

        IrcLogger.log_debug(section=SectionIRC.MSG_CONTEXT,
                            data=json.dumps(message_context.as_dict(), cls=GeneralCustomJsonEncoder))

        await self.logic_commands.execute_command(
            context=message_context
        )

    # ------------------------------------------------------------------------------------------------------------------
    async def handle_user_notice(self, user_notice:re.Match, *, line:str):
        """
        Method is called when twitch sends a USERNOTICE message
        """
        tags_group_str,user,channel,text = user_notice.groups()
        tags = await TagsUSERNOTICE.import_from_group_as_str(tags_group_str)
        print(f"{Fore.Plum('USERNOTICE')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    async def handle_user_notice_raid(self, user_notice_raid:re.Match, *, line:str):
        """
        Method is called when twitch sends a USERNOTICE message
        """
        tags_group_str,channel = user_notice_raid.groups()
        tags = await TagsUSERNOTICE.import_from_group_as_str(tags_group_str)
        print(f"{Fore.Plum('USERNOTICE RAID')} | {line} | {tags}")

    # ------------------------------------------------------------------------------------------------------------------
    async def handle_user_state(self, user_state:re.Match, *, line:str):
        """
        Method is called when twitch sends a USERSTATE message
        """
        tags_group_str,channel = user_state.groups()
        tags = await TagsUSERSTATE.import_from_group_as_str(tags_group_str)
        print(f"{Fore.Plum('USERSTATE')} | {line} | {tags}")

    # ------------------------------------------------------------------------------------------------------------------
    async def handle_UNKNOWN(self, _, line:str):
        """
        Method is called when the protocol can't find an appropriate match for the given string
        """
        print(Fore.SlateGray(f"NOT CAUGHT | {line}"))
        IrcLogger.log_warning(section=SectionIRC.HANDLER_UNKNOWN, data=line)