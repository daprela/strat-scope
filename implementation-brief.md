# Implementation Brief — Local HTTPS Foundation

**Active Mode:** `FOUNDATION` (Stage 3B), revision 2, resumed 23 October 2026.

**Status:** `READY_FOR_IMPLEMENTATION` — work-order readiness only.

**Execution status:** `COMPLETE`; implementation-gate accepted and recorded [REC-FOUNDATION](implementation-ledger.md). See [foundation evidence](foundation-evidence/) and [operating instructions](FOUNDATION.md).

**Architecture authority:** [architecture-dossier.md](analysis/tradingview/architecture-dossier.md), revision 2, `IMPLEMENTATION_READY_WITH_NON_BLOCKING_GAPS`; [architecture-review.md](analysis/tradingview/architecture-review.md), revision 1, `READY WITH NON-BLOCKING CHANGES`.

**Implementation standards:** [implementation-standards.md](analysis/tradingview/implementation-standards.md), revision 3, `STANDARDS_READY` / `READY_FOR_FOUNDATION_BOOTSTRAP`; Gate G6 satisfied. Applicable guides: [backend](backend/DEVELOPMENT.md), [frontend](frontend/DEVELOPMENT.md), [UI realization](frontend/UI-DEVELOPMENT.md), and their colocated AGENTS.md files, cumulatively with root AGENTS.md.

**UI impact:** `NOT_REQUIRED` for this infrastructure-only bootstrap. No product task, screen, interaction, navigation, theme choice, or trading state is implemented. Frontend build and renderer feasibility checks use isolated technical fixtures; they do not become a product screen or approved UI realization. Adding a product shell or user-facing workflow requires a UI-bearing brief with actual approved artifacts inspected.

**UI authority consulted for exclusions:** [ui-dossier.md](analysis/tradingview/ui-dossier.md), revision 35; [visual-system.md](analysis/tradingview/visual-system.md), revision 7; [ui-review.md](analysis/tradingview/ui-review.md), revision 5, `READY WITH NON-BLOCKING UI CHANGES`. G4 r14 / G5 r9 are current; older standards/coordination summaries do not override those identities. UIADV-INT-002 remains open for MP-096 light/dark, with 0 BLOCKING / 0 HIGH / 1 MEDIUM / 2 LOW findings overall.

**Implementation ledger entries considered at intake:** None; no ledger or REC-FOUNDATION existed then. Completion review subsequently created root [implementation-ledger.md](implementation-ledger.md), REC-FOUNDATION. **Maintenance case:** N/A.

## 1. Scope and completion

The user requests installation of the approved foundation, reachable at **https://127.0.0.1:4111**, with a certificate trusted by the browser so opening the URL produces no certificate interstitial. That instruction authorizes implementation after this work order; no new G6 or G7 approval is required for the bounded bootstrap.

In scope: locked toolchains; a single local service serving built local assets; origin/capability transport infrastructure and generated contracts; configuration, diagnostics and start/stop/readiness tooling; isolated SQLite/immutable-file/Parquet capability proofs; and Lightweight Charts installation, license preservation and renderer feasibility evidence. Bootstrap may expose technical readiness and serve its locally built client entry without implementing the chart-workspace tasks. It must identify unimplemented capabilities honestly and cannot display fabricated market/trading/save success.

Completion requires actual frozen installation, required checks, platform capability evidence, verified launch/stop/relaunch, and successful browser navigation to the exact HTTPS URL with certificate validation enabled. Only subsequent implementation-gate acceptance may record `REC-FOUNDATION` and make foundation readiness eligible for `READY_FOR_BEHAVIORAL_IMPLEMENTATION`. A written brief, dependency cache, HTTP-only listener, self-signed untrusted certificate, or bypassed TLS check does not meet completion.

Out of scope: provider connections or credentials, data acquisition, source-folder adoption/preferences, market catalog behavior, studies, drawing tools, replay, simulated orders/fees/sizing, backup/restore product workflows, product screens, external completed-run import, remote hosting, and all deferred capabilities in standards Section 5. No placeholder business endpoints, invented financial conventions, or thirteen empty services/modules.

### Historical execution constraints (revision 1)

