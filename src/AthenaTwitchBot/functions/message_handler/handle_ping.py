# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.message_context import MessageContext
from AthenaTwitchBot.data.message_flags import MessageFlags

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
async def handle_ping(context:MessageContext, ping_response:str) -> None:
    """
    A simple handler to correctly set a response to the Twitch PING command

    Parameters:
    - context:
    - ping_response:
    """
    context.flag = MessageFlags.ping # use special flag to make sure the output parse knows wha to do
    context.output = " ".join(f"PONG {ping_response}")