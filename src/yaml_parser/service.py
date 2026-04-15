from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import ValidationError
from .loader import load_yaml_file
from .resolver import resolve_inheritance
from .validator import validate_sections


def parse_and_validate_detailed(
    path: str | Path,
) -> tuple[dict[str, dict[str, Any]], list[ValidationError], list[ValidationError]]:
    raw = load_yaml_file(path)
    resolved, resolve_errors = resolve_inheritance(raw)
    validation_errors = validate_sections(resolved)

    resolve_errors = sorted(
        resolve_errors,
        key=lambda err: (err.section, err.field, err.message),
    )
    validation_errors = sorted(
        validation_errors,
        key=lambda err: (err.section, err.field, err.message),
    )
    return resolved, resolve_errors, validation_errors


def parse_and_validate(path: str | Path) -> tuple[dict[str, dict[str, Any]], list[ValidationError]]:
    resolved, resolve_errors, validation_errors = parse_and_validate_detailed(path)
    all_errors = resolve_errors + validation_errors
    return resolved, all_errors
