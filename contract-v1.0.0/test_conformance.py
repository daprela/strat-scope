"""Authoring conformance challenges; production viewer is not the oracle."""

import hashlib
import json
from copy import deepcopy
from datetime import datetime, timedelta

import contract_tools as c
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
import reference_producer as p


def at(hour=9, minute=0, seconds=0):
    return f"2026-01-05T{hour:02d}:{minute:02d}:{seconds:02d}.000000000Z"


@pytest.fixture
def source():
    return p.example_input()


@pytest.fixture
def bundle(tmp_path, source):
    return p.write_bundle(tmp_path / "run", source, shard_rows=2)


def rewrite_manifest(bundle, change):
    path = bundle / "manifest.json"
    data = json.loads(path.read_text())
    change(data)
    path.write_bytes(p.encode(data))


def resign(bundle, changed_path):
    """Resign a changed fixture so semantic checks survive digest qualification."""

    def refresh(ref):
        path = bundle / ref["path"]
        if ref["path"].endswith(".json"):
            node = json.loads(path.read_text())
            for entry in node["entries"]:
                if "file" in entry:
                    refresh(entry["file"])
            path.write_bytes(p.encode(node))
        raw = path.read_bytes()
        ref.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

    manifest = json.loads((bundle / "manifest.json").read_text())
    assert (bundle / changed_path).exists()
    for descriptor in manifest["sections"].values():
        for kind in ("time_index", "entity_index", "state_index"):
            if descriptor[kind]:
                refresh(descriptor[kind])
    (bundle / "manifest.json").write_bytes(p.encode(manifest))


def assert_rejected(bundle, code):
    with pytest.raises(c.ContractError) as error:
        c.validate_bundle(bundle)
    assert error.value.code == code


def test_all_nine_sections_cross_producer_validation(bundle):
    report = c.validate_bundle(bundle)
    assert report["base_contract_valid"]
    assert report["physical_rows"] == {
        "trade_facts": 4,
        "position_history": 4,
        "strategy_events": 1,
        "visual_history": 5,
        "indicator_series": 1,
        "indicator_points": 4,
        "sessions": 4,
        "equity_curve": 3,
        "monthly_returns": 1,
    }
    assert len(report["limits"]) == 4


@pytest.mark.parametrize("typed", [False, True], ids=["empty-index", "typed-zero-row-parquet"])
def test_zero_trade_unavailable_reports(tmp_path, source, typed):
    source["rows"] = {"trade_facts": []}
    source["manifest"]["report"] = dict(
        summary=None,
        trade_stats=None,
        drawdown=None,
        unavailable_reasons={
            "summary": "not supplied",
            "trade_stats": "not supplied",
            "drawdown": "not supplied",
        },
    )
    root = p.write_bundle(tmp_path / "zero", source, typed_empty=typed)
    assert c.validate_bundle(root)["semantic_facts"]["trade_facts"] == 0


def test_identical_repeats_have_full_physical_coverage(tmp_path, source):
    original = source["rows"]["trade_facts"][0]
    original["metadata_json"] = '{"a":1,"b":[2,3]}'
    repeat = deepcopy(original)
    repeat["metadata_json"] = '{ "b": [2, 3], "a": 1.0 }'
    source["rows"]["trade_facts"].append(repeat)
    report = c.validate_bundle(p.write_bundle(tmp_path / "duplicate", source, shard_rows=2))
    assert report["physical_rows"]["trade_facts"] == 5
    assert report["semantic_facts"]["trade_facts"] == 4


def test_same_minute_terminal_has_no_state(tmp_path, source):
    removal = source["rows"]["visual_history"][3]
    removal.update(known_at_utc=at(9, 15, 30), sequence_num=1)
    source["rows"]["visual_history"].pop(2)
    root = p.write_bundle(tmp_path / "same-minute", source)
    c.validate_bundle(root)
    result = c.BundleAccess(root, c.Budget()).state_rows(
        "visual_history", at(9, 15), at(9, 16), at(9, 15)
    )
    assert "fib" not in {row["visual_id"] for row in result}


