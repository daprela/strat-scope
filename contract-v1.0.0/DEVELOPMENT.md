# Development Standards (contract-v1.0.0/)

- **Status:** `ACTIVE`; version 1, Gate G6 approved 22/10/2026.
- **Last Reviewed:** 22/10/2026.
- **Scope Root & Governed Paths:** contract-v1.0.0/ maintained reference Python producer, validator, evidence builder and conformance tests.
- **Separately Governed Nested Scopes:** None. Example bundles, generated conformance output and caches are not coding scopes.
- **Authority:** [implementation-standards.md](../analysis/tradingview/implementation-standards.md), revision 3, G6-DEC-009. These reference tools remain separate from the chart application; external completed-run import is excluded from v1.

## Language Standards Summary

| Language | Version | Adopted primary standard | Maintaining authority / edition | Enforcement alignment |
|---|---|---|---|---|
| Python | 3.14 validation environment; existing PyArrow adapter | PEP 8 | CPython, living PEP accessed 21/10/2026 | Python compilation and existing pytest conformance checks |

## Python Operational Rules

Primary source: [PEP 8](https://peps.python.org/pep-0008/), accessed 21/10/2026. Use four spaces, snake_case values/functions/modules, PascalCase classes and uppercase constants. Group imports by standard library, third party and local dependencies. Use pathlib and explicit dataclass/type semantics consistent with the maintained code.

Preserve schema/dialect boundaries, stable error codes, original precision, occurrence identity, bounded reference-query semantics and immutable published examples. Validate unknown inputs before using them; confined paths and safe errors must not disclose credentials or unrelated paths. Do not infer whole-bundle validity, historical truth or production readiness from partial queries or digest checks alone.

Comments/docstrings explain validation boundaries and evidence limits. Expected invalid-contract results retain attributable codes/locations. Tests use independent positive/negative fixtures and observable outcomes; preserve the distinction between producer and validator algorithms, conformance and reference access demonstrations. Changes to normative contract meaning require their owning authority, not a style-only edit.

## Continuity, Tool Alignment and Scope Adaptations

Continuity impact is LOW. Apply the profile to touched/new code; preserve unrelated formatting. No whole-scope strict-typing retrofit, mass Ruff reformatting, extra schema/query library or product integration is approved. The backend's framework and formatter requirements do not silently apply here.

When maintaining these tools, use a separate locked Python environment with their actual PyArrow/pytest requirements. The README contains predecessor repository paths and environment references that are absent from this checkout; do not claim those commands work or repair that independent history in a standards task.

Compile maintained scripts and, when behavior changes, run the existing local conformance tests with the required environment and temporary outputs. Record actual commands and dependency availability; do not claim execution when the environment is absent. Never overwrite frozen examples or conformance evidence merely to check formatting. Production viewer behavior and provider integration require separate evidence.
