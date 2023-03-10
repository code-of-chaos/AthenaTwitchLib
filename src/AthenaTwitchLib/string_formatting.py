# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def twitch_irc_output_format(text:str) -> bytes:
    """
    Formats the string into the correct byte;, ; structure expected by the Twitch IRC
    """
    #TODO make the "new line" raise a specific error for the library to handle
    #   Given twitch doesn't parse new lines in texts, this shouldn't be allowed on our end
    text_flat:str = text.replace('\r\n',' ').replace('\n',' ')
    return f"{text_flat}\r\n".encode("utf_8")