def test_new_same_minute_form_is_complete_replacement(tmp_path, source):
    updated = source["rows"]["visual_history"][2]
    updated.update(known_at_utc=at(9, 15, 30), sequence_num=1)
    root = p.write_bundle(tmp_path / "replacement", source)
    c.validate_bundle(root)
    result = c.BundleAccess(root, c.Budget()).state_rows(
        "visual_history", at(9, 20), at(9, 21), at(9, 15)
    )
    fib = next(row for row in result if row["visual_id"] == "fib")
    assert fib["fact_id"] == "fib-update"
    assert json.loads(fib["payload_json"])["method"] is None


def test_carry_in_and_removal_queries_are_bounded(bundle):
    budget = c.Budget(max_nodes=2, max_rows=2)
    access = c.BundleAccess(bundle, budget)
    rows = access.state_rows("visual_history", at(9, 50), at(9, 51), at(9, 50))
    assert [row["fact_id"] for row in rows] == ["fib-update"]
    assert budget.rows == 2  # The selected state shares a shard with its CREATE.
    assert (
        c.BundleAccess(bundle, c.Budget()).state_rows(
            "visual_history", at(10, 20), at(10, 21), at(10, 20)
        )
        == []
    )


def test_future_geometry_is_known_and_early_market_sample_is_withheld(bundle):
    access = c.BundleAccess(bundle, c.Budget())
    orb = access.state_rows("visual_history", at(9, 20), at(9, 21), at(9, 5))
    assert [row["fact_id"] for row in orb] == ["orb-create"]
    rows = c.BundleAccess(bundle, c.Budget()).replay_time_rows(
        "indicator_points", at(9, 1), at(9, 5), at(9, 4)
    )
    assert {row["fact_id"] for row in rows} == {"point-1", "point-2", "point-4"}
    predecessor = c.BundleAccess(bundle, c.Budget()).predecessor(
        "indicator_points", "ema", at(9, 4), at(9, 4)
    )
    assert predecessor["fact_id"] == "point-2"


def test_predecessor_exhaustion_does_not_claim_absence(bundle):
    access = c.BundleAccess(bundle, c.Budget(max_predecessors=1))
    with pytest.raises(c.ContractError, match="REFUSED_OVER_LIMIT"):
        access.predecessor("indicator_points", "ema", at(9, 4), at(9, 4))


@pytest.mark.parametrize("section", ["equity_curve", "monthly_returns"])
def test_report_embargo_even_for_early_coordinates(bundle, section):
    with pytest.raises(c.ContractError, match="REPORT_EMBARGOED"):
        c.BundleAccess(bundle, c.Budget()).replay_time_rows(section, at(), at(12), at(10))
    assert c.BundleAccess(bundle, c.Budget()).replay_time_rows(section, at(), at(12), at(11))


def test_independent_session_start_and_unclosed_position(bundle):
    rows = c.BundleAccess(bundle, c.Budget()).state_rows("sessions", at(9, 2), at(9, 3), at(9, 2))
    assert {row["session_id"] for row in rows} == {"london", "overlap"}
    positions = c.BundleAccess(bundle, c.Budget()).state_rows(
        "position_history", at(9, 40), at(9, 41), at(9, 40)
    )
    assert positions[0]["action"] == "UPDATE"
    assert positions[0]["net_pnl"] is None


def test_nanosecond_inclusive_endpoint(tmp_path, source):
    row = source["rows"]["visual_history"][0]
    row["geometry_type"] = "TREND_LINE"
    payload = json.loads(row["payload_json"])
    payload["geometry"] = dict(
        kind="TREND_LINE",
        start_time_utc=at(),
        end_time_utc="2026-01-05T09:30:00.123456789Z",
        price_start=1.0,
        price_end=2.0,
    )
    row["payload_json"] = json.dumps(payload)
    root = p.write_bundle(tmp_path / "nanoseconds", source)
    c.validate_bundle(root)
    result = c.BundleAccess(root, c.Budget()).state_rows(
        "visual_history",
        payload["geometry"]["end_time_utc"],
        "2026-01-05T09:30:00.123456790Z",
        at(9, 5),
    )
    assert result[0]["fact_id"] == "orb-create"


