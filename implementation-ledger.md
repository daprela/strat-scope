# Implementation Ledger

- **Project:** Dukascopy Chart Workspace and Historical Trading
- **Architecture Authority:** [architecture-dossier.md](analysis/tradingview/architecture-dossier.md), revision 2
- **Standards Authority:** [implementation-standards.md](analysis/tradingview/implementation-standards.md), revision 3

## Completed Slices & Records Index

| Record ID | Date | Scope | Capability | Review Verdict | Standards Follow-Up Needed? |
|---|---|---|---|---|---|
| REC-FOUNDATION | 23/10/2026 | FOUNDATION | Local TLS platform, tooling and capability bootstrap | ACCEPTED | NO |

---

## REC-FOUNDATION — Local TLS foundation

- **Date:** 23/10/2026
- **Governing Brief:** [implementation-brief.md](implementation-brief.md), FOUNDATION revision 2
- **Maintenance Case:** N/A
- **Review Verdict & Signal:** `ACCEPTED` → `SLICE_ACCEPTED_AND_RECORDED`
- **Foundation readiness:** `READY_FOR_BEHAVIORAL_IMPLEMENTATION`, subject to each selected slice's prerequisites
- **Review scope:** Same-agent implementation review; independent architecture/UI audits remain their existing authorities

### 1. Blast-radius and conformance audit

The 58 new source/configuration/license files are individually enumerated and
hashed in [source-inventory.json](foundation-evidence/source-inventory.json).
Backend/frontend code, migrations, test probes, tools, root Makefile/.gitignore,
scripts, FOUNDATION.md and sanitized foundation evidence are within the approved
blast radius. The brief revision, this ledger and project-state coordination use
their explicit governance exceptions. Readonly authority identities are in
[authorities.json](foundation-evidence/authorities.json).

**Blast-radius compliance: PASS.** No unrelated refactor or source authority,
reference-tool, captured evidence, approved visual or dossier output edit occurred.
No business feature or product UI realization is accepted in this record.

**Accepted deviations:** None. Installation/evidence limits are recorded below.
Detailed conformance assessment: [review.md](foundation-evidence/review.md).

### 2. Durable implementation facts

| Fact ID | Class | Description and reusable context | Source | Standards Owner |
|---|---|---|---|---|
| FND-001 | ARCHITECTURE_REALIZATION | One direct Uvicorn TLS worker serves local Vite assets and infrastructure endpoints at 127.0.0.1:4111. No product domain services or provider edge is fabricated. | IB-C-001/008; IS-FND/RUN/BUILD | NONE |
| FND-002 | ARCHITECTURE_REALIZATION | Authority is framework-independent. Exact Host/Origin checks and a 300-second purpose-bound in-memory status capability protect HTTP/WS. Expiry/disconnect never transfers ownership; revocation/restart fences old epochs. | IB-C-002/003; IB-D-003; TF-005 | NONE |
| FND-003 | ARCHITECTURE_REALIZATION | fcntl flock excludes independent store owners. SQLite FULL synchronization, DELETE journaling and ordered identity-checked migrations publish only after complete hashed content is flushed, directory-flushed and verified. Scoped revisions preserve unrelated state; operation outcomes reconcile lost acknowledgements. | IB-C-004–006; IB-D-002; TF-006; ADV-VER-001 | NONE |
| FND-004 | ESTABLISHED_IMPLEMENTATION_FACT | Strict edge models preserve integer/unit/occurrence and decimal strings, including actual immutable Parquet retention/reopen. Canonical OpenAPI and generated TS transport types include status/update/exact-value models; runtime decoders reject unsafe or obsolete values. These are infrastructure contracts, not monetary policy. | IB-C-007; IB-V-006/011 | NONE |
| FND-005 | LOCAL_IMPLEMENTATION_CHOICE | CPython 3.14.8 conventional GIL, Node 24.18.0, uv 0.12.24; exact Python/npm dependency identities and licenses are retained in installation.json and both locks. App uses TS 6; an isolated generator workspace uses its released TS-5 peer internally with one npm root installation/lock and no peer bypass. | IB-D-001; IS-PKG/UI/QA | NONE |
| FND-006 | ESTABLISHED_IMPLEMENTATION_FACT | Test-only native Lightweight Charts 5.2.1 adapter demonstrates paired candle/volume geometry, exact source retention, side-aware hover, panes, primitives, native export and lifecycle cleanup. It keeps 100k resident buckets per chart and pages render buffers; this is no archive cap or product UI acceptance. | IB-P-004/010; IB-V-008/009 | NONE |
| FND-007 | LOCAL_IMPLEMENTATION_CHOICE | Fresh local EC CA and IP-SAN leaf are outside source under ~/.local/share/strat-scope/tls. User NSS trust is installed; graphical Chromium's persistent app profile passed normal TLS 1.3 navigation. Leaf expires 23 October 2027; public fingerprint/SAN/dates are in tls.txt. Renew/retest when changing identity/profile. | IB-D-004; IB-V-010 | NONE |
| FND-008 | ESTABLISHED_IMPLEMENTATION_FACT | make bootstrap/run/ready/browser/stop/check/test-db/test-e2e/contracts-check provide reproducible installation, bounded configuration, actual-profile access, identity-checked shutdown and scoped evidence. Allowlisted rotating JSONL diagnostics expose safe bounded counts and timings. | IB-P-006–009; IB-V-001/007/010 | NONE |