On 22 October 2026 the earlier managed session allowed writes only to this checkout and `/tmp`, with restricted networking. Creating an AF_INET socket failed at socket creation with `PermissionError: [Errno 1] Operation not permitted`; no listener was started. `npm view lightweight-charts version --fetch-retries=0 --fetch-timeout=10000` failed with `EAI_AGAIN registry.npmjs.org`. Sandbox escalation is unavailable under the active permission policy. No approval request or automatic approval-review rejection occurred.

Installed tools observed: Python 3.14.8, Node v24.18.0, npm 11.16.0, uv 0.12.24, OpenSSL, certutil and Caddy. The read-only npm cache lists Lightweight Charts 5.2.1 and approved-line React/Vite tarballs; uv caches contain relevant packages. Cache presence does not prove a complete compatible dependency set or successful frozen installation. No runtime dependencies were installed in this task.

An existing Caddy root certificate is present in the system trust-anchor directory. Its presence does not prove that an available service certificate covers 127.0.0.1, that its signing service is usable, or that the user's browser trusts it. No CA private key was read/copied, trust store changed, certificate generated, or certificate validation claimed.

### Resume observations (23 October 2026)

The user requested that this existing foundation be resumed and finished. npm registry access and an actual bind/listen/connect to 127.0.0.1:4111 now pass. Host escalation is available and was used for the explicitly owned local installation, browser trust integration and physical/browser tests. The revision-1 environment blocker is resolved for the verified installation.

The approved toolchain is installed and locked. Runtime state and fresh local TLS keys are under `~/.local/share/strat-scope/`, outside the synced checkout. The certificate has IP SAN 127.0.0.1; public identity/date evidence is in `foundation-evidence/tls.txt`. Its public root was installed into both user NSS locations. Actual graphical Chromium with a persistent app profile passed normal TLS navigation, secure-context and authenticated status checks. `make browser` reopens that verified profile. No certificate validation bypass was used. System-wide trust installation required a sudo password and was not completed; `make ready` validates against the installed public CA explicitly. Other browser profiles, including the user's separate Vivaldi default profile, are not certified. The desktop requirement is discharged for the actual Chromium profile recorded in `foundation-evidence/desktop-https.json`.

An isolated tooling workspace under `frontend/tools/contracts/` resolves the released OpenAPI generator's TypeScript-5 peer dependency; application compilation remains TypeScript 6, with one root npm installation/lockfile and no peer-check bypass. This realizes the existing approved toolchain without selecting a new application platform. Initial renderer failures are retained under `foundation-evidence/attempt-*/`; final paging, native hit testing, visible drawing workload and canvas-draw fencing are measured separately from product behavior. Final review must inspect executed evidence rather than infer acceptance from this resume narrative.

## 2. Mandatory blast-radius contract

| Rule | Paths / interfaces | Enforcement |
|---|---|---|
| IB-BR-ALLOW | `backend/pyproject.toml`, `backend/uv.lock`, `backend/.python-version`, `backend/src/`, `backend/tests/`, `backend/migrations/`, `backend/tools/` | Create only foundation host/configuration/authority/retention infrastructure, generated schema tooling and the capability tests described here. No business implementation. |
| IB-BR-ALLOW | `frontend/package.json`, `frontend/package-lock.json`, `frontend/.node-version`, `frontend/index.html`, `frontend/tsconfig*.json`, `frontend/vite.config.ts`, `frontend/vitest.config.ts`, `frontend/playwright.config.ts`, `frontend/eslint.config.*`, `frontend/.prettier*`, `frontend/src/`, `frontend/tests/`, `frontend/tools/`, `frontend/public/licenses/` | Locked build, minimal technical entry, generated transport declarations, adapter feasibility fixtures and scoped tests only. No workspace/task UI. |
| IB-BR-ALLOW | Root `.gitignore`, `Makefile`, `scripts/`, `FOUNDATION.md`, `foundation-evidence/` | Bounded bootstrap/start/stop/readiness commands, installation/trust instructions and sanitized reproducible evidence only. No secret material in tracked evidence. |
| IB-BR-READONLY | All AGENTS.md / DEVELOPMENT.md / UI-DEVELOPMENT.md files; all `analysis/tradingview/` source authorities, approvals, visuals, captured evidence and generators; `contract-v1.0.0/`; `architecture/` | Consume the active authorities as-is. Existing contract utilities are separate authoring tools, not product dependencies. Do not modify authority to fit implementation. |
| IB-BR-READONLY | This `implementation-brief.md` | Scope changes require an explicit revised brief before coding outside these bounds. |
| IB-BR-FORBID | All other repository paths; sibling market-data outputs; `.git/`, `.agents/`, `.codex/`, `.aws/`; existing generated dossier artifacts | No unrelated edits, package upgrades, opportunistic refactoring, blanket formatting, captured-HTML execution or evidence mutation. |

