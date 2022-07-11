# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaTwitchBot.models.twitch_channel import TwitchChannel
from AthenaTwitchBot.models.twitch_bot_method import TwitchBotMethod

from AthenaTwitchBot.functions.general import channel_list_to_TwitchChannels

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True,eq=False,order=False,kw_only=True)
class TwitchBot:
    nickname:str
    oauth_token:str
    channels:list[TwitchChannel|str]
    prefix:str

    # Twitch-specific capabilities : https://dev.twitch.tv/docs/irc/capabilities
    twitch_capability_commands:bool=False
    twitch_capability_membership:bool=False
    twitch_capability_tags:bool=True # only one that has the default set to true, as this is required to make reply's work

    # noinspection PyDataclass
    commands:dict[str:TwitchBotMethod]=field(init=False)
    scheduled_tasks:list[TwitchBotMethod]=field(init=False)

    # non init slots


    # ------------------------------------------------------------------------------------------------------------------
    # - init -
    # ------------------------------------------------------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        cls.commands = {}
        cls.scheduled_tasks = []
        twitch_bot_obj = super(TwitchBot, cls).__new__(cls,*args,**kwargs)

        # store commands, tasks, etc...
        #   Done for ease of use
        for k,v in cls.__dict__.items():
            if isinstance(v,TwitchBotMethod):
                v.owner = twitch_bot_obj
                if v.is_command:
                    for name in v.command_names:
                        twitch_bot_obj.commands[name] = v
                if v.is_scheduled_task:
                    twitch_bot_obj.scheduled_tasks.append(v)

        return twitch_bot_obj

    def __post_init__(self):
        # format every channel into the correct model
        self.channels = channel_list_to_TwitchChannels(self.channels)