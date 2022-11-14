# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import inspect

# Athena Packages

# Local Imports
from AthenaTwitchBot.commands import CommandMemory, CommandLogic

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class BotLogic:
    def __new__(cls, *args, **kwargs) -> BotLogic:
        # Actually create the object
        #   Else you can't link the object with the correct functions
        #   This entire section solves the issue of calling functions that were still a part of the class,
        #       and not the instance
        obj:BotLogic = object.__new__(cls)

        for item_name in obj.__dir__():
            # This way we can get all the functions tied to the bot instance,
            #   and not only the `BotLogic` class
            if not callable(coroutine_callback := getattr(obj, item_name)) or not hasattr(coroutine_callback, "_command_logic"):
                continue

            # We need to test if it is a coroutine
            #   If not, raise a big old error but only in debug and not production
            #   In production, this is meant to not fail anymore,
            #       Therefor no check is needed in production (AKA: assert)
            assert inspect.iscoroutinefunction(coroutine_callback), f"The function `{coroutine_callback}` was not a coroutine when the Bot is being assembled"
            cmd_logic:CommandLogic = coroutine_callback._command_logic

            # if no channels are set,
            #   the command can be executed on all channels
            if not cmd_logic.channels:
                CommandMemory.assign_global_cmd(
                    cmd_logic=cmd_logic,
                    coroutine_callback=coroutine_callback
                )
                # Go to next item on the obj.__dir__()
                continue

            # Else, go over all channels
            for channel in cmd_logic.channels:
                CommandMemory.assign_channel_cmd(
                    cmd_logic=cmd_logic,
                    channel=channel,
                    coroutine_callback=coroutine_callback
                )

        # Run the init, as the user might do certain things there
        #   Only useful for the class that inherits from BotLogic
        # noinspection PyArgumentList
        obj.__init__(*args, **kwargs)
        return obj