Generated environments/build output under `backend/.venv/`, `frontend/node_modules/`, `frontend/dist/`, and scoped test caches are permitted local ignored outputs, never authored source or evidence of accepted behavior by themselves. Private TLS keys and runtime state stay outside tracked/synced source in explicitly configured owned local paths. `/tmp` may hold disposable test stores; it is not a persistent installed data store.

Governance exceptions to coding scope: project-router may update root `project-state.md` after this briefing; implementation-gate alone may create/append root `implementation-ledger.md` after review. Neither is part of the coding agent's allowed production edits. No dossier source was changed by this brief, so dossier viewer/checksums/ZIP regeneration is not triggered by this root-only handoff.

## 3. Source map

| Authority | Relevant material |
|---|---|
| Architecture Sections 8 / 11 / 12 | BND-001–013; DEP-001–021; semantic contracts and forbidden dependencies |
| Architecture Sections 19–24 | TX-003–005; CONC; owner/version/epoch publication, failure recovery and SECR/TEN confinement |
| Architecture Sections 28–30 / 34 | TF-005–010; ARCHV/AUDV; bounded local diagnostics; FREEDOM-001–005; DEFER-001–007 |
| Architecture review revision 1 | ADV-VER-001: simultaneous publication must preserve unrelated acknowledged durable state |
| Standards revision 3 Sections 2–5 / 11; standards-approval.json | Active G6 stack, dependency policy, required commands and scoped prerequisites |
| Root and backend/frontend scoped guides | Language rules, strict checks, import boundaries, stylesheet/renderer restrictions |
| UI dossier r35 / visual system r7 / UI review r5 | Current design identities and explicit exclusion of affected entry/folder behavior; no product UI conformance claimed |
| Repository inspection / user request | At initial intake roots contained governance only and ledger was absent; foundation source inventory now exists; exact endpoint and trusted HTTPS requirement retained |

## 4. UI impact and authority

No material product UI is authorized here; no `IB-U-*` entries or product-screen acceptance is claimed. Do not copy a mockup/prototype or target markup into the runtime. A renderer probe uses synthetic, clearly labelled fixture data and consumes canonical VIS roles where it demonstrates approved geometry. Its results establish technical feasibility only. Product UI, including keyboard/numeric task alternatives, still needs its approved slice references and runtime UIV evidence.

The latest UI finding is narrowed to the MP-096 invalid-risk readback. It does not block this infrastructure-only brief and must not be silently closed. Data location still requires its architecture-owned adoption/publication contract.

## 5. Project and scoped standards (`IB-P-*`)

All rows are **REQUIRED**, with class/provenance inherited from the cited active standard; none is a new stack choice.

