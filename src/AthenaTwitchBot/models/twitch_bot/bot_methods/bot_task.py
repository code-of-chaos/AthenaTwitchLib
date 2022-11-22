# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from collections.abc import Awaitable
from dataclasses import dataclass, field
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import TypeAlias

# Custom Library
from AthenaLib.models.time import TimeValue, Minute

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext
# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
_TBotTaskCallback = Callable[[Any, MessageContext], Awaitable[None]]


@dataclass(slots=True)
class BotTask:
    """
    A function the bot executes every interval. Does not depend on chat input, but is able to write to chat.
    Uses an empty MessageContext to write to the channel that it needs to.
    If a user wants to register a command to the bot, they should make a method in class which inherits from TwitchBot,
        Like the following example:

    ```python
    class CustomBot(TwitchBot):
        @BotTask.register(interval=Minute(10))
        async def command_test(self, context:MessageContext):
            context.reply("thanks for joining the chat")
    ```

    Parameters of the BotMentionedStart.register decorator:
    - interval: An AthenaLib Time_Value class to be used as the interval
    - channel : list of TwitchChannel values which defines on which channels this command should be enabled.
        If left unassigned it will work on all channels the bot is joined on
    """

    callback:_TBotTaskCallback
    interval:TimeValue=field(default_factory=lambda: Minute(10))
    registered:ClassVar[list[BotTask]]=[]

    @classmethod
    def register(cls, *,interval:TimeValue=Minute(10)) -> Callable[[_TBotTaskCallback], None]:
        """Registers the function to the class"""
        # allows the usage as a decorator
        #   Doesn't behave like a regular decorator because we aren't storing a "wrapper" which handles args and kwargs
        #   Args and kwargs of the function are handled by the handle_chat_message function
        #   It is expected that the function is located within the defined TwitchBot of the application
        def decorator(fnc: _TBotTaskCallback) -> None:
            cls.registered.append(
                cls(callback=fnc, interval=interval)
            )
        return decorator
