# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
import asyncio
import functools
import json
import re

# Athena Packages
from AthenaColor import ForeNest as Fore
from AthenaLib.general.json import GeneralCustomJsonEncoder

# Local Imports
from AthenaTwitchLib.irc.bot import Bot
from AthenaTwitchLib.irc.data.enums import BotEvent
from AthenaTwitchLib.irc.message_context import MessageContext,MessageCommandContext
from AthenaTwitchLib.irc.tags import TagsPRIVMSG, TagsUSERSTATE, TagsUSERNOTICE
from AthenaTwitchLib.logger import SectionIRC, IrcLogger
import AthenaTwitchLib.irc.data.regex as RegexPatterns

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class _TransportBuffer:
    """
    Simple class to be used by the `IrcConnectionProtocol`, before the transporter object is actually set.
    It keeps the to be sent message into a small buffer, for it to then be parsed and deleted once the
    actual transporter is present in the `IrcConnectionProtocol`
    """
    buffer: list[bytes] = field(default_factory=list)

    def write(self, data:bytes):
        """
        Stores data to the buffer
        """
        self.buffer.append(data)

def log_handler(fnc:Callable) -> Any:
    """
    Simple decorator to keep track of how many calls are made to handlers
    """
    @functools.wraps(fnc)
    async def wrapper(*args, **kwargs):
        IrcLogger.log_track(section=SectionIRC.HANDLER_CALLED, data=fnc.__name__),
        if (line := kwargs.get("line", None)) is not None:
            IrcLogger.log_debug(section=SectionIRC.MSG_ORIGINAL, data=line),

        return await fnc(*args, **kwargs)

    return wrapper

