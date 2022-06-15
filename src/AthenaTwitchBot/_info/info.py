# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
# noinspection PyProtectedMember
import AthenaLib._info.formatting as f
from AthenaTwitchBot._info._v import VERSION

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def info(*, to_str: bool = False) -> None | str:
    # todo needs a lot of work
    line = "-" * 128
    header = f.header(f"""{line}
{f.title("AthenaTwitchBot", to_str)} v{VERSION}
is made by Andreas Sas.
{line}
""", to_str)

    body = f"""
Package setup:
    {f.sub_modules("data", to_str)} : ...
    {f.sub_modules("decorators", to_str)} : ...
    {f.sub_modules("functions", to_str)} : ...
    {f.sub_modules("models", to_str)} : ...
"""

    text = f"{header}{body}{line}"

    # export to console or string
    if to_str:
        return text
    else:
        print(text)