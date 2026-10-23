# Contract-authoring decisions

Date: 2026-10-10. Scope: first normative local Run Bundle **v1.0**, wire identifier `1.0.0`.

The user directly authorized complete authoring and retaining version 1.0 because the preceding document was a draft. The concrete technical choices below are authoring decisions made under that delegation. Historical implementation and accepted records are evidence of behavior, not a reason to preserve unsupported format rules. These decisions define producer/reader obligations; they do not approve implementation or target-product scope.

| ID | Decision and rationale | Contract |
|---|---|---|
| CA-001 | Retain `1.0.0`; withdraw released-draft, v1.1-only and fictitious legacy obligations. No real retained producer profile was supplied. | §§1,13 |
| CA-002 | One `manifest.json`; no default section probes; explicit descriptors, typed empty sections, confined relative references. Matches a discoverable publication unit while removing permissive aliases. | §§2,4 |
| CA-003 | Publish a new hidden staging directory by atomic rename, with fsync and immutable files. SHA-256 binds exact consumed bytes; identity checks cover actual reads and publication of their results. These are coherence guarantees, not authenticity or universal locking. | §§2,12 |
| CA-004 | Nine-digit UTC strings, signed INT64 sequences within JSON-safe range, finite binary64 amounts. Explicit nulls represent unknown values. Preserve negative prices/rebates and distinguish units. Exact Arrow and physical Parquet schemas remove coercion ambiguity. | §3; physical registry |
| CA-005 | Knowledge is separate from coordinate/occurrence time. Replay reveals the containing M1 minute; section/minute sequence is authoritative and must not reverse exact knowledge order. No cross-section order is asserted. | §§3,6,8,9 |
| CA-006 | Required executions are immutable per-fill facts with explicit position/action identity. Optional producer full-state position history owns grouping/current totals/final outcomes. No viewer aggregation becomes an authoritative position or report. | §6 |
| CA-007 | Define six native geometry kinds with complete typed payloads. UPDATE replaces the full state; REMOVE is terminal. Preserve raw facts and last same-minute effective form. Methods explain emitted evidence without calculating it. | §8 |
| CA-008 | Immutable series catalogue plus scalar points, with VALUE/WARMUP/GAP. Corrections/deletion are excluded in v1; a revised series gets a new identity. Late-known earlier samples cannot leak through coordinate filtering. | §9 |
| CA-009 | Independent START/END session facts and connected strategy catalogue. Sessions may overlap or have no trades. Nullable attribution filters trades only; visual/indicator/session evidence stays run-level. Connectedness is runner-owned, reference structure is checkable. | §5 |
| CA-010 | Report categories are complete or explicitly unavailable. Define every metric's population, units, signs, fractions/percent points and undefined ratios. Equity/monthly evidence becomes indexed Parquet; no inferred YTD or zero defaults. Run-end embargo covers transport and metadata. | §10 |
| CA-011 | Time/entity trees and state interval trees, with exact coverage, 64-entry fanout, bounded shards and digest references. State indexes supply carry-in and same-minute resolution without scans. Reader budgets are separate from producer validity. | §11 |
| CA-012 | Precise absence/empty/unsupported/withheld/insufficient/refused/change outcomes. Optional faults preserve independently established evidence. No stale forms, hidden thinning or substitute success. | §§11,12 |
| CA-013 | Namespaced optional extension envelopes; unknown required features block acceptance. Unknown major versions grant no semantic subset by familiar field names. Real empirical adapters require actual artifacts and separate authority. | §§4,13 |
| CA-014 | Normative prose and machine schemas agree; examples/tools do not amend them. Explicit full validation and separate bounded demonstrations provide authoring evidence. External runner interoperability and viewer conformance remain unproved. | §§1,14 |

Explicit v1 exclusions: setup catalogue/lifecycle; indicator sample correction/deletion; scheduled visual expiry without an explicit lifecycle fact; generated indicator/calculated strategy results; inferred position summaries; authoritative derived YTD/peak/trough analytics; implicit market matching; cross-major semantic compatibility; fictional draft legacy profiles. These exclusions close the corresponding authoring questions rather than silently leaving them unspecified.

New field/layout/index requirements are intentional. They may be incompatible with earlier draft-labelled bytes or permissive fixtures. Such bytes do not establish a released compatibility baseline. Never rewrite their version string to fabricate conformance; inspect them only through a separately evidenced empirical adapter if one is later authorized.
