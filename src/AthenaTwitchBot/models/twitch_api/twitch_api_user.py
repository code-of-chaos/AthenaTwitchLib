# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaTwitchBot.data.twitch_api_scopes import TwitchApiScopes

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class TwitchApiUser:
    id:str=None
    login:str=None
    display_name:str=None
    type:str=None
    broadcaster_type:str=None
    description:str=None
    profile_image_url:str=None
    offline_image_url:str=None
    view_count:int=None
    email:str=None
    created_at:str=None

    scopes:set[TwitchApiScopes]=None

    @classmethod
    def new_from_dict(cls, data:dict) -> TwitchApiUser:
        obj = cls()
        for k,v in data.items():
            setattr(obj, k, v)
        return obj

    def set_scopes(self, data:list[str]) -> TwitchApiUser:
        scopes_string_mapping = TwitchApiScopes.string_mapping()
        self.scopes = set(scopes_string_mapping[scope] for scope in data)
        return self

