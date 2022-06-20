# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import unittest

# Custom Library
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class TestTwitchChannel(unittest.TestCase):
    def test_general(self):
        self.assertEqual(
            "#directiveathena",
            str(TwitchChannel("directiveathena"))
        )
        self.assertEqual(
            "#directiveathena",
            str(TwitchChannel("#directiveathena"))
        )
        with self.assertRaises(ValueError):
            TwitchChannel("this is not going to work")