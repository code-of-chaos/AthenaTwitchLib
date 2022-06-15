# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.wrapper_helpers.scheduled_task import ScheduledTask

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def scheduled_task_method(*,delay:int=3600,before:bool=True): # default is every hour
    """
    Create a method that runs every couple of seconds.
    The delay parameter is defined in seconds
    :param before:
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
            delay=delay,
            before=before,
            callback=wrapper
        )
        return wrapper
    return decorator