| ID | Upstream standard / class | Rule and enforcement |
|---|---|---|
| IB-P-001 | IS-FND-001 / ARCHITECTURE_CONSTRAINED | Preserve logical owners and inward contracts; import/effect checks, no process per boundary. |
| IB-P-002 | IS-FND-002, IS-RUN-001 / PROJECT_TECHNOLOGY_DECISION | CPython 3.14 conventional GIL, FastAPI/Pydantic 2/Uvicorn; one authoritative service worker serving the built local client. Record actual runtime/GIL versions. |
| IB-P-003 | IS-COM-001 / PROJECT_TECHNOLOGY_DECISION; IS-SEC-001 / ARCHITECTURE_CONSTRAINED | Same-origin HTTP JSON and authenticated WS, generated OpenAPI TS contracts including update envelopes; runtime decoding, exact Host/Origin validation and capability isolation. Positive and negative transport tests. |
| IB-P-004 | IS-UI-001/002 / PROJECT_TECHNOLOGY_DECISION | React 19, TS 6, Vite 8, Lightweight Charts 5.2.x exact released pin, native adapter, local assets/notices; no wrapper, fork, competing state/theme library or CDN. Test-only renderer proof does not implement a trading screen. |
| IB-P-005 | IS-STORE-001, IS-NUM-001 / PROJECT_TECHNOLOGY_DECISION; IS-DATA-001, IS-STATE-001 / ARCHITECTURE_CONSTRAINED | stdlib SQLite, ordered tracked SQL migrations, immutable owned Parquet via PyArrow; lossless decimal/integer strings and explicit units; real publication/recovery proofs. No rounding policy. |
| IB-P-006 | IS-PKG-001, IS-BUILD-001 / ENGINEERING_POLICY_DECISION | uv/uv.lock and npm/package-lock.json, Node 24; exact compatible pins and frozen install/build record. Locally bundled assets served by the service, offline runtime for retained data. |
| IB-P-007 | IS-QA-001 / ENGINEERING_POLICY_DECISION; IS-VERIFY-001 / ARCHITECTURE_CONSTRAINED | Wire all prescribed backend/frontend commands below; distinguish structural/unit, physical storage, browser and measured P3 evidence. No generic coverage percentage gate. |
| IB-P-008 | IS-OPS-001 / ENGINEERING_POLICY_DECISION | Validated service-only configuration, safe JSONL rotation: 10 MiB current plus four rotated files, events at most 16 KiB; local counters/timings, bounded metric labels, no secrets/raw histories/remote telemetry. Config and secret-sentinel tests. |
| IB-P-009 | IS-SCOPE-001 / ENGINEERING_POLICY_DECISION; scoped DEVELOPMENT guides | Backend Ruff 88 columns / strict basedpyright; TS strict, noUncheckedIndexedAccess, exactOptionalPropertyTypes, hooks lint; Prettier two spaces/100 columns/single quotes/semicolons; SQLite bound values and immutable accepted migrations. Existing dossier/reference tools remain isolated. |
| IB-P-010 | frontend/UI-DEVELOPMENT.md UIS-REAL-002–004/011/013, scoped IMPLEMENTATION_DERIVED and APPROVED_PROPOSAL | Keep chart objects/pixels inside adapter; canonical semantic token map supplies visual values; preserve original bucket identity, independent side absence and local license attribution. Probe data never claims provider truth or product UI acceptance. |

## 6. Prior implementation context (`IB-E-*`)

At foundation intake no accepted records existed; no prior `IB-E-*` implementation fact is invented. Reuse existing governance and authoring workflows as read-only context. Installed tools, cache entries and the system trust anchor are observed environment facts to **VERIFY BEFORE USE**, not accepted project realizations. Verify no implementation appeared after this inspection before creating competing infrastructure.

## 7. Architecture constraints (`IB-C-*`)

| ID | Category | Constraint | Source |
|---|---|---|---|
| IB-C-001 | BOUNDARY / FORBIDDEN_DEP | Core semantic owners remain independent of FastAPI/Pydantic, SQLite/PyArrow, vendor SDKs and chart types. Only introduce inward contracts actually needed by foundation capabilities. | IMPL-001; BND-010/012/013; DEP-011/015–021; ARCHV-001 |
| IB-C-002 | SECURITY_TENANT | One authority per owned store across processes. An additional browser cannot become a second writer; connection loss alone never grants takeover. Check purpose/owner/version/epoch at acceptance and publication; shutdown/revocation fences callbacks. | SECR-001/006/007; TEN-001; CONC-001–005; ARCHV-005 |
| IB-C-003 | SECURITY_TENANT | Loopback is insufficient authorization. Foreign Host/Origin, unbound callers, invalid/reused/stale capabilities and unauthorized WS must fail without state change. Capability bootstrap cannot be read by a foreign page. No wildcard CORS or tokens in URLs/logs/browser persistence. | FREEDOM-004; SECR-001/003/008; IS-COM-001 enforcement |
| IB-C-004 | DATAOWN / SECURITY_TENANT | Source roots are read-only; writes confined to explicit owned roots outside the synced checkout. Reject path traversal/symlink escapes and unsafe configuration before mutation. No provider secrets or private captures in source/browser/schema/logs/exports/evidence. | IMPL-003/011; SECR-003/004/008; TEN-001/004; ARCHV-003 |
| IB-C-005 | RESILIENCE | Retain and verify complete immutable content before atomic metadata publication. Acknowledgement names exact retained generation. Crash/reopen yields old or new coherent referenced state; uncertain acknowledgement reconciles actual publication. | TX-003–005; INV-04/12; CONS-15/16; FAIL-012–020; TF-006 |
| IB-C-006 | RESILIENCE | Catalog publication, checkpoint and scoped replacement must preserve unrelated acknowledged state; stale candidates cannot regress active references. Synthetic opaque foundation fixtures test the mechanism without implementing catalog/run behavior. | ADV-VER-001; CONC-005–010; TX-003–005 |
| IB-C-007 | CONTRACT / DATAOWN | Preserve integer time values with units and exact decimal representations at transport/Parquet boundaries; drawing coordinates are derived only. No financial rounding, price/quantity conventions or timestamp shifts for paired quotes. | DRV-001/006; IMPL-002/004; IS-NUM-001; DEFER-003/004 |
| IB-C-008 | BOUNDARY / AUDIT | No provider, replay, execution, study or folder-adoption behavior in bootstrap; no fictitious completed capabilities, market data or saved-success assertions. Diagnostics are bounded sanitized operational evidence, separate from retained semantic facts. | BND-003–009/011 exclusions; IMPL-015; LOG-001–005; AUD-001–004; DEFER-001–007 |

