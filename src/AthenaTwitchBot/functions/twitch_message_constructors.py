# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Callable
from datetime import datetime
import time

# Custom Library
from AthenaColor import StyleNest, ForeNest, HEX

# Custom Packages
from AthenaTwitchBot.models.twitch_message import TwitchMessage, TwitchMessagePing, TwitchMessageOnlyForBot

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
def _find_PING(content:list[str]) -> TwitchMessagePing|False:
    if content[0] == "PING":
        # construct the ping message again as this has to be sent to TWITCH again
        return TwitchMessagePing(text=" ".join(content[1:]))
    return False

def _find_bot_only(content:list[str],message:str, bot_name:str) -> TwitchMessageOnlyForBot|False:
    if content[0] == ":tmi.twitch.tv":
        return TwitchMessageOnlyForBot(text=message)
    elif content[0] == f":{bot_name}!{bot_name}@{bot_name}.tmi.twitch.tv":
        return TwitchMessageOnlyForBot(text=message)
    elif content[0] == f":{bot_name}.tmi.twitch.tv":
        return TwitchMessageOnlyForBot(text=message)
    elif not message: # content is empty
        return TwitchMessageOnlyForBot()
    return False

TAG_MAPPING:dict[str:Callable] = {
    "@badge-info": lambda tm, tag_value: setattr(tm, "badge_info", tag_value),
    "badges": lambda tm, tag_value: setattr(tm, "badges", tag_value),
    "client-nonce": lambda tm, tag_value: setattr(tm, "client_nonce", tag_value),
    "color": lambda tm, tag_value: setattr(tm, "color", HEX(tag_value)),
    "display-name": lambda tm, tag_value: setattr(tm, "display_name", tag_value),
    "emotes": lambda tm, tag_value: setattr(tm, "emotes", tag_value),
    "first-msg": lambda tm, tag_value: setattr(tm, "first_msg", bool(tag_value)),
    "flags": lambda tm, tag_value: setattr(tm, "flags", tag_value),
    "id": lambda tm, tag_value: setattr(tm, "message_id", tag_value),
    "mod": lambda tm, tag_value: setattr(tm, "mod", bool(tag_value)),
    "room-id": lambda tm, tag_value: setattr(tm, "room_id", tag_value),
    "subscriber": lambda tm, tag_value: setattr(tm, "subscriber", bool(tag_value)),
    "tmi-sent-ts": lambda tm, tag_value: setattr(tm, "tmi_sent_ts", int(tag_value)),
    "turbo": lambda tm, tag_value: setattr(tm, "turbo", bool(tag_value)),
    "user-id": lambda tm, tag_value: setattr(tm, "user_id", int(tag_value)),
    "user-type": lambda tm, tag_value: setattr(tm, "user_type", tag_value),
}

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def twitch_message_constructor_tags(message_bytes:bytearray, bot_name:str) -> TwitchMessage:
    print(message_bytes)
    message = message_bytes.decode("UTF_8")
    content = message.split(" ")

    # Certain twitch sent messages have a different consistency than a regular user sent message
    #   If this happens, this has to be caught before the message is parsed further
    if ping_message := _find_PING(content):
        return ping_message

    if bot_only_message := _find_bot_only(content, message, bot_name):
        return bot_only_message

    # with tags enabled, we know that the first element of the list above contains all the user's tags
    #   This enables us to loop them and assign them to the message
    #   This is done to make them accessible to the command parsing
    # The second part of the split message is the user definement. The user id is found in the tags
    # IRC message string is found next
    # The channel from which it is sent is also recieved.
    #   When the bot is only installed in one channel, this isn't usefull, but if a bot is used in multiple channels
    #   this is part of the usefull known context
    # Finally all text should be clumped together again, to be searched though for a custom command
    #   This is to be done by the protocol class, not the message constructir

    tags, user, irc_message, channel, *text = content
    twitch_message:TwitchMessage = TwitchMessage(
        message=message,
        message_type=irc_message,
        channel=channel,
        user=user,
        text=" ".join(text).replace(":", "", 1) #only remove the first ":"
    )


    for tag in tags.split(";"):
        # dict mapping is easier than a whole IF-ELSE or match case check
        tag_name, tag_value = tag.split("=")
        try:
            TAG_MAPPING[tag_name](tm=twitch_message,tag_value=tag_value)
        except KeyError:
            print(StyleNest.Bold(ForeNest.Maroon(f"Unkown tag of '{tag_name}' found. Please create a bug report on the git repo")))
            pass

    return twitch_message