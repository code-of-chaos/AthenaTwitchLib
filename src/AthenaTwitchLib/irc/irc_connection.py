# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import asyncio
import functools
import socket

# Athena Packages
from AthenaLib.constants.text import NEW_LINE

# Local Imports
from AthenaTwitchLib.irc.bot_data import BotData
from AthenaTwitchLib.irc.data.enums import ConnectionEvent
from AthenaTwitchLib.irc.irc_connection_protocol import IrcConnectionProtocol
from AthenaTwitchLib.logger import SectionIRC, IrcLogger
from AthenaTwitchLib.string_formatting import twitch_irc_output_format
from AthenaTwitchLib.irc.logic import CommandLogic, TaskLogic, BaseCommandLogic

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class IrcConnection:
    """
    Class that constructs the IRC connection which governs how the connection to Twitch is made.
    Relies on BotData to control the access to the Twitch IRC chat
    Relies on logic_commands and logic_tasks for the connection to be populated with custom functionality
    """
    bot_data:BotData

    ssl_enabled: bool = True
    host: str = 'irc.chat.twitch.tv'
    port: int = 6667
    port_ssl: int = 6697

    restart_attempts:int=5 # if set to -1, will run forever

    conn_event: asyncio.Future = None
    conn_protocol: type[IrcConnectionProtocol] = IrcConnectionProtocol

    logic_commands:BaseCommandLogic = field(default_factory=CommandLogic)
    logic_tasks:TaskLogic = field(default_factory=TaskLogic)

    # Non init
    _current_restart_attempt:int=field(init=False, default=0)
    _loop: asyncio.AbstractEventLoop = field(init=False, default_factory=asyncio.get_running_loop)

    def __post_init__(self):
        if self.conn_event is None:
            self.conn_event = self._loop.create_future()

    # ------------------------------------------------------------------------------------------------------------------
    # - Support methods -
    # ------------------------------------------------------------------------------------------------------------------
    def _socket_factory(self) -> socket.socket:
        """
        Simple method that creates the required socket for the asyncio.Protocol factory
        """
        sock:socket.socket = socket.socket()
        sock.settimeout(5.)
        sock.connect((
            self.host,
            self.port_ssl if self.ssl_enabled else self.port
        ))
        return sock

    # ------------------------------------------------------------------------------------------------------------------
    # - Main Methods -
    # ------------------------------------------------------------------------------------------------------------------
    async def connect(self):
        """
        Constructor function for the BotData and all its logical systems like the asyncio.Protocol handler.
        It also logs the irc in onto the Twitch IRC server
        """
        while self.restart_attempts != 0:

            # Assemble the asyncio.Protocol
            #   The custom protocol_type needs a constructor to known which patterns to use, settings, etc...
            transport, protocol_obj = await self._loop.create_connection( # type: asyncio.BaseTransport, object
                protocol_factory=functools.partial(
                    self.conn_protocol,

                    # Assign the logic
                    #   If this isn't defined, the protocol can't handle anything correctly
                    bot_data=self.bot_data,
                    logic_commands=self.logic_commands,

                    # For restarts, exits and other special events
                    #   The functions following out of this require the connection class for some things
                    conn_event=self.conn_event
                ),
                server_hostname=self.host,
                ssl=self.ssl_enabled,
                sock=self._socket_factory()
            )
            if transport is None:
                IrcLogger.log_error(section=SectionIRC.CONNECTION_REFUSED)
                raise ConnectionRefusedError
            else:
                IrcLogger.log_debug(section=SectionIRC.CONNECTION_MADE)

            # Give the protocol the transporter,
            #   so it can easily create write calls to the connection
            protocol_obj.transport = transport

            # Log the irc in on the IRC server
            self.login_bot(transport=transport)

            # noinspection PyTypeChecker
            self.logic_tasks.start_all_tasks(transport, self._loop)

            # Waiting portion of the IrcConnection,
            #   This regulates the irc starting back up and restarting
            match await self.conn_event:
                case ConnectionEvent.RESTART:
                    self._current_restart_attempt +=1
                    print(f"{NEW_LINE*25}{'-'*25}RESTART ATTEMPT {self._current_restart_attempt}{'-'*25}")
                    IrcLogger.log_warning(section=SectionIRC.CONNECTION_RESTART,
                                          data=f"attempt={self._current_restart_attempt}")

                    # Close the transport,
                    #   Else it will stay open forever
                    transport.close()

                    # just wait a set interval,
                    #   to make sure we aren't seen as a ddos
                    await asyncio.sleep(0.5)

                    # Clear previous tasks
                    self.logic_tasks.stop_all_tasks()

                    # restarts it all
                    self.restart_attempts -= 1
                    continue

                case ConnectionEvent.EXIT | _:
                    IrcLogger.log_warning(section=SectionIRC.CONNECTION_EXIT, data=f"called by ConnectionEvent")
                    self.logic_tasks.stop_all_tasks()
                    self._loop.stop()
                    break

    def login_bot(self, transport: asyncio.Transport|asyncio.BaseTransport):
        """
        Steps that need to be taken for the BotData to be logged into the Twitch IRC chat
        """
        # Login into the irc chat
        #   Not handled by the protocol,
        #   as it is a direct write only feature and doesn't need to respond to anything
        transport.write(twitch_irc_output_format(f"PASS oauth:{self.bot_data.oath_token}"))
        transport.write(twitch_irc_output_format(f"NICK {self.bot_data.name}"))

        IrcLogger.log_debug(
            section=SectionIRC.LOGIN,
            data=f"[{self.bot_data.name=}, {self.bot_data.join_channel=}, {self.bot_data.join_message=}, {self.bot_data.prefix=}]"
        )

        # Join all channels and don't wait for the logger to finish
        for channel in self.bot_data.join_channel:
            transport.write(twitch_irc_output_format(f"JOIN #{channel}"))

        # Request correct capabilities
        if self.bot_data.capability_tags:
            transport.write(twitch_irc_output_format("CAP REQ :twitch.tv/tags"))
        if self.bot_data.capability_commands:
            transport.write(twitch_irc_output_format("CAP REQ :twitch.tv/commands"))
        if self.bot_data.capability_membership:
            transport.write(twitch_irc_output_format("CAP REQ :twitch.tv/membership"))

        IrcLogger.log_debug(
            section=SectionIRC.LOGIN_CAPABILITY,
            data=f"tags={self.bot_data.capability_tags};commands={self.bot_data.capability_commands};membership{self.bot_data.capability_membership}"
        )

        # will catch all those that are Truthy (not: "", None, False, ...)
        if self.bot_data.join_message:
            for channel in self.bot_data.join_channel:
                transport.write(twitch_irc_output_format(f"PRIVMSG #{channel} :{self.bot_data.join_message}"))

            IrcLogger.log_debug(section=SectionIRC.LOGIN_MSG, data=f"Sent Join Message : {self.bot_data.join_message}")
