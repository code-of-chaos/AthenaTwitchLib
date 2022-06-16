# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.outputs.output import Output

# ----------------------------------------------------------------------------------------------------------------------
# - All -
# ----------------------------------------------------------------------------------------------------------------------
__all__ = [
    "output_connection_made", "output_connection_ping", "output_undefined"
]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
async def output_connection_made(output:Output, **kwargs):
    await output.connection_made(**kwargs)

async def output_connection_ping(output:Output, **kwargs):
    await output.connection_ping(**kwargs)

async def output_undefined(output:Output, **kwargs):
    await output.undefined(**kwargs)