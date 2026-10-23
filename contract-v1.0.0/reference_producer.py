"""Independent v1.0 byte producer; no imports from viewer or validator.

Input is {manifest: metadata without sections, rows: {section: [full rows]}}.
The caller owns semantic validity. Publication refuses an existing destination.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
REGISTRY = json.loads((HERE / "physical-schemas.json").read_text())["sections"]


def encode(value) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n"
    ).encode()


def floor_time(value):
    return value[:16] + ":00.000000000Z"


def next_minute(value):
    return (datetime.fromisoformat(value[:16]) + timedelta(minutes=1)).strftime(
        "%Y-%m-%dT%H:%M:00.000000000Z"
    )


def after_endpoint(value):
    digits = int(value[20:29])
    if digits != 999999999:
        return value[:20] + f"{digits + 1:09d}Z"
    return (datetime.fromisoformat(value[:19]) + timedelta(seconds=1)).strftime(
        "%Y-%m-%dT%H:%M:%S.000000000Z"
    )


def key(kind, entry):
    if kind == "time":
        return entry["first_time"] or ""
    if kind == "entity":
        return "{}|{}|{:016d}|{}".format(
            entry["entity_id"], entry["time_utc"], entry["sequence_num"], entry["fact_id"]
        )
    return "{}|{}|{}".format(
        entry["coordinate_start_utc"], entry["known_from_utc"], entry["fact_id"]
    )


def bounds(kind, entries, branch=False):
    """Compute exact envelopes from emitted entries independently of validator."""
    result = {
        name: None
        for name in ("min_key", "max_key", "min_start", "max_end", "min_known", "max_known_end")
    }
    result["count"] = 0
    children = [item["summary"] for item in entries if item["summary"]["count"]] if branch else []
    if branch and children:
        result.update(
            count=sum(item["count"] for item in children),
            min_key=min(item["min_key"] for item in children),
            max_key=max(item["max_key"] for item in children),
        )
        if kind == "state":
            for name in ("min_start", "min_known"):
                result[name] = min(item[name] for item in children)
            for name in ("max_end", "max_known_end"):
                result[name] = (
                    None
                    if any(item[name] is None for item in children)
                    else max(item[name] for item in children)
                )
    elif not branch:
        active = [item for item in entries if kind != "time" or item["row_count"]]
        result["count"] = (
            sum(item["row_count"] for item in entries) if kind == "time" else len(entries)
        )
        if active:
            result["min_key"] = min(key(kind, item) for item in active)
            result["max_key"] = max(
                item["last_time"] if kind == "time" else key(kind, item) for item in active
            )
            if kind == "state":
                result["min_start"] = min(item["coordinate_start_utc"] for item in active)
                result["min_known"] = min(item["known_from_utc"] for item in active)
                for source, target in (
                    ("coordinate_end_utc", "max_end"),
                    ("known_to_utc", "max_known_end"),
                ):
                    result[target] = (
                        None
                        if any(item[source] is None for item in active)
                        else max(item[source] for item in active)
                    )
    return result


def state_entries(section, located, manifest):
    unique = {}
    for row, ref, offset in located:
        unique.setdefault(row["fact_id"], (row, ref, offset))
    histories = defaultdict(list)
    for item in unique.values():
        histories[item[0][REGISTRY[section]["entity_field"]]].append(item)
    entries = []
    for identity, items in histories.items():
        items.sort(key=lambda item: (item[0]["known_at_utc"], item[0]["sequence_num"]))
        by_minute = {floor_time(item[0]["known_at_utc"]): item for item in items}
        effective = list(by_minute.values())
        first = items[0][0]
        for number, (row, ref, offset) in enumerate(effective):
            if row["action"] == "REMOVE":
                continue
            start, end = floor_time(first["known_at_utc"]), None
            if section == "visual_history":
                geometry = json.loads(row["payload_json"])["geometry"]
                kind = geometry["kind"]
                if kind in {"BOX", "TREND_LINE"}:
                    start = geometry["start_time_utc"]
                    end = (
                        geometry["end_time_utc"]
                        if kind == "BOX"
                        else after_endpoint(geometry["end_time_utc"])
                    )
                elif kind in {"MARKER", "ARROW"}:
                    start, end = floor_time(geometry["time_utc"]), next_minute(geometry["time_utc"])
                elif kind not in {"HORIZONTAL_LEVEL", "PRICE_ZONE"}:
                    start, end = manifest["start_time_utc"], manifest["end_time_utc"]
            elif section == "position_history":
                start = row["entry_time_utc"]
                end = next_minute(row["exit_time_utc"]) if row["action"] == "CLOSE" else None
            elif section == "sessions":
                start = first["boundary_time_utc"]
                end = next_minute(row["boundary_time_utc"]) if row["action"] == "END" else None
            entries.append(
                dict(
                    entity_id=identity,
                    fact_id=row["fact_id"],
                    file=ref,
                    row=offset,
                    known_from_utc=floor_time(row["known_at_utc"]),
                    known_to_utc=floor_time(effective[number + 1][0]["known_at_utc"])
                    if number + 1 < len(effective)
                    else None,
                    coordinate_start_utc=start,
                    coordinate_end_utc=end,
                )
            )
    return sorted(entries, key=lambda item: key("state", item))


def write_bundle(
    destination: Path,
    source: dict,
    shard_rows: int = 4096,
    typed_empty: bool = False,
    validate: bool = False,
) -> Path:
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(destination)
    if not 1 <= shard_rows <= 4096:
        raise ValueError("shard_rows must be 1..4096")
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".bundle-staging-", dir=destination.parent))
    manifest = json.loads(json.dumps(source["manifest"]))
    manifest["sections"] = {}

    def store_bytes(path, raw):
        target = stage / path
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        return dict(path=path, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))

    def tree(section, kind, entries):
        current, level = [], 0
        chunks = [entries[i : i + 64] for i in range(0, len(entries), 64)] or [[]]
        while True:
            for number, chunk in enumerate(chunks):
                summary = bounds(kind, chunk, level > 0)
                node = dict(index_kind=kind, level=level, summary=summary, entries=chunk)
                raw = encode(node)
                if len(raw) > 65536:
                    raise ValueError("index byte limit exceeded")
                ref = store_bytes(f"indexes/{section}-{kind}-{level}-{number}.json", raw)
                current.append(dict(file=ref, summary=summary))
            if len(current) == 1:
                return current[0]["file"]
            if level == 31:
                raise ValueError("index depth exceeded")
            chunks = [current[i : i + 64] for i in range(0, len(current), 64)]
            current, level = [], level + 1

    for section, input_rows in source["rows"].items():
        layout = REGISTRY[section]
        time_field, entity_field = layout["time_field"], layout["entity_field"]
        rows = sorted(
            input_rows,
            key=lambda row: (
                row[time_field],
                row["known_at_utc"],
                row["sequence_num"],
                row["fact_id"],
            ),
        )
        types = {"string": pa.string(), "int64": pa.int64(), "float64": pa.float64()}
        schema = pa.schema(
            [
                pa.field(item["name"], types[item["type"]], nullable=item["nullable"])
                for item in layout["fields"]
            ],
            metadata={b"bv.contract": b"run-bundle/1.0.0", b"bv.section": section.encode()},
        )
        time_entries, located = [], []
        chunks = [rows[i : i + shard_rows] for i in range(0, len(rows), shard_rows)] or (
            [[]] if typed_empty else []
        )
        for number, chunk in enumerate(chunks):
            table = pa.Table.from_pylist(chunk, schema=schema)
            sink = pa.BufferOutputStream()
            pq.write_table(table, sink, version="2.6", compression="zstd", row_group_size=4096)
            raw = sink.getvalue().to_pybytes()
            if len(raw) > 8388608:
                raise ValueError("shard stored byte limit exceeded")
            ref = store_bytes(f"data/{section}-{number}.parquet", raw)
            time_entries.append(
                dict(
                    file=ref,
                    row_count=len(chunk),
                    first_time=chunk[0][time_field] if chunk else None,
                    last_time=chunk[-1][time_field] if chunk else None,
                )
            )
            located.extend((row, ref, i) for i, row in enumerate(chunk))
        entity_entries = [
            dict(
                entity_id=row[entity_field],
                fact_id=row["fact_id"],
                time_utc=row[time_field],
                known_at_utc=row["known_at_utc"],
                sequence_num=row["sequence_num"],
                file=ref,
                row=offset,
            )
            for row, ref, offset in located
        ]
        entity_entries.sort(key=lambda item: key("entity", item))
        manifest["sections"][section] = dict(
            schema_id=f"run-bundle/1.0.0/{section}",
            optional=section != "trade_facts",
            row_count=len(rows),
            time_field=time_field,
            entity_field=entity_field,
            time_index=tree(section, "time", time_entries),
            entity_index=tree(section, "entity", entity_entries),
            state_index=tree(section, "state", state_entries(section, located, manifest))
            if layout["state_index"]
            else None,
        )
    # Encoding does not depend on validator logic. The public CLI validates in a
    # separate process before rename; tests use the explicit low-level mode to
    # emit coherent indexes around invalid rows and challenge validation.
    raw_manifest = encode(manifest)
    if len(raw_manifest) > 1048576:
        raise ValueError("manifest byte limit exceeded")
    store_bytes("manifest.tmp", raw_manifest)
    os.rename(stage / "manifest.tmp", stage / "manifest.json")
    if validate:
        subprocess.run(
            [sys.executable, str(HERE / "contract_tools.py"), str(stage)],
            check=True,
            capture_output=True,
            text=True,
        )
    for directory, _, _ in os.walk(stage, topdown=False):
        fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    # Caller must serialize publications in this parent. Never replace/reuse IDs.
    if destination.exists():
        raise FileExistsError(destination)
    os.rename(stage, destination)
    fd = os.open(destination.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    return destination


def example_input():
    def at(h, m=0, seconds=0):
        return f"2026-01-05T{h:02d}:{m:02d}:{seconds:02d}.000000000Z"

    def row(section, fid, known, seq=0, **values):
        values.update(fact_id=fid, known_at_utc=known, sequence_num=seq, metadata_json="{}")
        return {field["name"]: values.get(field["name"]) for field in REGISTRY[section]["fields"]}

    def payload(geometry, method=None):
        return json.dumps(
            dict(geometry=geometry, label=None, method=method, style={}, extensions={})
        )

    start, end = at(9), at(11)
    manifest = dict(
        contract_id="backtest-viewer.run-bundle",
        format_version="1.0.0",
        run_id="reference-run",
        completed=True,
        completed_at_utc="2026-01-06T00:00:00.000000000Z",
        asset_name="EURUSD",
        timeframe="M1",
        start_time_utc=start,
        end_time_utc=end,
        initial_balance=10000.0,
        instrument=dict(
            price_unit="USD/EUR",
            quantity_unit="EUR",
            quote_currency="USD",
            account_currency="USD",
            price_decimals=5,
            quantity_decimals=0,
            price_basis="BID",
            market_dataset_id=None,
        ),
        primary_strategy_id="primary",
        strategies=[
            dict(
                strategy_id="primary",
                name="ORB",
                version="runner-example",
                parent_strategy_id=None,
                known_at_utc=start,
                metadata={},
            ),
            dict(
                strategy_id="confirmation",
                name="EMA confirmation",
                version="runner-example",
                parent_strategy_id="primary",
                known_at_utc=start,
                metadata={},
            ),
        ],
        execution_settings={"spread_model": "producer-defined"},
        source_data_location=None,
        report=dict(
            summary=dict(
                total_net_profit=12.0,
                gross_profit=15.0,
                gross_loss=0.0,
                total_trades=1,
                profit_factor=None,
                expected_payoff=12.0,
                return_on_max_drawdown=6.0,
            ),
            trade_stats=dict(
                winning_trades=1,
                losing_trades=0,
                win_rate=1.0,
                average_win=12.0,
                average_loss=None,
                win_loss_ratio=None,
                max_consecutive_wins=1,
                max_consecutive_losses=0,
                largest_winning_trade=12.0,
                largest_losing_trade=None,
                average_trade_duration_seconds=3000.0,
            ),
            drawdown=dict(
                max_drawdown=2.0,
                max_drawdown_pct=0.0002,
                relative_drawdown_pct=0.0002,
                relative_drawdown=2.0,
            ),
            unavailable_reasons={},
        ),
        required_features=["core.v1"],
        extensions={},
    )
    fills = []
    for fid, when, action, side, quantity, price, gross, cost in [
        ("fill-1", at(9, 10), "ENTRY", "BUY", 1000.0, 1.1, None, 1.0),
        ("fill-2", at(9, 20), "SCALE_IN", "BUY", 500.0, 1.102, None, 0.5),
        ("fill-3", at(9, 30), "SCALE_OUT", "SELL", 500.0, 1.11, 5.0, 0.5),
        ("fill-4", at(10), "EXIT", "SELL", 1000.0, 1.112, 10.0, 1.0),
    ]:
        fills.append(
            row(
                "trade_facts",
                fid,
                when,
                execution_id=fid,
                position_id="position-1",
                timestamp_utc=when,
                side=side,
                action=action,
                quantity=quantity,
                price=price,
                realized_gross_pnl=gross,
                commission=cost,
                other_costs=0.0,
                strategy_id="primary",
                setup_id="setup-1",
                session_id="london",
            )
        )
    positions = []
    for number, (when, action, current, entered, exited, realized) in enumerate(
        [
            (at(9, 10), "OPEN", 1000.0, 1000.0, 0.0, -1.0),
            (at(9, 20), "UPDATE", 1500.0, 1500.0, 0.0, -1.5),
            (at(9, 30), "UPDATE", 1000.0, 1500.0, 500.0, 3.0),
            (at(10), "CLOSE", 0.0, 1500.0, 1500.0, 12.0),
        ],
        1,
    ):
        positions.append(
            row(
                "position_history",
                f"position-state-{number}",
                when,
                position_id="position-1",
                action=action,
                direction="LONG",
                entry_execution_id="fill-1",
                last_execution_id=f"fill-{number}",
                entry_time_utc=at(9, 10),
                entry_price=1.1,
                initial_quantity=1000.0,
                open_quantity=current,
                total_entry_quantity=entered,
                total_exit_quantity=exited,
                realized_net_pnl=realized,
                net_pnl=12.0 if action == "CLOSE" else None,
                exit_time_utc=at(10) if action == "CLOSE" else None,
                duration_seconds=3000.0 if action == "CLOSE" else None,
                strategy_id="primary",
                setup_id="setup-1",
                session_id="london",
            )
        )
    visuals = [
        row(
            "visual_history",
            "orb-create",
            at(9, 5),
            visual_id="orb",
            action="CREATE",
            geometry_type="BOX",
            payload_json=payload(
                dict(
                    kind="BOX",
                    start_time_utc=start,
                    end_time_utc=at(9, 30),
                    price_low=1.09,
                    price_high=1.105,
                )
            ),
            session_id="london",
        ),
        row(
            "visual_history",
            "fib-create",
            at(9, 15),
            visual_id="fib",
            action="CREATE",
            geometry_type="HORIZONTAL_LEVEL",
            payload_json=payload(
                dict(kind="HORIZONTAL_LEVEL", price=1.108),
                dict(name="Fibonacci", parameters={"ratio": 0.618}, metadata={}),
            ),
            session_id="london",
        ),
        row(
            "visual_history",
            "fib-update",
            at(9, 25),
            visual_id="fib",
            action="UPDATE",
            geometry_type="HORIZONTAL_LEVEL",
            payload_json=payload(dict(kind="HORIZONTAL_LEVEL", price=1.109)),
            session_id="london",
        ),
        row(
            "visual_history",
            "fib-remove",
            at(10, 15),
            visual_id="fib",
            action="REMOVE",
            removal_reason="producer lifecycle ended",
            session_id="london",
        ),
        row(
            "visual_history",
            "entry-marker",
            at(9, 10),
            visual_id="marker",
            action="CREATE",
            geometry_type="ARROW",
            payload_json=payload(
                dict(kind="ARROW", time_utc=at(9, 10), placement="PRICE", price=1.1, direction="UP")
            ),
            session_id="london",
        ),
    ]
    rows = dict(
        trade_facts=fills,
        position_history=positions,
        strategy_events=[
            row(
                "strategy_events",
                "event-1",
                at(9, 10),
                event_id="event-1",
                timestamp_utc=at(9, 10),
                event_type="ENTRY_CONFIRMED",
                message="Producer emitted confirmation",
                position_id="position-1",
                execution_id="fill-1",
                strategy_id="primary",
                setup_id="setup-1",
                session_id="london",
            )
        ],
        visual_history=visuals,
        indicator_series=[
            row(
                "indicator_series",
                "ema",
                start,
                series_id="ema",
                name="EMA",
                component="value",
                unit="USD/EUR",
                axis="PRICE",
                method_json=json.dumps(dict(name="EMA", parameters={"period": 20}, metadata={})),
                style_json="{}",
                session_id="london",
            )
        ],
        indicator_points=[
            row(
                "indicator_points",
                "point-1",
                at(9, 1),
                series_id="ema",
                sample_time_utc=at(9, 1),
                value=None,
                status="WARMUP",
            ),
            row(
                "indicator_points",
                "point-2",
                at(9, 2),
                series_id="ema",
                sample_time_utc=at(9, 2),
                value=1.1,
                status="VALUE",
            ),
            row(
                "indicator_points",
                "point-3",
                at(9, 6),
                series_id="ema",
                sample_time_utc=at(9, 3),
                value=1.101,
                status="VALUE",
            ),
            row(
                "indicator_points",
                "point-4",
                at(9, 4),
                series_id="ema",
                sample_time_utc=at(9, 4),
                value=None,
                status="GAP",
            ),
        ],
        sessions=[
            row(
                "sessions",
                "london-start",
                start,
                session_id="london",
                action="START",
                boundary_time_utc=start,
                label="London",
            ),
            row(
                "sessions",
                "overlap-start",
                at(9, 1),
                session_id="overlap",
                action="START",
                boundary_time_utc=at(9, 1),
                label="Independent no-trade session",
            ),
            row(
                "sessions",
                "overlap-end",
                at(9, 45),
                session_id="overlap",
                action="END",
                boundary_time_utc=at(9, 45),
                label="Independent no-trade session",
            ),
            row(
                "sessions",
                "london-end",
                end,
                session_id="london",
                action="END",
                boundary_time_utc=end,
                label="London",
            ),
        ],
        equity_curve=[
            row(
                "equity_curve",
                "curve-1",
                start,
                timestamp_utc=start,
                equity=10000.0,
                balance=10000.0,
            ),
            row(
                "equity_curve",
                "curve-2",
                at(9, 10),
                timestamp_utc=at(9, 10),
                equity=9998.0,
                balance=9999.0,
            ),
            row("equity_curve", "curve-3", end, timestamp_utc=end, equity=10012.0, balance=10012.0),
        ],
        monthly_returns=[
            row(
                "monthly_returns",
                "month-1",
                end,
                year=2026,
                month=1,
                return_pct=0.12,
                profit=12.0,
                trades_count=1,
            )
        ],
    )
    return dict(manifest=manifest, rows=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--shard-rows", type=int, default=4096)
    parser.add_argument("--typed-empty", action="store_true")
    args = parser.parse_args()
    source = json.loads(args.input.read_text()) if args.input else example_input()
    print(write_bundle(args.output, source, args.shard_rows, args.typed_empty, validate=True))


if __name__ == "__main__":
    main()
