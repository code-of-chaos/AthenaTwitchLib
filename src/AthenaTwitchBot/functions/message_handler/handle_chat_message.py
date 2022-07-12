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
from AthenaTwitchBot.models.bot_methods.bot_custom_reward import BotCustomReward
from AthenaTwitchBot.models.bot_methods.bot_first_time_chatter import BotFirstTimeChatter
import AthenaTwitchBot.data.global_vars as gbl

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
async def handle_chat_message(
        context:MessageContext,tags:str, user_name_str:str, channel_str:str, text:tuple[str]
) -> None:
    context.tags = tags
    context.channel = channel_str
    context.user = user_name_str
    context.chat_message = text

    # a command is invoked
    if text[0].startswith(":!") and BotCommand.registered is not None:
        try:
            command: BotCommand = BotCommand.registered[text[0][2:]]
        except KeyError:
            return

        match context, command:
            # Subscriber only commands
            case MessageContext(tags=MessageTags(subscriber=False)), BotCommand(subscriber_only=True):
                return
            case MessageContext(tags=MessageTags(subscriber=True)), BotCommand(subscriber_only=True, args=True):
                await command.callback(self=gbl.bot, context=context, args=text[1:])
            case MessageContext(tags=MessageTags(subscriber=True)), BotCommand(subscriber_only=True, args=False):
                await command.callback(self=gbl.bot, context=context)

            # any remaining cases
            case _, BotCommand(args=True):
                await command.callback(self=gbl.bot, context=context, args=text[1:])
            case _, BotCommand(args=False):
                await command.callback(self=gbl.bot, context=context)

    # the bot is mentioned
    elif text[0].startswith(f":@{gbl.bot.nickname}") and BotMentioned.registered is not None:
        await BotMentioned.registered.callback(self=gbl.bot, context=context)

    # other edge cases
    else:
        # custom redeemable with text is caught
        if (custom_reward_id := context.tags.custom_reward_id) is not NOTHING:
            if BotCustomReward.registered is not None and custom_reward_id in BotCustomReward.registered:
                    await BotCustomReward.registered[custom_reward_id].callback(self=gbl.bot, context=context)

        # first time chatter
        if context.tags.first_msg:
            if BotFirstTimeChatter.registered is not None:
                await BotFirstTimeChatter.registered.callback(self=gbl.bot, context=context)