"""Generate immutable reference examples and attributable operation evidence."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import contract_tools as c
import reference_producer as p


def main() -> None:
    directory = Path(__file__).resolve().parent
    source = p.example_input()
    (directory / "example-input.json").write_text(json.dumps(source, indent=2) + "\n")
    examples = directory / "examples"
    full = examples / "full"
    if not full.exists():
        p.write_bundle(full, source, shard_rows=2, validate=True)
    empty_source = copy.deepcopy(source)
    empty_source["manifest"]["run_id"] = "reference-zero"
    empty_source["manifest"]["report"] = {
        "summary": None,
        "trade_stats": None,
        "drawdown": None,
        "unavailable_reasons": {
            name: "Not supplied" for name in ("summary", "trade_stats", "drawdown")
        },
    }
    empty_source["rows"] = {"trade_facts": []}
    empty = examples / "empty"
    if not empty.exists():
        p.write_bundle(empty, empty_source, typed_empty=True, validate=True)
    reports = {"full": c.validate_bundle(full), "empty": c.validate_bundle(empty)}
    budget = c.Budget(max_nodes=2, max_rows=2)
    states = c.BundleAccess(full, budget).state_rows(
        "visual_history",
        "2026-01-05T09:50:00.000000000Z",
        "2026-01-05T09:51:00.000000000Z",
        "2026-01-05T09:50:00.000000000Z",
    )
    reports["carry_in"] = {
        "selected_fact_ids": [row["fact_id"] for row in states],
        "consumed_nodes": budget.nodes,
        "decoded_rows": budget.rows,
        "consumed_bytes_including_manifest_recheck": budget.bytes,
    }
    predecessor_budget = c.Budget(max_predecessors=2)
    prior = c.BundleAccess(full, predecessor_budget).predecessor(
        "indicator_points",
        "ema",
        "2026-01-05T09:04:00.000000000Z",
        "2026-01-05T09:04:00.000000000Z",
    )
    reports["predecessor"] = {
        "selected_fact_id": prior["fact_id"],
        "candidate_steps": predecessor_budget.predecessors,
        "reason": "The nearer sample is known later than the cursor; seek continues within budget.",
    }
    (directory / "reference-evidence.json").write_text(json.dumps(reports, indent=2) + "\n")
    print(
        json.dumps(
            {
                "examples": list(reports),
                "base_valid": reports["full"]["base_contract_valid"]
                and reports["empty"]["base_contract_valid"],
            }
        )
    )


if __name__ == "__main__":
    main()
