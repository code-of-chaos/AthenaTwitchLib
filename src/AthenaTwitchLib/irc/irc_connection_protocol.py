# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
import re
from dataclasses import dataclass, field
import functools
from typing import Any, Callable
import json

# Athena Packages
from AthenaColor import ForeNest as Fore
from AthenaLib.general.json import GeneralCustomJsonEncoder

# Local Imports
from AthenaTwitchLib.irc.regex import RegexPatterns
from AthenaTwitchLib.irc.tags import TagsPRIVMSG, TagsUSERSTATE
from AthenaTwitchLib.logger import IrcSection, IrcLogger
from AthenaTwitchLib.irc.message_context import MessageContext,MessageCommandContext
from AthenaTwitchLib.irc.data.enums import BotEvent
from AthenaTwitchLib.irc.bot import Bot

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
class _TransportBuffer:
    """
    Simple class to be used by the `IrcConnectionProtocol`, before the transporter object is actually set.
    It keeps the to be sent message into a small buffer, for it to then be parsed and deleted once the
    actual transporter is present in the `IrcConnectionProtocol`
    """
    buffer: list[bytes] = []

    @classmethod
    def write(cls, data:bytes):
        cls.buffer.append(data)

def log_handler(fnc:Callable) -> Any:
    """
    Simple decorator to keep track of how many calls are made to handlers
    """
    @functools.wraps(fnc)
    async def wrapper(*args, **kwargs):
        IrcLogger.log_debug(section=IrcSection.HANDLER_CALLED, text=fnc.__name__),
        IrcLogger.log_debug(section=IrcSection.MSG, text=kwargs.get("line", None)),
        return await fnc(*args, **kwargs)

    return wrapper

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class IrcConnectionProtocol(asyncio.Protocol):
    """
    Asyncio.Protocol child class,
    Holds all logic to convert the incoming Twitch IRC messages to useful calls/data
    """
    regex_patterns: RegexPatterns
    bot_event_future: asyncio.Future
    bot_obj:Bot

    _transport: asyncio.transports.Transport = None  # delayed as it has to be set after the connection has been made
    loop :asyncio.AbstractEventLoop = field(init=False)

    def __post_init__(self):
        self.loop = asyncio.get_running_loop()

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
            return _TransportBuffer

        return self._transport

    @transport.setter
    def transport(self, value:asyncio.transports.Transport):
        """
        Setter of the `transport` property
        Executes any write calls in the buffer, and the deletes the buffer
        """
        self._transport = value

        if _TransportBuffer.buffer:
            for data in _TransportBuffer.buffer:
                self._transport.write(data)

            _TransportBuffer.buffer.clear()

    # ------------------------------------------------------------------------------------------------------------------
    # - Protocol Calls (aka, calls made by asyncio.Protocol) -
    # ------------------------------------------------------------------------------------------------------------------
    def data_received(self, data: bytearray) -> None:
        """
        First hit of the protocol when it receives data from Twitch IRC
        Because twitch sends in this data in bytes, and sometimes multiple different message,
        the function has to decode and split the data on every new line
        """

        # TODO sort on most used messages

        for line in data.decode().split("\r\n"):
            # An Empty line
            if not line:
                continue

            elif message := self.regex_patterns.message.match(line):
                if cmd_match := self.regex_patterns.message_command.match(message.groups()[-1]):
                    self.loop.create_task(self.handle_message_command(message, cmd_match, line=line))
                else:
                    self.loop.create_task(self.handle_message(message, line=line))

            elif line == "PING :tmi.twitch.tv":
                self.loop.create_task(self.handle_ping(line=line))

            elif server_message := self.regex_patterns.server_message.match(line):
                self.loop.create_task(self.handle_server_message(server_message, line=line))

            elif join := self.regex_patterns.join.match(line):
                self.loop.create_task(self.handle_join(join, line=line))

            elif part := self.regex_patterns.part.match(line):
                self.loop.create_task(self.handle_part(part, line=line))

            elif server_353 := self.regex_patterns.server_353.match(line):
                self.loop.create_task(self.handle_server_353(server_353, line=line))

            elif server_366 := self.regex_patterns.server_366.match(line):
                self.loop.create_task(self.handle_server_366(server_366, line=line))

            elif server_cap := self.regex_patterns.server_cap.match(line):
                self.loop.create_task(self.handle_server_cap(server_cap, line=line))

            elif user_notice := self.regex_patterns.user_notice.match(line):
                self.loop.create_task(self.handle_user_notice(user_notice, line=line))

            elif user_state := self.regex_patterns.user_state.match(line):
                self.loop.create_task(self.handle_user_state(user_state, line=line))

            else:
                self.loop.create_task(self.handle_UNKNOWN(line))

    def connection_lost(self, exc: Exception | None) -> None:
        if exc is not None:
            print(exc)

        if not self.bot_event_future.done():
            self.bot_event_future.set_result(BotEvent.RESTART)

    # ------------------------------------------------------------------------------------------------------------------
    # - Line handlers -
    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_ping(self,*, line):
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
            username=self.regex_patterns.username.findall(user)[0],
            channel=channel,
            text=text,
            transport=self.transport,
            bot_event_future=self.bot_event_future,
            original_line=line
        )
        IrcLogger.log_debug(
            section=IrcSection.MSG_CONTEXT,
            text=json.dumps(message_context.as_dict(), cls=GeneralCustomJsonEncoder)
        )

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_message_command(self, message:re.Match, cmd_match:re.Match, *, line:str):
        """
        Method is called when any user (irc or viewer) sends a message in the channel,
        which is presumed to be an irc command
        """
        print(f"{Fore.Orchid('MESSAGE_COMMAND')} | {message.groups()[-1]} | {Fore.SlateGray(line)}")

        # Extract data from matched message
        #   Easily done due to regex groups
        tags_group_str,user,channel,text = message.groups()
        command, args = cmd_match.groups()

        message_context = MessageCommandContext(
            tags=await TagsPRIVMSG.import_from_group_as_str(tags_group_str),
            user=user,
            username=self.regex_patterns.username.findall(user)[0],
            channel=channel,
            text=f"!{command}",
            transport=self.transport,
            bot_event_future=self.bot_event_future,
            original_line=line,
            command=command,
            args=args.strip().split(" ")
        )

        IrcLogger.log_debug(
            section=IrcSection.MSG_CONTEXT,
            text=json.dumps(message_context.as_dict(), cls=GeneralCustomJsonEncoder)
        )

        await self.bot_obj.command_logic.execute_command(
            context=message_context
        )

    # ------------------------------------------------------------------------------------------------------------------
    @log_handler
    async def handle_user_notice(self, user_notice:re.Match, *, line:str):
        """
        Method is called when twitch sends a USERNOTICE message
        """
        print(f"{Fore.Plum('USERNOTICE')} | {line}")

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
    async def handle_UNKNOWN(self, line:str):
        """
        Method is called when the protocol can't find an appropriate match for the given string
        """
        print(Fore.SlateGray(f"NOT CAUGHT | {line}"))
        IrcLogger.log_warning(
            section=IrcSection.HANDLER_UNKNOWN,
            text=line
        )