def test_negative_prices_rebates_and_unassigned_trades(tmp_path, source):
    source["rows"] = {"trade_facts": [source["rows"]["trade_facts"][0]]}
    row = source["rows"]["trade_facts"][0]
    row.update(
        price=-1.0,
        commission=-0.5,
        strategy_id=None,
        session_id=None,
        setup_id=None,
        metadata_json='{"signed":-3}',
    )
    assert (
        c.validate_bundle(p.write_bundle(tmp_path / "signed", source))["semantic_facts"][
            "trade_facts"
        ]
        == 1
    )


def test_opaque_geometry_is_valid_but_withheld(tmp_path, source):
    row = source["rows"]["visual_history"][0]
    row["geometry_type"] = "runner.curve"
    payload = json.loads(row["payload_json"])
    payload["geometry"] = dict(kind="runner.curve", opaque=[1, 2, 3])
    row["payload_json"] = json.dumps(payload)
    root = p.write_bundle(tmp_path / "opaque", source)
    result = c.validate_bundle(root)
    assert result["opaque_optional_evidence"] == ["visual_history:orb-create"]
    with pytest.raises(c.ContractError, match="UNSUPPORTED_GEOMETRY"):
        c.BundleAccess(root, c.Budget()).state_rows(
            "visual_history", at(9, 20), at(9, 21), at(9, 5)
        )


MANIFEST_FAILURES = [
    ("missing-run-id", lambda m: m.pop("run_id"), "INVALID_SCHEMA"),
    ("whitespace-id", lambda m: m.update(run_id=" run "), "INVALID_SCHEMA"),
    ("completed-string", lambda m: m.update(completed="true"), "INVALID_SCHEMA"),
    ("completed-false", lambda m: m.update(completed=False), "INVALID_SCHEMA"),
    (
        "invalid-completion",
        lambda m: m.update(completed_at_utc="2026-02-30T00:00:00.000000000Z"),
        "INVALID_TIME",
    ),
    ("unknown-version", lambda m: m.update(format_version="2.0.0"), "UNSUPPORTED_VERSION"),
    ("missing-version", lambda m: m.pop("format_version"), "UNSUPPORTED_VERSION"),
    (
        "unknown-required-feature",
        lambda m: m["required_features"].append("runner.required"),
        "UNSUPPORTED_REQUIRED_FEATURE",
    ),
    ("equal-interval", lambda m: m.update(end_time_utc=m["start_time_utc"]), "INVALID_RANGE"),
    (
        "timezone-offset",
        lambda m: m.update(start_time_utc="2026-01-05T09:00:00.000000000+00:00"),
        "INVALID_SCHEMA",
    ),
    ("inline-equity-alias", lambda m: m.update(equity_curve=[]), "INVALID_SCHEMA"),
    ("no-core-section", lambda m: m["sections"].pop("trade_facts"), "INVALID_SCHEMA"),
    ("bad-count", lambda m: m["sections"]["trade_facts"].update(row_count=99), "INVALID_INDEX"),
    ("count-bool", lambda m: m["sections"]["trade_facts"].update(row_count=True), "INVALID_SCHEMA"),
    (
        "primary-parent",
        lambda m: m["strategies"][0].update(parent_strategy_id="confirmation"),
        "INVALID_REFERENCE",
    ),
    (
        "strategy-cycle",
        lambda m: m["strategies"][1].update(parent_strategy_id="confirmation"),
        "INVALID_REFERENCE",
    ),
    (
        "primary-mismatch",
        lambda m: m.update(primary_strategy_id="confirmation"),
        "INVALID_REFERENCE",
    ),
    ("report-empty", lambda m: m["report"].update(summary={}), "INVALID_SCHEMA"),
    ("report-reason-missing", lambda m: m["report"].update(summary=None), "INVALID_REPORT"),
    ("ratio-domain", lambda m: m["report"]["trade_stats"].update(win_rate=80.0), "INVALID_SCHEMA"),
    (
        "count-total",
        lambda m: m["report"]["trade_stats"].update(winning_trades=2),
        "INVALID_REPORT",
    ),
]


