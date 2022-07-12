# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaLib.data.text import NOTHING

# Custom Packages
from AthenaTwitchBot.models.message_context import MessageContext
from AthenaTwitchBot.models.message_tags import MessageTags
from AthenaTwitchBot.models.bot_methods.bot_command import BotCommand
from AthenaTwitchBot.models.bot_methods.bot_mentioned import BotMentioned
from AthenaTwitchBot.models.bot_methods.bot_mentioned_start import BotMentionedStart
from AthenaTwitchBot.models.bot_methods.bot_custom_reward import BotCustomReward
from AthenaTwitchBot.models.bot_methods.bot_first_time_chatter import BotFirstTimeChatter
import AthenaTwitchBot.data.global_vars as gbl

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
async def _execute_command(command:BotCommand, context:MessageContext, text:tuple[str]):
    if command.args:
        await command.callback(self=gbl.bot, context=context, args=text[1:])
    else:
        await command.callback(self=gbl.bot, context=context)

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
async def handle_chat_message(
        context:MessageContext,tags:str|None, user_name_str:str, channel_str:str, text:tuple[str]
) -> None:
    """
    Main handler for every chat message
    Will use the stored BotCommand, BotMentioned, BotCustomReward, BotFirstTimeChatter objects to correctly
        find which callback it should use on the specific message.

    Should always silently return a None value if the command was wrong or the command was called by a user that
        wasn't allowed to use the specific command.

    Parameters:
    - context:
    - tags:
    - user_name_str:
    - channel_str:
    - text:
    """

    # define context attributes before it is handed off to the specific callback (or not used at all)
    #   Done so the user can use this information in their specific callback code
    context.tags = tags
    context.channel = channel_str
    context.user = user_name_str
    context.chat_message = text

    # ------------------------------------------------------------------------------------------------------------------
    # Command catching
    # ------------------------------------------------------------------------------------------------------------------
    if text[0].startswith(f":{gbl.bot.command_prefix}") and gbl.bot_command_enabled:
        try:
            command: BotCommand = BotCommand.registered[text[0][2:]]
        except KeyError:
            return

        # do a pattern match here as it is the easiest manner to compare the structures against each other
        match context, command:
            # catch a command that was meant to be used by a moderator but wasn't called by a moderator
            case MessageContext(tags=MessageTags(mod=False)), BotCommand(mod_only=True):
                return
            # Subscriber only commands
            case MessageContext(tags=MessageTags(mod=True)), BotCommand(mod_only=True):
                await _execute_command(command=command, context=context, text=text)

            # catch a command that was meant to be used by a subscriber but wasn't called by a subscriber
            case MessageContext(tags=MessageTags(subscriber=False)), BotCommand(subscriber_only=True):
                return
            # Subscriber only commands
            case MessageContext(tags=MessageTags(subscriber=True)), BotCommand(subscriber_only=True):
                await _execute_command(command=command, context=context, text=text)

            # catch a command that is only allowed on a specific channel
            #   If the command was caught in a channel that wasn't in the allowed channels, simply return
            case MessageContext(channel=msg_channel), BotCommand(channels=cmd_channels) if cmd_channels is not None \
                and msg_channel not in cmd_channels :
                return

            # any remaining cases
            case _:
                await _execute_command(command=command, context=context, text=text)

        return

    # the bot is mentioned at the start of the message
    elif text[0].startswith(f":@{gbl.bot.nickname}") and gbl.bot_mentioned_start_enabled:
        await BotMentionedStart.registered.callback(self=gbl.bot, context=context)
        return

    # ------------------------------------------------------------------------------------------------------------------
    # other edge cases
    # ------------------------------------------------------------------------------------------------------------------

    # the bot was mentioned in a message
    if f"@{gbl.bot.nickname}" in " ".join(text) and gbl.bot_mentioned_enabled:
        await BotMentioned.registered.callback(self=gbl.bot, context=context)

    # custom redeemable with text is caught
    if (custom_reward_id := context.tags.custom_reward_id) is not NOTHING \
            and gbl.bot_custom_reward_enabled \
            and custom_reward_id in BotCustomReward.registered:
        await BotCustomReward.registered[custom_reward_id].callback(self=gbl.bot, context=context)

    # first time chatter
    if context.tags.first_msg and gbl.bot_first_time_chatter_enabled:
        await BotFirstTimeChatter.registered.callback(self=gbl.bot, context=context)