"""Standalone v1.0 contract validation and bounded reference access.

This authoring tool does not import or modify the production viewer. Full
validation is explicit whole-bundle work; bounded queries have separate budgets.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import os
import re
import stat
import time
from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
PHYSICAL = json.loads((HERE / "physical-schemas.json").read_text())
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}\Z")
STAMP = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{9}Z\Z")
NAMESPACE = re.compile(r"[a-z][a-z0-9_]*\.[a-z][a-z0-9_.-]*\Z")
MAX_INT = 9007199254740991
BASE_GEOMETRIES = {"HORIZONTAL_LEVEL", "PRICE_ZONE", "TREND_LINE", "BOX", "MARKER", "ARROW"}


class ContractError(ValueError):
    """A stable attributable validation or availability result."""

    def __init__(self, code: str, location: str, detail: str):
        super().__init__(f"{code}: {location}: {detail}")
        self.code, self.location, self.detail = code, location, detail


def require(condition: bool, code: str, location: str, detail: str) -> None:
    if not condition:
        raise ContractError(code, location, detail)


def validate_path(path: str) -> None:
    require(
        len(path) <= 240
        and all(re.fullmatch(r"[a-z0-9][a-z0-9._-]*", part) for part in path.split("/")),
        "PATH_CONFINEMENT",
        path,
        "invalid relative path",
    )


def instant(value: Any, location: str = "timestamp") -> str:
    require(
        isinstance(value, str) and bool(STAMP.fullmatch(value)),
        "INVALID_TIME",
        location,
        "canonical nanosecond UTC required",
    )
    try:
        parsed = datetime.fromisoformat(value[:19])
    except ValueError as exc:
        raise ContractError("INVALID_TIME", location, "invalid Gregorian date/time") from exc
    require(parsed.year >= 1970, "INVALID_TIME", location, "year before 1970")
    return value


def minute(value: str) -> str:
    return instant(value)[:16] + ":00.000000000Z"


def minute_after(value: str) -> str:
    try:
        return (datetime.fromisoformat(instant(value)[:16]) + timedelta(minutes=1)).strftime(
            "%Y-%m-%dT%H:%M:00.000000000Z"
        )
    except OverflowError as exc:
        raise ContractError("INVALID_TIME", value, "minute boundary overflow") from exc


def nanosecond_after(value: str) -> str:
    instant(value)
    fraction = int(value[20:29])
    if fraction < 999999999:
        return value[:20] + f"{fraction + 1:09d}Z"
    try:
        return (datetime.fromisoformat(value[:19]) + timedelta(seconds=1)).strftime(
            "%Y-%m-%dT%H:%M:%S.000000000Z"
        )
    except OverflowError as exc:
        raise ContractError("INVALID_TIME", value, "endpoint overflow") from exc


def strict_json(raw: bytes | str, location: str, limit: int) -> Any:
    raw = raw.encode("utf-8") if isinstance(raw, str) else raw
    require(
        len(raw) <= limit and not raw.startswith(b"\xef\xbb\xbf"),
        "INVALID_JSON",
        location,
        "byte limit or BOM",
    )

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in items:
            require(key not in result, "INVALID_JSON", location, "duplicate object key")
            result[key] = value
        return result

    def constant(value: str) -> None:
        raise ContractError("INVALID_JSON", location, f"nonstandard number {value}")

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ContractError("INVALID_JSON", location, "invalid UTF-8/JSON") from exc

    def walk(item: Any, depth: int) -> None:
        if isinstance(item, (dict, list)):
            require(depth <= 16, "INVALID_JSON", location, "nesting exceeds 16 containers")
        if isinstance(item, str):
            require(
                not any(0xD800 <= ord(char) <= 0xDFFF for char in item),
                "INVALID_JSON",
                location,
                "unpaired surrogate",
            )
        elif isinstance(item, float):
            require(math.isfinite(item), "INVALID_NUMBER", location, "nonfinite value")
        elif type(item) is int:
            require(
                abs(item) <= MAX_INT, "INVALID_NUMBER", location, "integer outside JSON-safe domain"
            )
        elif isinstance(item, dict):
            for key, child in item.items():
                walk(key, depth)
                walk(child, depth + 1)
        elif isinstance(item, list):
            for child in item:
                walk(child, depth + 1)

    walk(value, 1)
    require(isinstance(value, dict), "INVALID_JSON", location, "root must be object")
    return value


def check_schema(
    value: Any, schema: dict[str, Any], root: dict[str, Any] | None = None, location: str = "json"
) -> None:
    """Evaluate exactly the JSON Schema vocabulary used by this package.

    This is not a general-purpose JSON Schema implementation. Tests exercise
    every employed keyword; independent validators may use the standard files.
    """
    root = schema if root is None else root
    if "$ref" in schema:
        target = root
        for part in schema["$ref"][2:].split("/"):
            target = target[part]
        check_schema(value, target, root, location)
    for operator in ("anyOf", "oneOf"):
        if operator in schema:
            matches = 0
            for candidate in schema[operator]:
                try:
                    check_schema(value, candidate, root, location)
                    matches += 1
                except ContractError:
                    pass
            require(
                matches >= 1 if operator == "anyOf" else matches == 1,
                "INVALID_SCHEMA",
                location,
                operator,
            )
    if "const" in schema:
        require(
            type(value) is type(schema["const"]) and value == schema["const"],
            "INVALID_SCHEMA",
            location,
            "constant mismatch",
        )
    if "enum" in schema:
        require(
            any(type(value) is type(option) and value == option for option in schema["enum"]),
            "INVALID_SCHEMA",
            location,
            "enum mismatch",
        )
    kind = schema.get("type")
    valid_type = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "number": type(value) in (int, float),
        "integer": type(value) is int,
        "boolean": type(value) is bool,
        "null": value is None,
    }
    if kind:
        require(valid_type[kind], "INVALID_SCHEMA", location, f"expected {kind}")
    if type(value) in (int, float):
        require(math.isfinite(value), "INVALID_NUMBER", location, "nonfinite")
        for key, ok in (
            ("minimum", lambda bound: value >= bound),
            ("maximum", lambda bound: value <= bound),
        ):
            if key in schema:
                require(ok(schema[key]), "INVALID_SCHEMA", location, key)
    if isinstance(value, str):
        require(
            len(value) >= schema.get("minLength", 0)
            and len(value) <= schema.get("maxLength", len(value)),
            "INVALID_SCHEMA",
            location,
            "string length",
        )
        if "pattern" in schema:
            require(
                bool(re.search(schema["pattern"], value)),
                "INVALID_SCHEMA",
                location,
                "pattern mismatch",
            )
    if isinstance(value, list):
        require(
            len(value) >= schema.get("minItems", 0)
            and len(value) <= schema.get("maxItems", len(value)),
            "INVALID_SCHEMA",
            location,
            "array size",
        )
        if schema.get("uniqueItems"):
            encoded = [json.dumps(x, sort_keys=True) for x in value]
            require(
                len(encoded) == len(set(encoded)),
                "INVALID_SCHEMA",
                location,
                "duplicate array item",
            )
        for i, item in enumerate(value):
            check_schema(item, schema.get("items", {}), root, f"{location}[{i}]")
    if isinstance(value, dict):
        require(
            set(schema.get("required", [])).issubset(value),
            "INVALID_SCHEMA",
            location,
            "missing required key",
        )
        require(
            len(value) <= schema.get("maxProperties", len(value)),
            "INVALID_SCHEMA",
            location,
            "too many properties",
        )
        for name, item in value.items():
            matched = False
            if name in schema.get("properties", {}):
                check_schema(item, schema["properties"][name], root, f"{location}.{name}")
                matched = True
            for pattern, child in schema.get("patternProperties", {}).items():
                if re.search(pattern, name):
                    check_schema(item, child, root, f"{location}.{name}")
                    matched = True
            require(
                matched or schema.get("additionalProperties", True),
                "INVALID_SCHEMA",
                location,
                f"unknown field {name}",
            )
            if not matched and isinstance(schema.get("additionalProperties"), dict):
                check_schema(item, schema["additionalProperties"], root, f"{location}.{name}")


def arrow_schema(section: str) -> pa.Schema:
    fields = PHYSICAL["sections"][section]["fields"]
    types = {"string": pa.string(), "int64": pa.int64(), "float64": pa.float64()}
    return pa.schema(
        [pa.field(f["name"], types[f["type"]], nullable=f["nullable"]) for f in fields],
        metadata={b"bv.contract": b"run-bundle/1.0.0", b"bv.section": section.encode()},
    )


def row_key(section: str, row: dict[str, Any]) -> tuple[Any, ...]:
    field = PHYSICAL["sections"][section]["time_field"]
    return row[field], row["known_at_utc"], row["sequence_num"], row["fact_id"]


def index_key(kind: str, entry: dict[str, Any]) -> str:
    if kind == "time":
        return entry["first_time"] or ""
    if kind == "entity":
        return (
            f"{entry['entity_id']}|{entry['time_utc']}|"
            f"{entry['sequence_num']:016d}|{entry['fact_id']}"
        )
    return f"{entry['coordinate_start_utc']}|{entry['known_from_utc']}|{entry['fact_id']}"


def summarize(kind: str, entries: list[dict[str, Any]], branch: bool = False) -> dict[str, Any]:
    summary = dict.fromkeys(
        ("min_key", "max_key", "min_start", "max_end", "min_known", "max_known_end")
    )
    summary["count"] = 0
    if not entries:
        return summary
    if branch:
        children = [entry["summary"] for entry in entries if entry["summary"]["count"]]
        if not children:
            return summary
        summary["count"] = sum(x["count"] for x in children)
        summary["min_key"] = min(x["min_key"] for x in children)
        summary["max_key"] = max(x["max_key"] for x in children)
        if kind == "state":
            for key in ("min_start", "min_known"):
                summary[key] = min(x[key] for x in children)
            for key in ("max_end", "max_known_end"):
                summary[key] = (
                    None if any(x[key] is None for x in children) else max(x[key] for x in children)
                )
    else:
        active = [entry for entry in entries if kind != "time" or entry["row_count"]]
        summary["count"] = sum(x["row_count"] for x in entries) if kind == "time" else len(entries)
        if active:
            summary["min_key"] = min(index_key(kind, x) for x in active)
            summary["max_key"] = max(
                x["last_time"] if kind == "time" else index_key(kind, x) for x in active
            )
            if kind == "state":
                summary["min_start"] = min(x["coordinate_start_utc"] for x in active)
                summary["min_known"] = min(x["known_from_utc"] for x in active)
                for source, target in (
                    ("coordinate_end_utc", "max_end"),
                    ("known_to_utc", "max_known_end"),
                ):
                    summary[target] = (
                        None
                        if any(x[source] is None for x in active)
                        else max(x[source] for x in active)
                    )
    return summary


@dataclass
class Budget:
    """Explicit reference-operation limits; not a supported product ceiling."""

    max_nodes: int = 1000
    max_bytes: int = 64 * 1024 * 1024
    max_rows: int = 100000
    max_predecessors: int = 1000
    max_seconds: float = 5.0
    nodes: int = 0
    bytes: int = 0
    rows: int = 0
    predecessors: int = 0
    started: float = dataclass_field(default_factory=time.monotonic)

    def charge(
        self, *, nodes: int = 0, bytes_count: int = 0, rows: int = 0, predecessors: int = 0
    ) -> None:
        require(
            self.nodes + nodes <= self.max_nodes
            and self.bytes + bytes_count <= self.max_bytes
            and self.rows + rows <= self.max_rows
            and self.predecessors + predecessors <= self.max_predecessors
            and time.monotonic() - self.started <= self.max_seconds,
            "REFUSED_OVER_LIMIT",
            "request",
            "reference budget exceeded; no substitute result",
        )
        self.nodes += nodes
        self.bytes += bytes_count
        self.rows += rows
        self.predecessors += predecessors


class BundleAccess:
    """Confined content-bound file reads and pruned index traversals."""

    def __init__(self, root: Path, budget: Budget | None = None):
        self.root = root.resolve(strict=True)
        root_info = self.root.stat()
        self.root_identity = (root_info.st_dev, root_info.st_ino)
        self.current_owner: str | None = None
        self.owners: dict[str, str] = {}
        self.budget = budget
        self.observed: dict[str, tuple[int, ...]] = {}
        self.manifest_raw = self._read("manifest.json", 1048576)
        self.manifest_digest = hashlib.sha256(self.manifest_raw).hexdigest()
        self.manifest = strict_json(self.manifest_raw, "manifest", 1048576)
        require(
            self.manifest.get("format_version") == "1.0.0",
            "UNSUPPORTED_VERSION",
            "manifest",
            "exact supported version is 1.0.0",
        )
        check_schema(self.manifest, json.loads((HERE / "manifest.schema.json").read_text()))
        validate_manifest(self.manifest)

    def _open(self, path: str) -> int:
        validate_path(path)
        parts = path.split("/")
        root_fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        directory_fd = root_fd
        try:
            info = os.fstat(root_fd)
            require(
                (info.st_dev, info.st_ino) == self.root_identity,
                "OBSERVATION_CHANGED",
                "bundle",
                "bundle directory replaced",
            )
            for part in parts[:-1]:
                next_fd = os.open(
                    part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory_fd
                )
                if directory_fd != root_fd:
                    os.close(directory_fd)
                directory_fd = next_fd
            return os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd)
        except OSError as exc:
            raise ContractError(
                "PATH_OR_FILE_UNAVAILABLE", path, "confined regular file unavailable"
            ) from exc
        finally:
            if directory_fd != root_fd:
                os.close(directory_fd)
            os.close(root_fd)

    @staticmethod
    def _identity(info: os.stat_result) -> tuple[int, ...]:
        return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns

    def _read(self, path: str, limit: int, expected: dict[str, Any] | None = None) -> bytes:
        fd = self._open(path)
        try:
            before = os.fstat(fd)
            require(
                stat.S_ISREG(before.st_mode) and before.st_size <= limit,
                "INVALID_FILE",
                path,
                "regular file/byte limit",
            )
            if expected:
                require(
                    before.st_size == expected["bytes"],
                    "INTEGRITY_MISMATCH",
                    path,
                    "stored length mismatch",
                )
            if self.budget:
                self.budget.charge(bytes_count=before.st_size)
            with os.fdopen(fd, "rb", closefd=False) as stream:
                raw = stream.read(limit + 1)
            after = os.fstat(fd)
            require(
                self._identity(before) == self._identity(after),
                "OBSERVATION_CHANGED",
                path,
                "mutation during read",
            )
            require(len(raw) == before.st_size, "INTEGRITY_MISMATCH", path, "short/long read")
            if expected:
                require(
                    hashlib.sha256(raw).hexdigest() == expected["sha256"],
                    "INTEGRITY_MISMATCH",
                    path,
                    "SHA-256 mismatch",
                )
            identity = self._identity(after)
            require(
                path not in self.observed or self.observed[path] == identity,
                "OBSERVATION_CHANGED",
                path,
                "different source generation",
            )
            self.observed[path] = identity
            return raw
        finally:
            os.close(fd)

    def ref_bytes(self, ref: dict[str, Any], limit: int) -> bytes:
        check_schema(
            ref, json.loads((HERE / "manifest.schema.json").read_text())["$defs"]["file_ref"]
        )
        validate_path(ref["path"])
        require(ref["bytes"] <= limit, "INVALID_FILE", ref["path"], "declared byte limit")
        if self.current_owner:
            require(
                self.owners.get(ref["path"], self.current_owner) == self.current_owner,
                "INVALID_INDEX",
                ref["path"],
                "cross-section file ownership",
            )
            self.owners[ref["path"]] = self.current_owner
        return self._read(ref["path"], limit, ref)

    def node(
        self, ref: dict[str, Any], kind: str, expected_summary: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        if self.budget:
            self.budget.charge(nodes=1)
        node = strict_json(self.ref_bytes(ref, 65536), ref["path"], 65536)
        check_schema(node, json.loads((HERE / "index.schema.json").read_text()))
        require(node["index_kind"] == kind, "INVALID_INDEX", ref["path"], "wrong index kind")
        require(
            node["summary"] == summarize(kind, node["entries"], node["level"] > 0),
            "INVALID_INDEX",
            ref["path"],
            "summary mismatch",
        )
        if expected_summary is not None:
            require(
                node["summary"] == expected_summary,
                "INVALID_INDEX",
                ref["path"],
                "child summary differs",
            )
        keys = (
            [x["summary"]["min_key"] or "" for x in node["entries"]]
            if node["level"]
            else [index_key(kind, x) for x in node["entries"]]
        )
        require(keys == sorted(keys), "INVALID_INDEX", ref["path"], "unordered entries")
        return node

    def entries(
        self,
        ref: dict[str, Any],
        kind: str,
        predicate=None,
        visited: set[str] | None = None,
        parent_level: int | None = None,
        expected_summary=None,
    ):
        visited = set() if visited is None else visited
        require(ref["path"] not in visited, "INVALID_INDEX", ref["path"], "cycle/shared node")
        visited.add(ref["path"])
        node = self.node(ref, kind, expected_summary)
        require(
            parent_level is None or node["level"] == parent_level - 1,
            "INVALID_INDEX",
            ref["path"],
            "unbalanced tree",
        )
        if node["level"]:
            for child in node["entries"]:
                if predicate is None or predicate(child["summary"]):
                    yield from self.entries(
                        child["file"], kind, predicate, visited, node["level"], child["summary"]
                    )
        else:
            yield from node["entries"]

    def shard(self, section: str, ref: dict[str, Any]) -> list[dict[str, Any]]:
        raw = self.ref_bytes(ref, 8388608)
        file = pq.ParquetFile(io.BytesIO(raw))
        require(
            file.schema_arrow.equals(arrow_schema(section), check_metadata=False),
            "INVALID_PHYSICAL_SCHEMA",
            ref["path"],
            "column order/type/nullability mismatch",
        )
        physical_types = {"string": "BYTE_ARRAY", "int64": "INT64", "float64": "DOUBLE"}
        for number, definition in enumerate(PHYSICAL["sections"][section]["fields"]):
            column = file.schema.column(number)
            annotations = {"string": {"UTF8"}, "int64": {"NONE", "INT_64"}, "float64": {"NONE"}}
            require(
                column.name == definition["name"]
                and column.physical_type == physical_types[definition["type"]]
                and column.converted_type in annotations[definition["type"]]
                and column.max_definition_level == int(definition["nullable"])
                and column.max_repetition_level == 0,
                "INVALID_PHYSICAL_SCHEMA",
                ref["path"],
                "physical fields disagree with declared schema",
            )
        metadata = file.metadata.metadata or {}
        require(
            metadata.get(b"bv.contract") == b"run-bundle/1.0.0"
            and metadata.get(b"bv.section") == section.encode(),
            "INVALID_PHYSICAL_SCHEMA",
            ref["path"],
            "contract metadata",
        )
        require(
            file.num_row_groups == 1 and file.metadata.num_rows <= 4096,
            "INVALID_PHYSICAL_SCHEMA",
            ref["path"],
            "row-group bounds",
        )
        group = file.metadata.row_group(0)
        require(
            group.total_byte_size <= 16777216
            and file.metadata.format_version == "2.6"
            and all(not group.column(i).file_path for i in range(group.num_columns))
            and all(
                set(group.column(i).encodings)
                <= {"PLAIN", "PLAIN_DICTIONARY", "RLE", "RLE_DICTIONARY", "BIT_PACKED"}
                for i in range(group.num_columns)
            )
            and all(
                group.column(i).compression in {"UNCOMPRESSED", "ZSTD"}
                for i in range(group.num_columns)
            ),
            "INVALID_PHYSICAL_SCHEMA",
            ref["path"],
            "size/compression",
        )
        if self.budget:
            self.budget.charge(rows=file.metadata.num_rows)
        rows = file.read_row_group(0).to_pylist()
        for row in rows:
            validate_row(section, row, self.manifest)
        require(
            rows == sorted(rows, key=lambda x: row_key(section, x)),
            "INVALID_ORDER",
            ref["path"],
            "shard ordering",
        )
        return rows

    def verify_stable(self) -> None:
        for path, expected in list(self.observed.items()):
            fd = self._open(path)
            try:
                require(
                    self._identity(os.fstat(fd)) == expected,
                    "OBSERVATION_CHANGED",
                    path,
                    "consumed file replaced/modified",
                )
            finally:
                os.close(fd)
        raw = self._read("manifest.json", 1048576)
        require(
            hashlib.sha256(raw).hexdigest() == self.manifest_digest,
            "OBSERVATION_CHANGED",
            "manifest",
            "manifest changed",
        )

    def time_rows(self, section: str, start: str, end: str) -> list[dict[str, Any]]:
        instant(start)
        instant(end)
        require(start < end, "INVALID_RANGE", "request", "half-open range required")
        descriptor = self.manifest["sections"][section]

        def selected(summary):
            return bool(
                summary["count"] and summary["max_key"] >= start and summary["min_key"] < end
            )

        result = []
        for entry in self.entries(descriptor["time_index"], "time", selected):
            if entry["row_count"] and entry["last_time"] >= start and entry["first_time"] < end:
                result.extend(
                    row
                    for row in self.shard(section, entry["file"])
                    if start <= row[descriptor["time_field"]] < end
                )
        self.verify_stable()
        return deduplicate(section, result)

    def replay_time_rows(
        self, section: str, start: str, end: str, cursor: str
    ) -> list[dict[str, Any]]:
        """Apply knowledge/report gating to a bounded coordinate query."""
        gate = minute(cursor)
        if section in {"equity_curve", "monthly_returns"}:
            require(
                gate >= minute(self.manifest["end_time_utc"]),
                "REPORT_EMBARGOED",
                section,
                "report not yet disclosed",
            )
        return [
            row
            for row in self.time_rows(section, start, end)
            if minute(row["known_at_utc"]) <= gate
        ]

    def predecessor(
        self, section: str, entity_id: str, before: str, cursor: str
    ) -> dict[str, Any] | None:
        """Seek backwards through entity branches, counting unrevealable candidates."""
        require(bool(ID.fullmatch(entity_id)), "INVALID_ID", "request", "entity ID")
        instant(before)
        gate = minute(cursor)
        prefix, upper = entity_id + "|", entity_id + "|" + before
        seen = set()

        def candidates(ref, level=None, expected=None):
            require(ref["path"] not in seen, "INVALID_INDEX", ref["path"], "cycle/shared node")
            seen.add(ref["path"])
            node = self.node(ref, "entity", expected)
            require(
                level is None or node["level"] == level - 1,
                "INVALID_INDEX",
                ref["path"],
                "tree level",
            )
            for entry in reversed(node["entries"]):
                if node["level"]:
                    summary = entry["summary"]
                    if (
                        summary["count"]
                        and summary["max_key"] >= prefix
                        and summary["min_key"] < upper
                    ):
                        yield from candidates(entry["file"], node["level"], summary)
                elif entry["entity_id"] == entity_id and entry["time_utc"] < before:
                    yield entry

        descriptor = self.manifest["sections"][section]
        cache = {}
        for entry in candidates(descriptor["entity_index"]):
            if self.budget:
                self.budget.charge(predecessors=1)
            if minute(entry["known_at_utc"]) > gate:
                continue
            path = entry["file"]["path"]
            if path not in cache:
                cache[path] = self.shard(section, entry["file"])
            require(entry["row"] < len(cache[path]), "INVALID_INDEX", path, "row pointer")
            row = cache[path][entry["row"]]
            require(
                row["fact_id"] == entry["fact_id"]
                and row[descriptor["entity_field"]] == entity_id
                and row[descriptor["time_field"]] == entry["time_utc"]
                and row["known_at_utc"] == entry["known_at_utc"]
                and row["sequence_num"] == entry["sequence_num"],
                "INVALID_INDEX",
                path,
                "entity pointer mismatch",
            )
            self.verify_stable()
            return row
        self.verify_stable()
        return None

    def state_rows(
        self, section: str, start: str, end: str, cursor: str | None
    ) -> list[dict[str, Any]]:
        """Select replay forms, or historical forms when cursor is None.

        Returns emitted states. Rendering still must clip each form to its
        effective period and geometric extent under the selected mode.
        """
        instant(start)
        instant(end)
        require(start < end, "INVALID_RANGE", "request", "half-open viewport required")
        if cursor is not None:
            cursor = minute(cursor)
        descriptor = self.manifest["sections"][section]
        require(
            descriptor["state_index"] is not None, "INSUFFICIENT_HISTORY", section, "no state index"
        )

        def possible(summary):
            return bool(
                summary["count"]
                and summary["min_start"] < end
                and (summary["max_end"] is None or summary["max_end"] > start)
                and (
                    summary["min_known"] <= cursor
                    if cursor is not None
                    else summary["min_known"] < end
                )
                and (
                    summary["max_known_end"] is None
                    or summary["max_known_end"] > (cursor if cursor is not None else start)
                )
            )

        selected = []
        cache = {}
        for entry in self.entries(descriptor["state_index"], "state", possible):
            if entry["coordinate_start_utc"] >= end or (
                entry["coordinate_end_utc"] is not None and entry["coordinate_end_utc"] <= start
            ):
                continue
            if (
                entry["known_from_utc"] > cursor
                if cursor is not None
                else entry["known_from_utc"] >= end
            ) or (
                entry["known_to_utc"] is not None
                and entry["known_to_utc"] <= (cursor if cursor is not None else start)
            ):
                continue
            path = entry["file"]["path"]
            if path not in cache:
                cache[path] = self.shard(section, entry["file"])
            require(entry["row"] < len(cache[path]), "INVALID_INDEX", path, "row pointer")
            row = cache[path][entry["row"]]
            require(
                row["fact_id"] == entry["fact_id"]
                and minute(row["known_at_utc"]) == entry["known_from_utc"],
                "INVALID_INDEX",
                path,
                "state pointer mismatch",
            )
            require(
                row.get("geometry_type") is None or row["geometry_type"] in BASE_GEOMETRIES,
                "UNSUPPORTED_GEOMETRY",
                section,
                "opaque optional form withheld",
            )
            selected.append(row)
        self.verify_stable()
        return deduplicate(section, selected)


def validate_manifest(manifest: dict[str, Any]) -> None:
    for field in ("start_time_utc", "end_time_utc", "completed_at_utc"):
        instant(manifest[field], field)
    require(
        manifest["start_time_utc"] < manifest["end_time_utc"],
        "INVALID_RANGE",
        "manifest",
        "start must precede end",
    )
    require(
        "core.v1" in manifest["required_features"]
        and all(x == "core.v1" for x in manifest["required_features"]),
        "UNSUPPORTED_REQUIRED_FEATURE",
        "manifest",
        "unknown required feature",
    )
    require(
        "indicator_points" not in manifest["sections"]
        or "indicator_series" in manifest["sections"],
        "INVALID_REFERENCE",
        "indicator_points",
        "declared points require catalogue section",
    )
    for descriptor in manifest["sections"].values():
        for name in ("time_index", "entity_index", "state_index"):
            if descriptor[name] is not None:
                validate_path(descriptor[name]["path"])
    seen = {}
    for strategy in manifest["strategies"]:
        sid = strategy["strategy_id"]
        require(sid not in seen, "INVALID_REFERENCE", "strategies", "duplicate strategy")
        parent = strategy["parent_strategy_id"]
        require(
            parent is None if not seen else parent in seen,
            "INVALID_REFERENCE",
            sid,
            "primary/parent order",
        )
        instant(strategy["known_at_utc"])
        require(
            manifest["start_time_utc"] <= strategy["known_at_utc"] <= manifest["end_time_utc"],
            "INVALID_TIME",
            sid,
            "strategy knowledge outside run",
        )
        if parent:
            require(
                seen[parent]["known_at_utc"] <= strategy["known_at_utc"],
                "INVALID_TIME",
                sid,
                "parent not yet known",
            )
        seen[sid] = strategy
    require(
        manifest["primary_strategy_id"] == manifest["strategies"][0]["strategy_id"],
        "INVALID_REFERENCE",
        "primary_strategy_id",
        "first/root strategy required",
    )
    report = manifest["report"]
    missing = {name for name in ("summary", "trade_stats", "drawdown") if report[name] is None}
    require(
        set(report["unavailable_reasons"]) == missing,
        "INVALID_REPORT",
        "report",
        "category reasons do not match nulls",
    )
    if report["summary"] and report["trade_stats"]:
        total = report["summary"]["total_trades"]
        stats = report["trade_stats"]
        require(
            stats["winning_trades"] + stats["losing_trades"] <= total,
            "INVALID_REPORT",
            "report",
            "counts exceed total",
        )
        require(
            total != 0 or stats["win_rate"] is None,
            "INVALID_REPORT",
            "win_rate",
            "zero-trade ratio must be null",
        )
    summary, stats, drawdown = report["summary"], report["trade_stats"], report["drawdown"]
    if summary:
        require(
            summary["gross_loss"] != 0 or summary["profit_factor"] is None,
            "INVALID_REPORT",
            "profit_factor",
            "zero denominator",
        )
        require(
            summary["total_trades"] != 0 or summary["expected_payoff"] is None,
            "INVALID_REPORT",
            "expected_payoff",
            "zero denominator",
        )
        require(
            (drawdown is not None and drawdown["max_drawdown"] != 0)
            or summary["return_on_max_drawdown"] is None,
            "INVALID_REPORT",
            "return_on_max_drawdown",
            "zero/unknown denominator",
        )
    if stats:
        for count, fields in (
            ("winning_trades", ("average_win", "largest_winning_trade")),
            ("losing_trades", ("average_loss", "largest_losing_trade")),
        ):
            require(
                stats[count] != 0 or all(stats[field_name] is None for field_name in fields),
                "INVALID_REPORT",
                count,
                "empty outcome class",
            )
        require(
            stats["average_loss"] not in (None, 0) or stats["win_loss_ratio"] is None,
            "INVALID_REPORT",
            "win_loss_ratio",
            "undefined denominator",
        )
    if drawdown:
        require(
            (drawdown["relative_drawdown"] is None) == (drawdown["relative_drawdown_pct"] is None),
            "INVALID_REPORT",
            "relative_drawdown",
            "paired unavailable fields",
        )


def validate_row(section: str, row: dict[str, Any], manifest: dict[str, Any]) -> None:
    location = f"{section}:{row.get('fact_id', 'missing')}"
    fields = PHYSICAL["sections"][section]["fields"]
    require(
        list(row) == [field["name"] for field in fields],
        "INVALID_ROW",
        location,
        "exact fields required",
    )
    for field in fields:
        name, kind, value = field["name"], field["type"], row[field["name"]]
        if value is None:
            require(field["nullable"], "INVALID_ROW", location, f"null {name}")
            continue
        require(
            {
                "string": isinstance(value, str),
                "int64": type(value) is int,
                "float64": type(value) is float,
            }[kind],
            "INVALID_ROW",
            location,
            f"type {name}",
        )
        if kind == "float64":
            require(math.isfinite(value), "INVALID_NUMBER", location, name)
        if name.endswith("_id"):
            require(bool(ID.fullmatch(value)), "INVALID_ID", location, name)
        if name.endswith("_utc"):
            instant(value, location + "." + name)
        if name.endswith("_json"):
            strict_json(value, location + "." + name, 16384)
    require(0 <= row["sequence_num"] <= MAX_INT, "INVALID_SEQUENCE", location, "integer domain")
    require(
        manifest["start_time_utc"] <= row["known_at_utc"] <= manifest["end_time_utc"],
        "INVALID_TIME",
        location,
        "knowledge outside run",
    )
    for name in (
        "timestamp_utc",
        "sample_time_utc",
        "boundary_time_utc",
        "entry_time_utc",
        "exit_time_utc",
    ):
        if row.get(name) is not None:
            require(
                manifest["start_time_utc"] <= row[name] <= row["known_at_utc"],
                "INVALID_TIME",
                location,
                f"{name} outside run/after knowledge",
            )
    if section in {"trade_facts", "strategy_events", "indicator_series"}:
        identity = {
            "trade_facts": "execution_id",
            "strategy_events": "event_id",
            "indicator_series": "series_id",
        }[section]
        require(row["fact_id"] == row[identity], "INVALID_ID", location, "fact/object identity")
    enums = {
        "trade_facts": {
            "side": {"BUY", "SELL"},
            "action": {"ENTRY", "EXIT", "SCALE_IN", "SCALE_OUT"},
        },
        "position_history": {"action": {"OPEN", "UPDATE", "CLOSE"}, "direction": {"LONG", "SHORT"}},
        "visual_history": {"action": {"CREATE", "UPDATE", "REMOVE"}},
        "sessions": {"action": {"START", "END"}},
        "indicator_points": {"status": {"VALUE", "WARMUP", "GAP"}},
        "indicator_series": {"axis": {"PRICE", "SEPARATE"}},
    }
    for field, values in enums.get(section, {}).items():
        require(row[field] in values, "INVALID_ROW", location, field)
    if section == "trade_facts":
        require(row["quantity"] > 0, "INVALID_ROW", location, "fill quantity")
        require(
            row["timestamp_utc"] < manifest["end_time_utc"] or row["action"] == "EXIT",
            "INVALID_TIME",
            location,
            "only EXIT may occur at end",
        )
    if section == "strategy_events":
        require(
            1 <= len(row["event_type"]) <= 128
            and (row["message"] is None or len(row["message"]) <= 4096),
            "INVALID_ROW",
            location,
            "event strings",
        )
    if section == "position_history":
        require(
            row["initial_quantity"] > 0
            and row["total_entry_quantity"] > 0
            and row["open_quantity"] >= 0
            and row["total_exit_quantity"] >= 0,
            "INVALID_ROW",
            location,
            "position quantities",
        )
        close = row["action"] == "CLOSE"
        require(
            all(
                (row[x] is not None) == close
                for x in ("net_pnl", "exit_time_utc", "duration_seconds")
            ),
            "INVALID_ROW",
            location,
            "completion fields",
        )
        require(
            not close or (row["open_quantity"] == 0 and row["duration_seconds"] >= 0),
            "INVALID_ROW",
            location,
            "closed position",
        )
    if section == "visual_history":
        removal = row["action"] == "REMOVE"
        require(
            (row["geometry_type"] is None) == removal and (row["payload_json"] is None) == removal,
            "INVALID_GEOMETRY",
            location,
            "action-specific payload",
        )
        require(
            removal or row["removal_reason"] is None,
            "INVALID_GEOMETRY",
            location,
            "removal reason on active form",
        )
        require(
            row["removal_reason"] is None or len(row["removal_reason"]) <= 1024,
            "INVALID_ROW",
            location,
            "reason length",
        )
        if not removal:
            payload = strict_json(row["payload_json"], location, 16384)
            check_schema(payload, json.loads((HERE / "visual-payload.schema.json").read_text()))
            geometry = payload["geometry"]
            require(
                geometry["kind"] == row["geometry_type"],
                "INVALID_GEOMETRY",
                location,
                "discriminator mismatch",
            )
            for key, value in geometry.items():
                if geometry["kind"] in BASE_GEOMETRIES and key.endswith("_utc"):
                    instant(value, location)
            if geometry["kind"] in {"TREND_LINE", "BOX"}:
                require(
                    geometry["start_time_utc"] < geometry["end_time_utc"],
                    "INVALID_GEOMETRY",
                    location,
                    "empty/reversed interval",
                )
            if geometry["kind"] in {"PRICE_ZONE", "BOX"}:
                require(
                    geometry["price_low"] <= geometry["price_high"],
                    "INVALID_GEOMETRY",
                    location,
                    "price bounds",
                )
            if geometry["kind"] in {"MARKER", "ARROW"}:
                require(
                    (geometry["price"] is not None) == (geometry["placement"] == "PRICE"),
                    "INVALID_GEOMETRY",
                    location,
                    "marker price/placement",
                )
    if section == "indicator_points":
        require(
            (row["value"] is not None) == (row["status"] == "VALUE"),
            "INVALID_ROW",
            location,
            "point status/value",
        )
    if section == "indicator_series":
        require(
            all(1 <= len(row[x]) <= 256 for x in ("name", "component", "unit")),
            "INVALID_ROW",
            location,
            "series labels",
        )
        require(
            row["axis"] != "PRICE" or row["unit"] == manifest["instrument"]["price_unit"],
            "INVALID_ROW",
            location,
            "price-axis units",
        )
        payload_schema = json.loads((HERE / "visual-payload.schema.json").read_text())
        method = strict_json(row["method_json"], location, 16384)
        check_schema(method, payload_schema["properties"]["method"])
        check_schema(
            strict_json(row["style_json"], location, 16384), payload_schema["properties"]["style"]
        )
    if section == "sessions":
        require(1 <= len(row["label"]) <= 256, "INVALID_ROW", location, "session label")
    if section == "monthly_returns":
        require(
            1970 <= row["year"] <= 9999
            and 1 <= row["month"] <= 12
            and 0 <= row["trades_count"] <= MAX_INT,
            "INVALID_ROW",
            location,
            "calendar/count",
        )
        month = f"{row['year']:04d}-{row['month']:02d}"
        require(
            manifest["start_time_utc"][:7] <= month <= manifest["end_time_utc"][:7]
            and row["known_at_utc"] == manifest["end_time_utc"],
            "INVALID_TIME",
            location,
            "monthly span/knowledge",
        )


def deduplicate(section: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    known = {}
    for row in rows:
        decoded = {
            key: strict_json(value, key, 16384)
            if key.endswith("_json") and value is not None
            else value
            for key, value in row.items()
        }
        identity = row["fact_id"]
        if identity in known:
            require(
                semantic_equal(known[identity][1], decoded),
                "CONFLICTING_IDENTITY",
                section,
                identity,
            )
        else:
            known[identity] = row, decoded
    result = [pair[0] for pair in known.values()]
    seen_sequences = set()
    for row in result:
        key = minute(row["known_at_utc"]), row["sequence_num"]
        require(key not in seen_sequences, "INVALID_SEQUENCE", section, "same-minute collision")
        seen_sequences.add(key)
    result.sort(key=lambda row: (minute(row["known_at_utc"]), row["sequence_num"]))
    for before, after in zip(result, result[1:]):
        require(
            minute(before["known_at_utc"]) != minute(after["known_at_utc"])
            or before["known_at_utc"] <= after["known_at_utc"],
            "INVALID_SEQUENCE",
            section,
            "sequence reverses knowledge time",
        )
    return result


def semantic_equal(left: Any, right: Any) -> bool:
    if type(left) in (int, float) and type(right) in (int, float):
        return left == right
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(
            semantic_equal(left[key], right[key]) for key in left
        )
    if isinstance(left, list):
        return len(left) == len(right) and all(
            semantic_equal(a, b) for a, b in zip(left, right, strict=True)
        )
    return left == right


def validate_relationships(data: dict[str, list[dict[str, Any]]], manifest: dict[str, Any]) -> None:
    strategies = {x["strategy_id"]: x for x in manifest["strategies"]}
    executions = {x["execution_id"]: x for x in data.get("trade_facts", [])}
    groups = defaultdict(list)
    for row in executions.values():
        groups[row["position_id"]].append(row)
    for pid, rows in groups.items():
        rows.sort(key=lambda row: (row["known_at_utc"], row["sequence_num"]))
        require(rows[0]["action"] == "ENTRY", "INVALID_LIFECYCLE", pid, "missing ENTRY")
        closed = False
        for i, row in enumerate(rows):
            require(
                not closed and (i == 0 or row["action"] != "ENTRY"),
                "INVALID_LIFECYCLE",
                pid,
                "reopen/duplicate entry",
            )
            expected_side = (
                rows[0]["side"]
                if row["action"] in {"ENTRY", "SCALE_IN"}
                else {"BUY": "SELL", "SELL": "BUY"}[rows[0]["side"]]
            )
            require(row["side"] == expected_side, "INVALID_ROW", pid, "execution side/action")
            require(
                all(row[k] == rows[0][k] for k in ("strategy_id", "setup_id", "session_id")),
                "INVALID_REFERENCE",
                pid,
                "position attribution changed",
            )
            closed = row["action"] == "EXIT"
    sessions = defaultdict(list)
    for row in data.get("sessions", []):
        sessions[row["session_id"]].append(row)
    for sid, rows in sessions.items():
        require(
            len(rows) == 2
            and [x["action"] for x in rows] == ["START", "END"]
            and rows[0]["boundary_time_utc"] < rows[1]["boundary_time_utc"]
            and rows[0]["label"] == rows[1]["label"],
            "INVALID_LIFECYCLE",
            sid,
            "session START/END",
        )
    series = {x["series_id"]: x for x in data.get("indicator_series", [])}
    samples = set()
    for row in data.get("indicator_points", []):
        key = row["series_id"], row["sample_time_utc"]
        require(
            key not in samples, "INVALID_IDENTITY", row["fact_id"], "duplicate/corrected sample"
        )
        samples.add(key)
        require(
            row["series_id"] in series
            and series[row["series_id"]]["known_at_utc"] <= row["known_at_utc"],
            "INVALID_REFERENCE",
            row["fact_id"],
            "series not yet established",
        )
    for section, rows in data.items():
        for row in rows:
            if row.get("strategy_id"):
                strategy = strategies.get(row["strategy_id"])
                require(
                    strategy is not None and strategy["known_at_utc"] <= row["known_at_utc"],
                    "INVALID_REFERENCE",
                    row["fact_id"],
                    "strategy missing/not known",
                )
            if row.get("session_id") and section != "sessions":
                session = sessions.get(row["session_id"])
                require(
                    bool(session) and session[0]["known_at_utc"] <= row["known_at_utc"],
                    "INVALID_REFERENCE",
                    row["fact_id"],
                    "session missing/not known",
                )
            if section == "strategy_events":
                if row["position_id"]:
                    require(
                        row["position_id"] in groups,
                        "INVALID_REFERENCE",
                        row["fact_id"],
                        "missing position",
                    )
                    require(
                        groups[row["position_id"]][0]["known_at_utc"] <= row["known_at_utc"],
                        "INVALID_REFERENCE",
                        row["fact_id"],
                        "position not yet known",
                    )
                if row["execution_id"]:
                    execution = executions.get(row["execution_id"])
                    require(
                        execution is not None
                        and execution["known_at_utc"] <= row["known_at_utc"]
                        and (
                            row["position_id"] is None
                            or row["position_id"] == execution["position_id"]
                        ),
                        "INVALID_REFERENCE",
                        row["fact_id"],
                        "execution missing/not known/mismatched",
                    )
    for section, entity, first, update, terminal in (
        ("visual_history", "visual_id", "CREATE", "UPDATE", "REMOVE"),
        ("position_history", "position_id", "OPEN", "UPDATE", "CLOSE"),
    ):
        histories = defaultdict(list)
        for row in data.get(section, []):
            histories[row[entity]].append(row)
        for identity, rows in histories.items():
            require(rows[0]["action"] == first, "INVALID_LIFECYCLE", identity, "missing first form")
            ended = False
            for i, row in enumerate(rows):
                require(
                    not ended and (i == 0 or row["action"] in {update, terminal}),
                    "INVALID_LIFECYCLE",
                    identity,
                    "illegal transition",
                )
                require(
                    row["session_id"] == rows[0]["session_id"],
                    "INVALID_REFERENCE",
                    identity,
                    "session changed",
                )
                ended = row["action"] == terminal
                if section == "position_history":
                    entry, last = (
                        executions.get(row["entry_execution_id"]),
                        executions.get(row["last_execution_id"]),
                    )
                    require(
                        entry is not None
                        and last is not None
                        and entry["position_id"] == identity
                        and last["position_id"] == identity
                        and entry["action"] == "ENTRY"
                        and entry["known_at_utc"] <= last["known_at_utc"] <= row["known_at_utc"],
                        "INVALID_REFERENCE",
                        identity,
                        "snapshot execution links",
                    )
                    require(
                        row["entry_time_utc"] == entry["timestamp_utc"]
                        and row["entry_price"] == entry["price"]
                        and row["initial_quantity"] == entry["quantity"]
                        and row["direction"] == ("LONG" if entry["side"] == "BUY" else "SHORT"),
                        "INVALID_REFERENCE",
                        identity,
                        "entry fields",
                    )
                    immutable = (
                        "direction",
                        "entry_execution_id",
                        "entry_time_utc",
                        "entry_price",
                        "initial_quantity",
                        "strategy_id",
                        "setup_id",
                        "session_id",
                    )
                    require(
                        all(row[k] == rows[0][k] for k in immutable)
                        and all(
                            row[k] == entry[k] for k in ("strategy_id", "setup_id", "session_id")
                        ),
                        "INVALID_REFERENCE",
                        identity,
                        "immutable snapshot facts",
                    )
                    require(
                        (i != 0 or row["last_execution_id"] == row["entry_execution_id"])
                        and (
                            not ended
                            or (
                                last["action"] == "EXIT"
                                and row["exit_time_utc"] == last["timestamp_utc"]
                            )
                        ),
                        "INVALID_REFERENCE",
                        identity,
                        "OPEN/CLOSE fill",
                    )
    for section, keys in (
        ("equity_curve", ("timestamp_utc",)),
        ("monthly_returns", ("year", "month")),
    ):
        values = [tuple(row[k] for k in keys) for row in data.get(section, [])]
        require(
            len(values) == len(set(values)), "INVALID_IDENTITY", section, "duplicate coordinate"
        )


def expected_states(
    section: str,
    records: list[tuple[dict[str, Any], dict[str, Any], int]],
    manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    """Independently derive the producer index's declared effective coverage."""
    entity_field = PHYSICAL["sections"][section]["entity_field"]
    by_fact = {}
    for row, ref, offset in records:
        by_fact.setdefault(row["fact_id"], (row, ref, offset))
    by_entity = defaultdict(list)
    for row, ref, offset in by_fact.values():
        by_entity[row[entity_field]].append((row, ref, offset))
    output = []
    for identity, history in by_entity.items():
        effective = {}
        for item in sorted(history, key=lambda x: (x[0]["known_at_utc"], x[0]["sequence_num"])):
            effective[minute(item[0]["known_at_utc"])] = item
        values = list(effective.values())
        first = min(history, key=lambda x: (x[0]["known_at_utc"], x[0]["sequence_num"]))[0]
        for i, (row, ref, offset) in enumerate(values):
            if row["action"] == "REMOVE":
                continue
            coordinate_start, coordinate_end = minute(first["known_at_utc"]), None
            if section == "visual_history":
                geometry = strict_json(row["payload_json"], row["fact_id"], 16384)["geometry"]
                kind = geometry["kind"]
                if kind in {"TREND_LINE", "BOX"}:
                    coordinate_start = geometry["start_time_utc"]
                    coordinate_end = (
                        nanosecond_after(geometry["end_time_utc"])
                        if kind == "TREND_LINE"
                        else geometry["end_time_utc"]
                    )
                elif kind in {"MARKER", "ARROW"}:
                    coordinate_start, coordinate_end = (
                        minute(geometry["time_utc"]),
                        minute_after(geometry["time_utc"]),
                    )
                elif kind not in BASE_GEOMETRIES:
                    coordinate_start, coordinate_end = (
                        manifest["start_time_utc"],
                        manifest["end_time_utc"],
                    )
            elif section == "position_history":
                coordinate_start = row["entry_time_utc"]
                coordinate_end = (
                    minute_after(row["exit_time_utc"]) if row["action"] == "CLOSE" else None
                )
            elif section == "sessions":
                coordinate_start = first["boundary_time_utc"]
                coordinate_end = (
                    minute_after(row["boundary_time_utc"]) if row["action"] == "END" else None
                )
            output.append(
                {
                    "entity_id": identity,
                    "fact_id": row["fact_id"],
                    "file": ref,
                    "row": offset,
                    "known_from_utc": minute(row["known_at_utc"]),
                    "known_to_utc": minute(values[i + 1][0]["known_at_utc"])
                    if i + 1 < len(values)
                    else None,
                    "coordinate_start_utc": coordinate_start,
                    "coordinate_end_utc": coordinate_end,
                }
            )
    return sorted(output, key=lambda x: index_key("state", x))