@pytest.mark.parametrize(
    "name,change,code", MANIFEST_FAILURES, ids=[item[0] for item in MANIFEST_FAILURES]
)
def test_manifest_rejections(bundle, name, change, code):
    rewrite_manifest(bundle, change)
    assert_rejected(bundle, code)


SEMANTIC_FAILURES = [
    ("missing-entry", "trade_facts", 0, {"action": "SCALE_IN"}, "INVALID_LIFECYCLE"),
    ("exit-side", "trade_facts", 3, {"side": "BUY"}, "INVALID_ROW"),
    ("nonpositive-fill", "trade_facts", 0, {"quantity": 0.0}, "INVALID_ROW"),
    ("nan-price", "trade_facts", 0, {"price": float("nan")}, "INVALID_NUMBER"),
    ("empty-fact-id", "trade_facts", 0, {"fact_id": ""}, "INVALID_ID"),
    ("execution-id-mismatch", "trade_facts", 0, {"execution_id": "different"}, "INVALID_ID"),
    ("future-occurrence", "trade_facts", 0, {"timestamp_utc": at(10)}, "INVALID_TIME"),
    ("unknown-strategy", "trade_facts", 0, {"strategy_id": "missing"}, "INVALID_REFERENCE"),
    ("sequence-negative", "trade_facts", 0, {"sequence_num": -1}, "INVALID_SEQUENCE"),
    ("sequence-unsafe", "trade_facts", 0, {"sequence_num": c.MAX_INT + 1}, "INVALID_SEQUENCE"),
    (
        "changed-position-attribution",
        "trade_facts",
        1,
        {"strategy_id": "confirmation"},
        "INVALID_REFERENCE",
    ),
    ("missing-session", "trade_facts", 0, {"session_id": "missing"}, "INVALID_REFERENCE"),
    ("event-missing-fill", "strategy_events", 0, {"execution_id": "missing"}, "INVALID_REFERENCE"),
    (
        "event-future-position",
        "strategy_events",
        0,
        {"known_at_utc": at(9, 5), "timestamp_utc": at(9, 5), "execution_id": None},
        "INVALID_REFERENCE",
    ),
    ("position-missing-open", "position_history", 0, {"action": "UPDATE"}, "INVALID_LIFECYCLE"),
    ("position-early-outcome", "position_history", 0, {"net_pnl": 12.0}, "INVALID_ROW"),
    ("position-wrong-entry", "position_history", 0, {"entry_price": 1.2}, "INVALID_REFERENCE"),
    ("position-close-still-open", "position_history", 3, {"open_quantity": 10.0}, "INVALID_ROW"),
    ("visual-missing-create", "visual_history", 0, {"action": "UPDATE"}, "INVALID_LIFECYCLE"),
    ("visual-remove-geometry", "visual_history", 3, {"geometry_type": "BOX"}, "INVALID_GEOMETRY"),
    ("visual-session-change", "visual_history", 2, {"session_id": "overlap"}, "INVALID_REFERENCE"),
    ("point-gap-value", "indicator_points", 3, {"value": 1.0}, "INVALID_ROW"),
    ("point-unknown-series", "indicator_points", 0, {"series_id": "missing"}, "INVALID_REFERENCE"),
    ("point-future-sample", "indicator_points", 0, {"sample_time_utc": at(10)}, "INVALID_TIME"),
    ("point-correction", "indicator_points", 2, {"sample_time_utc": at(9, 2)}, "INVALID_IDENTITY"),
    ("series-wrong-unit", "indicator_series", 0, {"unit": "pips"}, "INVALID_ROW"),
    ("session-label-changed", "sessions", 2, {"label": "changed"}, "INVALID_LIFECYCLE"),
    ("monthly-month-invalid", "monthly_returns", 0, {"month": 13}, "INVALID_ROW"),
    ("monthly-early-knowledge", "monthly_returns", 0, {"known_at_utc": at(10)}, "INVALID_TIME"),
]


