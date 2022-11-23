# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
from AthenaTwitchLib.logger._types import TwitchLoggerType
from AthenaTwitchLib.logger.irc import IrcLogger

# ----------------------------------------------------------------------------------------------------------------------
# - Extra simple features -
# ----------------------------------------------------------------------------------------------------------------------
def get_irc_logger() -> IrcLogger:
    """
    Tiny function to get the IRC logger without too much extra syntax
    """
    return IrcLogger.get_logger(TwitchLoggerType.IRC)