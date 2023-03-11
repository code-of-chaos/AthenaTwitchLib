# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import asyncio

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.bot_data import BotData
from AthenaTwitchLib.irc.data.enums import ConnectionEvent
from AthenaTwitchLib.irc.irc_line_handler_sequence import IrcLineHandlerSequence
from AthenaTwitchLib.logger import IrcSections, IrcLogger
from AthenaTwitchLib.string_formatting import twitch_irc_output_format
from AthenaTwitchLib.irc.irc_line_handler import IrcLineHandler

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
    line_handler_sequence: IrcLineHandlerSequence

    # Non init
    transport: asyncio.transports.Transport = field(init=False)  # delayed as it has to be set after the connection has been made
    _loop :asyncio.AbstractEventLoop = field(init=False)


    def __post_init__(self):
        self._loop = asyncio.get_running_loop()

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

        self._loop.create_task(IrcLogger.debug(
            section=IrcSections.LOGIN,
            msg=f"[{self.bot_data.name=}, {self.bot_data.join_channel=}, {self.bot_data.join_message=}, {self.bot_data.prefix=}]"
        ))

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

        self._loop.create_task(IrcLogger.debug(
            section=IrcSections.LOGIN_CAPABILITY,
            msg=f"tags={self.bot_data.capability_tags};commands={self.bot_data.capability_commands};membership{self.bot_data.capability_membership}"
        ))

        # will catch all those that are Truthy (not: "", None, False, ...)
        if self.bot_data.join_message:
            for channel in self.bot_data.join_channel:
                self.transport.write(twitch_irc_output_format(f"PRIVMSG #{channel} :{self.bot_data.join_message}"))

            self._loop.create_task(IrcLogger.debug(
                section=IrcSections.LOGIN_MSG,
                msg=f"Sent Join Message : {self.bot_data.join_message}"
            ))

    def data_received(self, data: bytearray) -> None:
        """
        First hit of the protocol when it receives data from Twitch IRC
        Because twitch sends in this data in bytes, and sometimes multiple different message,
        the function has to decode and split the data on every new line
        """

        # Goes over all non-empty lines
        for line in filter(None,data.decode().split("\r\n")):
            for line_handler in self.line_handler_sequence: #type: IrcLineHandler
                if not(matched_content := line_handler.regex_pattern.match(line)):
                    continue
                # A valid match was found
                self._loop.create_task(
                    line_handler.handle_line(
                        conn_event=self.conn_event,
                        transport=self.transport,
                        matched_content=matched_content,
                        original_line=line
                    )
                )
                break

            # if the For loop wasn't broken, meaning no valid regex patterns were validated
            #   Can be done because "line_handler_unknown" is not included in the iter of self.line_handler_sequence
            else:
                self._loop.create_task(
                    self.line_handler_sequence.line_handler_unknown.handle_line(
                        conn_event=self.conn_event,
                        transport=self.transport,
                        matched_content=None,
                        original_line=line
                    )
                )

    def connection_lost(self, exc: Exception | None) -> None:
        if exc is not None:
            print(exc)

        if not self.conn_event.done():
            self.conn_event.set_result(ConnectionEvent.RESTART)