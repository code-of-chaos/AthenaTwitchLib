# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

from collections.abc import Callable
from collections.abc import Mapping
from collections.abc import Awaitable
from typing import Any
from typing import ClassVar

# Custom Library
from AthenaLib.data.text import NOTHING
from AthenaColor import ForeNest

# Custom Packages
import AthenaTwitchBot.data.global_vars as gbl
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext
from AthenaTwitchBot.models.twitch_bot.message_tags import MessageTags
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_command import BotCommand
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_mentioned import BotMentioned
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_mentioned_start import BotMentionedStart
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_custom_reward import BotCustomReward
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_first_time_chatter import BotFirstTimeChatter
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_chat_message import BotChatMessage
from AthenaTwitchBot.models.twitch_bot.both_methods.bot_method_inheritance.callback import BotMethodCallback
from AthenaTwitchBot.models.twitch_user import TwitchUser
from AthenaTwitchBot.models.twitch_channel import TwitchChannel
from AthenaTwitchBot.data.message_flags import MessageFlags
from AthenaTwitchBot.data.irc_twitch import *

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
async def _execute_command(command:BotMethodCallback, context:MessageContext) -> Any:
    if command.args:
        await command(callback_self=gbl.bot, context=context, args=context.chat_message[1:])
    else:
        await command(callback_self=gbl.bot, context=context)

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class LineHandler:
    TWITCH_SPECIFIC_IRC_MAPPING: ClassVar[Mapping[str, Callable[[MessageContext], Awaitable[None]]]] = {}
    TWITCH_IRC_MAPPING: ClassVar[Mapping[str, Callable[[MessageContext], Awaitable[None]]]] = {}

    @classmethod
    def _define_mappings(cls) -> None:
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
        cls.TWITCH_IRC_MAPPING = {
            "PART": cls.handle_user_part,
            "JOIN": cls.handle_user_join,
        }

    @classmethod
    async def handle_line(cls, line:bytes) -> None:
        if cls.TWITCH_SPECIFIC_IRC_MAPPING is None:
            cls._define_mappings()

        # Assemble a bare context
        #   This is handled by the MessageContext class
        #   Decoding of the line into a string format is also handled by the MessageContext class
        await cls.handle_context(context := MessageContext(raw_input=line))
        assert gbl.bot_server is not None
        await gbl.bot_server.output_all(context)

    @classmethod
    async def handle_context(cls,context:MessageContext) -> None:
        assert gbl.bot is not None
        # match the pattern of th line to something we can use and pas off to other "sub handlers"
        #   User "sub handlers" for ease of writing and stuff like that
        match context.raw_input_decoded_split:
            # ----------------------------------------------------------------------------------------------------------
            # - Primary section -
            # ----------------------------------------------------------------------------------------------------------
            case ["PING", _]:
                # catch the ping as soon as possible
                await cls.handle_ping(context)
                return

            case [str(tags), str(user_name_str), "PRIVMSG", str(channel_str), *text]:
                # CATCHES the following pattern:
                # @badge-info=;badges=;client-nonce=4ac36d90556713038f596be25cc698a2;color=#1E90FF;display-name=badcop_;emotes=;first-msg=0;flag=;id=8b506bf0-517d-4ae7-9dcb-bce5c2145412;mod=0;room-id=600187263;subscriber=0;tmi-sent-ts=1655367514927;turbo=0;user-id=56931496;user-type=
                # :badcop_!badcop_@badcop_.tmi.twitch.tv
                # PRIVMSG
                # #directiveathena
                # :that sentence was poggers
                context.tags = MessageTags.new_from_tags_str(tags)
                context.channel = TwitchChannel(channel_str)
                context.user = TwitchUser(user_name_str)
                context.chat_message = tuple(text)
                await cls.handle_chat_message(context)
                return

            case [str(tags), ":tmi.twitch.tv", twitch_specific_irc, str(channel_str), *text] if (
                    twitch_specific_irc in cls.TWITCH_SPECIFIC_IRC_MAPPING
            ):
                # CATCHES the following pattern:
                # @badge-info=;badges=moderator/1;color=;display-name=eva_athenabot;emote-sets=0,300374282,8b453104-5c38-4b89-86b8-8c2e6373dc8a;mod=1;subscriber=0;user-type=mod
                # :tmi.twitch.tv
                # ...
                # #directiveathena
                context.tags = MessageTags.new_from_tags_str(tags)
                context.channel = TwitchChannel(channel_str)
                context.chat_message = tuple(text)
                await cls.TWITCH_SPECIFIC_IRC_MAPPING[twitch_specific_irc](context)
                return

            case [str(user_name_str), twitch_irc, str(channel_str), *text] if (
                    twitch_irc in cls.TWITCH_IRC_MAPPING
            ):
                # CATCHES the following pattern:
                # :twidi_angel!twidi_angel@twidi_angel.tmi.twitch.tv
                # PART
                # #directiveathena
                context.channel = TwitchChannel(channel_str)
                context.user = TwitchUser(user_name_str)
                context.chat_message = tuple(text)
                await cls.TWITCH_IRC_MAPPING[twitch_irc](context,)
                return

            # ----------------------------------------------------------------------------------------------------------
            # - Secondary section -
            # ----------------------------------------------------------------------------------------------------------
            case [_tmi_twitch_tv, str(_), gbl.bot.nickname, *_] if (
                    _tmi_twitch_tv == TMI_TWITCH_TV
            ):
                # CATCHES the following pattern:
                # :tmi.twitch.tv
                # 001
                # eva_athenabot
                # :Welcome, GLHF!
                await cls.handle_bot_channel(context)
                return

            case [":tmi.twitch.tv", "CAP", "*", "ACK", capability]:
                # CATCHES the following pattern:
                # :tmi.twitch.tv
                # CAP
                # *
                # ACK
                # :twitch.tv/tags
                await cls.handle_bot_capabilities(context, capability)
                return

            case [str(bot_name_long), "JOIN", str(_)] if (
                    bot_name_long == f"{gbl.bot.nickname_irc}!{gbl.bot.nickname}{gbl.bot.nickname_at}.tmi.twitch.tv"
            ):
                # CATCHES the following pattern:
                # :eva_athenabot!eva_athenabot@eva_athenabot.tmi.twitch.tv
                # JOIN
                # #directiveathena
                await cls.handle_bot_join(context)
                return

            case [str(bot_name_long), str(_), gbl.bot.nickname, str(_), *_] if (
                    bot_name_long == f"{gbl.bot.nickname_irc}.tmi.twitch.tv"
            ):
                # CATCHES the following pattern:
                # :eva_athenabot.tmi.twitch.tv
                # 353
                # eva_athenabot
                # =
                # #directiveathena
                # :eva_athenabot
                await cls.handle_bot_channel(context)
                return

            case _:
                print(f"NOT CAUGHT : {ForeNest.Maroon(context.raw_input_decoded)}")
                return

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def handle_ping(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.ping # use special flag to make sure the output parse knows wha to do
        context.output = f"PONG {context.raw_input_decoded_split[1:]}"

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def handle_bot_join(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_bot_capabilities(cls, context:MessageContext,capability:str) -> None:
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_bot_channel(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def handle_user_join(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_user_part(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def handle_irc_clearchat(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_clearmsg(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_globaluserstate(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_hosttarget(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_notice(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_reconnect(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_roomstate(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_usernotice(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_userstate(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output
    @classmethod
    async def handle_irc_whisper(cls, context:MessageContext) -> None:
        context.flag = MessageFlags.no_output

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def handle_chat_message(cls, context:MessageContext) -> None:
        assert gbl.bot is not None
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
