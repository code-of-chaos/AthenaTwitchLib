# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import enum
from typing import Callable

# Athena Packages
from AthenaColor import ForeNest

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Section for Twitch IRC -
# ----------------------------------------------------------------------------------------------------------------------
class IrcSections(enum.Enum):
    """
    An Enum where the section is tied to the color which it will be printed as
    """
    BACKEND = "BACKEND", ForeNest.White
    CLEARCHAT = "CLEARCHAT", ForeNest.White
    CLEARMSG = "CLEARMSG", ForeNest.White
    FRONTEND = "FRONTEND", ForeNest.White
    GLOBALUSERSTATE = "GLOBALUSERSTATE", ForeNest.White
    JOIN = "JOIN", ForeNest.White
    NOTICE = "NOTICE", ForeNest.White
    PART = "PART", ForeNest.White
    PING = "PING", ForeNest.White
    PRIVMSG = "PRIVMSG", ForeNest.White
    ROOMSTATE = "ROOMSTATE", ForeNest.White
    SERVER_353 = "SERVER_353", ForeNest.White
    SERVER_366 = "SERVER_366", ForeNest.White
    SERVER_CAP = "SERVER_CAP", ForeNest.White
    SERVER_MESSAGE = "SERVER_MESSAGE", ForeNest.White
    USERNOTICE = "USERNOTICE", ForeNest.White
    USERSTATE = "USERSTATE", ForeNest.White
    WHISPER = "WHISPER", ForeNest.White

    HANDLER_CALLED = "HANDLER_CALLED", ForeNest.White
    HANDLER_UNKNOWN = "HANDLER_UNKNOWN", ForeNest.White
    MSG_ORIGINAL = "MSG_ORIGINAL", ForeNest.White
    MSG_CONTEXT = "MSG_CONTEXT", ForeNest.White
    MSG_TAGS = "MSG_TAGS", ForeNest.White
    MSG_TAGS_UNKNOWN = "MSG_TAGS_UNKNOWN", ForeNest.White
    CONNECTION_ATTEMPT = "CONNECTION_ATTEMPT", ForeNest.White
    CONNECTION_REFUSED = "CONNECTION_REFUSED", ForeNest.White
    CONNECTION_MADE = "CONNECTION_MADE", ForeNest.White
    CONNECTION_RESTART = "CONNECTION_RESTART", ForeNest.White
    CONNECTION_EXIT = "CONNECTION_EXIT", ForeNest.White
    CONNECTION_END = "CONNECTION_END", ForeNest.White
    LOGIN = "LOGIN", ForeNest.White
    LOGIN_MSG = "LOGIN_MSG", ForeNest.White
    LOGIN_CAPABILITY = "LOGIN_CAPABILITY", ForeNest.White
    CMD_DATA = "CMD_DATA", ForeNest.White
    CMD_UNKNOWN = "CMD_UNKNOWN", ForeNest.White
    CMD_NOT_PARSABLE = "CMD_NOT_PARSABLE", ForeNest.White

    # ------------------------------------------------------------------------------------------------------------------
    UNKNOWN = "UNKNOWN", ForeNest.White
    def __str__(self) -> str:
        return self.value[0]

    @property
    def color(self) -> Callable:
        return self.value[1]


# ----------------------------------------------------------------------------------------------------------------------
# - Section for Twitch API -
# ----------------------------------------------------------------------------------------------------------------------
class APISections(enum.Enum):
    """
    Enum which holds all possible section types for the ApiLogger
    """

    USER_DATA = "USER_DATA", ForeNest.White
    TOKEN_DATA = "TOKEN_DATA", ForeNest.White
    TOKEN_INVALID = "TOKEN_INVALID", ForeNest.White
    REQUEST_SEND = "REQUEST_SEND", ForeNest.White
    REQUEST_RESULT = "REQUEST_RESULT", ForeNest.White

    # ------------------------------------------------------------------------------------------------------------------
    UNKNOWN = "UNKNOWN", ForeNest.White
    def __str__(self) -> str:
        return self.value[0]

    @property
    def color(self) -> Callable:
        return self.value[1]

