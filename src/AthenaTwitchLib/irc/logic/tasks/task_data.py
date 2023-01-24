# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
import datetime

# Athena Packages

# Local Imports


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class TaskData:
    """
    Simple dataclass to hold basic information about the hard coded task.
    Meant for the `TaskLogic` class to differentiate what to do when it needs to execute the tasks
    """
    at:datetime.timedelta = None
    interval:datetime.timedelta = None
    channel:str = None

    def __post_init__(self):
        if self.at is not None:
            self.interval = self.at