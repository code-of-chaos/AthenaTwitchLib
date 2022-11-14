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

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
_logging_enabled:bool=True
_log_all_messages:bool=False

def output_if_enabled(fnc):
    """
    Simple decorator used by the BotLogger
    Meant to reduce the repetition of writing if checks
    """
    @functools.wraps(fnc)
    async def wrapper(*args, **kwargs):
        global _logging_enabled
        if not _logging_enabled:
            return None
        return await fnc(*args, **kwargs)
    return wrapper

def sanitize_sql(txt:str) -> str:
    """
    Simple function to sanitize the sql input
    """
    return txt.replace("'", "''")

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotLogger:
    """
    Master class to handle all logging calls to the sqlite database file.
    """
    path:pathlib.Path
    logging_enabled:bool=False
    log_all_messages:bool=False

    # Non Init stuff
    logger:ClassVar[BotLogger] = None

    @classmethod
    def set_logger(cls, **kwargs):
        cls.logger = BotLogger(**kwargs)

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

            await db.execute(f"""
                CREATE TABLE IF NOT EXISTS `handled_message`  (
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
                VALUES ('{sanitize_sql(handler_name)}');
            """)

    @output_if_enabled
    async def log_unknown_tag(self, tag_type:str, tag_name:str, tag_value:str):
        """
        Logs that an unknown irc tag to the AthenaTwitchBot was found
        """
        async with self._db_connect() as db:
            await db.execute(f"""
                INSERT INTO unknown_tags (tag_type,tag_name, tag_value)
                VALUES ('{sanitize_sql(tag_type)}','{sanitize_sql(tag_name)}', '{sanitize_sql(tag_value)}');
            """)

    @output_if_enabled
    async def log_unknown_message(self, message:str):
        """
        Logs that an unknown irc tag to the AthenaTwitchBot was found
        """
        async with self._db_connect() as db:
            await db.execute(f"""
                INSERT INTO unknown_message (text)
                VALUES ('{sanitize_sql(message)}');
            """)

    @output_if_enabled
    async def log_handled_message(self, line:str):
        """
        Logs that an unknown irc tag to the AthenaTwitchBot was found
        """
        async with self._db_connect() as db:
            await db.execute(f"""
                INSERT INTO handled_message (text)
                VALUES ('{sanitize_sql(line)}');
            """)
