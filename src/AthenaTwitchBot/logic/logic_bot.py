# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import inspect
from typing import ClassVar, Coroutine, Type, Callable

# Athena Packages

# Local Imports
from AthenaTwitchBot.logic.logic_memory import LogicMemory
from AthenaTwitchBot.logic.logic_types import MessageLogic, CommandLogic, LogicTypes

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class LogicBot:
    default_channel:ClassVar[str]

    # noinspection PyProtectedMember
    def __new__(cls, *args, **kwargs) -> LogicBot:
        # Actually create the object
        #   Else you can't link the object with the correct functions
        #   This entire section solves the issue of calling functions that were still a part of the class,
        #       and not the instance
        obj:LogicBot = object.__new__(cls)

        for item_name in obj.__dir__():
            # This way we can get all the functions tied to the bot instance,
            #   and not only the `LogicBot` class
            if not callable(coroutine := getattr(obj, item_name)) or not hasattr(coroutine, "_type"):
                continue

            # Check for which type it is
            match coroutine._type:
                # Coroutine is a callback for a command
                case LogicTypes.COMMAND:
                    cls._assign_logic(
                        coroutine=coroutine,
                        logic_cls=CommandLogic,
                        mem_assign_call=LogicMemory.assign_as_command
                    )

                 # Coroutine is a callback for handling all user messages
                case LogicTypes.MESSAGE:
                    cls._assign_logic(
                        coroutine=coroutine,
                        logic_cls=MessageLogic,
                        mem_assign_call=LogicMemory.assign_as_normal_message
                    )
                case _:
                    raise TypeError(f"{coroutine._type} not found in LogicBot")

        # Run the init, as the user might do certain things there
        #   Only useful for the class that inherits from LogicBot
        # noinspection PyArgumentList
        obj.__init__(*args, **kwargs)
        return obj

    @classmethod
    def _assign_logic(cls, coroutine: Coroutine, logic_cls: Type[MessageLogic], mem_assign_call: Callable):
        # We need to test if it is a coroutine
        #   If not, raise a big old error but only in debug and not production
        #   In production, this is meant to not fail anymore,
        #       Therefor no check is needed in production (AKA: assert)
        assert inspect.iscoroutinefunction(coroutine), f"The function `{coroutine}` was not a coroutine when the Bot is being assembled"

        # noinspection PyProtectedMember,PyArgumentList
        logic: MessageLogic = logic_cls(
            coroutine=coroutine,
            **coroutine._kwargs,
        )

        # if no channels are set,
        #   the command can be executed on all channels
        if not logic.channels:
            mem_assign_call(logic=logic, channel=cls.default_channel)
            # Go to next item on the obj.__dir__()

        # Else, go over all channels
        for channel in logic.channels:
            mem_assign_call(logic=logic, channel=channel)

