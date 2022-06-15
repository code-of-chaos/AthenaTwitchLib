# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def frequent_output_method(delay:int=3600): # default is every hour
    """
    Create a method that runs every couple of seconds.
    The delay parameter is defined in seconds
    :param delay:
    :return:
    """

    def decorator(fnc):
        def wrapper(*args, **kwargs):
            return fnc(*args, **kwargs)

        # store attributes for later use by the bot
        #   to be used by the protocol to assign it top an async call loop
        wrapper.is_frequent_output = True # typo caught by NoirPi
        wrapper.delay = delay
        return wrapper
    return decorator