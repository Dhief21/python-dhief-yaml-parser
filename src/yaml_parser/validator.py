from __future__ import annotations

from typing import Any

from .errors import ValidationError
from .schema import ALLOWED_LOG_LEVELS, DATABASE_SCHEMA, ROOT_SCHEMA


def _is_int(value: Any) -> bool:
    # bool is a subclass of int in Python, but it is not a valid integer here.
    return isinstance(value, int) and not isinstance(value, bool)


def validate_sections(sections: dict[str, dict[str, Any]]) -> list[ValidationError]:
    errors: list[ValidationError] = []

    for section_name, section in sections.items():
        errors.extend(_validate_unknown_keys(section_name, section))
        errors.extend(_validate_root_fields(section_name, section))

    return errors


def _validate_unknown_keys(section_name: str, section: dict[str, Any]) -> list[ValidationError]:
    errors: list[ValidationError] = []

    for key in section:
        if key not in ROOT_SCHEMA:
            errors.append(ValidationError(section_name, key, "chave desconhecida"))

    database = section.get("database")
    if isinstance(database, dict):
        for key in database:
            if key not in DATABASE_SCHEMA:
                errors.append(ValidationError(section_name, f"database.{key}", "chave desconhecida"))

    return errors


def _validate_root_fields(section_name: str, section: dict[str, Any]) -> list[ValidationError]:
    errors: list[ValidationError] = []

    app_name = section.get("app_name")
    if not isinstance(app_name, str) or not app_name.strip():
        errors.append(ValidationError(section_name, "app_name", "deve ser string nao vazia"))

    debug = section.get("debug")
    if not isinstance(debug, bool):
        errors.append(ValidationError(section_name, "debug", "deve ser boolean"))

    max_connections = section.get("max_connections")
    if not _is_int(max_connections):
        errors.append(ValidationError(section_name, "max_connections", "deve ser inteiro"))
    elif not 1 <= max_connections <= 1000:
        errors.append(ValidationError(section_name, "max_connections", "fora do intervalo (1..1000)"))

    timeout_seconds = section.get("timeout_seconds")
    if not _is_int(timeout_seconds):
        errors.append(ValidationError(section_name, "timeout_seconds", "deve ser inteiro"))
    elif not 1 <= timeout_seconds <= 300:
        errors.append(ValidationError(section_name, "timeout_seconds", "fora do intervalo (1..300)"))

    log_level = section.get("log_level")
    if not isinstance(log_level, str):
        errors.append(ValidationError(section_name, "log_level", "deve ser string"))
    elif log_level not in ALLOWED_LOG_LEVELS:
        errors.append(
            ValidationError(
                section_name,
                "log_level",
                "valor invalido; permitido: INFO, DEBUG, WARNING, ERROR",
            )
        )

    database = section.get("database")
    if not isinstance(database, dict):
        errors.append(ValidationError(section_name, "database", "deve ser objeto"))
    else:
        errors.extend(_validate_database_fields(section_name, database))

    return errors


def _validate_database_fields(section_name: str, database: dict[str, Any]) -> list[ValidationError]:
    errors: list[ValidationError] = []

    host = database.get("host")
    if not isinstance(host, str) or not host.strip():
        errors.append(ValidationError(section_name, "database.host", "deve ser string nao vazia"))

    port = database.get("port")
    if not _is_int(port):
        errors.append(ValidationError(section_name, "database.port", "deve ser inteiro"))
    elif not 1 <= port <= 65535:
        errors.append(ValidationError(section_name, "database.port", "fora do intervalo (1..65535)"))

    pool_size = database.get("pool_size")
    if not _is_int(pool_size):
        errors.append(ValidationError(section_name, "database.pool_size", "deve ser inteiro"))
    elif not 1 <= pool_size <= 100:
        errors.append(ValidationError(section_name, "database.pool_size", "fora do intervalo (1..100)"))

    return errors
