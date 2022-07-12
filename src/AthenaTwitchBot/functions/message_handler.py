# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.message_context import MessageContext
from AthenaTwitchBot.data.itc_twitch import *
import AthenaTwitchBot.data.global_vars as gbl
from AthenaTwitchBot.data.message_flags import MessageFlags

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
async def line_received_handler(line: bytearray):
    await gbl.bot_server.output_all(context=await message_handler(line))

async def message_handler(line:bytearray) -> MessageContext:
    context = MessageContext(raw_input=line)
    match context.raw_input_decoded_split:
        case "PING", *ping_response :
            # CATCHES the following pattern:
            # PING
            # :tmi.twitch.tv
            print("pinged")
            context.flag = MessageFlags.ping
            context.output = " ".join(ping_response)

        case _tmi_twitch_tv, str(_), gbl.bot.nickname, *_ if (
                _tmi_twitch_tv == TMI_TWITCH_TV
        ):
            # CATCHES the following pattern:
            # :tmi.twitch.tv
            # 001
            # eva_athenabot
            # :Welcome, GLHF!
            context.output = None # undefined output, not needed for anything to send back to twitch

        case str(tags), str(user_name_str), "PRIVMSG", str(channel_str), *text if (
            gbl.bot.twitch_capability_tags
        ):
            # CATCHES the following pattern:
            # @badge-info=;badges=;client-nonce=4ac36d90556713038f596be25cc698a2;color=#1E90FF;display-name=badcop_;emotes=;first-msg=0;flag=;id=8b506bf0-517d-4ae7-9dcb-bce5c2145412;mod=0;room-id=600187263;subscriber=0;tmi-sent-ts=1655367514927;turbo=0;user-id=56931496;user-type=
            # :badcop_!badcop_@badcop_.tmi.twitch.tv
            # PRIVMSG
            # #directiveathena
            # :that sentence was poggers
            print("message, with tags enabled")
            context.tags = tags
            context.channel = channel_str
            context.user=user_name_str
            context.chat_message = text
            context.output = None

        case str(user_name_str), "PRIVMSG", str(channel_str), *text if (
                not gbl.bot.twitch_capability_tags
        ):
            # CATCHES the following pattern:
            # :badcop_!badcop_@badcop_.tmi.twitch.tv
            # PRIVMSG
            # #directiveathena
            # :that sentence was poggers
            print("message, with tags disabled")
            context.user=user_name_str
            context.channel = channel_str
            context.chat_message = text

            context.output = None

        case str(bot_name_long), "JOIN", str(_) if (
                bot_name_long == f":{gbl.bot.nickname}!{gbl.bot.nickname}@{gbl.bot.nickname}.tmi.twitch.tv"
        ):
            # CATCHES the following pattern:
            # :eva_athenabot!eva_athenabot@eva_athenabot.tmi.twitch.tv
            # JOIN
            # #directiveathena
            context.output = None

        case ":tmi.twitch.tv", "CAP", "*", "ACK", ":twitch.tv/tags":
            # CATCHES the following pattern:
            # :tmi.twitch.tv
            # CAP
            # *
            # ACK
            # :twitch.tv/tags
            context.output = None

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
            context.output = None

        case str(bot_name_long), str(_), gbl.bot.nickname, str(_), *_ \
            if bot_name_long == f":{gbl.bot.nickname}.tmi.twitch.tv":
            # CATCHES the following pattern:
            # :eva_athenabot.tmi.twitch.tv
            # 353
            # eva_athenabot
            # =
            # #directiveathena
            # :eva_athenabot
            context.output = None

        case _:
            # something wasn't caught correctly
            context.output = None


    return context