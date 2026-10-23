# v1.0 contract authoring evidence

Date: 2026-10-10. Wire version: **1.0.0**. Environment: repository-pinned Python **3.14.8**, PyArrow **25.0.1**, pytest and Ruff. No dependency/lock changes.

The independent byte producer and full base-contract validator agree on both checked-in examples. The [machine results](reference-evidence.json) retain manifest digests and physical/semantic counts. The full example has all nine sections: four fills, four position states, one event, five visual lifecycle facts, one series catalogue, four samples, four independent session facts, three curve points and one monthly row. Its explicit two-row sharding challenges multi-file coverage. The empty example has a complete typed zero-row core and unavailable report categories.

The authoring suite passed **134 tests** in **4.15 seconds**. [JUnit results](conformance-junit.xml) record every case and outcome. Coverage includes strict JSON, canonical nanosecond/calendar boundaries, exact physical fields and types, nullability, Parquet version/compression/row groups, manifest/default/version rejection, reference/lifecycle/sequence failures, numeric domains, duplicates and input permutation, geometry discriminators/full replacements, opaque extension independence, sessions, point corrections, report denominators/embargo, path/symlink/integrity/mutation checks, index coverage and bounded refusal.

Commands from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q -p no:cacheprovider --basetemp=/tmp/bv-contract-conformance-pytest --junitxml=maintenance-cases/MC-2026-10-10-RUN-BUNDLE-CONTRACT-RECOVERY/contract-v1.0.0/conformance-junit.xml maintenance-cases/MC-2026-10-10-RUN-BUNDLE-CONTRACT-RECOVERY/contract-v1.0.0/test_conformance.py
.venv/bin/ruff check --no-cache maintenance-cases/MC-2026-10-10-RUN-BUNDLE-CONTRACT-RECOVERY/contract-v1.0.0
.venv/bin/ruff format --no-cache --check maintenance-cases/MC-2026-10-10-RUN-BUNDLE-CONTRACT-RECOVERY/contract-v1.0.0
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python maintenance-cases/MC-2026-10-10-RUN-BUNDLE-CONTRACT-RECOVERY/contract-v1.0.0/build_evidence.py
```

Bounded demonstrations:

| Operation | Established result | Accounted work |
|---|---|---|
| Carry-in visual at 09:50, outside its update minute | `fib-update`, no viewport-local emission required | One state node and two decoded rows; 18,459 bytes including manifest reread |
| Predecessor for sample coordinate before 09:04 at cursor 09:04 | `point-2`; nearer `point-3` is not yet known | Two candidate steps; one selected shard |
| Multi-level 130-point fixture, two-row shards, narrow 3-second range | Exact values 120, 121, 122 | Two nodes and four decoded rows, rather than 130 rows |
| Same fixture, backward seek before 09:02 | Exact value 119 | Two nodes, two decoded rows, one candidate |
| Byte/node/row/predecessor/elapsed budget exhaustion | `REFUSED_OVER_LIMIT`, no partial success | Explicit accounted refusal; no substitute resolution or fallback scan |

Ruff lint and format checks pass. Publication tests establish that validation failure leaves only hidden staging and that an existing final destination is not overwritten. This exercises the reference protocol; historical crash durability and storage-hardware behavior still require deployment/producer evidence.

The [105-rule disposition](rule-disposition.md) maps every audit authoring obligation to an explicit norm, exclusion, executable evidence or stated producer/reader obligation. It does **not** claim production execution of every policy. The schema evaluator is intentionally limited to employed Draft 2020-12 vocabulary, with dedicated challenges for those keywords. No independent general-purpose schema library or second-language producer was installed.

Limits: no actual external runner was supplied; no current-viewer v1.0 conformance or rendered UI proof; no supported-configuration benchmark; no proof of historical knowledge truth, report/strategy correctness, connectedness, run-ID namespace uniqueness across external producers, or fsync execution from bundle bytes alone. The source audit's 70 old tests and 23 probes remain historical behavior evidence, not the contract oracle. Full `make check` was not run because production implementation, browser files, configuration and dependencies were not changed by this authoring task.

Post-install verification: all **seven** canonical files match their prepared sources and [installation receipt](../canonical-install-receipt.json). All **105** inventory IDs are present once in the disposition matrix. The existing focused run-evidence/replay suite passed **70 tests in 4.71 seconds** after schema/specification installation. Scoped `git diff --check` passed. The standards and repository-guide edits preserve the pre-existing working-tree content, with only the prepared contract erratum added; no source/browser changes, commits, pushes or deployments were performed.

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q -p no:cacheprovider --basetemp=/tmp/bv-run-contract-postinstall-pytest tests/unit/bnd002 tests/unit/bnd003/test_temporal_policy.py tests/unit/test_contracts.py tests/integration/test_run_evidence_reading_integration.py tests/integration/test_run_inspection_integration.py tests/integration/test_replay_navigation_integration.py
```
