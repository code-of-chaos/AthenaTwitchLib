# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
from AthenaTwitchLib.logger._custom_logger import CustomLogger as _CustomLogger
from AthenaTwitchLib.logger.sections import IrcSections, APISections
import logging as _logging

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
IrcLogger = _CustomLogger(
    logger=_logging.getLogger('IrcLogger'),
    log_to_file=True,
    log_filename="irc.log"
)
IrcLogger.logger.setLevel(_logging.DEBUG)

ApiLogger = _CustomLogger(
    logger=_logging.getLogger('ApiLogger'),
    log_to_file=True,
    log_filename="api.log"
)
ApiLogger.logger.setLevel(_logging.DEBUG)