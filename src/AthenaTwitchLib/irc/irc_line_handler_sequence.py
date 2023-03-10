# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterator

# Athena Packages

# Local Imports
from AthenaTwitchLib.irc.irc_line_handler import IrcLineHandler
import AthenaTwitchLib.irc.line_handlers as lh
import AthenaTwitchLib.irc.data.regex as RegexPatterns

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class IrcLineHandlerSequence:
    line_handler_message:IrcLineHandler = field(default_factory=lambda: lh.LineHandler_Message(
        regex_pattern=RegexPatterns.message
    ))
    line_handler_ping:IrcLineHandler = field(default_factory=lambda: lh.LineHandler_Ping(
        regex_pattern=RegexPatterns.server_ping
    ))
    line_handler_server_message:IrcLineHandler = field(default_factory=lambda: lh.LineHandler_ServerMessage(
        regex_pattern=RegexPatterns.server_message
    ))
    line_handler_join:IrcLineHandler =  field(default_factory=lambda: lh.LineHandler_Join(
        regex_pattern=RegexPatterns.join
    ))
    line_handler_part:IrcLineHandler =  field(default_factory=lambda: lh.LineHandler_Part(
        regex_pattern=RegexPatterns.part
    ))
    line_handler_server353:IrcLineHandler =  field(default_factory=lambda: lh.LineHandler_Server353(
        regex_pattern=RegexPatterns.server_353
    ))
    line_handler_server366:IrcLineHandler =  field(default_factory=lambda: lh.LineHandler_Server366(
        regex_pattern=RegexPatterns.server_366
    ))
    line_handler_server_cap:IrcLineHandler =  field(default_factory=lambda: lh.LineHandler_ServerCap(
        regex_pattern=RegexPatterns.server_cap
    ))
    line_handler_user_notice:IrcLineHandler =  field(default_factory=lambda: lh.LineHandler_UserNotice(
        regex_pattern=RegexPatterns.user_notice
    ))
    line_handler_user_state:IrcLineHandler =  field(default_factory=lambda: lh.LineHandler_UserState(
        regex_pattern=RegexPatterns.user_state
    ))
    line_handler_unknown:IrcLineHandler =  field(default_factory=lambda: lh.LineHandler_Unknown(
        regex_pattern=None
    ))

    def __iter__(self) -> Iterator[IrcLineHandler]:
        yield self.line_handler_message
        yield self.line_handler_ping
        yield self.line_handler_server_message
        yield self.line_handler_join
        yield self.line_handler_part
        yield self.line_handler_user_notice
        yield self.line_handler_server353
        yield self.line_handler_server366
        yield self.line_handler_server_cap
        yield self.line_handler_user_state
        # line_handler_unknown IS NOT INCLUDED IN ITER! Called separately