### Exact local HTTPS acceptance

Bind the configured service to `127.0.0.1:4111` and serve built frontend/API/WS from `https://127.0.0.1:4111` / `wss://127.0.0.1:4111`. Never silently switch to another port, HTTP, a network-wide bind, or a different hostname. Host/Origin allowlists must reflect the exact HTTPS launch origin.

Supply a valid server certificate with **IP Subject Alternative Name 127.0.0.1**, matching private key, valid dates, and a chain trusted by the actual browser profile on the computer opening that URL. Certificate/key paths are service-only configuration. Use existing valid local certificate infrastructure if available; otherwise provision a local development CA and integrate its public root into the relevant trust stores through the host's supported mechanism. Preserve private CA/service keys outside tracked/synced source and exports. Do not repurpose or copy a system CA private key into the repository.

The already selected Uvicorn host can terminate TLS using configured certificate/key files; an additional production reverse proxy is not required by this brief. If the host requires a materially different deployment mechanism, return that choice to standards rather than silently add a second service. A local trust-provisioning utility is installation support only, with its exact version and trust changes documented.

Verify with normal certificate validation from the host and by opening the URL in the intended browser profile. Do not use `curl -k`, `ignoreHTTPSErrors`, `--ignore-certificate-errors`, certificate-warning click-throughs or disabled validation as acceptance. A test-specific CA bundle proves chain/hostname validation only, not trust in the user's browser. A CA installed on the service machine cannot by itself prove trust in a browser on another machine; 127.0.0.1 must resolve to the service's actual host.

## 8. Implementation freedom and decisions to report

| ID | Type | Allowed choice / required report | Relevance |
|---|---|---|---|
| IB-F-001 | Freedom | Local helper names and bounded test organization within the allowed paths; no semantic or topology change. | LOCAL; FREEDOM-001/005 |
| IB-D-001 | Decision to record | Exact compatible released dependency/tool pins within G6 lines, actual licenses/notices and offline build output; report successful clean frozen resolution, not just cache availability. | LOCAL realization; IS-PKG-001 |
| IB-D-002 | Decision to record | Store ownership primitive and SQLite/immutable-file flush/publication implementation. Candidate: OS-held exclusive lock, SQLite transactional references with durable settings, file flush + atomic publication + directory flush before reference commit. Report actual settings, filesystem and every tested crash frontier; no guarantee before evidence. | LOCAL realization of IS-STORE-001 / FREEDOM-003; reusable evidence |
| IB-D-003 | Decision to record | Same-origin capability bootstrap, short-lived purpose binding, in-memory frontend handling, revocation and second-tab policy; expiration bound must be explicitly validated/documented without inventing provider timing. Record attack tests and denied stale publication. | LOCAL realization of IS-COM-001; no accounts/tenancy |
| IB-D-004 | Decision to record | Certificate source, public fingerprint/SAN/expiry, trust-store integration and browser-profile evidence; never report keys/tokens. Record direct TLS launch/configuration and renewal procedure. | LOCAL installation realization; user endpoint requirement |

No IB-D authorizes changing a project-wide stack, security guarantee, domain rule or UI design. Such conflicts route to the owning authority.

