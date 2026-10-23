"""Bounded foreground service, schema and installation commands."""

import argparse
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["bootstrap", "run", "contracts", "contracts-check"])
    args = parser.parse_args()
    env = os.environ | {"UV_CACHE_DIR": "/tmp/strat-scope-uv-cache",
                        "npm_config_cache": "/tmp/strat-scope-npm-cache",
                        "PYTHONPATH": str(ROOT / "backend/src")}

    def run(command: list[str], scope: str) -> None:
        subprocess.run(command, cwd=ROOT / scope, env=env, check=True)

    if args.command == "bootstrap":
        run(["uv", "sync", "--frozen"], "backend")
        run(["npm", "ci"], "frontend")
        run(["npm", "run", "build"], "frontend")
    elif args.command == "run":
        os.chdir(ROOT / "backend")
        os.execve(ROOT / "backend/.venv/bin/python",
                  [str(ROOT / "backend/.venv/bin/python"), "-m", "strat_scope"], env)
    else:
        generated = ROOT / "frontend/src/generated/api.ts"
        schema = ROOT / "foundation-evidence/openapi.json"
        previous = (schema.read_bytes(), generated.read_bytes()) if args.command == "contracts-check" else None
        run(["uv", "run", "python", "tools/export_schema.py"], "backend")
        run(["npm", "run", "contracts"], "frontend")
        if previous is not None and previous != (schema.read_bytes(), generated.read_bytes()):
            raise SystemExit("Generated schema/types drift; regenerate and inspect")


if __name__ == "__main__":
    main()
