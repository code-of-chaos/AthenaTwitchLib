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
    ssl_enabled: bool = True
    host: str = 'irc.chat.twitch.tv'
    port: int = 6667
    port_ssl: int = 6697

    connect_attempts:int=5

    conn_protocol: type[IrcConnectionProtocol] = IrcConnectionProtocol

    logic_commands:BaseCommandLogic = field(default_factory=CommandLogic)
    logic_tasks:TaskLogic = field(default_factory=TaskLogic)

    # Non init
    _current_restart_attempt:int=field(init=False, default=0)
    _loop: asyncio.AbstractEventLoop = field(init=False, default_factory=asyncio.get_running_loop)

    # ------------------------------------------------------------------------------------------------------------------
    # - Support methods -
    # ------------------------------------------------------------------------------------------------------------------
    async def _create_connection(self, bot_data:BotData) -> tuple[asyncio.Future, asyncio.BaseTransport,IrcConnectionProtocol]:
        # Creates the socket
        sock:socket.socket = socket.socket()
        sock.settimeout(5.)
        sock.connect((
            self.host,
            self.port_ssl if self.ssl_enabled else self.port)
        )

        # Creates the connection's event tied to the connection
        conn_event = self._loop.create_future()

        # Assemble the asyncio.Protocol
        #   The custom protocol_type needs a constructor to known which patterns to use, settings, etc...
        transport, protocol_obj = await self._loop.create_connection(
            protocol_factory=functools.partial(
                self.conn_protocol,

                # Assign the logic
                #   If this isn't defined, the protocol can't handle anything correctly
                bot_data=bot_data,
                logic_commands=self.logic_commands,

                # For restarts, exits and other special events
                #   The functions following out of this require the connection class for some things
                conn_event=conn_event
            ),
            server_hostname=self.host,
            ssl=self.ssl_enabled,
            sock=sock,
        )

        # Once everything is established, we can return the result
        return conn_event, transport, protocol_obj

    # ------------------------------------------------------------------------------------------------------------------
    # - Main Methods -
    # ------------------------------------------------------------------------------------------------------------------
    async def connect(self, bot_data:BotData) -> None:
        """
        Constructor function for the BotData and all its logical systems like the asyncio.Protocol handler.
        It also logs the irc in onto the Twitch IRC server
        """
        while True:
            for _ in range(self.connect_attempts):
                conn_event, transport, protocol_obj = await self._create_connection(bot_data=bot_data)
                if transport:
                    IrcLogger.log_debug(section=SectionIRC.CONNECTION_MADE)
                    break

            # Break did not occur,
            #   meaning no connection was established
            else:
                IrcLogger.log_error(section=SectionIRC.CONNECTION_REFUSED)
                raise ConnectionError

            # noinspection PyTypeChecker
            self.logic_tasks.start_all_tasks(transport, self._loop)

            # Waiting portion of the IrcConnection,
            #   This regulates the irc starting back up and restarting
            match await conn_event:
                case ConnectionEvent.RESTART:
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
                    continue

                case ConnectionEvent.EXIT | _:
                    IrcLogger.log_warning(section=SectionIRC.CONNECTION_EXIT, data=f"called by ConnectionEvent")
                    self.logic_tasks.stop_all_tasks()
                    break