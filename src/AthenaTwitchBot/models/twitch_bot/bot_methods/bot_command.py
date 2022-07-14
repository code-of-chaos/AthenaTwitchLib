# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, ClassVar

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotCommand:
    """
    A command, always preceded by the TwitchBot.command_prefix.
    Holds the callback to be used when a user calls the command in chat.
    If a user wants to register a command to the bot, they should make a method in class which inherits from TwitchBot,
        Like the following example:

    ```python
    class CustomBot(TwitchBot):
        @BotCommand.register(name="test")
        async def command_test(self, context:MessageContext):
            context.reply("the test was successful")
    ```

    The TwitchBot.command_prefix should not be defined in the `name` argument

    Parameters of the BotCommand.register decorator:
    - args : Boolean option to allow the remaining chat words after the command to be used in the `args` argument
    - subscriber_only : Boolean option to only allow subscribers to use this command (cannot be used with `mod_only`)
    - mod_only : Boolean option to only allow moderators to use this command (cannot be used with `subscriber_only`)
    - channel : list of TwitchChannel values which defines on which channels this command should be enabled.
        If left unassigned it will work on all channels the bot is joined on
    """
    name:str
    callback:Callable
    args:bool
    subscriber_only:bool
    mod_only:bool
    channels:list[TwitchChannel]=None

    registered:ClassVar[dict[str,BotCommand]]=None

    @classmethod
    def register(
            cls, name:str,
            *,
            args:bool=False,subscriber_only:bool=False, mod_only:bool=False):
        """Registers the function to the class"""

        # make sure the register exists
        if cls.registered is None:
            cls.registered = {}

        # only allow commands to be used by one level of roles,
        #   and not by multiple at the same time
        if subscriber_only and mod_only:
            raise ValueError("A command can not be used by both a sub and a mod. Choose one or the other")

        # make sure we don't overwrite an already defined command with the same name
        if name in cls.registered:
            raise ValueError(f"A BotCommand with the name of '{name}' already exists")

        # allows the usage as a decorator
        #   Doesn't behave like a regular decorator because we aren't storing a "wrapper" which handles args and kwargs
        #   Args and kwargs of the function are handled by the handle_chat_message function
        #   It is expected that the function is located within the defined TwitchBot of the application
        def decorator(fnc):
            cls.registered[name] = cls(
                name=name,
                callback=fnc,
                args=args,
                subscriber_only=subscriber_only,
                mod_only=mod_only
            )
        return decorator