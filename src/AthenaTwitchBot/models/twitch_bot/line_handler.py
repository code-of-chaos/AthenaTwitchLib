# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Callable

# Custom Library
from AthenaLib.data.text import NOTHING
from AthenaColor import ForeNest

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_command import BotCommand
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_mentioned import BotMentioned
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_mentioned_start import BotMentionedStart
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_custom_reward import BotCustomReward
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_first_time_chatter import BotFirstTimeChatter
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_chat_message import BotChatMessage
from AthenaTwitchBot.data.message_flags import MessageFlags
from AthenaTwitchBot.data.irc_twitch import *
import AthenaTwitchBot.data.global_vars as gbl

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
async def _execute_command(command:BotCommand, context:MessageContext):
    if command.args:
        await command(callback_self=gbl.bot, context=context, args=context.chat_message[1:])
    else:
        await command(callback_self=gbl.bot, context=context)

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class LineHandler:
    TWITCH_SPECIFIC_IRC_MAPPING: dict[str:Callable] = None
    TWITCH_IRC_MAPPING: dict[str:Callable] = None

    @classmethod
    def _define_mappings(cls):
        cls.TWITCH_SPECIFIC_IRC_MAPPING = {
            "CLEARCHAT": cls.handle_irc_clearchat,
            "CLEARMSG": cls.handle_irc_clearmsg,
            "GLOBALUSERSTATE": cls.handle_irc_globaluserstate,
            "HOSTTARGET": cls.handle_irc_hosttarget,
            "NOTICE": cls.handle_irc_notice,
            "RECONNECT": cls.handle_irc_reconnect,
            "ROOMSTATE": cls.handle_irc_roomstate,
            "USERNOTICE": cls.handle_irc_usernotice,
            "USERSTATE": cls.handle_irc_userstate,
            "WHISPER": cls.handle_irc_whisper,
        }
        cls.TWITCH_IRC_MAPPING: dict[str:Callable] = {
            "PART": cls.handle_user_part,
            "JOIN": cls.handle_user_join,
        }

    @classmethod
    async def handle_line(cls, line:bytearray):
        if cls.TWITCH_SPECIFIC_IRC_MAPPING is None:
            cls._define_mappings()

        # Assemble a bare context
        #   This is handled by the MessageContext class
        #   Decoding of the line into a string format is also handled by the MessageContext class
        await cls.handle_context(context := MessageContext(raw_input=line))
        await gbl.bot_server.output_all(context)

    @classmethod
    async def handle_context(cls,context:MessageContext) -> None:
        # match the pattern of th line to something we can use and pas off to other "sub handlers"
        #   User "sub handlers" for ease of writing and stuff like that
        if (
            not isinstance(context.raw_input_decoded_split, list) and 
            any(not isinstance(s, str) for s in context.raw_input_decoded_split)
        ):
            print(f"NOT CORRECT TYPE : {ForeNest.Maroon(context.raw_input_decoded)}")
            return

        tmp = context.raw_input_decoded_split

        if tmp[0] == "PING":
            await cls.handle_ping(context)
            return
        elif tmp[2] == "PRIVMSG":
            context.tags = tmp[0]
            context.user = tmp[1]
            context.channel = tmp[3]
            context.chat_message = tmp[4:]  # TODO think this could throw an error...
            await cls.handle_chat_message(context)
            return
        elif tmp[1] == TMI_TWITCH_TV and tmp[2] in cls.TWITCH_SPECIFIC_IRC_MAPPING:
            context.tags = tmp[0]
            context.channel = tmp[3]
            context.chat_message = tmp[4:]  # TODO think this could throw an error...
            await cls.TWITCH_SPECIFIC_IRC_MAPPING[tmp[2]](context)
            return
        elif tmp[1] in cls.TWITCH_IRC_MAPPING:
            context.channel = tmp[2]
            context.user = tmp[0]
            context.chat_message = tmp[3:]  # TODO think this could throw an error...
            await cls.TWITCH_IRC_MAPPING[tmp[1]](context)
            return
        elif tmp[0] == TMI_TWITCH_TV:
            await cls.handle_bot_channel(context)
            return
        elif all(
            tmp[0] == ":tmi.twitch.tv",
            tmp[1] == "CAP",
            tmp[2] == "*",
            tmp[3] == "ACK",
            len(tmp == 4)
        ):
            await cls.handle_bot_capabilities(context, tmp[4])
            return
        elif (
            tmp[1] == "JOIN" and
            tmp[0] == f"{gbl.bot.nickname_irc}!{gbl.bot.nickname}{gbl.bot.nickname_at}.tmi.twitch.tv"
        ):
            await cls.handle_bot_join(context)
            return
        elif tmp[0] == f"{gbl.bot.nickname_irc}.tmi.twitch.tv":
            await cls.handle_bot_channel(context)
            return
        else:
            print(f"NOT CAUGHT : {ForeNest.Maroon(context.raw_input_decoded)}")
            return
                

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def handle_ping(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.ping # use special flag to make sure the output parse knows wha to do
        context.output = f"PONG {context.raw_input_decoded_split[1:]}"

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def handle_bot_join(cls, context:MessageContext):
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_bot_capabilities(cls, context:MessageContext,capability:str):
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_bot_channel(cls, context:MessageContext):
        context.flag = MessageFlags.no_output

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def handle_user_join(cls, context:MessageContext):
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_user_part(cls, context:MessageContext):
        context.flag = MessageFlags.no_output

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def handle_irc_clearchat(cls, context:MessageContext):
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_clearmsg(cls, context:MessageContext):
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_globaluserstate(cls, context:MessageContext):
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_hosttarget(cls, context:MessageContext):
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_notice(cls, context:MessageContext):
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_reconnect(cls, context:MessageContext):
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_roomstate(cls, context:MessageContext):
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_usernotice(cls, context:MessageContext):
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_userstate(cls, context:MessageContext):
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_whisper(cls, context:MessageContext):
        context.flag = MessageFlags.no_output

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def handle_chat_message(cls, context:MessageContext) -> None:
        # define context attributes before it is handed off to the specific callback (or not used at all)
        #   Done so the user can use this information in their specific callback code

        # --------------------------------------------------------------------------------------------------------------
        # Command catching
        # --------------------------------------------------------------------------------------------------------------
        if (context.chat_message[0].startswith(gbl.bot.command_prefix_irc)
            and (cmd_name := context.chat_message[0][2:]) in BotCommand.registered
        ):
            command:BotCommand = BotCommand.registered[cmd_name]
            if (
                # catch a command that was meant to be used by a moderator but wasn't called by a moderator
                (command.mod_only and not context.tags.mod)
                # catch a command that was meant to be used by a subscriber but wasn't called by a subscriber
                or (command.subscriber_only and not context.tags.subscriber)
            ):
                return
            await _execute_command(command=command, context=context)
            return

        # the bot is mentioned at the start of the message
        if context.chat_message[0].startswith(gbl.bot.nickname_at_irc) and BotMentionedStart.registered:
            await _execute_command(command=BotMentionedStart.registered, context=context)
            return

        # --------------------------------------------------------------------------------------------------------------
        # other edge cases
        # --------------------------------------------------------------------------------------------------------------
        # the bot was mentioned in a message
        if gbl.bot.nickname_at in context.chat_message and BotMentioned.registered:
            await _execute_command(command=BotMentioned.registered, context=context,)

        # custom redeemable with text is caught
        if ((custom_reward_id := context.tags.custom_reward_id) is not NOTHING
            and custom_reward_id in BotCustomReward.registered):
            await _execute_command(command=BotCustomReward.registered[custom_reward_id], context=context)

        # first time chatter
        if context.tags.first_msg and BotFirstTimeChatter.registered:
            await _execute_command(command=BotFirstTimeChatter.registered, context=context)

        if context.flag == MessageFlags.undefined and BotChatMessage.registered is not None:
            await _execute_command(command=BotChatMessage.registered, context=context)
