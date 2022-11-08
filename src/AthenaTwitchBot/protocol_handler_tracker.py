# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import aiofiles
import asyncio
import pathlib
import json
from typing import Callable, Any
import functools

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
path = pathlib.Path("data/protocol_handler_tracker.json")
if not path.exists():
    with open(path, "w") as _file:
        json.dump({}, _file)

async def _json(fnc:Callable) -> None:
    global path

    async with aiofiles.open(path, "r") as file:
        data = json.loads(await file.read())

    with open(path, "w") as file:
        if (keyword := fnc.__name__) in data:
            data[keyword] += 1
        else:
            data[keyword] = 1

        json.dump(data, file, indent=2)

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def track_handler(fnc:Callable) -> Any:
    """
    Simple decorator to keep track of how many calls are made to handlers
    """
    @functools.wraps(fnc)
    async def wrapper(*args, **kwargs):
        result, _ = await asyncio.gather(
            fnc(*args, **kwargs),
            _json(fnc)
        )
        return result

    return wrapper

