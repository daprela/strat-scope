# Run Bundle v1.0 contract package

The wire version is **1.0.0**. This is the first authored normative contract; the preceding same-labelled Markdown was a draft. The repository viewer is **NOT_CONFORMANT** to this contract. No application behavior or external runner integration was changed or certified here.

The canonical document is repository-root `backtest-data-format.md`; this directory retains its identical authoring copy. Canonical schemas live under `contracts/editable/`; package copies are byte-identical:

| Canonical file | Package file |
|---|---|
| `run_bundle_contract.json` | [manifest.schema.json](manifest.schema.json) |
| `run_bundle_physical_schemas.json` | [physical-schemas.json](physical-schemas.json) |
| `run_bundle_visual_payload.schema.json` | [visual-payload.schema.json](visual-payload.schema.json) |
| `run_bundle_index.schema.json` | [index.schema.json](index.schema.json) |

[Decision ledger](decision-ledger.md) explains new choices and exclusions. [Rule disposition](rule-disposition.md) covers all 105 audit obligations. [Conformance evidence](conformance-evidence.md) records checks, scope and limitations. [Governance reconciliation](../governance-reconciliation.md) withdraws invalid predecessor premises and defines the implementation follow-up.

From the repository root, using its pinned environment:

```bash
.venv/bin/python maintenance-cases/MC-2026-10-10-RUN-BUNDLE-CONTRACT-RECOVERY/contract-v1.0.0/reference_producer.py /tmp/my-new-run-bundle --shard-rows 2
.venv/bin/python maintenance-cases/MC-2026-10-10-RUN-BUNDLE-CONTRACT-RECOVERY/contract-v1.0.0/contract_tools.py /tmp/my-new-run-bundle
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -p no:cacheprovider maintenance-cases/MC-2026-10-10-RUN-BUNDLE-CONTRACT-RECOVERY/contract-v1.0.0/test_conformance.py
```

The output directory must not exist. For runner-supplied input, add `--input <input.json>` to the producer command. [example-input.json](example-input.json) demonstrates the input shape: explicit manifest metadata and full rows for each section. JSON-valued Parquet cells are JSON **strings** in that input. All columns are typed from the physical registry; nullable fields remain columns. The producer generates shards, complete indexes and digests independently of validator algorithms. The CLI runs the separate validator on staging bytes before atomic directory publication. Serialize publishers for a shared parent; the reference utility is a single-publisher authoring example, not a concurrent runner service. Failed staging remains hidden for diagnosis and explicit owner cleanup; it never becomes an eligible published bundle.

The low-level `write_bundle(..., validate=False)` function exists to build deliberately malformed test fixtures. It must not be used to claim conformant publication. The valid checked-in examples are [full/manifest.json](examples/full/manifest.json) and [empty/manifest.json](examples/empty/manifest.json). The first includes all nine sections and multiple shards; the second proves typed zero-row core evidence and explicit unavailable reports. Negative fixtures are reproducible named cases in `test_conformance.py`, including mutations re-signed to exercise semantic checks beyond digest rejection.

`contract_tools.py` has strict JSON/schema checks, exact physical checks, relationship/lifecycle checks, complete index verification, consumed-byte digest checks and confined source observation. It evaluates only the JSON Schema vocabulary used by these supplied schemas; it is not a general JSON Schema library. Standard schemas can also be consumed by independent Draft 2020-12 validators. No new runtime dependency was added.

`BundleAccess` supplies bounded **reference access demonstrations**, not the viewer's complete qualification/transport/rendering implementation. `time_rows` reads coordinate candidates; `replay_time_rows` applies knowledge/report gating; `state_rows` selects indexed replay or historical full states; `predecessor` seeks qualified earlier samples. A rendering consumer must still clip forms, qualify referenced catalogue/market/context evidence and deliver the scoped availability results required by the contract. Use full-validation evidence tied to the immutable manifest digest when asserting complete producer index coverage. A partial query does not prove whole-bundle validity. An unsupported geometry makes this simple section query raise; a production reader must preserve independently qualified objects through its scoped fault model.

The demonstrator budget counts bytes (including rereads), nodes, decoded rows and predecessor candidates, and checks elapsed time between operations. It does not establish a hard preemptive decoding deadline, hostile-file memory isolation, a supported viewer ceiling, or production performance. Full validation intentionally visits all known evidence and is a separate explicit operation. No hidden whole-history fallback is used by bounded query methods.

The Python helpers accept an exact instant for their cursor parameter and derive the contract's containing-minute reveal cursor. This convenience is not a new on-disk cursor field or finer replay granularity.

```python
from pathlib import Path
from contract_tools import Budget, BundleAccess

budget = Budget(max_nodes=2, max_rows=2)
reader = BundleAccess(Path("examples/full"), budget)
forms = reader.state_rows(
    "visual_history",
    "2026-01-05T09:50:00.000000000Z",
    "2026-01-05T09:51:00.000000000Z",
    "2026-01-05T09:50:00.000000000Z",
)
assert [form["fact_id"] for form in forms] == ["fib-update"]
```

Producer attestations remain necessary for historical knowledge truth, reported result accuracy, strategy connectedness, the actual publication sequence and ownership of the run-ID namespace. The validator does not pretend to prove them from files. Reader implementation, supported-configuration benchmarks, rendered verification and any real producer interoperability remain separate work.
