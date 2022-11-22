# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import enum

# Athena Packages
from AthenaLib.logging import AthenaSqliteLogger

# Local Imports
from AthenaTwitchLib.string_formatting import sanitize_sql

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
class TwitchLoggerType(enum.StrEnum):
    IRC = enum.auto()
    API = enum.auto()

SQL_CREATE_TABLES:list[str] = [
f"""
CREATE TABLE IF NOT EXISTS `called_handlers`  (
    `id` INTEGER PRIMARY KEY,
    `handler_name` TEXT NOT NULL
);
""", f"""
CREATE TABLE IF NOT EXISTS `unknown_tags`  (
    `id` INTEGER PRIMARY KEY,
    `tag_type` TEXT NOT NULL,
    `tag_name` TEXT NOT NULL,
    `tag_value` TEXT NOT NULL
);
""", f"""
CREATE TABLE IF NOT EXISTS `unknown_message`  (
    `id` INTEGER PRIMARY KEY,
    `text` TEXT NOT NULL
);
""", f"""
CREATE TABLE IF NOT EXISTS `handled_message`  (
    `id` INTEGER PRIMARY KEY,
    `text` TEXT NOT NULL
);
"""
]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class IrcLogger(AthenaSqliteLogger):

    async def create_tables(self):
        """
        Method is run by the `bot_constructor` on startup, as it creates the tables the logger needs,
        but only if they don't exist already
        """
        with self.if_enabled():
            async with self._db_connect() as db:
                for sql in SQL_CREATE_TABLES:
                    await db.execute(sql)

    async def log_handler_called(self, handler_name:str):
        """
        Logs that a protocol line handler has been called
        """
        with self.if_enabled():
            async with self._db_connect() as db:
                await db.execute(f"""
                    INSERT INTO called_handlers (handler_name)
                    VALUES ('{sanitize_sql(handler_name)}');
                """)

    async def log_unknown_tag(self, tag_type:str, tag_name:str, tag_value:str):
        """
        Logs that an unknown irc tag to the AthenaTwitchLib was found
        """
        with self.if_enabled():
            async with self._db_connect() as db:
                await db.execute(f"""
                    INSERT INTO unknown_tags (tag_type,tag_name, tag_value)
                    VALUES ('{sanitize_sql(tag_type)}','{sanitize_sql(tag_name)}', '{sanitize_sql(tag_value)}');
                """)

    async def log_unknown_message(self, message:str):
        """
        Logs that an unknown irc tag to the AthenaTwitchLib was found
        """
        with self.if_enabled():
            async with self._db_connect() as db:
                await db.execute(f"""
                    INSERT INTO unknown_message (text)
                    VALUES ('{sanitize_sql(message)}');
                """)

    async def log_handled_message(self, line:str):
        """
        Logs that an unknown irc tag to the AthenaTwitchLib was found
        """
        with self.if_enabled():
            async with self._db_connect() as db:
                await db.execute(f"""
                    INSERT INTO handled_message (text)
                    VALUES ('{sanitize_sql(line)}');
                """)