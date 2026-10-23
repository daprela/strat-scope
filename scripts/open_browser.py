"""Open a separately verified browser profile for this local installation."""

import os
from pathlib import Path

root = Path.home() / ".local/share/strat-scope"
browser_id = os.environ.get("STRAT_SCOPE_BROWSER_ID", "chromium")
if not browser_id.replace("-", "").isalnum():
    raise SystemExit("STRAT_SCOPE_BROWSER_ID must contain only letters, digits, and hyphens")
base = root / ("browser-profile" if browser_id == "chromium" else f"{browser_id}-profile")
default = Path.home() / ".cache/ms-playwright/chromium-1243/chrome-linux64/chrome"
executable = Path(os.environ.get("STRAT_SCOPE_BROWSER", str(default)))
if not executable.is_file() or not base.is_dir():
    raise SystemExit("Verified browser/profile unavailable; rerun its browser verification first")
os.execv(executable, [str(executable), f"--user-data-dir={base}", "https://127.0.0.1:4111"])
