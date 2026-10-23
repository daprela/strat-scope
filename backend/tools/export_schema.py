"""Regenerate the canonical transport schema without opening runtime stores."""

import json
from pathlib import Path

from strat_scope.app import create_app
from strat_scope.config import REPOSITORY, Config

schema = create_app(
    Config(Path("/tmp/unused"), Path("/tmp/cert"), Path("/tmp/key"))
).openapi()
target = REPOSITORY / "foundation-evidence" / "openapi.json"
target.parent.mkdir(exist_ok=True)
target.write_text(json.dumps(schema, sort_keys=True, indent=2) + "\n")
