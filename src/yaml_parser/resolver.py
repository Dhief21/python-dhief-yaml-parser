from __future__ import annotations

from copy import deepcopy
from typing import Any

from .errors import ValidationError


def resolve_inheritance(config: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[ValidationError]]:
   
    resolved: dict[str, dict[str, Any]] = {}
    errors: list[ValidationError] = []
    visiting: set[str] = set()

    def merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
        result = deepcopy(base)
        for key, value in override.items():
            if key == "_inherits":
                continue
            if isinstance(value, dict) and isinstance(result.get(key), dict):
                result[key] = merge_dicts(result[key], value)
            else:
                result[key] = deepcopy(value)
        return result

    def resolve_section(section_name: str) -> dict[str, Any] | None:
        if section_name in resolved:
            return resolved[section_name]

        raw = config.get(section_name)
        if not isinstance(raw, dict):
            errors.append(
                ValidationError(section_name, "_section", "secao deve ser um objeto")
            )
            return None

        if section_name in visiting:
            errors.append(
                ValidationError(section_name, "_inherits", "ciclo de heranca detectado")
            )
            return None

        visiting.add(section_name)
        parent_name = raw.get("_inherits")

        if parent_name is None:
            base = {}
        elif not isinstance(parent_name, str):
            errors.append(
                ValidationError(section_name, "_inherits", "deve ser string")
            )
            base = {}
        elif parent_name not in config:
            errors.append(
                ValidationError(
                    section_name,
                    "_inherits",
                    f"secao pai inexistente: {parent_name}",
                )
            )
            base = {}
        else:
            parent_resolved = resolve_section(parent_name)
            base = parent_resolved if parent_resolved is not None else {}

        current = merge_dicts(base, raw)
        visiting.remove(section_name)
        resolved[section_name] = current
        return current

    for name in config:
        resolve_section(name)

    return resolved, errors
