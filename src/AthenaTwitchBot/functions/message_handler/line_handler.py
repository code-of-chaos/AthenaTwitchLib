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
from AthenaTwitchBot.data.irc_twitch import *
import AthenaTwitchBot.data.global_vars as gbl

from AthenaTwitchBot.functions.message_handler.handle_ping import handle_ping
from AthenaTwitchBot.functions.message_handler.handle_chat_message import handle_chat_message
from AthenaTwitchBot.functions.message_handler.handle_join import handle_join
from AthenaTwitchBot.functions.message_handler.handle_capabilities import handle_capabilities
from AthenaTwitchBot.functions.message_handler.handle_uncaught import handle_uncaught
from AthenaTwitchBot.functions.message_handler.handle_channel import handle_channel

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
async def line_handler(line:bytearray) -> None:
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
            await handle_ping(context, NOTHING.join(ping_response))

        case _tmi_twitch_tv, str(_), gbl.bot.nickname, *_ if (
                _tmi_twitch_tv == TMI_TWITCH_TV
        ):
            # CATCHES the following pattern:
            # :tmi.twitch.tv
            # 001
            # eva_athenabot
            # :Welcome, GLHF!
            await handle_channel(context)

        case str(tags), str(user_name_str), "PRIVMSG", str(channel_str), *text if (
            gbl.bot.twitch_capability_tags
        ):
            # CATCHES the following pattern:
            # @badge-info=;badges=;client-nonce=4ac36d90556713038f596be25cc698a2;color=#1E90FF;display-name=badcop_;emotes=;first-msg=0;flag=;id=8b506bf0-517d-4ae7-9dcb-bce5c2145412;mod=0;room-id=600187263;subscriber=0;tmi-sent-ts=1655367514927;turbo=0;user-id=56931496;user-type=
            # :badcop_!badcop_@badcop_.tmi.twitch.tv
            # PRIVMSG
            # #directiveathena
            # :that sentence was poggers
            await handle_chat_message(context, tags, user_name_str, channel_str, text)


        case str(user_name_str), "PRIVMSG", str(channel_str), *text if (
                not gbl.bot.twitch_capability_tags
        ):
            # CATCHES the following pattern:
            # :badcop_!badcop_@badcop_.tmi.twitch.tv
            # PRIVMSG
            # #directiveathena
            # :that sentence was poggers
            await handle_chat_message(context, None, user_name_str, channel_str, text)

        case str(bot_name_long), "JOIN", str(_) if (
                bot_name_long == f":{gbl.bot.nickname}!{gbl.bot.nickname}@{gbl.bot.nickname}.tmi.twitch.tv"
        ):
            # CATCHES the following pattern:
            # :eva_athenabot!eva_athenabot@eva_athenabot.tmi.twitch.tv
            # JOIN
            # #directiveathena
            await handle_join(context)

        case ":tmi.twitch.tv", "CAP", "*", "ACK", ":twitch.tv/tags":
            # CATCHES the following pattern:
            # :tmi.twitch.tv
            # CAP
            # *
            # ACK
            # :twitch.tv/tags
            await handle_capabilities(context)

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
            await handle_channel(context)

        case str(bot_name_long), str(_), gbl.bot.nickname, str(_), *_ \
            if bot_name_long == f":{gbl.bot.nickname}.tmi.twitch.tv":
            # CATCHES the following pattern:
            # :eva_athenabot.tmi.twitch.tv
            # 353
            # eva_athenabot
            # =
            # #directiveathena
            # :eva_athenabot
            await handle_channel(context)

        case _:
            # something wasn't caught correctly
            await handle_uncaught(context)


    await gbl.bot_server.output_all(context)