@pytest.mark.parametrize(
    "name,section,offset,changes,code",
    SEMANTIC_FAILURES,
    ids=[item[0] for item in SEMANTIC_FAILURES],
)
def test_semantic_rejections(tmp_path, source, name, section, offset, changes, code):
    source["rows"][section][offset].update(changes)
    root = p.write_bundle(tmp_path / name, source)
    assert_rejected(root, code)


@pytest.mark.parametrize(
    "changes",
    [{"price": 2.0}, {"metadata_json": '{"flag":1}'}],
    ids=["field", "boolean-is-not-number"],
)
def test_conflicting_repeats_are_rejected(tmp_path, source, changes):
    original = source["rows"]["trade_facts"][0]
    original["metadata_json"] = '{"flag":true}'
    repeat = dict(original, **changes)
    source["rows"]["trade_facts"].append(repeat)
    assert_rejected(p.write_bundle(tmp_path / "conflict", source), "CONFLICTING_IDENTITY")


def test_same_minute_sequence_collision_across_objects(tmp_path, source):
    source["rows"]["visual_history"][4]["known_at_utc"] = at(9, 5)
    assert_rejected(p.write_bundle(tmp_path / "collision", source), "INVALID_SEQUENCE")


def test_sequence_cannot_reverse_exact_knowledge_time(tmp_path, source):
    one, two = source["rows"]["trade_facts"][:2]
    one.update(known_at_utc=at(9, 20, 30), sequence_num=0)
    two.update(known_at_utc=at(9, 20, 10), sequence_num=1)
    assert_rejected(p.write_bundle(tmp_path / "reversed", source), "INVALID_SEQUENCE")


@pytest.mark.parametrize(
    "bad",
    [
        b'{"x":1,"x":2}',
        b"\xef\xbb\xbf{}",
        b'{"x":NaN}',
        b'{"x":Infinity}',
        b'{"x":1e999}',
        b'{"x":"\xff"}',
        b'{"x":"\\ud800"}',
        b"[]",
        b'{"x":9007199254740992}',
        (b'{"x":' * 17) + b"{}" + (b"}" * 17),
    ],
)
def test_strict_json(bad):
    with pytest.raises(c.ContractError):
        c.strict_json(bad, "fixture", 1048576)


@pytest.mark.parametrize(
    "stamp",
    [
        "09:00",
        "2026-01-05T09:00:00Z",
        "2026-01-05T09:00:00.0000000000Z",
        "2026-02-30T09:00:00.000000000Z",
        "2026-01-05T09:00:60.000000000Z",
        "1969-01-05T09:00:00.000000000Z",
    ],
)
def test_exact_time_rejections(stamp):
    with pytest.raises(c.ContractError, match="INVALID_TIME"):
        c.instant(stamp)


def test_timestamp_boundary_overflow():
    with pytest.raises(c.ContractError, match="INVALID_TIME"):
        c.minute_after("9999-12-31T23:59:00.000000000Z")
    with pytest.raises(c.ContractError, match="INVALID_TIME"):
        c.nanosecond_after("9999-12-31T23:59:59.999999999Z")


@pytest.mark.parametrize(
    "path",
    [
        "../outside.json",
        "/tmp/outside.json",
        "data/../outside.json",
        "data\\outside.json",
        "https://example.org/x",
        "data/.hidden",
        "data//file",
        "Data/file",
    ],
)
def test_path_confinement(bundle, path):
    access = c.BundleAccess(bundle)
    with pytest.raises(c.ContractError, match="PATH_CONFINEMENT"):
        access._open(path)


def test_symlink_is_never_followed(bundle, tmp_path):
    outside = tmp_path / "outside"
    outside.write_text("secret")
    (bundle / "escape").symlink_to(outside)
    with pytest.raises(c.ContractError, match="PATH_OR_FILE_UNAVAILABLE"):
        c.BundleAccess(bundle)._read("escape", 4096)


def test_consumed_shard_integrity_and_unreferenced_inertness(bundle):
    (bundle / "unreferenced.parquet").write_bytes(b"broken")
    c.validate_bundle(bundle)
    path = bundle / "data/trade_facts-0.parquet"
    raw = path.read_bytes()
    path.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
    assert_rejected(bundle, "INTEGRITY_MISMATCH")


