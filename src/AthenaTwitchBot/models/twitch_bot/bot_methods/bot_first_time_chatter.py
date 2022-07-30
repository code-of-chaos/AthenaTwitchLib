# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import ClassVar

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_method_inheritance.callback import BotMethodCallback
from AthenaTwitchBot.functions.athena_dataclass import _dataclass

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@_dataclass(slots=True)
class BotFirstTimeChatter(BotMethodCallback):
    """
    A function the bot does when a viewer joins the chat for the first time ever.
    If a user wants to register a command to the bot, they should make a method in class which inherits from TwitchBot,
        Like the following example:

    ```python
    class CustomBot(TwitchBot):
        @BotFirstTimeChatter.register()
        async def command_test(self, context:MessageContext):
            context.reply("thanks for joining the chat")
    ```

    Parameters of the BotFirstTimeChatter.register decorator:
    - channel : list of TwitchChannel values which defines on which channels this command should be enabled.
        If left unassigned it will work on all channels the bot is joined on
    """
    registered: ClassVar[BotFirstTimeChatter] = None

    @classmethod
    def register(
            cls,
            *,
            args:bool=False
    ):
        """Registers the function to the class"""
        # Only allow one registered command for this type
        if cls.registered is not None:
            raise ValueError("Only one First-Time-Chatter command can be allowed at the same time")

        # allows the usage as a decorator
        #   Doesn't behave like a regular decorator because we aren't storing a "wrapper" which handles args and kwargs
        #   Args and kwargs of the function are handled by the handle_chat_message function
        #   It is expected that the function is located within the defined TwitchBot of the application
        def decorator(fnc):
            cls.registered = cls(
                callback=fnc,
                args=args
            )
        return decorator