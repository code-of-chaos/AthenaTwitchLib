# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaLib.data.text import NOTHING
from AthenaColor import ForeNest

# Custom Packages
from AthenaTwitchBot.models.twitch_bot.message_context import MessageContext
from AthenaTwitchBot.models.twitch_bot.message_tags import MessageTags
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_command import BotCommand
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_mentioned import BotMentioned
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_mentioned_start import BotMentionedStart
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_custom_reward import BotCustomReward
from AthenaTwitchBot.models.twitch_bot.bot_methods.bot_first_time_chatter import BotFirstTimeChatter
from AthenaTwitchBot.data.message_flags import MessageFlags
from AthenaTwitchBot.data.irc_twitch import *
import AthenaTwitchBot.data.global_vars as gbl

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
async def _execute_command(command:BotCommand, context:MessageContext, text:tuple[str]):
    if command.args:
        await command(callback_self=gbl.bot, context=context, args=text[1:])
    else:
        await command(callback_self=gbl.bot, context=context)

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class LineHandler:
    @classmethod
    async def handle(cls,line:bytearray) -> None:
        """
        Handles a specific line brought in from the connection. Handles every line as a unique message.
        Will therefor constantly need to make new context objects and output them correctly.

        Parameters:
        - line:
        """

        # Assemble a bare context
        #   This is handled by the MessageContext class
        #   Decoding of the line into a string format is also handled by the MessageContext class
        context = MessageContext(raw_input=line)

        # match the pattern of th line to something we can use and pas off to other "sub handlers"
        #   User "sub handlers" for ease of writing and stuff like that
        match context.raw_input_decoded_split:
            case "PING", *ping_response :
                # CATCHES the following pattern:
                # PING
                # :tmi.twitch.tv
                await cls._handle_ping(context, NOTHING.join(ping_response))

            case _tmi_twitch_tv, str(_), gbl.bot.nickname, *_ if (
                    _tmi_twitch_tv == TMI_TWITCH_TV
            ):
                # CATCHES the following pattern:
                # :tmi.twitch.tv
                # 001
                # eva_athenabot
                # :Welcome, GLHF!
                await cls._handle_channel(context)

            case str(tags), str(user_name_str), "PRIVMSG", str(channel_str), *text if (
                gbl.bot.twitch_capability_tags
            ):
                # CATCHES the following pattern:
                # @badge-info=;badges=;client-nonce=4ac36d90556713038f596be25cc698a2;color=#1E90FF;display-name=badcop_;emotes=;first-msg=0;flag=;id=8b506bf0-517d-4ae7-9dcb-bce5c2145412;mod=0;room-id=600187263;subscriber=0;tmi-sent-ts=1655367514927;turbo=0;user-id=56931496;user-type=
                # :badcop_!badcop_@badcop_.tmi.twitch.tv
                # PRIVMSG
                # #directiveathena
                # :that sentence was poggers
                await cls._handle_chat_message(context, tags, user_name_str, channel_str, text)


            case str(user_name_str), "PRIVMSG", str(channel_str), *text if (
                    not gbl.bot.twitch_capability_tags
            ):
                # CATCHES the following pattern:
                # :badcop_!badcop_@badcop_.tmi.twitch.tv
                # PRIVMSG
                # #directiveathena
                # :that sentence was poggers
                await cls._handle_chat_message(context, None, user_name_str, channel_str, text)

            case str(bot_name_long), "JOIN", str(_) if (
                    bot_name_long == f":{gbl.bot.nickname}!{gbl.bot.nickname}@{gbl.bot.nickname}.tmi.twitch.tv"
            ):
                # CATCHES the following pattern:
                # :eva_athenabot!eva_athenabot@eva_athenabot.tmi.twitch.tv
                # JOIN
                # #directiveathena
                await cls._handle_join(context)

            case ":tmi.twitch.tv", "CAP", "*", "ACK", capability \
                if capability in {":twitch.tv/commands", ":twitch.tv/tags", ":twitch.tv/membership"} :
                # CATCHES the following pattern:
                # :tmi.twitch.tv
                # CAP
                # *
                # ACK
                # :twitch.tv/tags
                await cls._handle_capabilities(context)

            case str(bot_name_long), str(_), gbl.bot.nickname, "=", str(_), str(bot_name_short) if (
                    bot_name_long == f":{gbl.bot.nickname}.tmi.twitch.tv"
                    and bot_name_short == f":{gbl.bot.nickname}"
            ):
                # CATCHES the following pattern:
                # :eva_athenabot.tmi.twitch.tv
                # 353
                # eva_athenabot
                # =
                # #directiveathena
                # :eva_athenabot
                await cls._handle_channel(context)

            case str(bot_name_long), str(_), gbl.bot.nickname, str(_), *_ \
                if bot_name_long == f":{gbl.bot.nickname}.tmi.twitch.tv":
                # CATCHES the following pattern:
                # :eva_athenabot.tmi.twitch.tv
                # 353
                # eva_athenabot
                # =
                # #directiveathena
                # :eva_athenabot
                await cls._handle_channel(context)

            case str(tags), ":tmi.twitch.tv", "USERSTATE", str(channel_str), *text:
                # CATCHES the following pattern:
                # @badge-info=;badges=moderator/1;color=;display-name=eva_athenabot;emote-sets=0,300374282,8b453104-5c38-4b89-86b8-8c2e6373dc8a;mod=1;subscriber=0;user-type=mod
                # :tmi.twitch.tv
                # USERSTATE
                # #directiveathena
                await cls._handle_userstate(context)

            case str(user), "PART", str(channel_str), *text:
                # CATCHES the following pattern:
                # :twidi_angel!twidi_angel@twidi_angel.tmi.twitch.tv
                # PART
                # #directiveathena
                await cls._handle_part(context)

            case _:
                # something wasn't caught correctly
                await cls._handle_uncaught(context)


        await gbl.bot_server.output_all(context)

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def _handle_ping(cls, context:MessageContext, ping_response:str) -> None:
        context.flag = MessageFlags.ping # use special flag to make sure the output parse knows wha to do
        context.output = " ".join(f"PONG {ping_response}")

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def _handle_join(cls, context:MessageContext):
        context.flag = MessageFlags.no_output

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def _handle_capabilities(cls, context:MessageContext):
        context.flag = MessageFlags.no_output

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def _handle_uncaught(cls, context:MessageContext):
        print(f"NOT CAUGHT : {ForeNest.Maroon(context.raw_input_decoded)}")

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def _handle_channel(cls, context:MessageContext):
        context.flag = MessageFlags.no_output

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def _handle_userstate(cls, context:MessageContext):
        context.flag = MessageFlags.no_output

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def _handle_part(cls, context:MessageContext):
        context.flag = MessageFlags.no_output

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    async def _handle_chat_message(
            cls, context:MessageContext,tags:str|None, user_name_str:str, channel_str:str, text:tuple[str]
    ) -> None:
        # define context attributes before it is handed off to the specific callback (or not used at all)
        #   Done so the user can use this information in their specific callback code
        context.tags = tags
        context.channel = channel_str
        context.user = user_name_str
        context.chat_message = text

        # --------------------------------------------------------------------------------------------------------------
        # Command catching
        # --------------------------------------------------------------------------------------------------------------
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

                # catch a command that was meant to be used by a subscriber but wasn't called by a subscriber
                case MessageContext(tags=MessageTags(subscriber=False)), BotCommand(subscriber_only=True):
                    return

                # any remaining cases
                case _:
                    await _execute_command(command=command, context=context, text=text)

            return

        # the bot is mentioned at the start of the message
        elif text[0].startswith(f":@{gbl.bot.nickname}") and gbl.bot_mentioned_start_enabled:
            await _execute_command(command=BotMentionedStart.registered, context=context, text=text)

        # --------------------------------------------------------------------------------------------------------------
        # other edge cases
        # --------------------------------------------------------------------------------------------------------------
        # the bot was mentioned in a message
        if f"@{gbl.bot.nickname}" in " ".join(text) and gbl.bot_mentioned_enabled:
            await _execute_command(command=BotMentioned.registered, context=context, text=text)

        # custom redeemable with text is caught
        if (custom_reward_id := context.tags.custom_reward_id) is not NOTHING \
                and gbl.bot_custom_reward_enabled \
                and custom_reward_id in BotCustomReward.registered:
            await _execute_command(command=BotCustomReward.registered[custom_reward_id], context=context, text=text)

        # first time chatter
        if context.tags.first_msg and gbl.bot_first_time_chatter_enabled:
            await _execute_command(command=BotFirstTimeChatter.registered, context=context, text=text)
