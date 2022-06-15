# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from abc import ABC, abstractmethod

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_message import TwitchMessage

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Output(ABC):

    @abstractmethod
    def pre_launch(self):
        """Output the state of the application before anything is run"""
    @abstractmethod
    def message(self, message:TwitchMessage):
        """Output of a received message"""

    @abstractmethod
    def undefined(self,message=None):
        """Output anything that is supposed to be undefined (this should eventually not be present anymore)"""