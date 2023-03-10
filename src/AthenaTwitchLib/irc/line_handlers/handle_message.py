# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import asyncio
import re
import json

# Athena Packages
from AthenaColor import ForeNest as Fore
from AthenaLib.general.json import GeneralCustomJsonEncoder

# Local Imports
from AthenaTwitchLib.irc.irc_line_handler import IrcLineHandler
import AthenaTwitchLib.irc.data.regex as RegexPatterns
from AthenaTwitchLib.irc.message_context import MessageContext
from AthenaTwitchLib.irc.tags import TagsPRIVMSG
from AthenaTwitchLib.logger import SectionIRC, IrcLogger
from AthenaTwitchLib.irc.bot_data import BotData

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class LineHandler_Message(IrcLineHandler):
    """
    Class is called when any user (irc or viewer) sends a regular message in the channel
    """
    conn_event: asyncio.Future
    bot_data: BotData

    async def _output_on_ingest_console(self, matched_content: re.Match, original_line: str):
        print(f"{Fore.Orchid('MESSAGE')} | {original_line}")

    async def _output_on_ingest_logger(self, matched_content: re.Match, original_line: str):
        ...

    async def _handle_line(self, transport:asyncio.Transport, matched_content: re.Match, original_line: str):
        # Extract data from matched message
        #   Easily done due to regex groups
        tags_group_str, user, channel, possible_command, possible_args = matched_content.groups()

        # Create the context and run more checks
        message_context = MessageContext(
            tags=await TagsPRIVMSG.import_from_group_as_str(tags_group_str),
            user=user,
            username=RegexPatterns.username.findall(user)[0],
            channel=channel,
            possible_command=possible_command,
            possible_args=possible_args,
            original_line=original_line
        )
        IrcLogger.log_debug(
            section=SectionIRC.MSG_CONTEXT,
            data=json.dumps(message_context.as_dict(), cls=GeneralCustomJsonEncoder))
