# Using the Run Bundle v1.0 contract

Use the Markdown specification and JSON schemas as the contract. The Python scripts are optional reference and verification tools. Your backtester can implement the format using any language or compatible libraries.

| Files | Purpose |
|---|---|
| [backtest-data-format.md](../../../backtest-data-format.md) | Defines the format and its semantics. |
| Four JSON schemas under `contracts/editable/` | Define exact manifest, Parquet, geometry and index structures. |
| [reference_producer.py](reference_producer.py) | Generates example bundles or packages supplied data; optional. |
| [contract_tools.py](contract_tools.py) | Checks a bundle against the contract; optional. |
| Tests, evidence builder and installer | Repository authoring and maintenance tools. |

Give the backtester and viewer implementers the specification and these four canonical schema files:

- [run_bundle_contract.json](../../../contracts/editable/run_bundle_contract.json)
- [run_bundle_physical_schemas.json](../../../contracts/editable/run_bundle_physical_schemas.json)
- [run_bundle_visual_payload.schema.json](../../../contracts/editable/run_bundle_visual_payload.schema.json)
- [run_bundle_index.schema.json](../../../contracts/editable/run_bundle_index.schema.json)

The backtester implementer writes an exporter that produces the prescribed bundle: `manifest.json`, Parquet evidence files and their indexes. The recorded format version is `1.0.0`. Adopting the reference Python producer is optional.

To check an exported bundle, run this from the repository root using its existing Python environment. Replace `/path/to/run-bundle` with the bundle directory:

```bash
.venv/bin/python \
  maintenance-cases/MC-2026-10-10-RUN-BUNDLE-CONTRACT-RECOVERY/contract-v1.0.0/contract_tools.py \
  /path/to/run-bundle
```

The validator reports structural, semantic and index consistency errors. It cannot prove the producer's historical knowledge or financial-result accuracy.

**The current viewer still needs changes to consume this format.** The delivered package specifies and validates the exchange format; it does not complete the backtester-to-viewer integration. A conforming export requires a viewer implementation that supports this contract before end-to-end use.

See [README.md](README.md) for optional example generation and additional tooling details.

## Suggested prompt for the strategy-building system

Copy the prompt below into the system that builds and backtests the strategy. Provide it with `backtest-data-format.md` and the four canonical schemas listed above. Include the reference validator and examples if you want it to use those optional tools. The prompt requests an implemented exporter and actual saved backtest evidence.

