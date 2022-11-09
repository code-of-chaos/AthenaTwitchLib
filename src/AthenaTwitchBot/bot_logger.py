# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import functools
from dataclasses import dataclass
import aiosqlite
import pathlib
from typing import ClassVar
import contextlib
import base64

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
_output_enabled:bool=True

def output_if_enabled(fnc):
    """
    Simple decorator used by the BotLogger
    Meant to reduce the repetition of writing if checks
    """
    @functools.wraps(fnc)
    async def wrapper(*args, **kwargs):
        global _output_enabled
        if not _output_enabled:
            return None
        return await fnc(*args, **kwargs)
    return wrapper

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotLogger:
    """
    Master class to handle all logging calls to the sqlite database file.
    """
    path:pathlib.Path

    # Non Init stuff
    logger:ClassVar[BotLogger] = None

    @classmethod
    def set_logger(cls, /,*,output_enabled:bool=True, **kwargs):
        """
        Simple class-method to define the .logger attribute of the BotLogger class
        """
        global _output_enabled
        _output_enabled = output_enabled

        cls.logger = cls(**kwargs)

    @contextlib.asynccontextmanager
    async def _db_connect(self) -> aiosqlite.Connection:
        """
        Async Context manager to easily connect to the database
        Commits all changes to the db, before closing the connection
        """
        async with aiosqlite.connect(self.path) as db:
            yield db
            await db.commit()

    @output_if_enabled
    async def create_tables(self) -> None:
        """
        Method is run by the `bot_constructor` on startup, as it creates the tables the logger needs,
        but only if they don't exist already
        """
        async with self._db_connect() as db:
            await db.execute(f"""
                CREATE TABLE IF NOT EXISTS `called_handlers`  (
                    `id` INTEGER PRIMARY KEY,
                    `handler_name` TEXT NOT NULL
                );
            """)

            await db.execute(f"""
                CREATE TABLE IF NOT EXISTS `unknown_tags`  (
                    `id` INTEGER PRIMARY KEY,
                    `tag_type` TEXT NOT NULL,
                    `tag_name` TEXT NOT NULL,
                    `tag_value` TEXT NOT NULL
                );
            """)

            await db.execute(f"""
                CREATE TABLE IF NOT EXISTS `unknown_message`  (
                    `id` INTEGER PRIMARY KEY,
                    `text` TEXT NOT NULL
                );
            """)

    @output_if_enabled
    async def log_handler_called(self, handler_name:str):
        """
        Logs that a protocol line handler has been called
        """
        async with self._db_connect() as db:
            await db.execute(f"""
                INSERT INTO called_handlers (handler_name)
                VALUES ('{handler_name}');
            """)

    @output_if_enabled
    async def log_unknown_tag(self, tag_type:str, tag_name:str, tag_value:str):
        """
        Logs that an unknown irc tag to the AthenaTwitchBot was found
        """
        async with self._db_connect() as db:
            await db.execute(f"""
                INSERT INTO unknown_tags (tag_type,tag_name, tag_value)
                VALUES ('{tag_type}','{tag_name}', '{tag_value}');
            """)

    @output_if_enabled
    async def log_unknown_message(self, message:str):
        """
        Logs that an unknown irc tag to the AthenaTwitchBot was found
        """
        async with self._db_connect() as db:
            await db.execute(f"""
                INSERT INTO unknown_message (text)
                VALUES ('{base64.b64encode(message.encode()).decode()}');
            """)
