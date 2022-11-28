# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field, InitVar

# Athena Packages

# Local Imports
from AthenaTwitchLib.api.data.enums import TokenScope

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class TokenData:
    client_id:str
    login:str
    user_id:str
    expires_in:int
    scopes:InitVar[list[str]]

    # non init
    _scopes:set[TokenScope] = field(init=False, default_factory=set)

    @property
    def scopes(self):
        return self._scopes

    def __post_init__(self,scopes:list[str]):
        self._scopes = {TokenScope(scope) for scope in scopes}
