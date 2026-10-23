import hashlib
import os
import sqlite3
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from strat_scope.retention import MIGRATIONS, Store

WORKER = Path(__file__).resolve().parents[1] / "tools/storage_worker.py"
ENV = os.environ | {"PYTHONPATH": str(WORKER.parents[1] / "src")}


@pytest.mark.parametrize("reverse", [False, True])
def test_barrier_prepared_independent_publications_preserve_both_scopes(
    tmp_path: Path, reverse: bool
) -> None:
    store = Store(tmp_path)
    _ = store.publish("pinned", 0, "pin", b"retain", store.epoch)
    snapshot = store.references()
    barrier = threading.Barrier(3)

    def prepare(scope: str) -> tuple[str, int, bytes]:
        version = snapshot.get(scope, (0, ""))[0]
        barrier.wait(timeout=5)
        return scope, version, scope.encode()

    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(prepare, "catalog-fixture")
        second = pool.submit(prepare, "checkpoint-fixture")
        barrier.wait(timeout=5)
        candidates = [first.result(), second.result()]
    if reverse:
        candidates.reverse()
    for scope, version, payload in candidates:
        store.publish(scope, version, scope, payload, store.epoch)
    expected = store.references()
    store.close()
    reopened = Store(tmp_path)
    assert reopened.references() == expected
    assert set(expected) == {"pinned", "catalog-fixture", "checkpoint-fixture"}
    for scope, (_, digest) in expected.items():
        assert (reopened.content / digest).read_bytes() == (
            b"retain" if scope == "pinned" else scope.encode()
        )
    reopened.close()


