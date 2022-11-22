# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import asyncio

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.logic import CommandLogic
from AthenaTwitchLib.string_formatting import twitch_irc_output_format
from AthenaTwitchLib.logger import IrcLogger, TwitchLoggerType

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class Bot:
    """
    Base bot class for the connection
    """
    name:str
    oath_token:str
    join_channel:list[str] = field(default_factory=list)
    join_message:str = None
    prefix:str = "!"

    capability_tags:bool=True,
    capability_commands:bool=False,
    capability_membership:bool=False,

    # KW only
    command_logic:CommandLogic = field(kw_only=True, default_factory=CommandLogic)

    # non init
    transport:asyncio.BaseTransport|asyncio.Transport = field(init=False)
    logger:IrcLogger = field(init=False, default_factory=lambda:IrcLogger.get_logger(TwitchLoggerType.IRC))

    async def login(self):
        """
        Steps that need to be taken for the Bot to be logged into the Twitch IRC chat
        """
        # Login into the irc chat
        #   Not handled by the protocol,
        #   as it is a direct write only feature and doesn't need to respond to anything
        self.transport.write(twitch_irc_output_format(f"PASS oauth:{self.oath_token}"))
        self.transport.write(twitch_irc_output_format(f"NICK {self.name}"))
        for channel in self.join_channel:
            self.transport.write(twitch_irc_output_format(f"JOIN #{channel}"))

        # Request correct capabilities
        if self.capability_tags:  # this should always be requested, else answering to chat is not possible
            self.transport.write(twitch_irc_output_format(f"CAP REQ :twitch.tv/tags"))
        if self.capability_commands:
            self.transport.write(twitch_irc_output_format(f"CAP REQ :twitch.tv/commands"))
        if self.capability_membership:
            self.transport.write(twitch_irc_output_format(f"CAP REQ :twitch.tv/membership"))

        # will catch all those that are Truthy (not: "", None, False, ...)
        if self.join_message:
            for channel in self.join_channel:
                self.transport.write(twitch_irc_output_format(f"PRIVMSG #{channel} :{self.join_message}"))

