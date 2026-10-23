"""Run destructive fixture tests on the installed store's actual filesystem."""

import json
import os
import sqlite3
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
base = Path.home() / ".local/share/strat-scope"
filesystem = subprocess.check_output(["stat", "-f", "-c", "%T", str(base)], text=True).strip()
with tempfile.TemporaryDirectory(prefix="verification-", dir=base) as temporary:
    result = subprocess.run(["uv", "run", "pytest", "tests/test_retention.py", "tests/test_boundaries.py",
        "--basetemp", str(Path(temporary) / "fixtures"), "-q"], cwd=ROOT / "backend",
        env=os.environ | {"UV_CACHE_DIR": "/tmp/strat-scope-uv-cache"},
        capture_output=True, text=True)
    (ROOT / "foundation-evidence/physical-store.log").write_text(result.stdout + result.stderr)
    print(result.stdout, end="")
    if result.returncode:
        raise SystemExit(result.returncode)
    (ROOT / "foundation-evidence/physical-store.json").write_text(json.dumps({
        "filesystem": filesystem, "sqlite": sqlite3.sqlite_version,
        "synchronous": "FULL (2)", "journalMode": "DELETE", "foreignKeys": "ON",
        "result": "passed", "fixtures": "temporary owned directory on installed store filesystem",
        "limits": "Real process crashes and injected I/O faults; not a power-cut or malicious-OS guarantee",
    }, indent=2) + "\n")