## 9. Verification obligations (`IB-V-*`)

All rows require retained sanitized commands/results, observed versions and explicit limitations in `foundation-evidence/`. Test fixtures demonstrate mechanisms, not provider truth or business-feature completion.

| ID | Property / failure guarded against | Authority and expected evidence | Mechanism |
|---|---|---|---|
| IB-V-001 | Frozen reproducible install and offline locally served assets; imports respect boundaries | ARCH_VERIFICATION: ARCHV-001, IMPL-013/014; IS-PKG/BUILD/QA | Required scope commands; exact version/lock and asset-request records; no CDN runtime requests. |
| IB-V-002 | Foreign page cannot obtain capability; wrong Host/Origin/purpose/epoch rejected; allowed owner HTTP/WS works; second tab cannot mutate | ARCH_VERIFICATION: TF-005, ARCHV-003/005; SECR-001/006 | Service tests plus real-browser foreign-origin and two-tab tests, with controlled expiry/revocation. Verify normal bootstrap is usable without capability leakage. |
| IB-V-003 | Actual two-process exclusion and safe release after owner exit; disconnected writer cannot be bypassed | ARCH_VERIFICATION: TF-006, CONC-001–005, ARCHV-005 | Independent real processes against the same local owned store; publication barrier and stale-epoch tests. In-memory locks alone cannot pass. |
| IB-V-004 | Immutable content before references; crash/reopen old-or-new state, no acknowledged state regression; failure preserves prior active state | ARCH_VERIFICATION: TX-003–005, TF-006, ARCHV-006 | Empty initialization / supported migration upgrades and rollback; real-process interruption before/after file flush, reference commit and before ack; missing/corrupt content, disk-full/failure injection; record filesystem/settings. |
| IB-V-005 | Independent publications preserve unrelated durable records and pinned content | ARCH_VERIFICATION: ADV-VER-001, TF-006, CONC-005–010 | Barrier-controlled catalog-like/checkpoint-like and scoped-replacement fixtures, reopen and compare complete state including unrelated acknowledged records. No business implementation or arbitrary sleeps. |
| IB-V-006 | Exact instants/units/decimals/occurrences survive JSON and Parquet round-trip; unsafe roots rejected | ARCH_VERIFICATION: TF-006/007, ARCHV-003/006, AUDV-001/003 | Independent expected boundary values beyond JS safe integer range; explicit unit/decimal checks, escapes/symlinks/invalid config, secret-sentinel checks. No monetary-policy examples invented. |
| IB-V-007 | Safe bounded diagnostics, rotation and truthful failure/readiness; no capability/private payload leakage | ARCH_VERIFICATION: LOG-001–005, SECR-003/008, AUDV-001/003; IS-OPS-001 | 16 KiB event/10 MiB rotation and dropped-event counters, config rejection, sentinel scans, bounded metric dimensions; logs are not saved-state authority. |
| IB-V-008 | Installed renderer can implement paired geometry without false timestamps/precision or missing layers | ARCH_VERIFICATION: IMPL-013/014, TF-010; IS-UI-002 (UI references are feasibility targets only) | Test-only native-adapter custom-series/primitives probe: filled Bid-left/hollow Ask-right and volumes per original bucket; absence, autoscale, hit/crosshair identity, panes, precision mapping, disposal/resize, local export and notices. Preserve original values; do not implement product task controls. |
| IB-V-009 | Renderer feasibility meets accepted workload rather than smoke-test-only performance | ARCH_VERIFICATION: TF-010, MET-001/002; SCALE-03/P3 | Record hardware/browser, two charts, 100k resident bars/chart, four study panes, 100 drawing primitives; ready-local initial viewport <2 s, interaction p95 <50 ms, local receipt-to-display within 1 s. Synthetic fixture timing does not certify provider integration or finished product journeys. |
| IB-V-010 | Exact requested HTTPS origin reachable, trusted, same-origin and restartable; no cert bypass | User deployment requirement implementing FREEDOM-004 / IS-RUN/COM/BUILD | Start → normal TLS readiness → intended browser profile → stop → listener closed → relaunch; record SAN/chain/date/trust evidence, secure-context/asset/WS results with validation enabled. Block if actual trust or bind unavailable. |
| IB-V-011 | Generated schema/types and runtime WS/HTTP contracts agree; no manual generated edits | ARCH_VERIFICATION: contract boundary constraints / IS-COM-001 | Canonical OpenAPI export includes update envelopes, openapi-typescript regeneration byte comparison; malformed/unsafe precision envelopes rejected at runtime. |

