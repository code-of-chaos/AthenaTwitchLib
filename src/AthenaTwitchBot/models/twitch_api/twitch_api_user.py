# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from collections.abc import Mapping
from typing import Any
from typing import Self

# Custom Library

# Custom Packages
from AthenaTwitchBot.data.twitch_api_scopes import TwitchApiScopes

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class TwitchApiUser:
    id:str | None = None
    login:str | None = None
    display_name:str | None = None
    type:str | None = None
    broadcaster_type:str | None = None
    description:str | None = None
    profile_image_url:str | None = None
    offline_image_url:str | None = None
    view_count:int | None = None
    email:str | None = None
    created_at:str | None = None

    scopes:set[TwitchApiScopes] | None = None

    # `data` actually should have a type like Mapping[str, str | None]: type checker issue
    @classmethod
    def new_from_dict(cls, data:Mapping[str, Any]) -> Self:  # type: ignore[valid-type]
        return cls(**data)

    def set_scopes(self, data:list[str]) -> TwitchApiUser:
        scopes_string_mapping = TwitchApiScopes.string_mapping()
        self.scopes = set(scopes_string_mapping[scope] for scope in data)
        return self