```text
When building and backtesting this trading strategy, implement and integrate an
exporter that stores its trading evidence as a Backtest Viewer Run Bundle.
Deliver the exporter and a bundle from an actual backtest, with validation
evidence. Use the configured output root for completed bundles.

Read these supplied contract files before implementing the exporter:
- backtest-data-format.md
- run_bundle_contract.json
- run_bundle_physical_schemas.json
- run_bundle_visual_payload.schema.json
- run_bundle_index.schema.json

Follow their complete requirements. The format_version is exactly "1.0.0" and
contract_id is "backtest-viewer.run-bundle". Treat the earlier draft and any
permissive existing viewer behavior as historical evidence, not format authority.
If required contract files are missing or contradict each other, identify the
specific gap before claiming conformance. This prompt does not replace or amend
the supplied contract.

1. Capture evidence during the backtest as it becomes known to the strategy.
   Preserve occurrence/sample/geometry coordinates separately from simulated
   historical knowledge time. Do not substitute export wall-clock time for
   known_at_utc or retrospectively assign an earlier knowledge time to a result
   learned later. Record entry, scaling, partial-exit and final-exit fills with
   their actual identity, quantity, price, charges and attribution. Preserve the
   strategy's calculations and behavior while adding evidence capture/export.

2. Always emit trade_facts, including a valid empty core for a zero-trade run.
   Store individual executed fills with explicit fact_id/execution_id and
   position_id, using the prescribed ENTRY/SCALE_IN/SCALE_OUT/EXIT actions and
   BUY/SELL sides. A completed backtest may still contain open positions.
   Keep final position outcomes out of earlier facts and metadata.

3. Persist the additional evidence the strategy actually produces in the
   corresponding sections:
   - position_history: authoritative full OPEN/UPDATE/CLOSE position states,
     including producer-maintained quantities and completion facts;
   - strategy_events: decisions/events and their explicit associations;
   - visual_history: emitted levels, zones, trend lines, boxes, markers or
     arrows, including their CREATE/UPDATE/REMOVE history;
   - indicator_series and indicator_points: emitted scalar indicator samples,
     their catalogue/provenance, and VALUE/WARMUP/GAP states;
   - sessions: independently emitted START/END facts and session associations;
   - equity_curve and monthly_returns: producer-calculated report evidence.
   Respect contract optionality: omit sections when that evidence is genuinely
   not produced, and explain the omission. Declare indicator_series whenever
   indicator_points is declared, and sessions whenever session references are
   non-null. Do not fabricate missing evidence to populate a section.

4. Use the exact declared physical fields, order, types, nullability and file
   metadata for every Parquet shard. Nullable columns must exist even when all
   their values are null; use complete typed schemas for zero-row files.
   Store JSON payloads in the prescribed bounded UTF-8 JSON string columns.
   Use canonical nine-fractional-digit UTC strings, finite binary64 values and
   signed INT64 sequences within the contract's limits. Distinguish explicit
   zero from unknown/null; never coerce invalid data into invented defaults.

5. Assign stable fact and logical-object IDs. Preserve original facts and
   deterministic section/minute sequences; resolve references and lifecycle
   transitions according to the contract. Visual UPDATE is a complete state
   replacement and REMOVE is terminal. Use explicit geometry discriminators
   and payload fields; method names do not choose geometry. Indicator sample
   corrections/deletion are excluded in v1.0.0. Use a new series identity for
   a revised series instead of rewriting its earlier points.

6. Supply explicit run bounds, instrument/price/quantity units, account and
   quote currencies, precision, price basis, strategy catalogue and attribution.
   Declare dataset correspondence only when an actual dataset identity is known.
   Preserve nullable/unassigned attribution. Do not infer session starts from
   trades or visual relevance from a strategy filter. All metadata and payloads
   must contain only information known at the associated fact's knowledge time.

7. Populate the authoritative report from the producer's actual calculations.
   Follow each metric's defined population, costs, sign, denominator and units;
   distinguish fractions from percentage points. Explicitly null unavailable
   categories with the exact unavailable_reasons entries, and use null for
   undefined/unknown nullable metrics. Store curve/monthly evidence in their
   indexed sections, not inline manifest arrays. Do not invent zero metrics,
   final outcomes or YTD evidence to make an export look complete.

8. Build the required complete time/entity index trees and the state index
   wherever prescribed, including carry-in states and same-minute effective
   forms. Follow exact sort keys, coverage, summaries, row pointers, file size,
   row-group, fanout and depth limits. Preserve all historical facts even when
   only the last same-minute form is effective. Every file reference must have
   its confined relative path, final byte length and SHA-256 digest.

9. Publish one immutable bundle directory per completed run using the contract's
   hidden staging, manifest-last, validation, fsync and atomic directory-rename
   procedure. The only manifest filename is manifest.json. Mark completed true
   only for completed, validated evidence. Never overwrite a published run;
   changed evidence requires a new run_id and directory. Failed/interrupted
   exports must remain distinguishable from completed bundles.

10. Validate actual exported files against manifest structure, physical schemas,
    scalar/time rules, references, lifecycles, duplicates, sequences, digests
    and complete index coverage. Use contract_tools.py when supplied and runnable,
    or equivalent checks covering the same contract requirements. Exercise a
    normal completed-position run and a zero-trade run, plus scaling, still-open
    positions and optional evidence relevant to this strategy. Test that earlier
    knowledge states contain no later outcomes. Fix export defects before
    claiming conformance; report checks you could not run explicitly.

Deliver the exporter integrated with the backtest workflow, instructions for
configuring its output root, the actual bundle location(s), emitted/omitted
sections, and validation commands/results. Explain how contemporaneous knowledge,
producer calculations and immutable publication are ensured; file validation
alone cannot prove their historical truth or financial accuracy.

Use any compatible implementation language and libraries. The reference producer
is optional tooling and example-input.json is its helper input, not the Run Bundle
wire format. Scope this work to strategy evidence capture and compliant export.
The current viewer still needs separate support for this contract; successful
export validation is not evidence of completed viewer integration.
```
