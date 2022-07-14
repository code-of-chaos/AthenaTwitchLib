# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_method_inheritance.callback import BotMethodCallback

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotCustomReward(BotMethodCallback):
    """
    A function the bot does when a user redeems a reward which has a special message added to it.
    If a user wants to register a command to the bot, they should make a method in class which inherits from TwitchBot,
        Like the following example:

    ```python
    class CustomBot(TwitchBot):
        @BotCustomReward.register(custom_reward_id=...)
        async def command_test(self, context:MessageContext):
            context.reply("thanks for redeeming")
    ```

    Parameters of the BotCustomReward.register decorator:
    - custom_reward_id : the unique id Twitch assigns to the custom reward.
        The command needs this value to define on which eedeem it should trigger the callback
    - args : Boolean option to allow the remaining chat words after the command to be used in the `args` argument
    """
    custom_reward_id:str=None
    registered:ClassVar[dict[str,BotCustomReward]]=None

    @classmethod
    def register(
            cls,custom_reward_id:str,
            *,
            args:bool=False
    ):
        """Registers the function to the class"""
        # make sure the register exists
        if cls.registered is None:
            cls.registered = {}

        # make sure we don't overwrite an already defined command with the same name
        if custom_reward_id in cls.registered:
            raise ValueError(f"A BotCustomReward with the custom_reward_id of '{custom_reward_id}' already exists")

        # allows the usage as a decorator
        #   Doesn't behave like a regular decorator because we aren't storing a "wrapper" which handles args and kwargs
        #   Args and kwargs of the function are handled by the handle_chat_message function
        #   It is expected that the function is located within the defined TwitchBot of the application
        def decorator(fnc):
            cls.registered[custom_reward_id] = cls(
                custom_reward_id=custom_reward_id,
                callback=fnc,
                args=args
            )
        return decorator