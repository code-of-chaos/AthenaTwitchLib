# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library

# Custom Packages

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

    @classmethod
    def new_from_dict(cls, data:dict) -> TwitchApiUser:
        obj = cls()
        for k,v in data.items():
            setattr(obj, k, v)
        return obj
