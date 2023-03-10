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
from AthenaTwitchLib.irc.logic import TaskLogic
from AthenaTwitchLib.irc.data.exceptions import ConnectionEventUnknown
from AthenaTwitchLib.irc.irc_line_handler_sequence import IrcLineHandlerSequence

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

    bot_data: BotData

    ssl_enabled: bool = True
    host: str = 'irc.chat.twitch.tv'
    port: int = 6667
    port_ssl: int = 6697

    connect_attempts:int=5

    conn_protocol: type[IrcConnectionProtocol] = IrcConnectionProtocol
    line_handler_sequence : IrcLineHandlerSequence = field(default_factory=lambda : IrcLineHandlerSequence())

    logic_tasks:TaskLogic = field(default_factory=TaskLogic)

    # Non init
    _restartable:bool = True
    _loop: asyncio.AbstractEventLoop = field(init=False, default_factory=asyncio.get_running_loop)
    _connection_attempts:int = field(init=False, default=0)

    # ------------------------------------------------------------------------------------------------------------------
    # - Support methods -
    # ------------------------------------------------------------------------------------------------------------------
    async def _connection_create(self) -> tuple[asyncio.Future, asyncio.BaseTransport]:
        """
        Coroutine to attempt a connection to the Twitch IRC chat
        """

        # Log and output to console
        IrcLogger.log_debug(section=SectionIRC.CONNECTION_ATTEMPT, data=self._connection_attempts)
        print(f"{'-' * 25}NEW CONNECTION ATTEMPT {self._connection_attempts} {'-' * 25}")

        for _ in range(self.connect_attempts):
            # Creates the socket
            #   Need to do this every single time for an attempt
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

                    # create the mapping for each pattern to the correct callback
                    line_handler_sequence=self.line_handler_sequence,
                    # Assign the logic
                    #   If this isn't defined, the protocol can't handle anything correctly
                    bot_data=self.bot_data,

                    # For restarts, exits and other special events
                    #   The functions following out of this require the connection class for some things
                    conn_event=conn_event

                ),
                server_hostname=self.host,
                ssl=self.ssl_enabled,
                sock=sock,
            )

            # Something went wrong in the setup that caused a restart
            if transport is None:
                continue

            # Natural end of attempts
            break

        else:
            # Break did not occur,
            #   meaning no connection was established
            IrcLogger.log_error(section=SectionIRC.CONNECTION_REFUSED)
            raise ConnectionError

        # Once everything is established, we can return the result
        IrcLogger.log_debug(section=SectionIRC.CONNECTION_MADE)
        return conn_event, transport

    async def _connection_event_handler(self, conn_event: asyncio.Future) -> None:
        """
        Coroutine to await the asyncio.Future which governs a connection break event.
        Appropriately handles the event.
        """
        match await conn_event:
            case ConnectionEvent.RESTART:
                IrcLogger.log_warning(
                    section=SectionIRC.CONNECTION_RESTART,
                    data=f"called by ConnectionEvent with data: {str(conn_event)}"
                )
                self._restartable = True # makes sure we restart

            case ConnectionEvent.EXIT :
                IrcLogger.log_warning(
                    section=SectionIRC.CONNECTION_EXIT,
                    data=f"called by ConnectionEvent with data: {str(conn_event)}"
                )
                self._restartable = False # makes sure we exit

            case _:
                raise ConnectionEventUnknown

    # ------------------------------------------------------------------------------------------------------------------
    # - Main Methods -
    # ------------------------------------------------------------------------------------------------------------------
    async def connect(self) -> None:
        """
        Constructor function for the BotData and all its logical systems like the asyncio.Protocol handler.
        It also logs the irc in onto the Twitch IRC server
        """
        conn_event:asyncio.Future
        transport:asyncio.Transport|None = None

        # -*- Main body of connection loop -*-
        try:
            # As long as we can restart,
            #   The following while loop should keep running in the same way
            while self._restartable:
                # Sets up the connection and creates the protocol
                conn_event, transport = await self._connection_create()

                # Launch all repeating tasks
                #   noinspection PyTypeChecker
                self.logic_tasks.start_all_tasks(transport, self._loop)

                # Waiting portion of the IrcConnection,
                #   This regulates the irc starting back up and restarting
                await self._connection_event_handler(conn_event=conn_event)

                # If the connection can be reset
                #   Restart
                if self._restartable:
                    # Clear previous tasks
                    self.logic_tasks.stop_all_tasks()

                    # Close the transport,
                    #   Else it will stay open forever
                    transport.close()

                    self._connection_attempts += 1
                    print(f"{NEW_LINE * 25}")
                    continue

        # -*- Exception handlers -*-
        except TimeoutError:
            raise

        except ConnectionRefusedError:
            raise

        except ConnectionError:
            raise

        except ConnectionEventUnknown:
            raise

        # -*- Natural end -*-
        finally:
            IrcLogger.log_warning(
                section=SectionIRC.CONNECTION_END,
                data=f"Connection came to its natural end"
            )

            # Some cleanup
            if transport is not None and not transport.is_closing():
                transport.close()
            self.logic_tasks.stop_all_tasks()
