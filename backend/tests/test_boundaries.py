import ast
import json
from pathlib import Path
from typing import cast

import pytest
from pydantic import ValidationError

from strat_scope.config import REPOSITORY, confined, owned_root
from strat_scope.diagnostics import Diagnostics, Phase
from strat_scope.parquet import decode, encode
from strat_scope.retention import Store
from strat_scope.wire import ExactObservation


def test_exact_json_and_parquet_preserve_original_units_and_occurrences(
    tmp_path: Path,
) -> None:
    data = [
        {
            "instant": "9007199254740993",
            "unit": "ns",
            "occurrence": "18446744073709551615",
            "value": "12345678901234567890.000000000000000001",
        },
        {
            "instant": "9007199254740993",
            "unit": "ns",
            "occurrence": "18446744073709551616",
            "value": "-0.000000000000000001",
        },
        {
            "instant": "-9007199254740993",
            "unit": "ms",
            "occurrence": "0",
            "value": "0.00",
        },
    ]
    rows = [ExactObservation.model_validate(row) for row in data]
    store = Store(tmp_path)
    _, digest = store.publish("parquet-fixture", 0, "exact", encode(rows), store.epoch)
    store.close()
    store = Store(tmp_path)
    retained = (store.content / digest).read_bytes()
    assert [json.loads(row.model_dump_json()) for row in decode(retained)] == data
    store.close()
    for invalid in (9007199254740993, "1e20", "NaN", "Infinity"):
        with pytest.raises(ValidationError):
            ExactObservation.model_validate(data[0] | {"value": invalid})


def test_reject_unsafe_roots_and_symlink_escapes_before_mutation(
    tmp_path: Path,
) -> None:
    for root in (
        REPOSITORY / "runtime",
        REPOSITORY.parent,
        Path("relative"),
        Path("/"),
    ):
        with pytest.raises(ValueError):
            owned_root(root)
    (tmp_path / "escape").symlink_to(REPOSITORY, target_is_directory=True)
    for relative in ("../outside", "/etc/passwd", "escape/AGENTS.md"):
        with pytest.raises(ValueError):
            confined(tmp_path, relative)
    with pytest.raises(ValueError):
        owned_root(tmp_path / "escape" / "runtime")


def test_diagnostic_budget_rotation_and_secret_exclusion(tmp_path: Path) -> None:
    diagnostic = Diagnostics(tmp_path)
    diagnostic.emit(cast(Phase, "PRIVATE_SECRET_SENTINEL"), "failed")
    diagnostic.emit("startup", "ready", float("inf"))
    diagnostic.emit(cast(Phase, "x" * (16 * 1024 + 1)), "failed")
    assert diagnostic.dropped == 3
    # Fill real files to the production boundary, then trigger five rollovers.
    for _ in range(6):
        with (tmp_path / "diagnostics.jsonl").open("ab") as stream:
            stream.truncate(10 * 1024 * 1024 - 1)
        assert diagnostic.handler.stream is not None
        _ = diagnostic.handler.stream.seek(0, 2)
        diagnostic.emit("transport", "denied")
    assert diagnostic.rotations == 6
    assert len(list(tmp_path.glob("diagnostics.jsonl*"))) == 5
    for path in tmp_path.glob("diagnostics.jsonl*"):
        assert path.stat().st_size <= 10 * 1024 * 1024
    diagnostic.close()
    assert "PRIVATE_SECRET_SENTINEL" not in (tmp_path / "diagnostics.jsonl").read_text()


def test_inward_authority_has_no_framework_storage_or_renderer_imports() -> None:
    source = REPOSITORY / "backend/src/strat_scope/authority.py"
    imports = {
        node.module
        for node in ast.walk(ast.parse(source.read_text()))
        if isinstance(node, ast.ImportFrom)
    }
    assert imports <= {"collections.abc", "dataclasses"}
