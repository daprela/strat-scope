"""Collect public installation identities and scoped source hashes, never secrets.

Run with backend/.venv/bin/python after verification. Runtime stores, private TLS
material, browser-profile contents and captured target evidence are excluded.
"""

import hashlib
import importlib.metadata
import json
import platform
import sqlite3
import subprocess
import sys
import sysconfig
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "foundation-evidence"


def output(*args: str) -> str:
    return subprocess.check_output(args, text=True, cwd=ROOT).strip()


def main() -> None:
    project = tomllib.loads((ROOT / "backend/pyproject.toml").read_text())
    packages = []
    for distribution in importlib.metadata.distributions():
        license_files = []
        for file in distribution.files or []:
            if file.name.upper().startswith(("LICENSE", "NOTICE", "COPYING")):
                path = distribution.locate_file(file)
                if path.is_file():
                    license_files.append({"file": str(file),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        packages.append({"name": distribution.metadata["Name"], "version": distribution.version,
            "license": distribution.metadata.get("License-Expression") or distribution.metadata.get("License", "See installed license files")[:160],
            "installed_license_files": license_files})
    lock = json.loads((ROOT / "frontend/package-lock.json").read_text())
    npm = [{"path": path, "version": value.get("version"), "license": value.get("license", "See installed package notices")}
        for path, value in lock["packages"].items() if "node_modules/" in path]
    (OUT / "installation.json").write_text(json.dumps({
        "python": platform.python_version(), "implementation": platform.python_implementation(),
        "gil_enabled": sys._is_gil_enabled(), "free_threaded_build": bool(sysconfig.get_config_var("Py_GIL_DISABLED")),
        "sqlite": sqlite3.sqlite_version, "node": output("node", "--version"),
        "npm": output("npm", "--version"), "uv": output("uv", "--version"),
        "python_direct_dependencies": project["project"]["dependencies"],
        "python_packages_and_licenses": sorted(packages, key=lambda value: value["name"]),
        "npm_packages_and_licenses": npm,
        "transport_generator": "Isolated npm workspace, TypeScript 5.9.3 internally; application TypeScript 6.0.3; one root npm lock/install",
    }, indent=2) + "\n")

    readonly = ["AGENTS.md", "backend/AGENTS.md", "backend/DEVELOPMENT.md", "frontend/AGENTS.md",
        "frontend/DEVELOPMENT.md", "frontend/UI-DEVELOPMENT.md"]
    readonly += ["analysis/tradingview/" + name for name in ["architecture-dossier.md", "architecture-review.md",
        "requirements-dossier.md", "domain-model.md", "implementation-standards.md", "standards-approval.json",
        "ui-dossier.md", "visual-system.md", "ui-review.md"]]
    (OUT / "authorities.json").write_text(json.dumps({name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in readonly}, indent=2) + "\n")

    excluded_parts = {".venv", "node_modules", "dist", "__pycache__", ".pytest_cache", ".ruff_cache", "test-results", "playwright-report"}
    source = []
    for scope in ["backend", "frontend", "scripts"]:
        for path in (ROOT / scope).rglob("*"):
            if not path.is_file() or set(path.parts) & excluded_parts:
                continue
            relative = path.relative_to(ROOT).as_posix()
            if relative not in readonly:
                source.append(relative)
    source += [".gitignore", "Makefile", "FOUNDATION.md"]
    (OUT / "source-inventory.json").write_text(json.dumps({
        "baseline": "Application roots contained governance only; no git history available",
        "new_foundation_files": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sorted(source)},
        "governance_edits": {"implementation-brief.md": "implementation-brief resume revision",
            "project-state.md": "project-router coordination", "implementation-ledger.md": "implementation-gate recording if accepted"},
    }, indent=2) + "\n")
    entries = []
    for path in sorted(OUT.rglob("*")):
        if path.is_file() and path.name != "SHA256SUMS":
            entries.append(hashlib.sha256(path.read_bytes()).hexdigest() + "  " + path.relative_to(OUT).as_posix())
    (OUT / "SHA256SUMS").write_text("\n".join(entries) + "\n")


if __name__ == "__main__":
    main()
