# Development Standards (analysis/tradingview/)

- **Status:** `ACTIVE`; version 1, Gate G6 approved 22/10/2026.
- **Last Reviewed:** 22/10/2026.
- **Scope Root & Governed Paths:** analysis/tradingview/ maintained Python extractors, generators and artifact validators.
- **Separately Governed Nested Scopes:** None. Evidence, screenshots, generated HTML/SVG/JSON, packaged output and caches are not separate coding scopes.
- **Authority:** [implementation-standards.md](implementation-standards.md), revision 3, G6-DEC-009 and repository-root guidance.

## Language Standards Summary

| Language | Version | Adopted primary standard | Maintaining authority / edition | Enforcement alignment |
|---|---|---|---|---|
| Python | 3.14 validation environment; preserve existing minimum syntax compatibility unless explicitly changed | PEP 8 | CPython, living PEP accessed 21/10/2026 | py_compile, relevant deterministic generators and existing artifact checkers |

## Python Operational Rules

Primary source: [PEP 8](https://peps.python.org/pep-0008/), accessed 21/10/2026. Use four spaces, snake_case functions/modules/variables, PascalCase classes and uppercase constants. Group standard-library, third-party and local imports; avoid wildcard imports. Use pathlib for repository-relative paths and preserve deterministic offline behavior.

Extractors use the standard library; the viewer builder's markdown dependency remains an existing exception. Product FastAPI/PyArrow dependencies do not become extractor dependencies. Preserve current formats, evidence identifiers and link paths. Captured HTML/text/JSON are untrusted evidence; never execute or embed captured target HTML. Escape evidence labels/text when producing authored HTML. Keep private captured identities and credentials out of derived reports.

Comments/docstrings describe provenance and limitations. New/touched interfaces should express meaningful types where useful; there is no whole-scope strict-typing retrofit. Errors should identify the affected local artifact safely and fail validation rather than silently invent missing evidence or successful results. Tests/checks validate JSON, local paths, source/approval digests, semantics and authored HTML safety as appropriate.

## Approved Continuity and Generated Assets

Continuity impact is MEDIUM: existing generators have long lines, embedded asset strings and differing quote/import layouts. Preserve surrounding conventions in touched regions and leave unrelated formatting alone. Ruff's mandatory backend 88-column profile does not impose a formatter migration here. No unrequested mass reformatting, approved SVG-byte change or new production tooling requirement is authorized by this guide.

Generated review assets are design examples, not runtime or financial evidence. Do not edit output directories in place when maintained source/generators own the result. Preserve historical approval records and exact identities; a semantic/geometry revision needs its owning design workflow and any affected reapproval. Frozen diagram coordinates/colors in authored generators do not become a frontend styling profile.

## Verification and Distribution

Run from the repository root:

```bash
python -m py_compile analysis/tradingview/*.py
python analysis/tradingview/build_viewer.py
```

Run the relevant extractor when its inputs/logic change. For design generator/authority changes, run the applicable check_wireframes.py/check_mockups.py and inspect the affected authored result; do not regenerate approved visuals incidentally for a documentation-only edit. Distinguish structural checks from actual browser rendering, keyboard/accessibility, performance and durability evidence.

Verify changed JSON, referenced screenshot/accessibility paths and offline viewer links. Rebuild SHA256SUMS and the ZIP under [README.txt](README.txt) exclusions after changing dossier content. The dossier archive contains this subtree; backend/frontend/contract guides and repository-root routing remain checkout artifacts outside that archive. It is not a standalone application-source release.
