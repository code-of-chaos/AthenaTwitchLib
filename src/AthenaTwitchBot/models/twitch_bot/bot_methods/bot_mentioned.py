# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
import datetime

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_method_inheritance.rate_limit import BotMethodRateLimit

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotMentioned(BotMethodRateLimit):
    """
    A function the bot does when a chatter mentions the bot anywhere in its text.
    If a user wants to register a command to the bot, they should make a method in class which inherits from TwitchBot,
        Like the following example:

    ```python
    class CustomBot(TwitchBot):
        @BotMentioned.register()
        async def command_test(self, context:MessageContext):
            context.reply("thanks for joining the chat")
    ```

    Parameters of the BotMentioned.register decorator:
    - channel : list of TwitchChannel values which defines on which channels this command should be enabled.
        If left unassigned it will work on all channels the bot is joined on
    """
    registered:ClassVar[BotMentioned]=None

    @classmethod
    def register(
            cls,
            *,
            rate_limit:datetime.timedelta=None,args:bool=False
    ):
        """Registers the function to the class"""
        # Only allow one registered command for this type
        if cls.registered is not None:
            raise ValueError("Only one Mentioned Bot command can be allowed at the same time")

        # allows the usage as a decorator
        #   Doesn't behave like a regular decorator because we aren't storing a "wrapper" which handles args and kwargs
        #   Args and kwargs of the function are handled by the handle_chat_message function
        #   It is expected that the function is located within the defined TwitchBot of the application
        def decorator(fnc):
            cls.registered = cls(
                callback=fnc,
                rate_limit=rate_limit,
                args=args
            )

        return decorator