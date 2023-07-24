# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dataclasses
import logging
from typing import Callable

# Athena Packages
from AthenaColor import ForeNest

from AthenaTwitchLib.logger.sections import IrcSections, APISections

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
LEVELNAME_TO_COLOR:dict[str, Callable] = {
    "DEBUG":ForeNest.SlateGray,
    "INFO":ForeNest.Green,
    "WARNING":ForeNest.Orange,
    "ERROR":ForeNest.Red,
    "CRITICAL":ForeNest.DarkRed
}

# ----------------------------------------------------------------------------------------------------------------------
@dataclasses.dataclass(slots=True, kw_only=True)
class CustomLogger:
    logger:logging.Logger = dataclasses.field(default_factory=lambda:logging.getLogger('custom_logger'))
    log_format:logging.Formatter = dataclasses.field(default_factory=lambda: logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))

    log_to_file:bool = False
    log_filename:str = 'logger.log'

    def __post_init__(self):
        # Add the handlers for the logging destinations
        if self.log_to_file:
            file_handler = logging.FileHandler(self.log_filename)
            file_handler.setFormatter(self.log_format)
            self.logger.addHandler(file_handler)

    def debug(self, msg:str, **kwargs):
        self.log(level=logging.DEBUG, msg=msg, **kwargs)

    def info(self, msg:str, **kwargs):
        self.log(level=logging.INFO, msg=msg, **kwargs)

    def warning(self, msg:str, **kwargs):
        self.log(level=logging.WARNING, msg=msg, **kwargs)

    def error(self, msg:str, **kwargs):
        self.log(level=logging.ERROR, msg=msg, **kwargs)

    def critical(self, msg:str, **kwargs):
        self.log(level=logging.CRITICAL, msg=msg, **kwargs)

    def log(self,*, level:int, msg:str, section:IrcSections|APISections, **_):
        """
        Log a message with a custom section and level.
        Made into an async method, because eventually this will need to be remade into a logger that also connects to
        the SOL api
        """
        print(
            LEVELNAME_TO_COLOR[levelname := logging.getLevelName(level)](
                levelname.center(8), # Print Levelname
                section.color(str(section).center(24)),  # Print Section name
                msg,  # Print the actual section
                sep=" | "
            )
        )
        self.logger.log(level, f"{str(section)} | {msg}")

