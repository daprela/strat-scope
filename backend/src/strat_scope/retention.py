"""Opaque immutable publication adapter; no catalog/run schemas or policies."""

import fcntl
import hashlib
import os
import secrets
import sqlite3
from collections.abc import Callable
from pathlib import Path
from typing import cast

from strat_scope.config import confined, owned_root

MIGRATIONS = Path(__file__).resolve().parents[2] / "migrations"
type Reference = tuple[int, str]


def flush_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


class Store:
    def __init__(self, root: Path, migrations: Path = MIGRATIONS) -> None:
        self.root = owned_root(root)
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.lock = confined(root, "owner.lock").open("a+b")
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.lock.close()
            raise RuntimeError("store already owned") from None
        self.epoch = secrets.token_hex(16)
        self.active = True
        try:
            self.content = confined(root, "content")
            self.content.mkdir(exist_ok=True, mode=0o700)
            flush_directory(root)
            self.db = sqlite3.connect(confined(root, "metadata.sqlite"))
            self.db.execute("PRAGMA journal_mode = DELETE")
            self.db.execute("PRAGMA synchronous = FULL")
            self.db.execute("PRAGMA foreign_keys = ON")
            self.migrate(migrations)
            self.verify()
        except BaseException:
            self.close()
            raise

    def migrate(self, migrations: Path) -> None:
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations "
            "(version TEXT PRIMARY KEY, digest TEXT NOT NULL)"
        )
        self.db.commit()
        known = {path.name for path in migrations.glob("[0-9]*.sql")}
        applied = {
            row[0] for row in self.db.execute("SELECT version FROM schema_migrations")
        }
        if not applied <= known:
            raise ValueError("unsupported retained schema version")
        for migration in sorted(migrations.glob("[0-9]*.sql")):
            sql = migration.read_text()
            digest = hashlib.sha256(sql.encode()).hexdigest()
            row = self.db.execute(
                "SELECT digest FROM schema_migrations WHERE version = ?",
                (migration.name,),
            ).fetchone()
            if row is not None:
                if row[0] != digest:
                    raise ValueError("migration identity mismatch")
                continue
            # executescript does not own this transaction: include BEGIN explicitly.
            try:
                self.db.executescript("BEGIN IMMEDIATE;\n" + sql)
                self.db.execute(
                    "INSERT INTO schema_migrations (version, digest) VALUES (?, ?)",
                    (migration.name, digest),
                )
                self.db.commit()
            except BaseException:
                self.db.rollback()
                raise

    def check_epoch(self, epoch: str) -> None:
        if not self.active or epoch != self.epoch:
            raise PermissionError("obsolete publication epoch")

    def references(self) -> dict[str, Reference]:
        rows = cast(
            list[tuple[str, int, str]],
            self.db.execute(
                "SELECT scope, revision, digest FROM references_by_scope"
            ).fetchall(),
        )
        return {scope: (revision, digest) for scope, revision, digest in rows}

    def verify(self) -> None:
        if self.db.execute("PRAGMA integrity_check").fetchone() != ("ok",):
            raise ValueError("metadata integrity failure")
        for _, digest in self.references().values():
            payload = confined(self.content, digest).read_bytes()
            if hashlib.sha256(payload).hexdigest() != digest:
                raise ValueError("retained content integrity failure")

    def publish(
        self,
        scope: str,
        expected: int,
        operation: str,
        payload: bytes,
        epoch: str,
        frontier: Callable[[str], None] = lambda _: None,
    ) -> Reference:
        self.check_epoch(epoch)
        digest = hashlib.sha256(payload).hexdigest()
        existing = self.db.execute(
            "SELECT scope, revision, digest FROM publication_outcomes "
            "WHERE operation = ?",
            (operation,),
        ).fetchone()
        if existing is not None:
            if existing[0] != scope or existing[2] != digest:
                raise ValueError("operation identity conflict")
            return cast(Reference, (existing[1], existing[2]))
        target = confined(self.content, digest)
        if not target.exists():
            staging = confined(self.content, secrets.token_hex(16) + ".staging")
            try:
                with staging.open("xb") as stream:
                    stream.write(payload)
                    frontier("before_file_flush")
                    stream.flush()
                    os.fsync(stream.fileno())
                frontier("after_file_flush")
                os.replace(staging, target)
                flush_directory(self.content)
            finally:
                staging.unlink(missing_ok=True)
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError("retained content integrity failure")
        frontier("before_reference")
        try:
            self.db.execute("BEGIN IMMEDIATE")
            self.check_epoch(epoch)
            current = self.references().get(scope, (0, ""))[0]
            if current != expected:
                raise ValueError("publication version conflict")
            revision = expected + 1
            self.db.execute(
                "INSERT INTO references_by_scope (scope, revision, digest) "
                "VALUES (?, ?, ?) ON CONFLICT(scope) DO UPDATE SET "
                "revision = excluded.revision, digest = excluded.digest",
                (scope, revision, digest),
            )
            self.db.execute(
                "INSERT INTO publication_outcomes "
                "(operation, scope, revision, digest) VALUES (?, ?, ?, ?)",
                (operation, scope, revision, digest),
            )
            frontier("before_commit")
            self.check_epoch(epoch)
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise
        frontier("after_commit_before_ack")
        return revision, digest

    def close(self) -> None:
        self.active = False
        if hasattr(self, "db"):
            self.db.close()
        if not self.lock.closed:
            self.lock.close()
