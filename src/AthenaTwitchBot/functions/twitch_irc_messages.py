# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
def prep_message(message:str) -> bytes:
    return f"{message}\r\n".encode("UTF_8")
# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
nick = lambda nickname: prep_message(f"NICK {nickname}")
password = lambda oauth_token: prep_message(f"PASS oauth:{oauth_token}")
join = lambda channel: prep_message(f"JOIN #{channel}")
pong = lambda message: prep_message(f"PONG {message}")

request_commands = prep_message("CAP REQ :twitch.tv/commands")
request_membership = prep_message("CAP REQ :twitch.tv/membership")
request_tags = prep_message("CAP REQ :twitch.tv/tags")