# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import aiosqlite
import pathlib
from typing import Optional
import contextlib
import enum

# Athena Packages

# Local Imports

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
_bot_logger:Optional[BotLogger] = None

def get_bot_logger() -> BotLogger:
    global _bot_logger
    if _bot_logger is None:
        raise ValueError("No Bot Logger was setup")
    return _bot_logger

def set_bot_logger(bot_logger:BotLogger):
    global _bot_logger
    _bot_logger = bot_logger
    return _bot_logger
# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class BotLogger:
    path:pathlib.Path
    output_enabled:bool = True

    # Non init

    @contextlib.asynccontextmanager
    async def _db_connect(self) -> aiosqlite.Connection:
        async with aiosqlite.connect(self.path) as db:
            yield db
            await db.commit()

    async def connect(self) -> None:
        if not self.output_enabled:
            return

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

    async def log_handler_called(self, handler_name:str):
        async with self._db_connect() as db:
            await db.execute(f"""
                INSERT INTO called_handlers (handler_name)
                VALUES ('{handler_name}');
            """)

    async def log_unknown_tag(self, tag_type:str, tag_name:str, tag_value:str):
        async with self._db_connect() as db:
            await db.execute(f"""
                INSERT INTO unknown_tags (tag_type,tag_name, tag_value)
                VALUES ('{tag_type}','{tag_name}', '{tag_value}');
            """)
