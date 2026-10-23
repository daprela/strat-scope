"""Readiness and identity-checked shutdown for the locally installed foundation."""

import argparse
import json
import os
import signal
import socket
import ssl
import time
import urllib.request
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["ready", "stop"])
    args = parser.parse_args()
    base = Path.home() / ".local/share/strat-scope"
    store = Path(os.environ.get("STRAT_SCOPE_STORE", str(base / "store")))
    if args.command == "ready":
        # Normal hostname/chain validation using the installed public local CA.
        context = ssl.create_default_context(cafile=str(base / "tls/root.crt"))
        with urllib.request.urlopen("https://127.0.0.1:4111/api/ready",
                                    context=context, timeout=5) as response:
            print(response.read().decode())
        return
    identity = json.loads((store / "service.json").read_text())
    pid = int(identity["pid"])
    process = Path("/proc") / str(pid)
    if (process.stat().st_uid != os.getuid() or
        process.joinpath("stat").read_text().split()[21] != identity["birth"] or
        b"strat_scope" not in process.joinpath("cmdline").read_bytes()):
        raise SystemExit("Process identity mismatch; shutdown refused")
    os.kill(pid, signal.SIGTERM)
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", 4111), timeout=0.2):
                pass
        except OSError:
            print("Stopped; 127.0.0.1:4111 is closed")
            return
        time.sleep(0.05)
    raise SystemExit("Shutdown not verified; do not assume the store owner is released")


if __name__ == "__main__":
    main()
