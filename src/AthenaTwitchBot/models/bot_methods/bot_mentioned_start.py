# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import  Callable,ClassVar

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotMentionedStart:
    """
    A function the bot does when a chatter mentions at the start of their message.
    If a user wants to register a command to the bot, they should make a method in class which inherits from TwitchBot,
        Like the following example:

    ```python
    class CustomBot(TwitchBot):
        @BotMentionedStart.register()
        async def command_test(self, context:MessageContext):
            context.reply("thanks for joining the chat")
    ```

    Parameters of the BotMentionedStart.register decorator:
    - channel : list of TwitchChannel values which defines on which channels this command should be enabled.
        If left unassigned it will work on all channels the bot is joined on
    """
    callback:Callable
    channel:str|TwitchChannel=None


    registered:ClassVar[BotMentionedStart]=None

    def __post_init__(self):
        if isinstance(self.channel, str):
            self.channel = TwitchChannel(self.channel)

    @classmethod
    def register(cls, *, channel:TwitchChannel=None):
        """Registers the function to the class"""
        # make sure the register exists
        if cls.registered is not None:
            raise ValueError("Only one Mentioned Bot at the Start of a message command can be allowed at the same time")

        # allows the usage as a decorator
        #   Doesn't behave like a regular decorator because we aren't storing a "wrapper" which handles args and kwargs
        #   Args and kwargs of the function are handled by the handle_chat_message function
        #   It is expected that the function is located within the defined TwitchBot of the application
        def decorator(fnc):
            cls.registered = cls(callback=fnc,channel=channel)
        return decorator