"""Reopen the graphical browser profile actually verified for this installation."""

import os
from pathlib import Path

base = Path.home() / ".local/share/strat-scope/browser-profile"
default = Path.home() / ".cache/ms-playwright/chromium-1243/chrome-linux64/chrome"
executable = Path(os.environ.get("STRAT_SCOPE_BROWSER", str(default)))
if not executable.is_file() or not base.is_dir():
    raise SystemExit("Verified browser/profile unavailable; set STRAT_SCOPE_BROWSER and rerun verification")
os.execv(executable, [str(executable), f"--user-data-dir={base}", "https://127.0.0.1:4111"])
