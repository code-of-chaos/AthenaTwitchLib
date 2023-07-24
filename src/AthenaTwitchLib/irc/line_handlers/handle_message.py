# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
import asyncio
import re
import json

# Athena Packages
from AthenaLib.general.json import GeneralCustomJsonEncoder

# Local Imports
from AthenaTwitchLib.irc.irc_line_handler import IrcLineHandler
import AthenaTwitchLib.irc.data.regex as RegexPatterns
from AthenaTwitchLib.irc.message_context import MessageContext
from AthenaTwitchLib.irc.tags import TagsPRIVMSG
from AthenaTwitchLib.logger import IrcSections, IrcLogger

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class LineHandler_Message(IrcLineHandler):
    """
    Class is called when any user (irc or viewer) sends a regular message in the channel
    """
    _section:str = IrcSections.PRIVMSG

    async def handle_line(self, conn_event:asyncio.Future, transport: asyncio.Transport, matched_content: re.Match,
                          original_line: str):

        # Executes the default output and log when the data is first given.
        await super(LineHandler_Message, self).handle_line(conn_event, transport, matched_content, original_line)

        # Extract data from matched message
        #   Easily done due to regex groups
        tags_group_str, user, channel, possible_command, possible_args = matched_content.groups()

        # Create the context and run more checks
        message_context = MessageContext(
            tags=TagsPRIVMSG.import_from_group_as_str(tags_group_str),
            user=user,
            username=RegexPatterns.username.findall(user)[0],
            channel=channel,
            possible_command=possible_command,
            possible_args=possible_args,
            original_line=original_line
        )
        IrcLogger.debug(
            section=IrcSections.MSG_CONTEXT,
            msg=json.dumps(message_context.as_dict(), cls=GeneralCustomJsonEncoder)
        )