TransportBuffer = _TransportBuffer()

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class IrcConnectionProtocol(asyncio.Protocol):
    """
    Asyncio.Protocol child class,
    Holds all logic to convert the incoming Twitch IRC messages to useful calls/data
    """
    bot_event_future: asyncio.Future
    bot_obj:Bot

    _transport: asyncio.transports.Transport = None  # delayed as it has to be set after the connection has been made

    # Non init
    loop :asyncio.AbstractEventLoop = field(init=False)
    map_pattern_callbacks:list[tuple[re.Pattern, Callable]] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.loop = asyncio.get_running_loop()

        # Populate the map of matched to callback
        #   with the proper combinations of regex to awaitable callback
        self.map_pattern_callbacks.extend([
            (re.compile(fr"^@([^ ]*) ([^ ]*) PRIVMSG #([^:]*) :{self.bot_obj.prefix}([^ ]*)(.*)"), self.handle_message_command),
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
    # - Properties -
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def transport(self):
        """
        Getter of the `transport` property
        This is necessary as transport is set later by the constructor than when the protocol is created
        When the transport isn't set yet, it will store write data to a temp buffer
        This buffer will be removed after the setter of the `transport` property is called
        """
        if self._transport is None:
            return TransportBuffer

        return self._transport

    @transport.setter
    def transport(self, value:asyncio.transports.Transport):
        """
        Setter of the `transport` property
        Executes any write calls in the buffer, and the deletes the buffer
        """
        self._transport = value

        #Todo remove this constant buffer check, because the buffer should only be cleared once and then forgotten
        if TransportBuffer.buffer:
            for data in TransportBuffer.buffer:
                self._transport.write(data)

            TransportBuffer.buffer.clear()

    # ------------------------------------------------------------------------------------------------------------------
    # - Protocol Calls (aka, calls made by asyncio.Protocol) -
    # ------------------------------------------------------------------------------------------------------------------
    def data_received(self, data: bytearray) -> None:
        """
        First hit of the protocol when it receives data from Twitch IRC
        Because twitch sends in this data in bytes, and sometimes multiple different message,
        the function has to decode and split the data on every new line
        """

        # Goes over all non-empty lines
        for line in filter(None,data.decode().split("\r\n")):
            # Uses filter to get the correct pattern matched group and callback to the corresponding async function
            for callback,group in filter(None, (
                (call,output) if (output := pattern.match(line)) else False
                for pattern, call in self.map_pattern_callbacks
            )):
                self.loop.create_task(callback(group, line=line))
                break # breaks from the second for loop, so it doesn't call the 'no break' else clause

            # No break was called,
            #   meaning nothing could be mapped to a re pattern
            else:
                self.loop.create_task(self.handle_UNKNOWN(None, line))


    def connection_lost(self, exc: Exception | None) -> None:
        if exc is not None:
            print(exc)

        if not self.bot_event_future.done():
            self.bot_event_future.set_result(BotEvent.RESTART)

    # ------------------------------------------------------------------------------------------------------------------
    # - Line handlers -
    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_ping(self,_:re.Match, *, line):
        """
        Method is called when the Twitch server sends a keep alive PING message
        Needs to have the reply: `"PONG :tmi.twitch.tv` for the connection to remain alive
        """
        print(f"{Fore.Peru('PONG')} | {line}")

        # Need to keep alive
        self.transport.write("PONG :tmi.twitch.tv\r\n".encode())

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_server_message(self, server_message:re.Match, *, line:str):
        """
        Method is called when the Twitch server sends a message that isn't related to any user or room messages
        """
        print(f"{Fore.Blue('SERVER_MESSAGE')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_server_353(self, server_353: re.Match, *, line: str):
        """
        Method is called when twitch sends a 353 message
        """
        print(f"{Fore.AliceBlue('SERVER_353')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_server_366(self, server_366: re.Match, *, line: str):
        """
        Method is called when twitch sends a 353 message
        """
        print(f"{Fore.Ivory('SERVER_366')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_server_cap(self, server_cap: re.Match, *, line: str):
        """
        Method is called when twitch sends a CAP message
        """
        print(f"{Fore.Khaki('SERVER_CAP')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_join(self, join:re.Match,*, line:str):
        """
        Method is called when any user (irc or viewer) joins the channel
        """
        print(f"{Fore.Red('JOIN')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_part(self, part:re.Match, *, line:str):
        """
        Method is called when any user (irc or viewer) parts the channel
        """
        print(f"{Fore.DeepPink('PART')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
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
            bot_event_future=self.bot_event_future,
            original_line=line
        )
        IrcLogger.log_debug(section=SectionIRC.MSG_CONTEXT,
                            data=json.dumps(message_context.as_dict(), cls=GeneralCustomJsonEncoder))

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
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
            bot_event_future=self.bot_event_future,
            original_line=line,
            command=command,
            args=args.strip().split(" ")
        )

        IrcLogger.log_debug(section=SectionIRC.MSG_CONTEXT,
                            data=json.dumps(message_context.as_dict(), cls=GeneralCustomJsonEncoder))

        await self.bot_obj.command_logic.execute_command(
            context=message_context
        )

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_user_notice(self, user_notice:re.Match, *, line:str):
        """
        Method is called when twitch sends a USERNOTICE message
        """
        tags_group_str,user,channel,text = user_notice.groups()
        tags = await TagsUSERNOTICE.import_from_group_as_str(tags_group_str)
        print(f"{Fore.Plum('USERNOTICE')} | {line}")

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_user_notice_raid(self, user_notice_raid:re.Match, *, line:str):
        """
        Method is called when twitch sends a USERNOTICE message
        """
        tags_group_str,channel = user_notice_raid.groups()
        tags = await TagsUSERNOTICE.import_from_group_as_str(tags_group_str)
        print(f"{Fore.Plum('USERNOTICE RAID')} | {line} | {tags}")

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_user_state(self, user_state:re.Match, *, line:str):
        """
        Method is called when twitch sends a USERSTATE message
        """
        tags_group_str,channel = user_state.groups()
        tags = await TagsUSERSTATE.import_from_group_as_str(tags_group_str)
        print(f"{Fore.Plum('USERSTATE')} | {line} | {tags}")

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_UNKNOWN(self, _, line:str):
        """
        Method is called when the protocol can't find an appropriate match for the given string
        """
        print(Fore.SlateGray(f"NOT CAUGHT | {line}"))
        IrcLogger.log_warning(section=SectionIRC.HANDLER_UNKNOWN, data=line)