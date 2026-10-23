"""Run physical TLS start/stop/relaunch and browser checks with no cert bypass."""

import json
import os
import socket
import ssl
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CA = Path.home() / ".local/share/strat-scope/tls/root.crt"
ENV = os.environ | {"PYTHONPATH": str(ROOT / "backend/src")}


def start() -> subprocess.Popen[bytes]:
    process = subprocess.Popen([str(ROOT / "backend/.venv/bin/python"), "-m", "strat_scope"],
        cwd=ROOT / "backend", env=ENV, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    context = ssl.create_default_context(cafile=str(CA))
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Service startup failed")
        try:
            with urllib.request.urlopen("https://127.0.0.1:4111/api/ready", context=context, timeout=1) as response:
                if response.status == 200:
                    return process
        except (urllib.error.URLError, OSError):
            time.sleep(0.05)
    process.terminate()
    raise RuntimeError("TLS readiness deadline exceeded")


def stop(process: subprocess.Popen[bytes]) -> None:
    # Exercise the installed identity-checked command, rather than assuming PID exit.
    subprocess.run(["python", "scripts/service.py", "stop"], cwd=ROOT, env=ENV, check=True)
    process.wait(timeout=15)
    try:
        with socket.create_connection(("127.0.0.1", 4111), timeout=1):
            raise RuntimeError("Listener survives stop")
    except ConnectionRefusedError:
        pass
    if process.stderr is not None:
        _ = process.stderr.read()
        process.stderr.close()


def main() -> None:
    phases: list[str] = []
    process = start()
    try:
        phases.append("first TLS start and validated readiness passed")
        subprocess.run(["node", "tools/desktop-check.ts"],
                       cwd=ROOT / "frontend", check=True, timeout=60)
        phases.append("existing desktop browser TLS navigation passed")
    finally:
        stop(process)
    phases.append("identity-checked shutdown and listener closure passed")
    process = start()
    try:
        phases.append("same store and exact TLS origin relaunched")
        subprocess.run(["npm", "run", "test:e2e"], cwd=ROOT / "frontend", check=True)
        phases.append("Chromium transport and renderer checks passed")
    finally:
        stop(process)
    phases.append("final listener closure passed")
    (ROOT / "foundation-evidence/lifecycle.json").write_text(json.dumps({
        "origin": "https://127.0.0.1:4111", "validation": "hostname/chain enabled",
        "hostCA": "explicit installed local public CA; system trust was not installed",
        "phases": phases,
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
