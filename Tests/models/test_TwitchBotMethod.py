# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import unittest

# Custom Library
from AthenaTwitchBot.models.twitch_bot_method import TwitchBotMethod
from AthenaTwitchBot.models.twitch_channel import TwitchChannel

# Custom Packages
from Tests.support import EmptyBot

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
class TestBot_0(EmptyBot):
    @TwitchBotMethod().command(names="help")
    def command_help(self):
        return "not helping"

class TestBot_1(EmptyBot):
    def __init__(self):
        self.name = "TestBot_1"
        super(TestBot_1, self).__init__()

    @TwitchBotMethod(channels=["some_channel"]).command(names="help")
    def command_help(self):
        return f"{self.name}"

class TestBot_2(EmptyBot):
    @TwitchBotMethod.command(names="help")
    def command_help(self):
        return "not helping"

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Test_TwitchBotMethod(unittest.TestCase):
    def test_Bot0(self):
        test_bot0 = TestBot_0()

        self.assertEqual(
            [],
            test_bot0.command_help.channels
        )

        self.assertEqual(
            "not helping",
            test_bot0.command_help.callback()
        )

    def test_Bot1(self):
        test_bot1 = TestBot_1()
        self.assertEqual(
            [TwitchChannel("some_channel")],
            test_bot1.command_help.channels
        )
        self.assertIs(
            test_bot1,
            test_bot1.command_help.owner
        )
        self.assertEqual(
            test_bot1.name,
            test_bot1.command_help.callback()
        )

    def test_Bot2(self):
        test_bot2 = TestBot_2()
        self.assertEqual(
            [],
            test_bot2.command_help.channels
        )