def test_manifest_mutation_invalidates_observation(bundle):
    access = c.BundleAccess(bundle)
    rewrite_manifest(bundle, lambda m: m.update(run_id="different-run"))
    with pytest.raises(c.ContractError, match="OBSERVATION_CHANGED"):
        access.verify_stable()


def test_replaced_bundle_directory_invalidates_observation(bundle):
    access = c.BundleAccess(bundle)
    bundle.rename(bundle.parent / "old")
    bundle.mkdir()
    with pytest.raises(c.ContractError, match="OBSERVATION_CHANGED"):
        access.verify_stable()


@pytest.mark.parametrize(
    "variant",
    ["float32", "int32", "nullable", "extra", "missing", "wrong-metadata", "gzip", "two-groups"],
)
def test_physical_schema_rejections(bundle, variant):
    path = bundle / "data/trade_facts-0.parquet"
    table = pq.read_table(path)
    fields = list(table.schema)
    if variant == "float32":
        fields[fields.index(table.schema.field("price"))] = pa.field(
            "price", pa.float32(), nullable=False
        )
        table = table.cast(pa.schema(fields, metadata=table.schema.metadata))
    elif variant == "int32":
        fields[fields.index(table.schema.field("sequence_num"))] = pa.field(
            "sequence_num", pa.int32(), nullable=False
        )
        table = table.cast(pa.schema(fields, metadata=table.schema.metadata))
    elif variant == "nullable":
        fields[0] = fields[0].with_nullable(True)
        table = table.cast(pa.schema(fields, metadata=table.schema.metadata))
    elif variant == "extra":
        table = table.append_column("extra", pa.array([1] * table.num_rows))
    elif variant == "missing":
        table = table.drop(["commission"])
    elif variant == "wrong-metadata":
        table = table.replace_schema_metadata({b"bv.contract": b"wrong"})
    pq.write_table(
        table,
        path,
        version="2.6",
        compression="gzip" if variant == "gzip" else "zstd",
        row_group_size=1 if variant == "two-groups" else 4096,
    )
    resign(bundle, "data/trade_facts-0.parquet")
    assert_rejected(bundle, "INVALID_PHYSICAL_SCHEMA")


@pytest.mark.parametrize("kind", ["time", "entity", "state"])
def test_wrong_index_summary_is_rejected_after_resigning(bundle, kind):
    path = f"indexes/visual_history-{kind}-0-0.json"
    node = json.loads((bundle / path).read_text())
    node["summary"]["count"] += 1
    (bundle / path).write_bytes(p.encode(node))
    resign(bundle, path)
    assert_rejected(bundle, "INVALID_INDEX")


def test_state_index_cannot_omit_carry_in(bundle):
    path = "indexes/visual_history-state-0-0.json"
    node = json.loads((bundle / path).read_text())
    node["entries"] = [entry for entry in node["entries"] if entry["fact_id"] != "fib-update"]
    node["summary"] = p.bounds("state", node["entries"])
    (bundle / path).write_bytes(p.encode(node))
    resign(bundle, path)
    assert_rejected(bundle, "INVALID_INDEX")


def test_multilevel_pruning_avoids_whole_history(tmp_path, source):
    template = source["rows"]["indicator_points"][1]
    points = []
    for number in range(130):
        stamp = (datetime(2026, 1, 5, 9) + timedelta(seconds=number)).strftime(
            "%Y-%m-%dT%H:%M:%S.000000000Z"
        )
        points.append(
            dict(
                template,
                fact_id=f"dense-{number}",
                sample_time_utc=stamp,
                known_at_utc=stamp,
                sequence_num=number,
                value=float(number),
            )
        )
    source["rows"]["indicator_points"] = points
    root = p.write_bundle(tmp_path / "dense", source, shard_rows=2)
    c.validate_bundle(root)
    budget = c.Budget(max_nodes=4, max_rows=4)
    result = c.BundleAccess(root, budget).time_rows("indicator_points", at(9, 2), at(9, 2, 3))
    assert [row["value"] for row in result] == [120.0, 121.0, 122.0]
    assert budget.rows == 4
    assert budget.nodes == 2
    previous_budget = c.Budget(max_nodes=3, max_rows=2, max_predecessors=1)
    previous = c.BundleAccess(root, previous_budget).predecessor(
        "indicator_points", "ema", at(9, 2), at(9, 2)
    )
    assert previous["value"] == 119.0
    assert previous_budget.nodes == 2


