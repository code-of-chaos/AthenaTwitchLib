# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import pathlib
import json
from typing import Callable
import functools

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
path = pathlib.Path("data/protocol_handler_tracker.json")
if not path.exists():
    with open(path, "w") as _file:
        json.dump({}, _file)

def track_handler(fnc:Callable):
    """
    Simple decorator to keep track of how many calls are made to handlers
    """
    @functools.wraps(fnc)
    def wrapper(*args, **kwargs):
        global path

        with open(path, "r") as file:
            data = json.load(file)

        with open(path, "w") as file:
            if (keyword:=fnc.__name__) in data:
                data[keyword] += 1
            else:
                data[keyword] = 1

            json.dump(data, file, indent=2)

        return fnc(*args, **kwargs)

    return wrapper

