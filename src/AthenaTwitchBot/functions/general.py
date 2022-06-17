# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def channel_list_to_TwitchChannels(channels:list[str|TwitchChannel]) -> list[TwitchChannel]:
    return [
        TwitchChannel(channel) if not isinstance(channel, TwitchChannel) else channel
        for channel in channels
    ]

def cleanup_text(text:str) -> str:
    return text.replace("\n", " ")