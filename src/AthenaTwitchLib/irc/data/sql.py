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
TBL_LOGIC_COMMANDS = f"""
CREATE TABLE IF NOT EXISTS `commands`  (
    `id` INTEGER PRIMARY KEY,                               -- internal id
    `channel` TEXT NOT NULL,
    `command_name` TEXT NOT NULL,                           -- ![command_name]
    `command_arg` TEXT NOT NULL DEFAULT '*',                -- if this specific arg is present, execute this record, else everything is allowed
    `command_type` TEXT NOT NULL,                           -- Type of command, means it has extra logic attached to it
    `allow_user` INTEGER NOT NULL DEFAULT TRUE,
    `allow_sub` INTEGER NOT NULL DEFAULT FALSE,
    `allow_vip` INTEGER NOT NULL DEFAULT FALSE,
    `allow_mod` INTEGER NOT NULL DEFAULT FALSE,
    `allow_broadcaster` INTEGER NOT NULL DEFAULT FALSE,
    `output_text` TEXT DEFAULT NULL,                        -- text to output in chat
    `output_type` TEXT NOT NULL DEFAULT 'write'             -- reply or write output
);
"""
