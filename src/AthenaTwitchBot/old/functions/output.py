# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.outputs.abstract_output import AbstractOutput

# ----------------------------------------------------------------------------------------------------------------------
# - All -
# ----------------------------------------------------------------------------------------------------------------------
__all__ = [
    "output_connection_made", "output_connection_ping", "output_undefined", "output_scheduled_task", "output_reply",
    "output_write"
]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
async def output_connection_made(output:AbstractOutput, **kwargs):
    await output.connection_made(**kwargs)

async def output_connection_ping(output:AbstractOutput, **kwargs):
    await output.connection_ping(**kwargs)

async def output_undefined(output:AbstractOutput, **kwargs):
    await output.undefined(**kwargs)

async def output_scheduled_task(output:AbstractOutput, **kwargs):
    await output.scheduled_task(**kwargs)
async def output_write(output:AbstractOutput, **kwargs):
    await output.write(**kwargs)
async def output_reply(output:AbstractOutput, **kwargs):
    await output.reply(**kwargs)