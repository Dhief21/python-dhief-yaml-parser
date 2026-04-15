from __future__ import annotations

import argparse
import json

from .errors import format_error
from .service import parse_and_validate_detailed


def main() -> int:
    parser = argparse.ArgumentParser(description="Parser YAML com heranca e validacao")
    parser.add_argument("path", help="Caminho do arquivo YAML")
    args = parser.parse_args()

    try:
        resolved, resolve_errors, validation_errors = parse_and_validate_detailed(args.path)
    except FileNotFoundError:
        print(f"Erro: arquivo nao encontrado: {args.path}")
        return 2
    except ValueError as exc:
        print(f"Erro: {exc}")
        return 2

    total_errors = len(resolve_errors) + len(validation_errors)

    print("----------------------------Resumo---------------------------------")
    print(f"- Ambientes resolvidos: {len(resolved)}")
    print(f"- Total de erros: {total_errors}")
    print(f"- Erros de heranca/resolucao: {len(resolve_errors)}")
    print(f"- Erros de validacao: {len(validation_errors)}")

    if resolve_errors:
        print("\nErros de heranca/resolucao:")
        for err in resolve_errors:
            print(f"- {format_error(err)}")
    else:
        print("\nErros de heranca/resolucao:\n- Nenhum")

    if validation_errors:
        print("\nErros de validacao:")
        for err in validation_errors:
            print(f"- {format_error(err)}")
    else:
        print("\nErros de validacao:\n- Nenhum")

    print("\n----------------------------Configuracoes Resolvidas---------------------------------")
    print(json.dumps(resolved, ensure_ascii=False, indent=2, sort_keys=True))

    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