def test_process_exclusion_and_exit_release(tmp_path: Path) -> None:
    with subprocess.Popen(
        [sys.executable, str(WORKER), str(tmp_path), "hold"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        env=ENV,
    ) as process:
        assert process.stdout is not None and process.stdin is not None
        assert process.stdout.readline().strip() == "owned"
        with pytest.raises(RuntimeError, match="already owned"):
            Store(tmp_path)
        process.stdin.write("release\n")
        process.stdin.flush()
        assert process.wait(timeout=5) == 0
    store = Store(tmp_path)
    store.close()


def test_actual_sqlite_durable_settings(tmp_path: Path) -> None:
    store = Store(tmp_path)
    assert store.db.execute("PRAGMA synchronous").fetchone() == (2,)
    assert store.db.execute("PRAGMA journal_mode").fetchone() == ("delete",)
    assert store.db.execute("PRAGMA foreign_keys").fetchone() == (1,)
    store.close()


def test_epoch_revoked_between_acceptance_and_commit_cannot_publish(
    tmp_path: Path,
) -> None:
    store = Store(tmp_path)
    initial = store.publish("alpha", 0, "initial", b"old", store.epoch)

    def revoke(name: str) -> None:
        if name == "before_commit":
            store.active = False

    with pytest.raises(PermissionError):
        store.publish("alpha", 1, "new", b"new", store.epoch, revoke)
    assert store.references()["alpha"] == initial
    store.close()


@pytest.mark.parametrize(
    "frontier",
    [
        "before_file_flush",
        "after_file_flush",
        "before_reference",
        "before_commit",
        "after_commit_before_ack",
    ],
)
def test_killed_process_recovers_old_or_new_complete_state(
    tmp_path: Path, frontier: str
) -> None:
    store = Store(tmp_path)
    _ = store.publish("alpha", 0, "initial", b"old", store.epoch)
    unrelated = store.publish("unrelated", 0, "pin", b"pinned", store.epoch)
    store.close()
    with subprocess.Popen(
        [sys.executable, str(WORKER), str(tmp_path), frontier],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        env=ENV,
    ) as process:
        assert process.stdout is not None
        assert process.stdout.readline().strip() == frontier
        process.kill()
        process.wait(timeout=5)
    reopened = Store(tmp_path)
    expected = b"new" if frontier == "after_commit_before_ack" else b"old"
    assert reopened.references()["alpha"] == (
        2 if expected == b"new" else 1,
        hashlib.sha256(expected).hexdigest(),
    )
    assert reopened.references()["unrelated"] == unrelated
    if expected == b"new":
        assert reopened.publish("alpha", 1, "next", b"new", reopened.epoch)[0] == 2
    reopened.close()


def test_independent_candidates_preserve_scoped_state_and_pinned_content(
    tmp_path: Path,
) -> None:
    store = Store(tmp_path)
    # Both candidates captured the same initial snapshot. They publish in either order.
    initial = store.references()
    a = store.publish(
        "catalog-fixture",
        initial.get("catalog-fixture", (0, ""))[0],
        "catalog",
        b"catalog",
        store.epoch,
    )
    b = store.publish(
        "checkpoint-fixture",
        initial.get("checkpoint-fixture", (0, ""))[0],
        "checkpoint",
        b"checkpoint",
        store.epoch,
    )
    _ = store.publish("catalog-fixture", 1, "replacement", b"replacement", store.epoch)
    with pytest.raises(ValueError, match="version conflict"):
        store.publish("catalog-fixture", 0, "stale", b"stale", store.epoch)
    assert store.references()["checkpoint-fixture"] == b
    assert (store.content / a[1]).read_bytes() == b"catalog"
    with pytest.raises(ValueError, match="identity conflict"):
        store.publish("catalog-fixture", 2, "catalog", b"different", store.epoch)
    old_epoch = store.epoch
    store.close()
    store = Store(tmp_path)
    with pytest.raises(PermissionError):
        store.publish("new", 0, "obsolete", b"no", old_epoch)
    store.close()


@pytest.mark.parametrize(
    "frontier",
    ["before_file_flush", "after_file_flush", "before_reference", "before_commit"],
)
def test_disk_failure_preserves_previous_reference(
    tmp_path: Path, frontier: str
) -> None:
    store = Store(tmp_path)
    initial = store.publish("alpha", 0, "initial", b"old", store.epoch)

    def fail(name: str) -> None:
        if name == frontier:
            raise OSError(28, "fixture disk full")

    with pytest.raises(OSError):
        store.publish("alpha", 1, "next", b"new", store.epoch, fail)
    assert store.references()["alpha"] == initial
    store.close()
    reopened = Store(tmp_path)
    assert reopened.references()["alpha"] == initial
    reopened.close()


@pytest.mark.parametrize("corrupt", [False, True])
def test_missing_or_corrupt_referenced_content_blocks_open(
    tmp_path: Path, corrupt: bool
) -> None:
    store = Store(tmp_path)
    _, digest = store.publish("alpha", 0, "initial", b"old", store.epoch)
    store.close()
    path = tmp_path / "content" / digest
    if corrupt:
        path.write_bytes(b"corrupted")
    else:
        path.unlink()
    with pytest.raises((ValueError, FileNotFoundError)):
        Store(tmp_path)


def test_ordered_migration_upgrade_and_failed_upgrade_rollback(tmp_path: Path) -> None:
    root = tmp_path / "store"
    migrations = tmp_path / "migrations"
    migrations.mkdir()
    (migrations / "001_foundation.sql").write_text(
        (MIGRATIONS / "001_foundation.sql").read_text()
    )
    store = Store(root, migrations)
    initial = store.publish("alpha", 0, "initial", b"old", store.epoch)
    store.close()
    (migrations / "002_upgrade.sql").write_text("CREATE TABLE probe (value TEXT);")
    store = Store(root, migrations)
    assert store.references()["alpha"] == initial
    store.close()
    (migrations / "003_fail.sql").write_text(
        "CREATE TABLE should_rollback (value TEXT); INVALID SQL;"
    )
    with pytest.raises(sqlite3.Error):
        Store(root, migrations)
    with sqlite3.connect(root / "metadata.sqlite") as db:
        assert (
            db.execute(
                "SELECT name FROM sqlite_master WHERE name = 'should_rollback'"
            ).fetchall()
            == []
        )
        assert db.execute("SELECT COUNT(*) FROM schema_migrations").fetchone() == (2,)