No STANDARDIZATION_CANDIDATE or SUPERSESSION is introduced. No prior records exist.

### 3. Executed verification

| Obligations | Command / evidence | Observed result |
|---|---|---|
| IB-V-001/011 | make bootstrap; fresh uv frozen environment; make contracts-check; checks.log | PASS: frozen installation, local build, generated byte comparison and strict checks |
| IB-V-002 | backend transport/authority tests; Chromium foreign-origin/two-tab/WS test | PASS: valid owner works; invalid/foreign/stale/purpose/second owner denied |
| IB-V-003–005 | make test-db; physical-store.log/json | PASS: physical process exclusion, five crash frontiers, migration rollback, injected I/O failures, version/epoch fencing, concurrent candidate preservation |
| IB-V-006/007 | backend boundary tests on installed store filesystem | PASS: retained Parquet exactness, confinement, secret-sentinel rejection and production-budget log rotation |
| IB-V-008 | browser-checks.log, renderer light/dark PNG/JSON, native export PNGs; visual inspection | PASS: actual native hover, independent side/volume geometry, absence, panes, 100 visible drawings, export, resize and disposal |
| IB-V-009 | renderer-light.json / renderer-dark.json | PASS: initial 438.9/465.5 ms; interaction p95 19.1/19.9 ms; receipt-to-draw 38.9/37.5 ms |
| IB-V-010 | desktop-https.json/PNG; tls.txt; lifecycle.json | PASS: exact origin, trusted graphical Chromium, secure WS/assets, checked stop/listener closure/relaunch |

Totals: **25 backend tests, 3 frontend tests, 3 browser tests**, plus **22 physical
storage/boundary tests on the installed store filesystem**. Ruff, basedpyright,
TypeScript, ESLint, Prettier, build and root Python compilation pass. Actual
filesystem/SQLite settings and hardware/browser are retained in their evidence.

Evidence limits: the system CA bundle was not changed because sudo required a
password; validated host probes use the explicit public CA and actual graphical
Chromium independently uses installed NSS trust. Other browser profiles and failed
Vivaldi attempts are not certified. No certificate bypass was used. Physical
tests cover process crashes/injected faults, not power cuts. Renderer/data fixtures
are synthetic and do not certify providers, numerical policy, finished product
exports or product UIV. Earlier failed measurements are preserved.

### 4. Governance follow-up

- **Standards architect EVOLVE required:** NO; this record realizes existing G6 choices.
- **Next foundation state:** READY. No behavioral slice is selected or accepted.
- **Next implementation route:** implementation-brief / SCOPE_SELECTION, then human G7.
- **Unchanged scoped prerequisites:** MP-096 invalid-risk readback, Data location adoption and DEFER-001–007 remain with their existing owners. This record does not close them.
