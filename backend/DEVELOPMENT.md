# Development Standards (backend/)

- **Status:** `ACTIVE`; version 1, approved at Gate G6 on 22/10/2026.
- **Last Reviewed:** 22/10/2026.
- **Scope Root & Governed Paths:** backend/, including future Python source, tests, configuration and SQL migrations.
- **Separately Governed Nested Scopes:** None. Generated output, caches and runtime stores are excluded from manual source editing.
- **Authority:** [implementation-standards.md](../analysis/tradingview/implementation-standards.md), revision 3, especially IS-RUN-001, IS-STORE-001, IS-NUM-001 and IS-QA-001; G6-DEC-001/002/005/007/009.
- **Readiness:** Active conventions; application source, environments and check commands are not bootstrapped yet. An implementation brief governs coding scope.

## Language Standards Summary

| Language | Version | Adopted primary profile | Maintaining authority / edition | Enforcement alignment |
|---|---|---|---|---|
| Python | CPython 3.14.x, conventional GIL build | PEP 8 | CPython, living PEP accessed 21/10/2026 | Ruff format/check, strict basedpyright, pytest |
| SQL | SQLite dialect; record actual bundled runtime at bootstrap | Project SQLite SQL profile below | Project-authored style, SQLite language reference for syntax, accessed 21/10/2026 | Migration/persistence integration tests; no separate SQL formatter selected |

## Python Operational Rules

Primary source: [PEP 8](https://peps.python.org/pep-0008/), accessed 21/10/2026. Supplementary implementation references: [Decimal](https://docs.python.org/3.14/library/decimal.html), [Ruff formatter](https://docs.astral.sh/ruff/formatter/) and [basedpyright configuration](https://docs.basedpyright.com/latest/configuration/config-files/), consulted in the approved research round.

Use four spaces, snake_case functions/modules/variables, PascalCase classes and UPPER_SNAKE_CASE constants. Group standard-library, third-party and local imports; avoid wildcard imports. Ruff owns mechanical layout and import ordering. The approved profile uses an 88-column formatting target and E4/E7/E9/F/I/B/UP lint rules without formatter-conflicting layout checks.

Type new interfaces and unknown-data boundaries; use strict basedpyright. Validate external data at adapters before creating inward-defined values. FastAPI/Pydantic transport models, sqlite3/PyArrow representations, provider SDK objects and renderer types must not define core business contracts. Comments/docstrings explain reasons, preconditions and invariants rather than narrating syntax. Narrow suppressions require a reason; broad diagnostic disabling is prohibited.

Use pathlib for controlled roots. Preserve qualified basis, original integer timestamp units/occurrence identity and decimal representations. Construct monetary Decimal values from exact inputs; BND-009 owns approved precision/rounding/quantity conventions. Do not invent those under DEFER-004. Relative presentation coordinates and browser floats do not become persisted financial values.

Expected invalid inputs, missing prerequisites, conflicts and unavailable facts return explicit outcomes. Unexpected exceptions preserve safe causal context inside the service; external errors are sanitized. A timeout is not proof of nonpublication. Retry retention rather than an already applied edit/execution; reconcile uncertain publication under its original identity. Configuration and diagnostic rules come from IS-OPS-001, including secret exclusions and bounded resources.

Tests protect named observable properties with independent expected results. Use temporary owned paths, controlled fixtures and deterministic barriers rather than arbitrary sleeps. Separate domain/workflow checks from actual storage, process exclusion, crash/reopen, provider, browser and performance evidence. Include ARCHV-001–007/AUDV obligations and ADV-VER-001 when their capabilities are implemented. Fixtures do not certify actual provider access/session/finality.

## SQLite Operational Rules

Primary profile: this project's SQLite SQL profile. Syntax authority: [SQLite SQL language reference](https://www.sqlite.org/lang.html), accessed 21/10/2026. Supplement: [atomic commit](https://www.sqlite.org/atomiccommit.html). There is no claimed official SQLite formatting standard.

Use uppercase keywords, snake_case identifiers, four-space indentation, explicit columns and bound data parameters. Keep physical SQL behind the retention adapter. Number, order and track migrations; once used in an accepted implementation, evolve them through subsequent migrations rather than rewriting history. Verify empty initialization, supported-version upgrades and failure preservation with the actual SQLite runtime.

SQLite metadata and immutable evidence files do not share a transaction. Retain verified complete content before committing its active reference; preserve pinned inputs and unrelated acknowledged state. Use a tested local active store outside the synced checkout. Settings/flush/locking procedures require foundation evidence; a successful migration or mocked test does not prove durability or sole-writer exclusion.

## Approved Scope Adaptations and Tooling

This scope's approved Python application framework/adapter dependencies supplement the root's dossier-oriented standard-library guidance; extractors retain their own restrictions. Ruff's 88-column target is the approved PEP 8 line-length adaptation. No ORM, extra query engine or provider SDK is selected by these conventions.

Required commands after foundation configuration, run within backend/:

```bash
uv sync --frozen
uv run ruff check .
uv run ruff format --check .
uv run basedpyright
uv run pytest
```

Pin exact interpreter/tool/dependency versions and uv.lock at bootstrap; do not assert these commands exist or pass before configuration. Apply conventions to touched code within the active brief. No unrequested mass reformatting, speculative package installation or coding outside that blast radius.
