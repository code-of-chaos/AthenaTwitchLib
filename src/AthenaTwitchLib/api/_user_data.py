# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, frozen=True)
class UserData:
    id:str
    login:str
    display_name:str
    type:str
    broadcaster_type:str
    description:str
    profile_image_url:str
    offline_image_url:str
    view_count:str
    email:str
    created_at:str