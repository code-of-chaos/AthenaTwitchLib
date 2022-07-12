# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Any
# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Bot Server -
# ----------------------------------------------------------------------------------------------------------------------

# the variables stored here are to be set when the BotServer is created
#   These variables are used by various functions and classes to call back to

bot_server:Any=None # stands for the BotServer
bot:Any = None      # stands for the TwitchBot

bot_command_enabled:bool=False              # Changed on launch. Set there to make the message parsing less heavy.
bot_mentioned_start_enabled:bool=False      # Changed on launch. Set there to make the message parsing less heavy.
bot_mentioned_enabled:bool=False            # Changed on launch. Set there to make the message parsing less heavy.
bot_custom_reward_enabled:bool=False        # Changed on launch. Set there to make the message parsing less heavy.
bot_first_time_chatter_enabled:bool=False   # Changed on launch. Set there to make the message parsing less heavy.