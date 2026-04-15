from __future__ import annotations

ALLOWED_LOG_LEVELS = {"INFO", "DEBUG", "WARNING", "ERROR"}

ROOT_SCHEMA = {
    "app_name",
    "debug",
    "max_connections",
    "timeout_seconds",
    "log_level",
    "database",
    "_inherits",
}

DATABASE_SCHEMA = {
    "host",
    "port",
    "pool_size",
}
