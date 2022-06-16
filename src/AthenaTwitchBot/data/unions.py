# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Union

# Custom Library

# Custom Packages
from AthenaTwitchBot.functions.output import *
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
OUTPUT_CALLBACKS = Union[output_connection_made,output_connection_ping,output_undefined] # does this even work?
CHANNEL = str | TwitchChannel
CHANNELS = list[CHANNEL]