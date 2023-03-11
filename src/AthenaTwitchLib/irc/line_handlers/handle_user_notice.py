# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
import re
import dataclasses

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.irc_line_handler import IrcLineHandler
from AthenaTwitchLib.irc.tags import TagsUSERNOTICE
from AthenaTwitchLib.logger import IrcSections


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclasses.dataclass(slots=True)
class LineHandler_UserNotice(IrcLineHandler):
    """
    Class is called when any user (irc or viewer) sends a regular message in the channel
    """
    _section:IrcSections = IrcSections.USERNOTICE

    async def handle_line(self, conn_event:asyncio.Future, transport: asyncio.Transport, matched_content: re.Match,
                          original_line: str):
        # Executes the default output and log when the data is first given.
        await super(LineHandler_UserNotice, self).handle_line(conn_event, transport, matched_content, original_line)

        tags_group_str, user, channel, text = matched_content.groups()
        tags = await TagsUSERNOTICE.import_from_group_as_str(tags_group_str)