def validate_bundle(root: Path) -> dict[str, Any]:
    """Explicitly validate all known sections and all reachable indexes."""
    access = BundleAccess(root)
    data, records = {}, {}
    unsupported = []
    for name, descriptor in access.manifest["sections"].items():
        access.current_owner = name
        if name not in PHYSICAL["sections"]:
            validate_opaque_indexes(access, name, descriptor)
            unsupported.append(name)
            continue
        tree_paths = set()
        section_rows, section_records = [], []
        seen_shards = set()
        previous = None
        time_paths = set()
        for entry in access.entries(descriptor["time_index"], "time", visited=time_paths):
            require(
                entry["file"]["path"] not in seen_shards, "INVALID_INDEX", name, "duplicate shard"
            )
            seen_shards.add(entry["file"]["path"])
            rows = access.shard(name, entry["file"])
            field = descriptor["time_field"]
            require(
                len(rows) == entry["row_count"]
                and (rows[0][field] if rows else None) == entry["first_time"]
                and (rows[-1][field] if rows else None) == entry["last_time"],
                "INVALID_INDEX",
                name,
                "time coverage",
            )
            if rows and previous is not None:
                require(
                    previous <= row_key(name, rows[0]), "INVALID_ORDER", name, "global shard order"
                )
            if rows:
                previous = row_key(name, rows[-1])
            section_rows.extend(rows)
            section_records.extend((row, entry["file"], i) for i, row in enumerate(rows))
        require(
            len(section_rows) == descriptor["row_count"],
            "INVALID_INDEX",
            name,
            "manifest row count",
        )
        tree_paths.update(time_paths)
        entity_paths = set()
        actual = list(access.entries(descriptor["entity_index"], "entity", visited=entity_paths))
        require(not tree_paths & entity_paths, "INVALID_INDEX", name, "node shared between trees")
        tree_paths.update(entity_paths)
        expected = [
            {
                "entity_id": row[descriptor["entity_field"]],
                "fact_id": row["fact_id"],
                "time_utc": row[field],
                "known_at_utc": row["known_at_utc"],
                "sequence_num": row["sequence_num"],
                "file": ref,
                "row": offset,
            }
            for row, ref, offset in section_records
        ]
        require(
            actual == sorted(expected, key=lambda x: index_key("entity", x)),
            "INVALID_INDEX",
            name,
            "entity coverage",
        )
        data[name] = deduplicate(name, section_rows)
        records[name] = section_records
        if descriptor["state_index"]:
            state_paths = set()
            actual_state = list(
                access.entries(descriptor["state_index"], "state", visited=state_paths)
            )
            require(
                not tree_paths & state_paths, "INVALID_INDEX", name, "node shared between trees"
            )
            require(
                actual_state == expected_states(name, section_records, access.manifest),
                "INVALID_INDEX",
                name,
                "state/predecessor coverage",
            )
        unsupported.extend(
            f"{name}:{row['fact_id']}"
            for row in data[name]
            if name == "visual_history"
            and row["geometry_type"] is not None
            and row["geometry_type"] not in BASE_GEOMETRIES
        )
    validate_relationships(data, access.manifest)
    access.verify_stable()
    return {
        "format_version": "1.0.0",
        "base_contract_valid": True,
        "manifest_sha256": access.manifest_digest,
        "physical_rows": {name: len(items) for name, items in records.items()},
        "semantic_facts": {name: len(items) for name, items in data.items()},
        "opaque_optional_evidence": unsupported,
        "limits": [
            "Does not verify strategy-result accuracy or historical knowledge truth.",
            "Does not prove fsync/publication execution or producer connectedness.",
            "Opaque optional extension internals are not base semantics.",
            "Does not approve current viewer conformance or a production request ceiling.",
        ],
    }