@pytest.mark.parametrize(
    "budget",
    [c.Budget(max_nodes=0), c.Budget(max_rows=1), c.Budget(max_bytes=1), c.Budget(max_seconds=0)],
)
def test_budget_refusal_never_returns_partial_success(bundle, budget):
    # Fresh start prevents test scheduling time from consuming a normal budget.
    with pytest.raises(c.ContractError, match="REFUSED_OVER_LIMIT"):
        c.BundleAccess(bundle, deepcopy(budget)).time_rows("trade_facts", at(), at(11))


def test_publication_refuses_existing_destination(bundle, source):
    original = (bundle / "manifest.json").read_bytes()
    with pytest.raises(FileExistsError):
        p.write_bundle(bundle, source)
    assert (bundle / "manifest.json").read_bytes() == original


def test_full_history_retains_separate_effective_forms(bundle):
    rows = c.BundleAccess(bundle, c.Budget()).state_rows(
        "visual_history", at(9, 20), at(9, 30), None
    )
    assert {row["fact_id"] for row in rows if row["visual_id"] == "fib"} == {
        "fib-create",
        "fib-update",
    }


def test_empty_points_still_require_series_section(bundle):
    rewrite_manifest(bundle, lambda m: m["sections"].pop("indicator_series"))
    assert_rejected(bundle, "INVALID_REFERENCE")


@pytest.mark.parametrize(
    "change",
    [
        lambda report: report["summary"].update(profit_factor=0.0),
        lambda report: report["summary"].update(total_trades=0, expected_payoff=12.0),
        lambda report: report["trade_stats"].update(average_loss=0.0),
        lambda report: report["drawdown"].update(relative_drawdown=None),
    ],
)
def test_undefined_report_values_are_not_fabricated(bundle, change):
    rewrite_manifest(bundle, lambda m: change(m["report"]))
    assert_rejected(bundle, "INVALID_REPORT")


@pytest.mark.parametrize(
    "variant",
    [
        "reversed-price",
        "flattened-alias",
        "marker-placement",
        "unknown-unnamespaced",
        "style-range",
    ],
)
def test_geometry_payload_rejections(tmp_path, source, variant):
    row = source["rows"]["visual_history"][4 if variant == "marker-placement" else 0]
    payload = json.loads(row["payload_json"])
    code = "INVALID_GEOMETRY"
    if variant == "reversed-price":
        payload["geometry"].update(price_low=2.0, price_high=1.0)
    elif variant == "flattened-alias":
        payload["price"] = 1.1
        code = "INVALID_SCHEMA"
    elif variant == "marker-placement":
        payload["geometry"]["placement"] = "ABOVE_BAR"
    elif variant == "unknown-unnamespaced":
        row["geometry_type"] = "LINE"
        payload["geometry"] = {"kind": "LINE", "price": 1.1}
        code = "INVALID_SCHEMA"
    else:
        payload["style"] = {"opacity": 2.0}
        code = "INVALID_SCHEMA"
    row["payload_json"] = json.dumps(payload)
    assert_rejected(p.write_bundle(tmp_path / variant, source), code)


