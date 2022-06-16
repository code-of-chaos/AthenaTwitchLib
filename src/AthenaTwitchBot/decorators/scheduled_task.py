# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaLib.models.time import Second, Minute, Hour
from AthenaLib.functions.time import convert_time_to_seconds

# Custom Packages
from AthenaTwitchBot.models.wrapper_helpers.scheduled_task import ScheduledTask
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

from AthenaTwitchBot.data.unions import CHANNEL, CHANNELS


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def scheduled_task_method(*, delay:int|Second|Minute|Hour=3600, wait_before:bool=True, channel:CHANNEL|CHANNELS=None): # default is every hour
    """
    Create a method that runs every couple of seconds.
    The delay parameter is defined in seconds
    :param channel:
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

        # cast channel to the correct format to be used by ScheduledTask
        channels:list[TwitchChannel] = []
        if isinstance(channel, str):
            channels.append(TwitchChannel(channel))
        elif isinstance(channel, TwitchChannel):
            channels.append(channel)
        elif isinstance(channel, list):
            for c in channels:
                if isinstance(channel, str):
                    channels.append(TwitchChannel(channel))
                elif isinstance(channel, TwitchChannel):
                    channels.append(c)
                else:
                    return NotImplemented
        else:
            return NotImplemented

        wrapper.tsk = ScheduledTask(
            delay=convert_time_to_seconds(delay,to_int=True),
            wait_before=wait_before,
            callback=wrapper,
            channels=channels
        )
        return wrapper
    return decorator