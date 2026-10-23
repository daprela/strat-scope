"""Allowlisted operational events; free-form/private fields cannot enter logs."""

import json
import logging
import math
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Literal

type Phase = Literal["startup", "shutdown", "authority", "retention", "transport"]
type Outcome = Literal["ready", "denied", "failed", "stopped"]


class CountingHandler(RotatingFileHandler):
    rotations: int = 0

    def doRollover(self) -> None:
        super().doRollover()
        self.rotations += 1


class Diagnostics:
    def __init__(self, root: Path) -> None:
        self.handler = CountingHandler(
            root / "diagnostics.jsonl", maxBytes=10 * 1024 * 1024, backupCount=4
        )
        self.dropped = 0
        self.events = 0

    @property
    def rotations(self) -> int:
        return self.handler.rotations

    def emit(self, phase: Phase, outcome: Outcome, duration_ms: float = 0) -> None:
        if phase not in ("startup", "shutdown", "authority", "retention", "transport"):
            self.dropped += 1
            return
        if outcome not in ("ready", "denied", "failed", "stopped"):
            self.dropped += 1
            return
        if not math.isfinite(duration_ms) or duration_ms < 0:
            self.dropped += 1
            return
        message = json.dumps(
            {"phase": phase, "outcome": outcome, "duration_ms": duration_ms},
            allow_nan=False,
        )
        if len(message.encode()) > 16 * 1024:
            self.dropped += 1
            return
        record = logging.LogRecord("foundation", logging.INFO, "", 0, message, (), None)
        self.handler.emit(record)
        self.events += 1

    def close(self) -> None:
        self.handler.close()
