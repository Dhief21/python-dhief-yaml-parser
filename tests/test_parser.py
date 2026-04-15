from yaml_parser.resolver import resolve_inheritance
from yaml_parser.service import parse_and_validate
from yaml_parser.validator import validate_sections


def test_resolve_inheritance_deep_merge():
    raw = {
        "base": {
            "app_name": "api",
            "debug": False,
            "max_connections": 100,
            "timeout_seconds": 30,
            "log_level": "INFO",
            "database": {"host": "localhost", "port": 5432, "pool_size": 10},
        },
        "staging": {
            "_inherits": "base",
            "debug": True,
            "database": {"host": "staging-db"},
        },
    }

    resolved, errors = resolve_inheritance(raw)

    assert not errors
    assert resolved["staging"]["debug"] is True
    assert resolved["staging"]["database"]["host"] == "staging-db"
    assert resolved["staging"]["database"]["port"] == 5432
    assert resolved["staging"]["database"]["pool_size"] == 10


def test_resolve_inheritance_cycle_and_missing_parent():
    raw = {
        "a": {"_inherits": "b", "debug": True},
        "b": {"_inherits": "a", "debug": False},
        "c": {"_inherits": "missing"},
    }

    _resolved, errors = resolve_inheritance(raw)

    messages = [e.message for e in errors]
    assert any("ciclo de heranca" in msg for msg in messages)
    assert any("secao pai inexistente" in msg for msg in messages)


def test_validate_unknown_key_type_and_range_errors():
    sections = {
        "experimental": {
            "app_name": "api",
            "debug": True,
            "max_connections": "cinquenta",
            "timeout_seconds": 9999,
            "log_level": "VERBOSE",
            "unknown_setting": True,
            "database": {"host": "db", "port": 5432, "pool_size": 5},
        }
    }

    errors = validate_sections(sections)
    fields = [e.field for e in errors]

    assert "unknown_setting" in fields
    assert "max_connections" in fields
    assert "timeout_seconds" in fields
    assert "log_level" in fields


def test_validate_rejects_boolean_as_integer():
    sections = {
        "base": {
            "app_name": "api",
            "debug": False,
            "max_connections": True,
            "timeout_seconds": 30,
            "log_level": "INFO",
            "database": {
                "host": "db",
                "port": 5432,
                "pool_size": True,
            },
        }
    }

    errors = validate_sections(sections)
    fields = [e.field for e in errors]

    assert "max_connections" in fields
    assert "database.pool_size" in fields


def test_parse_and_validate_official_case_file():
    resolved, errors = parse_and_validate("examples/input_case.yaml")

    assert "base" in resolved
    assert "staging" in resolved
    assert "production" in resolved
    assert "experimental" in resolved

    formatted = [f"{e.section}.{e.field}:{e.message}" for e in errors]

    assert any("staging.max_connections:deve ser inteiro" in msg for msg in formatted)
    assert any("production.timeout_seconds:fora do intervalo (1..300)" in msg for msg in formatted)
    assert any("production.log_level:valor invalido" in msg for msg in formatted)
    assert any("experimental.unknown_setting:chave desconhecida" in msg for msg in formatted)
    assert any("experimental.timeout_seconds:fora do intervalo (1..300)" in msg for msg in formatted)
    assert any("_inherits:ciclo de heranca detectado" in msg for msg in formatted)
