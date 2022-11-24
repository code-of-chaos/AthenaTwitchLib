# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import functools
import socket
import asyncio
from dataclasses import dataclass, field
from typing import Callable

# Athena Packages
from AthenaLib.constants.text import NEW_LINE
# Local Imports
from AthenaTwitchLib.irc.irc_connection_protocol import IrcConnectionProtocol
from AthenaTwitchLib.irc.regex import RegexPatterns
from AthenaTwitchLib.irc.data.enums import BotEvent
from AthenaTwitchLib.irc.bot import Bot
from AthenaTwitchLib.logger import SectionIRC, IrcLogger

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class IrcConnection:
    bot_obj:Bot

    ssl_enabled: bool = True
    irc_host: str = 'irc.chat.twitch.tv'
    irc_port: int = 6667
    irc_port_ssl: int = 6697

    protocol_cls:type[IrcConnectionProtocol]=IrcConnectionProtocol
    restart_attempts:int=5 # if set to -1, will run forever
    current_restart_attempt:int=0

    # Non init
    loop: asyncio.AbstractEventLoop = field(init=False,default_factory=asyncio.get_running_loop)
    bot_event_future: asyncio.Future = field(init=False)

    async def construct(self):
        """
        Constructor function for the Bot and all its logical systems like the asyncio.Protocol handler.
        It also logs the irc in onto the Twitch IRC server
        """
        while self.restart_attempts != 0:

            # Assemble the asyncio.Protocol
            #   The custom protocol_type needs a constructor to known which patterns to use, settings, etc...
            bot_event:asyncio.Future = self.loop.create_future()

            bot_transport, protocol_obj = await self.loop.create_connection( # type: asyncio.BaseTransport, object
                protocol_factory=self._protocol_constructor(bot_event),
                server_hostname=self.irc_host,
                ssl=self.ssl_enabled,
                sock=self._assemble_socket()
            )
            if bot_transport is None:
                IrcLogger.log_error(section=SectionIRC.CONNECTION_REFUSED)
                raise ConnectionRefusedError
            else:
                IrcLogger.log_debug(section=SectionIRC.CONNECTION_MADE)

            # Give the protocol the transporter,
            #   so it can easily create write calls to the connection
            # bot_transport: asyncio.Transport
            protocol_obj.transport = self.bot_obj.transport = bot_transport

            # Log the irc in on the IRC server
            await self.bot_obj.login()

            # noinspection PyTypeChecker
            self.bot_obj.task_logic.start_all_tasks(bot_transport, self.loop)

            # Waiting portion of the IrcConnection,
            #   This regulates the irc starting back up and restarting
            match await bot_event :
                case BotEvent.RESTART:
                    self.current_restart_attempt +=1
                    print(f"{NEW_LINE*25}{'-'*25}RESTART ATTEMPT {self.current_restart_attempt}{'-'*25}")
                    IrcLogger.log_warning(
                        section=SectionIRC.CONNECTION_RESTART,
                        text=f"attempt={self.current_restart_attempt}"
                    )

                    # Close the transport,
                    #   Else it will stay open forever
                    bot_transport.close()

                    # just wait a set interval,
                    #   to make sure we aren't seen as a ddos
                    await asyncio.sleep(0.5)

                    # Clear previous tasks
                    self.bot_obj.task_logic.stop_all_tasks()

                    # restarts it all
                    self.restart_attempts -= 1
                    continue

                case BotEvent.EXIT | _:
                    IrcLogger.log_warning(
                        section=SectionIRC.CONNECTION_EXIT,
                        text=f"called by BotEvent")
                    self.bot_obj.task_logic.stop_all_tasks()
                    self.loop.stop()
                    break

    def _assemble_socket(self) -> socket.socket:
        """
        Simple method that creates the required socket for the asyncio.Protocol factory
        """
        sock = socket.socket()
        sock.settimeout(5.)
        sock.connect(
            (
                self.irc_host,
                self.irc_port_ssl if self.ssl_enabled else self.irc_port
            )
        )
        return sock

    def _protocol_constructor(self, bot_event:asyncio.Future) -> Callable:
        """
        Simple construction for the custom asyncio.Protocol class
        Seperated into its own function for better programming common sense
        """
        return functools.partial(
            self.protocol_cls,

            # Creates a new regex pattern
            #   in the event that it's matches must change during a restart
            regex_patterns=RegexPatterns(),

            # Assign the logic
            #   If this isn't defined, the protocol can't handle anything correctly
            bot_obj=self.bot_obj,

            # For restarts, exits and other special events
            bot_event_future=bot_event
        )