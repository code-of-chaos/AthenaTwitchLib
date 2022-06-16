# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.wrapper_helpers.scheduled_task import ScheduledTask

from AthenaLib.models.time import Second, Minute, Hour
from AthenaLib.functions.time import convert_time_to_seconds

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def scheduled_task_method(*,delay:int|Second|Minute|Hour=3600,wait_before:bool=True): # default is every hour
    """
    Create a method that runs every couple of seconds.
    The delay parameter is defined in seconds
    :param wait_before:
    :param delay:
    :return:
    """

    def decorator(fnc):
        def wrapper(*args, **kwargs):
            return fnc(*args, **kwargs)

        # store attributes for later use by the bot
        #   to be used by the protocol to assign it top an async call loop
        wrapper.is_task = True # typo caught by NoirPi
        wrapper.tsk = ScheduledTask(
            delay=convert_time_to_seconds(delay,to_int=True),
            wait_before=wait_before,
            callback=wrapper
        )
        return wrapper
    return decorator