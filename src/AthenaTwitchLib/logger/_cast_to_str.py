# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import dataclasses
import json
from typing import Any

# Athena Packages

# Local Imports
from AthenaTwitchLib.api.data.enums import HttpMethod, DataFromConnection, TokenScope
from AthenaTwitchLib.api.data.urls import TwitchApiUrl

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        match o:
            case HttpMethod() | DataFromConnection() | TokenScope() | TwitchApiUrl():
                return o.value
            case set():
                return list(o)
            case _:
                print(o)
                return super(CustomJsonEncoder, self).default(o)

def api_cast_to_str(obj:Any) -> str:
    if dataclasses.is_dataclass(obj):
        return json.dumps(dataclasses.asdict(obj), cls=CustomJsonEncoder)
    return str(obj)