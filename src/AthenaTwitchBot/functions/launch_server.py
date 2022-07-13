# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import tracemalloc

# Custom Library

# Custom Packages
import AthenaTwitchBot.data.global_vars as gbl
from AthenaTwitchBot.models.twitch_bot.twitch_bot import TwitchBot
from AthenaTwitchBot.models.twitch_bot.bot_server import BotServer
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_command import BotCommand
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_mentioned import BotMentioned
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_mentioned_start import BotMentionedStart
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_custom_reward import BotCustomReward
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_first_time_chatter import BotFirstTimeChatter

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def launch_server(*,twitch_bot:TwitchBot,**kwargs) -> None:
    """
    Simplified function which starts the server.
    Passes all arguments directly to the BotServer class.
    For correct parameters, go to the BotServer class.

    Defines some gbl variables on call before the Server is launched. These gbl variables are vital for the execution
    of the message handling.
    """
    tracemalloc.start()
    gbl.bot = twitch_bot

    gbl.bot_command_enabled = BotCommand.registered is not None
    gbl.bot_mentioned_start_enabled = BotMentionedStart.registered is not None
    gbl.bot_mentioned_enabled = BotMentioned.registered is not None
    gbl.bot_custom_reward_enabled = BotCustomReward.registered is not None
    gbl.bot_first_time_chatter_enabled = BotFirstTimeChatter.registered is not None

    gbl.bot_server = BotServer(**kwargs)
    gbl.bot_server.launch()