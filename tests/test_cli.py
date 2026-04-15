from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def _run_cli(yaml_path: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR / "src")
    return subprocess.run(
        [sys.executable, "-m", "yaml_parser.cli", str(yaml_path)],
        cwd=ROOT_DIR,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_cli_returns_zero_when_no_errors(tmp_path: Path):
    file_path = tmp_path / "valid.yaml"
    file_path.write_text(
        """
base:
  app_name: "api"
  debug: false
  max_connections: 10
  timeout_seconds: 30
  log_level: "INFO"
  database:
    host: "localhost"
    port: 5432
    pool_size: 5
""".strip()
        + "\n",
        encoding="utf-8",
    )

    result = _run_cli(file_path)

    assert result.returncode == 0
    assert "Total de erros: 0" in result.stdout
    assert "Erros de heranca/resolucao" in result.stdout
    assert "Erros de validacao" in result.stdout


def test_cli_returns_one_when_has_errors():
    result = _run_cli(ROOT_DIR / "examples" / "input_case.yaml")

    assert result.returncode == 1
    assert "Total de erros:" in result.stdout
    assert "Erros de heranca/resolucao" in result.stdout
    assert "Erros de validacao" in result.stdout


def test_cli_returns_two_when_file_not_found(tmp_path: Path):
    missing_path = tmp_path / "missing.yaml"
    result = _run_cli(missing_path)

    assert result.returncode == 2
    assert "arquivo nao encontrado" in result.stdout
