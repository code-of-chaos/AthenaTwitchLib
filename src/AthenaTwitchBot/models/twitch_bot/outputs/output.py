# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import abc

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.message_context import MessageContext

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Output(abc.ABC):
    """
    An abstract class to define which structure the output classes should use
    """
    async def output(self, context:MessageContext,**kwargs):
        """
        Output a context the correct end state
        """