Prescribed backend commands, within `backend/`: `uv sync --frozen`; `uv run ruff check .`; `uv run ruff format --check .`; `uv run basedpyright`; `uv run pytest`.

Prescribed frontend commands, within `frontend/`: `npm ci`; `npm run typecheck`; `npm run lint`; `npm run format:check`; `npm run test -- --run`; `npm run build`; `npm run test:e2e`. Define these scripts during bootstrap. Playwright Chromium supplies selective actual-browser evidence; report actual browser/profile trust scope. A headless pass with its own certificate store does not certify the user's desktop browser profile.

UIV product-screen acceptance is intentionally unperformed. Future UI-bearing slices retain UIV-DATA-003/VIS-002, UIV-A11Y, UIV-ADAPT, and UIV-EVID obligations; renderer probes and performance fixtures cannot discharge them.

## 10. Stop conditions (`IB-S-*`)

| ID | Condition | Consequence / owner |
|---|---|---|
| IB-S-001 | Need to edit any path outside IB-BR-ALLOW, or implement product UI/business behavior | Stop affected coding; implementation-brief revises scope and loads applicable approved UI artifacts before changes. |
| IB-S-002 | Approved-line dependency set, storage/ownership primitive or renderer cannot satisfy required properties | Preserve failures; standards-architect reconsiders the affected G6 realization. No fallback stack, weakened guarantees or untested durability claim. |
| IB-S-003 | Missing provider/calendar, numerical/study/tool, entry-readback or folder-adoption authority becomes relevant | Do not implement it. DEFER-001/002 → integration evidence; DEFER-003/004 → domain/calculation; MP-096 → ui-screen-designer then scoped G5/review; Data location → system-architecture-designer. |
| IB-S-004 | Listener/network/persistent-store/trust permissions unavailable, or actual browser trust cannot be verified | Execution blocked, not new approval gate. Host environment must supply permissions/certificate trust; keep installation and foundation acceptance incomplete. Revalidate when changing host, certificate, store filesystem or browser profile; the resumed verified installation has passed these checks. |
| IB-S-005 | Tests do not establish old-or-new recovery, unrelated-publication preservation, exclusion, precision or renderer capability | Stop foundation acceptance; correct local implementation or route genuine authority conflict. Preserve full evidence limits; do not record REC-FOUNDATION. |

## 11. Coding handoff and quality-gate assessment

Read this brief, cited active authorities and every applicable scoped guide before coding. Reinspect roots and existing ledger; reuse any subsequently accepted capabilities. Implement only the allowed foundation mechanisms. Preserve every IB-C and IB-P, use only stated freedom, report every IB-D, and produce IB-V evidence. Do not copy captured target markup or treat a fixture/prototype as product code. Honor IB-S rather than widening scope or inventing semantics.

Hand modified-file inventory/diff, exact commands/results, lock/runtime identities, sanitized physical/browser/performance evidence and unresolved limitations to **implementation-gate / REVIEW_AND_RECORD**, together with this brief and active standards/guides. Its acceptance, not this brief, owns the first ledger record.

Quality gates: architecture approval and G6 foundation intake pass; ledger absence verified; blast radius, exclusions, traceability, local decisions, verification and stop routes explicit. Behavioral foundation-readiness and selected-slice gates in the generic template are inapplicable to FOUNDATION intake; this mode specifically bootstraps the approved `READY_FOR_FOUNDATION_BOOTSTRAP` state. UI gate is inapplicable because no product UI is implemented. No new architectural, UI or project-wide technology decision is selected. Implementation can proceed under these authorities in a capable host environment; the earlier environment blocker is resolved for the installation/profile and physical-test scope recorded above. Executed results are retained in foundation-evidence; implementation-gate must review them before acceptance.

**Work-order signal:** `READY_FOR_IMPLEMENTATION`; **execution:** `COMPLETE`; **review signal:** `SLICE_ACCEPTED_AND_RECORDED`; **accepted foundation:** `REC-FOUNDATION`, ready for separately governed behavioral scope selection. Detailed conformance and limitations: [review](foundation-evidence/review.md).