def validate_opaque_indexes(access: BundleAccess, name: str, descriptor: dict[str, Any]) -> None:
    """Check generic opaque envelopes without opening extension payload shards."""
    paths, references = set(), {}
    count = 0
    for kind in ("time", "entity", "state"):
        root = descriptor[kind + "_index"]
        if root is None:
            continue
        visited = set()
        entries = list(access.entries(root, kind, visited=visited))
        require(not paths & visited, "INVALID_INDEX", name, "node shared between trees")
        paths.update(visited)
        for entry in entries:
            ref = entry["file"]
            validate_path(ref["path"])
            require(
                access.owners.get(ref["path"], name) == name,
                "INVALID_INDEX",
                ref["path"],
                "cross-section ownership",
            )
            access.owners[ref["path"]] = name
            if kind == "time":
                require(
                    ref["path"] not in references, "INVALID_INDEX", name, "duplicate opaque shard"
                )
                references[ref["path"]] = entry
                count += entry["row_count"]
                if entry["row_count"]:
                    require(
                        instant(entry["first_time"]) <= instant(entry["last_time"]),
                        "INVALID_INDEX",
                        name,
                        "opaque time bounds",
                    )
                else:
                    require(
                        entry["first_time"] is None and entry["last_time"] is None,
                        "INVALID_INDEX",
                        name,
                        "opaque empty bounds",
                    )
            else:
                shard = references.get(ref["path"])
                require(
                    shard is not None
                    and shard["file"] == ref
                    and entry["row"] < shard["row_count"],
                    "INVALID_INDEX",
                    name,
                    "opaque row reference",
                )
                for field_name, value in entry.items():
                    if field_name.endswith("_utc") and value is not None:
                        instant(value)
        if kind == "time":
            require(
                count == descriptor["row_count"], "INVALID_INDEX", name, "opaque declared row count"
            )
        elif kind == "entity":
            require(len(entries) == count, "INVALID_INDEX", name, "opaque entity count")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(validate_bundle(args.bundle), indent=2))
    except (ContractError, OSError, pa.ArrowException) as exc:
        print(json.dumps({"base_contract_valid": False, "error": str(exc)}))
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