def test_opaque_section_indexes_are_validated_without_payload_reads(bundle):
    descriptor = dict(
        schema_id="runner.extra",
        optional=True,
        row_count=0,
        time_field="known_at_utc",
        entity_field="fact_id",
        state_index=None,
    )
    for kind in ("time", "entity"):
        raw = p.encode(dict(index_kind=kind, level=0, summary=p.bounds(kind, []), entries=[]))
        path = f"indexes/opaque-{kind}.json"
        (bundle / path).write_bytes(raw)
        descriptor[kind + "_index"] = dict(
            path=path, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()
        )
    rewrite_manifest(bundle, lambda m: m["sections"].update({"runner.extra": descriptor}))
    assert c.validate_bundle(bundle)["opaque_optional_evidence"] == ["runner.extra"]
    rewrite_manifest(
        bundle, lambda m: m["sections"]["runner.extra"].update(schema_id="unqualified")
    )
    assert_rejected(bundle, "INVALID_SCHEMA")


def test_json_schema_vocabulary_used_by_package():
    # Challenge structural vocabulary independently of the large example fixture.
    cases = [
        (True, {"type": "integer"}),
        (False, {"const": 0}),
        (True, {"enum": [1]}),
        ({}, {"required": ["x"]}),
        ({"x": 1}, {"additionalProperties": False}),
        ({"x": "bad"}, {"additionalProperties": {"type": "integer"}}),
        ({"x": 1, "y": 2}, {"maxProperties": 1}),
        ({"acme.x": 1}, {"patternProperties": {"^acme\\.": {"type": "string"}}}),
        ([1, 1], {"uniqueItems": True}),
        ([1], {"minItems": 2}),
        ([1, 2], {"maxItems": 1}),
        (["bad"], {"items": {"type": "integer"}}),
        (1, {"minimum": 2}),
        (2, {"maximum": 1}),
        ("x", {"minLength": 2}),
        ("xx", {"maxLength": 1}),
        ("x", {"pattern": "^y$"}),
        (1, {"anyOf": [{"type": "string"}, {"type": "null"}]}),
        (1, {"oneOf": [{"type": "integer"}, {"type": "number"}]}),
        (1, {"$defs": {"x": {"type": "string"}}, "$ref": "#/$defs/x"}),
    ]
    for value, schema in cases:
        with pytest.raises(c.ContractError):
            c.check_schema(value, schema)


def test_permutation_does_not_supply_semantic_order(tmp_path, source):
    for rows in source["rows"].values():
        rows.reverse()
    root = p.write_bundle(tmp_path / "permuted", source, shard_rows=2)
    assert c.validate_bundle(root)["base_contract_valid"]
    assert (
        c.BundleAccess(root, c.Budget()).state_rows(
            "visual_history", at(9, 50), at(9, 51), at(9, 50)
        )[0]["fact_id"]
        == "fib-update"
    )


def test_opaque_geometry_fields_never_inherit_native_meaning(tmp_path, source):
    row = source["rows"]["visual_history"][0]
    row["geometry_type"] = "runner.opaque"
    payload = json.loads(row["payload_json"])
    payload["geometry"] = {
        "kind": "runner.opaque",
        "start_time_utc": ["opaque"],
        "price_low": "custom",
    }
    row["payload_json"] = json.dumps(payload)
    assert c.validate_bundle(p.write_bundle(tmp_path / "opaque-native-names", source))[
        "opaque_optional_evidence"
    ] == ["visual_history:orb-create"]


def test_json_container_depth_exact_boundary():
    c.strict_json((b'{"x":' * 16) + b"1" + (b"}" * 16), "depth-16", 4096)
    with pytest.raises(c.ContractError, match="INVALID_JSON"):
        c.strict_json((b'{"x":' * 17) + b"1" + (b"}" * 17), "depth-17", 4096)


def test_parquet_version_is_physical_contract_rule(bundle):
    path = bundle / "data/trade_facts-0.parquet"
    table = pq.read_table(path)
    pq.write_table(table, path, version="1.0", compression="zstd")
    resign(bundle, "data/trade_facts-0.parquet")
    assert_rejected(bundle, "INVALID_PHYSICAL_SCHEMA")


def test_cli_validation_precedes_publication(tmp_path, source):
    source["manifest"]["completed"] = False
    import subprocess

    with pytest.raises(subprocess.CalledProcessError):
        p.write_bundle(tmp_path / "never-published", source, validate=True)
    assert not (tmp_path / "never-published").exists()
    assert list(tmp_path.glob(".bundle-staging-*"))
