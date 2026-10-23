# Implementation Standards

## Document Status

- **Project:** Dukascopy Chart Workspace and Historical Trading.
- **Mode / version:** `INITIALIZE`, revision 3, 22 October 2026; Gate G6 approved and standards activated.
- **Status:** `STANDARDS_READY`.
- **Foundation Sub-State:** `READY_FOR_FOUNDATION_BOOTSTRAP`; application implementation has not started.
- **Architecture Authority:** [architecture-dossier.md](architecture-dossier.md), revision 2, `IMPLEMENTATION_READY_WITH_NON_BLOCKING_GAPS`; [architecture-review.md](architecture-review.md), revision 1, `READY WITH NON-BLOCKING CHANGES`.
- **UI Authority:** [ui-dossier.md](ui-dossier.md), revision 28; [visual-system.md](visual-system.md), revision 7; WF-SET-001-r13 / MP-SET-001-r7 approved at G4/G5. [ui-review.md](ui-review.md), revision 3, is `READY WITH NON-BLOCKING UI CHANGES`, with one MEDIUM finding, UIADV-INT-002.
- **Approval:** G6-DEC-004 was selected explicitly on 21 October 2026: “for charts I want to use Lightweight charts from TradingView, please add it to the specs”. On 22 October 2026 the user approved G6-DEC-001–003 and G6-DEC-005–010: “I approve all the remaining Open Gate G6 decisions”. All ten decisions from revision 2 are approved without further amendments. See [standards-approval.json](standards-approval.json) for the decision/authority/artifact identity record.
- **Activation boundary:** The approved IS rules, four scoped coding guides, frontend UI guide and cumulative root/scoped AGENTS routing are active. Their activation authorizes governed foundation briefing, not unbriefed production coding or a claim that dependencies, storage, provider access or rendering have been verified. Existing affected-scope prerequisites remain in Section 5.

## 1. Authority & Precedence

1. Requirements and domain authorities, then architecture-dossier.md: scope, meaning, boundaries, contracts, security, resilience and verification properties.
2. ui-dossier.md and visual-system.md: interaction, structure, approved visual references and semantic tokens. Later explicit overrides recorded there supersede historical values.
3. This active document: project foundation, tooling and dependency policy.
4. Activated scoped UI-DEVELOPMENT.md and DEVELOPMENT.md: UI realization and coding conventions.
5. implementation-brief.md when present: authorized work and blast radius.
6. implementation-ledger.md when present: historical results and accepted deviations; it does not silently override higher authority.

Existing root AGENTS.md remains applicable. Its dossier commands and read-only evidence requirements continue unchanged. The four scoped development guides and frontend UI guide are active. backend/ and frontend/ contain governance documents only; application manifests and an implementation ledger are not present. The independent contract-v1.0.0 authoring tools are existing Python reference utilities, not an implemented chart application. External run-bundle import remains excluded from v1. Older LOCAL-IMPLEMENTATION.md choices remain historical proposals; only its Lightweight Charts choice is now independently selected by this user instruction. Its Node service, time representations and broader feature examples gain no authority from that selection.

project-state.md records the current specialist review revision 3, completed Stage 3A and satisfied G6. It is coordination metadata; this document and the scoped guides supply standards authority.

## 2. Foundation Profile and Candidate Tests (`IS-*`)

**Tests:** B = a common choice is necessary before the first relevant implementation can start; R = independent slice choices would create substantial incompatibility or migration; N = capability is needed now by approved scope or foundation. Yes means the test passes. Scoped provider prerequisites are present requirements, not optional future features. Packages for them cannot be selected before evidence identifies the real integration.

**Strength** is REQUIRED or DEFAULT. All standards in this profile are active: inherited architectural obligations retain their source authority; technology and policy choices have explicit Gate G6 approval. Tool installation and proof of capability remain foundation work.

| Standard ID | Dimension / decision | Class | Scope | Strength | B/R/N | State / provenance |
|---|---|---|---|---|---|---|
| IS-FND-001 | Preserve thirteen logical boundaries, inward contracts and domain ownership; no process per boundary | ARCHITECTURE_CONSTRAINED | Application | REQUIRED | Yes/Yes/Yes | Inherited: BND-001–013, DEP-001–021, IMPL-001 |
| IS-DATA-001 | Explicit qualified basis, original precision and occurrence order, full discovered archive, common replay boundary | ARCHITECTURE_CONSTRAINED | Application | REQUIRED | Yes/Yes/Yes | Inherited: IMPL-002/004, CONTRACT-012/020 |
| IS-STATE-001 | Coherent working transitions; immutable input closure; atomic durable generation and exact saved acknowledgement | ARCHITECTURE_CONSTRAINED | Application | REQUIRED | Yes/Yes/Yes | Inherited: TX-001–006, CM-001–007, IMPL-003/006–010/012 |
| IS-SEC-001 | Sole authoritative writer, fenced epochs, confined input/write roots, protected data-only provider edge | ARCHITECTURE_CONSTRAINED | Application | REQUIRED | Yes/Yes/Yes | Inherited: CONC-001–012, SECR-001–008, TEN-001–004 |
| IS-VERIFY-001 | Separate domain, workflow, physical storage, integration, UI and performance evidence | ARCHITECTURE_CONSTRAINED | Application | REQUIRED | Yes/Yes/Yes | Inherited: TF-001–010, ARCHV-001–007, AUDV-001–004, ADV-VER-001, UIV-* |
| IS-FND-002 | One local Python service owns mutation; desktop browser presents locally served assets | PROJECT_TECHNOLOGY_DECISION | backend/, frontend/ | REQUIRED | Yes/Yes/Yes | Approved G6-DEC-001; FREEDOM-004, UIR-ENV-001/002 |
| IS-RUN-001 | CPython 3.14 conventional GIL build; FastAPI, Pydantic 2, Uvicorn with one authoritative worker | PROJECT_TECHNOLOGY_DECISION | backend/ | REQUIRED | Yes/Yes/Yes | Approved G6-DEC-001; BND-010–013, DEFER-007 |
| IS-COM-001 | Same-origin HTTP/JSON commands and bounded reads; authenticated WebSocket view/status updates; OpenAPI-derived TS transport types | PROJECT_TECHNOLOGY_DECISION | Application transport | REQUIRED | Yes/Yes/Yes | Approved G6-DEC-002; CONTRACT-001–020, SECR-001/006 |
| IS-UI-001 | React 19, TypeScript 6, Vite 8; CSS Modules and semantic CSS custom properties | PROJECT_TECHNOLOGY_DECISION | frontend/ | REQUIRED | Yes/Yes/Yes | Approved G6-DEC-003; UI-FREEDOM-001/004 |
| IS-UI-002 | TradingView Lightweight Charts behind an adapter; custom series/primitives for approved quote/drawing grammar and semantic DOM controls/readouts | PROJECT_TECHNOLOGY_DECISION | frontend/ | REQUIRED | Yes/Yes/Yes | User-selected G6-DEC-004; UI-FREEDOM-003, VIS-DATA-009/010; foundation bootstrap pending |
| IS-STORE-001 | SQLite through stdlib sqlite3 for durable work/catalog metadata; immutable owned Parquet evidence through PyArrow | PROJECT_TECHNOLOGY_DECISION | backend/ retention edge | REQUIRED | Yes/Yes/Yes | Approved G6-DEC-005; CONTRACT-015, TX-003–006, INT-001 |
| IS-NUM-001 | Exact integer instants with explicit units, decimal strings across JSON, Decimal for monetary implementation | PROJECT_TECHNOLOGY_DECISION | Application representations | REQUIRED | Yes/Yes/Yes | Approved G6-DEC-002; DRV-001/006, DEFER-004 |
| IS-PKG-001 | uv/uv.lock per Python environment; npm/package-lock.json for frontend; Node 24 build tooling | ENGINEERING_POLICY_DECISION | Maintained tooling/application | REQUIRED | Yes/Yes/Yes | Approved G6-DEC-006; deterministic offline execution, DEFER-007 |
| IS-BUILD-001 | Source-based local release: locked Python environment plus Vite static assets served by service; no CDN runtime assets | ENGINEERING_POLICY_DECISION | Application distribution | REQUIRED | Yes/Yes/Yes | Approved G6-DEC-006; UIR-ENV-002, IMPL-014 |
| IS-QA-001 | pytest/Ruff/basedpyright; tsc/ESLint/Prettier/Vitest/Testing Library/Playwright; property-specific acceptance | ENGINEERING_POLICY_DECISION | backend/, frontend/ | REQUIRED | Yes/Yes/Yes | Approved G6-DEC-007; TF/ARCHV/AUDV/UIV; not a coverage-percentage gate |
| IS-OPS-001 | Validated service-only configuration; sanitized rotating JSONL logs, local timings and correlated phases | ENGINEERING_POLICY_DECISION | backend/, frontend/ | REQUIRED | Yes/Yes/Yes | Approved G6-DEC-008; LOG/MET/TRACE/DIAG, DEFER-006 |
| IS-SCOPE-001 | backend/ and frontend/ for application; analysis/tradingview/ and contract-v1.0.0/ separately govern existing authoring tools | ENGINEERING_POLICY_DECISION | Repository routing | REQUIRED | Yes/Yes/Yes | Approved G6-DEC-009; fewest coherent maintained contexts |

No PROMOTED_IMPLEMENTATION_STANDARD exists: no implementation-ledger.md or accepted implementation precedent is present. No independently invented ARCHV or UIV identities are introduced here.

## 3. Standards Detail and Enforcement Plan

Commands in this section are **required future checks**, to be wired by an approved foundation brief. Their specification is active; they are not installed tools, existing scripts or passing results. Application roots currently contain governance documents only.

### Inherited constraints: IS-FND-001, IS-DATA-001, IS-STATE-001, IS-SEC-001, IS-VERIFY-001

Core semantic owners must remain independent of FastAPI/Pydantic, sqlite3/PyArrow, provider SDKs and renderer objects. Adapters translate into inward-defined values/contracts. UI cannot calculate authoritative fills, fees, coverage or saved success. Background computation produces candidates, while authorized version/epoch checks control publication. A process pool, if measured work requires one, receives bounded immutable inputs and cannot publish authoritative state directly. This is task execution within the local application, not thirteen services or a distributed queue.

Full-history navigation is independent of resident arrays. Preserve nanosecond bars and millisecond ticks with their actual unit and occurrence ordering; never import the older blueprint's millisecond-only rule. Current-history improvement cannot mutate retained run inputs. Working accepted/executed and exact saved versions remain independent.

**Enforcement:** pytest architecture checks for prohibited imports/capabilities and ARCHV-001–007; deterministic workflow barriers for CONC/IDEM/RETRY/ORDER; real-process reopen/failure tests for TX-003–006 and TF-006. Include ADV-VER-001: catalog publication racing with autosave or scoped run replacement must preserve unrelated acknowledged durable state. UI checks map to actual UIV identities. Static checks and mock storage cannot establish physical durability.

### Runtime and transport: IS-FND-002, IS-RUN-001, IS-COM-001

Bind the service to loopback, serve the built client from that origin, and keep one mutation authority per work store. Validate Host and Origin against the launch configuration; reject cross-origin mutations and WebSocket connections. A short-lived, purpose-bound application capability is required in addition to loopback. Do not place it in URLs, logs, backups or persistent browser storage; provider credentials never enter the client. The transport bootstrap must prove that a foreign web page cannot obtain the capability. Development proxying must preserve the same rules rather than enable wildcard CORS.

Use one Uvicorn authoritative worker, exclusive store ownership across processes, per-run ordering and version/owner/run/restore epoch fencing through publication. A second browser tab receives read-only/denied mutation authority. Losing a connection or observing a timeout cannot grant another writer permission while the previous writer can still publish. Acquisition follows application runtime authority and stops/fences callbacks on shutdown or revocation.

FastAPI/Pydantic represent transport validation, not business validity. Export OpenAPI from the service contract and use openapi-typescript for generated TS types. Include update envelope models in the canonical transport schema; enforce schema compatibility for WebSocket messages as well as HTTP responses. Native fetch/WebSocket are sufficient; do not add an additional client state/cache package at bootstrap. Generated declarations do not provide runtime validation: service responses and received messages require controlled decoding/contract checks at the boundary.

**Enforcement:** HTTP/WebSocket allowed-owner and foreign-origin tests, a two-service exclusion test against the same actual store, stale-epoch publication tests, and schema regeneration with a clean byte comparison. Command retry preserves logical occurrence identity and canonical payload; reconnect refreshes authorized snapshots rather than replaying unsaved intents. No endpoint inventory or new domain command is designed here.

### Presentation: IS-UI-001 and IS-UI-002

Use TradingView **Lightweight Charts**, the browser-side `lightweight-charts` npm package, as the required chart engine behind the BND-012 renderer adapter. Target the documented 5.2.x API line and freeze an exact compatible released package version during foundation bootstrap. Bundle its JavaScript and dependencies locally with the frontend. Use its native TypeScript API directly; no React wrapper package or vendor fork is selected. The surrounding React choice is approved under G6-DEC-003. Create/dispose chart instances and subscriptions with the UI lifecycle; resize and update existing instances rather than recreating them on each render.

Use semantic DOM controls, task surfaces and readouts around the chart. Keep library objects, chart buffers, viewport transforms and callbacks inside the adapter; core contracts and saved drawings carry semantic values, not `IChartApi`/series handles or pixels. Shell-local state uses the approved React hooks/reducers/context; canonical run, calculation, catalog and durability state remains service-owned. Explicit context generations prevent adopting obsolete views. Chart callbacks cannot advance replay or execute an instruction. Do not add another global state library until measured complexity establishes present need.

The renderer must support filled Bid / hollow Ask, adjacent Bid-left and Ask-right slots in one true UTC bucket, separate OHLCV and provider-volume readouts, exact active-theme colors, financial drawing anchors, panes, selection and local image export. Never shift actual timestamps to separate candle slots. Geometry can use bounded relative numeric coordinates while original instants/prices remain lossless outside the drawing transform. Virtualize/cull visible geometry; never turn view culling into a history-retention cap.

**Customization:** Use built-in series/panes where they satisfy the approved design, with adapter-owned custom series for paired candle/volume geometry and primitives for financially anchored drawings or annotations where needed. Two ordinary candlestick series sharing timestamps must not be assumed to provide adjacent side slots. A custom series can carry both quotes for one real UTC bucket and draw separate Bid/Ask slots within that bucket. Prove autoscale, hit testing, crosshair/selection and missing-side readouts against the original bucket identity; use equivalent custom geometry for paired filled/hollow volume bars. Hollow Ask bodies and open/close ticks remain required. Map VIS roles into library options and custom drawing code; library defaults never replace approved tokens. These are implementation requirements to demonstrate, not claims that the library's defaults already meet them. The documented [custom-series extension](https://tradingview.github.io/lightweight-charts/docs/plugins/custom_series), [series primitives](https://tradingview.github.io/lightweight-charts/docs/plugins/series-primitives) and [panes](https://tradingview.github.io/lightweight-charts/tutorials/how_to/panes) provide the intended extension mechanisms.

**Data and accessibility:** The chart receives already bounded application data; studies, replay, execution, storage and market acquisition remain with their existing owners. Explicitly convert source bar bucket instants to the library's UTC-seconds presentation representation and retain lossless original identities/units separately. Do not pass nanoseconds as JS numbers, collapse distinct events, shift timestamps for quote spacing or feed post-cursor facts to chart autoscaling/legends. Readouts and numeric drawing editing use original values; library canvas interactions do not establish keyboard or screen-reader support. Image export must include the intended chart/custom layers and approved source/boundary labels; verify any separately overlaid DOM/SVG content rather than assuming the library screenshot includes it.

**Distribution and attribution:** Follow the selected release's Apache-2.0 LICENSE/NOTICE and documented creator attribution/link instructions. Include its notices in local distribution and make the notice plus TradingView link available in application-accessible attribution content. A plain-text library credit can preserve VIS-CONT-003's local application identity; selecting this library does not authorize TradingView product branding or account/upgrade decorations. The optional on-chart attribution logo is not required by this spec; if selected later, route its placement through the UI owner. Runtime assets remain local and no background TradingView data request is introduced. Attribution guidance is recorded from the [official getting-started documentation](https://tradingview.github.io/lightweight-charts/docs#license-and-attribution); confirm against the exact installed release at packaging.

**Rationale/trade-off:** This is the user's explicit chart-engine choice. It reuses chart scales, panes and navigation while retaining adapter-owned custom quote geometry, drawings, accessible controls and export composition. No claim that the library alone meets P3 or supplies these complete application features is made. Replacing the engine or maintaining a vendor fork requires an explicit standards revision; a slice cannot silently substitute the earlier standalone Canvas engine.

**Enforcement:** frontend unit/component tests for transforms and truthful state; Playwright for keyboard/numeric alternatives, original coordinates, visual comparison and UIV-DATA-003/VIS-002; TF-010 on recorded hardware with two charts, 100k resident bars/chart, four study panes and 100 drawings. Ready-local initial viewport <2s, interaction p95 <50ms, display within 1s of local receipt remain the accepted targets. If this realization cannot meet them, return its technology decision for revision rather than weaken the targets.

### Persistence and exact representation: IS-STORE-001 and IS-NUM-001

SQLite is the durable metadata/reference publication mechanism; app-owned immutable files retain selected evidence and acquired history. PyArrow reads the actual Parquet schema in the external-source adapter and writes owned Parquet without silently coercing precision or occurrence identity. No ORM or general analytical SQL engine is needed at bootstrap. SQL migrations are numbered, ordered and tracked; test empty creation and supported-version upgrades before activation. Physical schemas are future implementation work under the existing conceptual ownership.

Stage, verify and durably retain complete referenced file content before atomically committing its active metadata reference. SQLite and filesystem writes are not a shared transaction: never reference incomplete files, acknowledge before durable closure, or let cleanup reclaim pinned content. Keep work/catalog publication compatible with unrelated committed state. Choose database settings and file flush/directory publication procedures in the foundation brief, then prove them with actual crash/reopen frontiers and negative tests. Merely selecting SQLite does not discharge TX-004/TX-005 or DEFER-007.

Keep the active store on a tested local filesystem outside this Google Drive checkout; configure its location explicitly. Do not assume synced/network filesystem locking or durability. Source read roots and owned write roots are separate. This choice does not supply the missing architecture-owned Data location adoption contract. Backups of owned work remain included; contract-v1.0.0 external-run import remains excluded.

Represent original instants as integers with explicit units internally and decimal integer strings over JSON where required to avoid JS precision loss. Use Decimal constructed from exact source representations for monetary calculations; do not use the process default context as an undocumented policy. Reject non-finite inputs. BND-009 must supply approved precision, rounding, quantity steps and independent examples under DEFER-004 before monetary behavior is implemented. This technology choice selects no financial rounding rule or inferred instrument value. Renderer floats must never round-trip into retained values implicitly.

**Enforcement:** pytest persistence/round-trip/migration tests for TF-006/007, ARCHV-003/006 and AUDV; interruption before/after content retention and reference commit, lost acknowledgement, source mutation, full disk, two-process ownership, stale saves, backup pinning and concurrent catalog/work publications. Compare original precision and whole recovered state; validate rejected candidates leave prior state intact.

### Dependencies, packaging and verification: IS-PKG-001, IS-BUILD-001, IS-QA-001

Use CPython 3.14.x and Node 24.x; Node is build/test tooling, not a second application service. uv manages the backend project and frozen lock; npm manages one frontend package and lock. Keep authoring-tool dependency groups separate from product runtime. For the existing contract tools, use their own environment/lock if they are maintained; do not add PyArrow to the standard-library-only evidence extractors.

Record exact interpreter, Node, tool and dependency versions in foundation evidence. React 19.x / TypeScript 6.x / Vite 8.x are approved compatibility lines; Lightweight Charts targets the documented 5.2.x line under the user-selected engine decision. Resolve and commit exact compatible released package pins during foundation bootstrap with clean install/build evidence. No floating latest resolution in verification or distribution. Major-line or capability changes require standards reconsideration. Official support documentation is research evidence, not proof that this repository's dependency set has been installed together.

Release locally built assets with the locked Python application. Runtime must work with local retained history and all UI assets offline; provider recovery separately requires network access. Provide a single documented local launch/stop path and actual readiness checks through the foundation brief. An installer, container or desktop wrapper is unnecessary for this baseline. Preserve the separate offline dossier build/package workflow.

Required backend checks after bootstrap: `uv sync --frozen`, `uv run ruff check .`, `uv run ruff format --check .`, `uv run basedpyright`, `uv run pytest`. Run within backend/ once configured. Use Ruff E4/E7/E9/F/I/B/UP rules without formatter-conflicting layout checks, 88-column formatting and basedpyright strict for new backend code. Required narrow suppressions name a reason; no broad whole-project disabling.

Required frontend checks after bootstrap, within frontend/: `npm ci`, `npm run typecheck`, `npm run lint`, `npm run format:check`, `npm run test -- --run`, `npm run build`, `npm run test:e2e`. Foundation must define these scripts. Use `tsc --noEmit` with strict, noUncheckedIndexedAccess and exactOptionalPropertyTypes; ESLint with typescript-eslint and React hooks rules; Prettier for formatting; Vitest/Testing Library for local behavior and Playwright Chromium for browser journeys. Record actual browser versions; other desktop engines may be checked for compatibility but are not silently certified. No additional production OS/installer support claim is selected by using Chromium for automation.

ARCHV import/effect checks belong to pytest and the scope's lint rules, with allowed dependencies traced to DEP-*; forbid framework/storage/vendor imports inward and provider/latest calls from replay panels. A syntactic parameter check cannot prove historical boundedness. UIA11Y checks require keyboard/focus/reflow observation, beyond lint or static SVGs. Test only relevant properties per brief; no duplicate arithmetic E2E suite, blanket coverage target, arbitrary test sleeps or network-required default tests. Controlled fixtures never certify provider/session/finality access.

### Configuration and diagnostics: IS-OPS-001

Service configuration declares confined read and owned storage/export roots, runtime limits and provider-independent settings. Reject invalid configuration before acquisition or mutation; do not guess a valid source root from a manifest. Keep secret material in service-only launch configuration supplied by the user/integration environment; do not prescribe a credential-entry UI or provider SDK before DEFER-001. Do not publish secrets via frontend environment variables, errors or generated schemas.

Use stdlib logging with structured JSONL rotation and monotonic phase timings. Opaque operation/generation identities may correlate LOG/TRACE records, never metric dimensions. Exclude raw provider payloads, credentials/capabilities, private captured identities, arrays and complete financial histories. Persist semantic AUD facts with owning state, independently of diagnostic retention. Local status UI consumes explicit normalized outcomes rather than log messages.

Approved initial diagnostic budget: maximum 10 MiB current log plus four rotated files, oldest first; bounded diagnostic events at most 16 KiB each. Truncate/drop oversized diagnostic fields with an explicit marker; never truncate semantic retained evidence. This is a tunable engineering resource budget, not a provider deadline or retention limit on market/run data. Publish dropped-event/rotation counts locally. Before any timed scheduler/provider behavior, its brief must supply finite validated bounds, cancellation, provider-feedback handling and performance evidence under DEFER-006. Staleness/session thresholds remain unresolved; no receipt means unknown freshness rather than closure.

**Enforcement:** configuration rejection, secret-sentinel exclusion, log-rotation/size tests, bounded metric labels, and measurement linking MET-001–005/TRACE-001–004 to DIAG-001–009. No remote telemetry or market-alert subsystem is introduced.

## 4. Capability Registry & Dependency Policy

All mechanisms in this registry are approved and active standards. Registry membership specifies the required foundation; it does not claim that a package has been installed or its implementation has passed verification.

| Capability | Canonical/default mechanism | Scope | Strength | Standard / state |
|---|---|---|---|---|
| Application host | CPython 3.14, FastAPI/Pydantic 2/Uvicorn | backend/ | REQUIRED | IS-RUN-001 / approved G6 |
| UI controls/build | React 19, TS 6, Vite 8, Node 24 | frontend/ | REQUIRED | IS-UI-001 / approved G6 |
| Presentation styling | CSS Modules/custom properties; no component theme library | frontend/ | REQUIRED | IS-UI-001 / approved G6 |
| Plot rendering | TradingView Lightweight Charts (`lightweight-charts`, 5.2.x API line), adapter-owned custom series/primitives and semantic DOM controls | frontend/ | REQUIRED | IS-UI-002 / user-selected G6-DEC-004; bootstrap pending |
| Wire contracts | OpenAPI, openapi-typescript, native fetch/WebSocket | Transport | REQUIRED | IS-COM-001 / approved G6 |
| Metadata/publication | sqlite3, ordered SQL migrations | backend/ retention | REQUIRED | IS-STORE-001 / approved G6 |
| Parquet evidence | PyArrow, immutable owned files | backend/ storage edge | REQUIRED | IS-STORE-001 / approved G6 |
| Exact monetary representation | stdlib Decimal; domain-owned context | backend/ | REQUIRED | IS-NUM-001 / approved G6 |
| Dependency installs | uv frozen lock; npm ci | Per environment | REQUIRED | IS-PKG-001 / approved G6 |
| Verification | Toolchain in Section 3, mapped TF/ARCHV/AUDV/UIV evidence | Application | REQUIRED | IS-QA-001 / approved G6 |
| Diagnostics | stdlib structured logging/local phase timings | Application | REQUIRED | IS-OPS-001 / approved G6 |

Reuse accepted capabilities; do not add competitors for local convenience. Introduce only present-needed dependencies, pin them, document capability/owner/license and blast radius, and include verification. Record reusable slice-local additions as STANDARDIZATION_CANDIDATE in the implementation ledger. A competing project platform or high-impact policy returns to G6. Never treat an approved but uninstalled package as an already implemented capability.

## 5. Deferred Capabilities and Scoped Prerequisites

| ID / classification | Capability | Why deferred / promotion trigger | Owner / effect |
|---|---|---|---|
| IS-DEF-001 / DEFERRED_CAPABILITY / DEFAULT | External completed-run import/viewer | Outside v1; explicit requirements/architecture/UI approval needed first | No library, parser or product adapter selected; existing contract authoring tools remain separate |
| IS-DEF-002 / DEFERRED_CAPABILITY / DEFAULT | Automatic missing-tick download, extra slippage, scripting, market alerts, volume profiles | Explicit approved future feature scope | No packages selected |
| IS-DEF-003 / DEFERRED_CAPABILITY / DEFAULT | Cloud synchronization, remote telemetry, accounts/tenancy, distributed work queue | A changed execution/authority requirement | No packages selected |
| IS-DEF-004 / DEFERRED_CAPABILITY / DEFAULT | Native wrapper/installers and mobile/touch | Explicit distribution/input requirement beyond source-based desktop baseline | No packages selected |
| IS-DEF-005 / DEFERRED_CAPABILITY / DEFAULT | Additional analytical query engine, GPU renderer, client state platform, binary transport | Measured bottleneck/complexity that accepted mechanisms cannot address within P3 | Review affected IS decision before choosing packages; none selected |

The following are **required v1 work with unresolved prerequisites**, not DEFERRED_CAPABILITY exclusions:

- DEFER-001/002: actual protected live-account SDK/API/entitlement, sessions, publication/finality and applicable historical FX evidence. Integration discovery selects the actual mechanism; no guessed Java bridge, demo provider or successful live claim.
- DEFER-003/004: study/tool/step/export conventions and monetary precision/valuation. Domain/calculation owner supplies scoped conventions and independent examples before affected briefing.
- DEFER-005 and UIADV-INT-002: UX owns opposite-side activation, direction-specific draft/estimate invalidation, readback and final commitment. Standards cannot choose this behavior or add a universal confirmation. Entry implementation remains unready until the affected UI authority is corrected/reapproved and reviewed.
- UISYN-MOD-004 / UI-IMPL-015: architecture owns Data location preference, validation/publication/catalog-adoption contract. Root confinement and SQLite selection do not resolve adoption semantics. Folder-setting implementation remains blocked.
- DEFER-006: diagnostic budgets are approved above; provider scheduling/timeouts/staleness still require scoped evidence. Do not invent session closure or new SLOs.
- DEFER-007: G6 approval settles the named stack directions only. A foundation brief and actual exclusion/durability/renderer capability evidence remain necessary; no blanket discharge or production-readiness claim.

## 6. Active Scoped UI Realization (`frontend/UI-DEVELOPMENT.md`)

These active rules are realized in repository-root frontend/UI-DEVELOPMENT.md. UI_DERIVED rules preserve existing design; IMPLEMENTATION_DERIVED rules realize approved IS decisions; APPROVED_PROPOSAL identifies UIS-DEC-001/002 accepted at G6. Scope is frontend/ only, with no separate guides per component folder. Both this traceability summary and the scoped guide must be updated coherently when an approved standard evolves.

| Rule | Classification / sources | Operational requirement and verification |
|---|---|---|
| UIS-REAL-001 | UI_DERIVED: UI-IMPL-002/016; UIS-PAT-006–013; UIV-STRUCT-001 | Preserve central chart, left drawing strip, top controls, right rail/drawers, scoped docks, range/calendar strip and floating Settings/Go to/replay capsule. Side panels start below the top toolbar and end above status chrome; bodies scroll inside those bounds. Future bundle launcher stays disabled. Verify all implemented view/state compositions against approved UI-ART entries. |
| UIS-REAL-002 | IMPLEMENTATION_DERIVED: IS-UI-001/002; UI-FREEDOM-001/004 | Shared controls own semantics, focus and styling; feature-local composition owns task assembly. Renderer only maps coordinates/presentation, not domain decisions. Reuse shared state/error/target presentations without merging independent conditions into one global status. |
| UIS-REAL-003 | UI_DERIVED: UI-IMPL-007/012/014; VIS-TOKEN-001–008, VIS revision 7 overrides | Consume semantic typography, colors, spacing, density, edge and motion roles. Exact light/dark neutrals, green/red candles/darker Bid edges and Buy/Sell palette follow the latest canonical values. Distinct financial/action/status/focus roles remain distinct tokens even when values coincide. UIV-VIS-001/002 compare actual roles in both themes. |
| UIS-REAL-004 | APPROVED_PROPOSAL: UIS-DEC-001; IS-UI-001; user-selected IS-UI-002 | Central CSS custom-property definitions map canonical VIS IDs to runtime role names; Lightweight Charts options/custom series/primitives and any SVG overlays read the same resolved roles. Raw color/spacing/type/radius/motion design literals are prohibited outside that map. Approved layout/financial geometry, dimensionless calculations, DPR scaling, zero and structural 100% are not substitute visual tokens; document their source. CSS Modules encapsulate selectors; no global feature overrides or new component-theme framework. |
| UIS-REAL-005 | UI_DERIVED: UI-IMPL-003/004; UIV-STATE-001–003; UIS-STATE-001–064 | Render loading, empty/absent, invalid, warm-up, error, stale, UNCERTAIN, conflict and restricted states from explicit contextual outcomes. Preserve correctly labelled prior views. Separate accepted waiting, triggered, whole execution, working version and acknowledged retained version. No fabricated zero, optimistic fill or false save success. |
| UIS-REAL-006 | UI_DERIVED: UI-IMPL-004/006; WF-ANN; UID-002/004/005 | Pending submission 027 retains original run/request/boundary/terms and a blocking reason; evaluation 092 is distinct. Failed save 015 uses error cues and retention-only retry; unknown publication 077 uses uncertainty and blocks progression/mutation pending reconciliation, unlike resolved 037. Test compound states rather than one flag at a time. |
| UIS-REAL-007 | UI_DERIVED: IF-JRN-002/007–010; UIR-ERR-001; UI-IMPL-005/006 | Keep draft and committed values separate. Validate using declared field/commit rules, associate errors with named fields and focus the relevant invalid context. Invalid edits preserve previous valid terms; superseded estimates are non-actionable. Exact target/version/remainder/units/risk and consequence remain co-present with actions. No unapproved opposite-side behavior or numerical bounds; UIADV-INT-002 and DEFER-003/004 gate affected work. |
| UIS-REAL-008 | UI_DERIVED: IF-CONF-001–003; UI-IMPL-005/008; IF-A11Y | Confirm destructive operation-specific scope, destination/replacement/discarded suffix and drawings independence; cancel preserves work. Changed versions require renewed review. A floating surface is not automatically modal: trap focus only for the approved modal interaction, restore invoke/surviving-context focus, and retain keyboard access to nonmodal task surfaces. No new confirmation step. |
| UIS-REAL-009 | UI_DERIVED: UIR-A11Y-001–006; VIS-A11Y-001–005; UIV-A11Y-001–003 | Use semantic HTML before ARIA, names and pressed/selected/disabled semantics with actual matching activation guards. Keep blocked reasons discoverable, focus independently visible, primary tasks keyboard-completable and drawings editable through numeric financial anchors/brush points. Verify both themes, non-color cues, actual contrast and reduced motion; optional animation cannot change replay order or processing. |
| UIS-REAL-010 | UI_DERIVED: UI-IMPL-009/016; UIS-ADAPT-001–006; UIV-ADAPT-001 | Preserve target/terms/reasons/actions at 1280×800 CSS baseline and enlargement/reflow. Panel bodies scroll while actions remain reachable. Do not shrink critical text to reproduce an SVG or infer a mandatory 640px/mobile breakpoint. Test zoom, two charts, long names/errors and the approved dock variants. |
| UIS-REAL-011 | UI_DERIVED: UI-IMPL-013/014; VIS-DATA-001–010; UIV-INT-003/DATA-003/VIS-002 | Independent Bid/Ask visibility does not select calculation basis, executable side or replay cursor. Both visible uses filled Bid-left / hollow Ask-right candles and side-specific volumes in one real bucket; both hidden preserves axes/drawings/named calculation context. Separate labelled OHLCV/absence reasons and direction ticks/numerics remain. |
| UIS-REAL-012 | UI_DERIVED: UI-IMPL-010/011/015; UIV-CONT-001/ACC-001/JRN-015 | Pin export source, retain boundary/units/assumptions/absence labels, reconcile unknown output, and exclude secrets/private evidence. Implement Data location only after its architecture contract; saved-run originals never silently follow a folder edit. |
| UIS-REAL-013 | APPROVED_PROPOSAL: UIS-DEC-002; IMPLEMENTATION_DERIVED IS-QA-001; UI-IMPL-011 | Prefer role/name semantic selectors; add stable data-testid only for otherwise ambiguous chart/layer targets. Fixture manifests identify relevant UI-ART, UIV and context versions; control async barriers without arbitrary sleeps. Collect runtime evidence for the implemented subset across both themes and material states. Do not conflate static artifact checks, pixel similarity, keyboard proof, financial truth, durability or P3. |

UIS-DEC-001 and UIS-DEC-002 are the UI engineering proposals approved at G6; derived rules do not reopen approved UX/visual direction. No UI deviations are approved. Modal implementation may use the WAI APG as supplementary guidance without overriding the dossier's nonmodal surfaces.

## 7. Active Scope Roots and Coding Profiles

Scope paths below are repository-relative; all four roots now contain ACTIVE DEVELOPMENT.md guides and cumulative AGENTS.md pointers. frontend/ also contains ACTIVE UI-DEVELOPMENT.md. Only governance files exist in the new application roots. Maintained source receives guidance; generated HTML/SVG/JSON, screenshots, evidence, caches and packaged examples are not independent coding scopes. Existing generators' embedded asset strings remain governed at their generator root, not by a new guide in every output directory.

| Scope root | Maintained language/version | Exactly one primary profile per language | Continuity | Approved enforcement / exception |
|---|---|---|---|---|
| backend/ (new) | Python 3.14 | CPython PEP 8 | LOW: no application code | Ruff 88-column deviation; strict basedpyright; pytest |
| backend/ migrations (same root) | SQLite SQL, runtime version recorded at bootstrap | Project SQLite SQL profile, syntax authority SQLite SQL language reference | LOW: no migrations | Uppercase keywords, snake_case identifiers, parameterized data, four spaces; migration integration tests; no separate SQL scope/formatter |
| frontend/ (new) | TypeScript 6 / TSX, React 19 | Google TypeScript Style Guide | LOW: no application code | TypeScript strict + ESLint; Prettier 100-column/two-space/single-quote/semicolon profile; JSX functional components and hooks are explicit React ecosystem adaptations |
| frontend/ (same root) | Authored HTML / CSS Modules, modern browser baseline | Google HTML/CSS Style Guide, one profile for each language | LOW: no application code | Prettier controls layout; explicit HTML closing tags, React className/JSX syntax, CSS Module local naming and semantic tokens supersede conflicting guide examples |
| analysis/tradingview/ (existing) | Python 3.14 validation environment; do not raise each script's minimum syntax without need | CPython PEP 8 | MEDIUM: mostly four-space/snake_case; long lines and quote/import variation in generators | Preserve current offline regeneration, py_compile and artifact checkers. Apply profile to touched/new code; no mass reformat, whole-scope strict typing retrofit or generated SVG hash change |
| contract-v1.0.0/ (existing reference tools) | Python 3.14 validation environment; existing PyArrow edge | CPython PEP 8 | LOW: sampled dataclass/type/snake_case style is compatible | Preserve pytest conformance semantics/immutable example identities; touched code only; no implicit integration into product runtime |

### Python operational profile (active scoped guides)

Use four-space indentation, snake_case functions/modules/variables, PascalCase classes and UPPER_SNAKE_CASE constants. Group standard-library, third-party and local imports; avoid wildcard imports. Use pathlib for controlled paths. Comments/docstrings explain contracts and reasons. New backend interfaces are typed, with unknown data validated at adapters; keep framework models outside core. Expected invalid/prerequisite outcomes are explicit results, unexpected errors retain safe causal context, and transport errors are sanitized. Tests name the protected observable rule and use independent expected results, temporary owned paths and deterministic barriers.

Project clarification: Ruff formatting at 88 columns replaces PEP 8's usual line target for new backend code. Existing authoring scopes retain surrounding quote/layout conventions in untouched regions; formatter adoption must not regenerate approved visual bytes incidentally. Original root AGENTS.md deterministic/offline/standard-library rules remain applicable to the dossier tools; FastAPI/PyArrow exceptions belong to their approved application adapters, not extractors. These scoped distinctions and the stated formatting/JSX/SQLite adaptations were approved under G6-DEC-009.

### TypeScript/TSX operational profile

Use ES modules, named exports, camelCase values/functions and PascalCase types/components; use type-only imports where appropriate. Prefer unknown to any at untrusted boundaries and narrow before use. Avoid non-null assertions and broad lint suppression; represent material outcome variants explicitly. Keep semantic identities/units distinct from display strings and mutable renderer handles. Hooks follow React's rules; effects subscribe/clean up against their context rather than duplicate canonical state. Test behavior through accessible controls; inject async completion to exercise stale results.

Project adaptations: Prettier controls mechanical formatting; React function components/JSX and CSS Modules are permitted. Generated transport declarations are excluded from manual style edits and regenerated from the canonical schema. Native browser number/date conversion cannot authorize financial rounding or truncate original timestamp precision.

### HTML/CSS and SQL operational profile

HTML uses semantic elements, explicit labels, valid nesting, explicit closing tags and safe text insertion. CSS uses two-space formatting, scoped classes and semantic custom properties; root token definitions are the only approved visual-literal registry. No inline captured markup or output-directory style edits. These rules adapt the primary Google HTML/CSS profile to JSX, locally served assets and canonical VIS roles.

SQL uses SQLite-supported syntax, uppercase keywords, snake_case identifiers, explicit columns and bound values. Migrations are immutable after accepted use; a subsequent migration evolves persisted representation. Test supported upgrade paths and failure preservation. Domain invariants, concurrency and filesystem durability are not inferred from DDL success. This is a project-authored SQLite profile, not a claim of an official SQLite formatting standard.

## 8. Primary Research Record

Official/maintainer sources consulted 21/10/2026. Sources describe language/tool capabilities; architecture and UI sources above determine this project's requirements. No latest-version or compatibility claim replaces frozen installation evidence.

| Source | Relevance / limit |
|---|---|
| [Python supported versions](https://devguide.python.org/versions/) | Python 3.14 is a supported bugfix line; choose it rather than infer a runtime from old notes |
| [PEP 8](https://peps.python.org/pep-0008/) | Primary Python profile; project continuity and explicit formatter deviations retained |
| [Decimal, Python 3.14](https://docs.python.org/3.14/library/decimal.html) | Decimal representation/context mechanisms; no project rounding convention supplied |
| [Apache Arrow Python installation](https://arrow.apache.org/docs/python/install.html) | Documents Python 3.14 compatibility; wheels/actual platform still need verification |
| [Node release working group](https://github.com/nodejs/Release) | Node 24 support line; 24 is in maintenance LTS at the review date, not active LTS |
| [FastAPI manual deployment](https://fastapi.tiangolo.com/deployment/manually/) | ASGI/Uvicorn realization; single-authority constraints come from this architecture |
| [React versions](https://react.dev/versions), [React TypeScript guidance](https://react.dev/learn/typescript) | React 19 and TSX adaptation |
| [TypeScript 6.0 release notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html), [strict](https://www.typescriptlang.org/tsconfig/strict), [indexed access](https://www.typescriptlang.org/tsconfig/noUncheckedIndexedAccess.html) | Compiler baseline and explicit checks |
| [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) | Primary TS style profile, with project/React deviations stated above |
| [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html) | Primary authored markup/styling profile, adapted to semantic tokens and JSX |
| [Vite guide](https://vite.dev/guide/) | Local development/build and static asset distribution; exact pins at bootstrap |
| [WHATWG Canvas](https://html.spec.whatwg.org/multipage/canvas.html) | Canvas substrate for library/custom drawing code; semantic DOM equivalents still required |
| [Lightweight Charts getting started](https://tradingview.github.io/lightweight-charts/docs), [NOTICE](https://github.com/tradingview/lightweight-charts/blob/master/NOTICE) | Documented 5.2 browser package, TypeScript declarations and creator attribution; preserve exact installed-release notices |
| [Lightweight Charts custom series](https://tradingview.github.io/lightweight-charts/docs/plugins/custom_series), [primitives](https://tradingview.github.io/lightweight-charts/docs/plugins/series-primitives), [panes](https://tradingview.github.io/lightweight-charts/tutorials/how_to/panes), [UTC timestamps](https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/UTCTimestamp) | Extension mechanisms and presentation-time mapping; approved dual-quote rendering and original-value retention still need implementation evidence |
| [SQLite atomic commit](https://www.sqlite.org/atomiccommit.html), [SQL language reference](https://www.sqlite.org/lang.html) | Commit assumptions and actual dialect, not cross-file atomicity or a style guide |
| [SQLite WAL](https://www.sqlite.org/wal.html) | Filesystem/shared-memory restrictions; synced paths are not assumed safe active stores |
| [uv locking/sync](https://docs.astral.sh/uv/concepts/projects/sync/), [Ruff formatter](https://docs.astral.sh/ruff/formatter/), [basedpyright configuration](https://docs.basedpyright.com/latest/configuration/config-files/) | Frozen installs, formatter/linter alignment and scoped type configuration |
| [openapi-typescript](https://openapi-ts.dev/introduction) | Local schema-to-type generation, not runtime validation |
| [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html), [Playwright assertions](https://playwright.dev/docs/test-assertions) | Controlled fixture and browser evidence mechanisms |
| [WAI modal-dialog APG](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) | Supplementary implementation guidance for actual modal surfaces only |

## 9. Approved Exceptions & Known Drift

| Classification / standard | Scope | Evidence / reason | Disposition |
|---|---|---|---|
| Approved profile adaptations | Scoped guides | Ruff 88-column backend profile; Prettier/JSX/CSS Modules adaptations; project-authored SQLite profile and existing-tool continuity | Approved G6-DEC-009; no additional deviation |
| Existing repository continuity | analysis/tradingview/ | Long generator lines, embedded styles and historical formatting | Preserve untouched source/output; approved touched-code profile does not rewrite approved SVGs |
| Reference-tool isolation | contract-v1.0.0/ | README references absent predecessor root paths/venv; standalone contract authoring remains separate | Do not claim those commands pass or repair the reference package in this standards task |
| Coordinator summary reconciled | project-state.md | UI review revision 3 and G6 approval recorded | Historical reviews and current design authorities preserved |
| No application verification | backend/, frontend/ | Source roots contain guides/routing only; selected dependencies are not installed | Future enforcement commands are specifications, not verification results |

## 10. Approved Gate G6 Decision Record

All ten decisions are approved. The chart engine was selected on 21 October 2026; on 22 October 2026 the user explicitly approved all nine remaining open rows in revision 2. No open Gate G6 decision remains. The following table preserves the evaluated alternatives and approved recommendations as the approval record.

| Decision ID | Layer | Scope | Candidates & trade-offs | Recommendation | Continuity / tooling impact | Project decision |
|---|---|---|---|---|---|---|
| G6-DEC-001 | FOUNDATION | Runtime/topology | Local Python service: exact arithmetic/Parquet ecosystem; Node service: one source language but separate exact/data choices; native wrapper: extra build/platform burden | IS-FND-002 / IS-RUN-001: Python 3.14 + FastAPI/Pydantic 2/Uvicorn, one authoritative worker and desktop browser | LOW application continuity; installs a Python runtime stack; real ownership/performance proof required | APPROVED: all remaining decisions, 22 October 2026 |
| G6-DEC-002 | FOUNDATION | Transport/precision | Same-origin HTTP+WS/JSON: straightforward diagnostics; native IPC: wrapper coupling; binary transport: more decoding/schema work | IS-COM-001 / IS-NUM-001: HTTP/WS, generated OpenAPI TS types, lossless integer/decimal wire forms and backend Decimal | Adds openapi-typescript; no financial precision/rounding defaults; schema and foreign-origin tests required | APPROVED: all remaining decisions, 22 October 2026 |
| G6-DEC-003 | FOUNDATION | Controls/styles | React/TS: explicit component ecosystem; another reactive framework: viable but no existing continuity; themed component suite: possible visual override burden | IS-UI-001: React 19 / TS 6 / Vite 8, hooks/reducers, CSS Modules/custom properties | LOW; one frontend package, no competing global state/theme library | APPROVED: all remaining decisions, 22 October 2026 |
| G6-DEC-004 | FOUNDATION | Chart adapter | Prior standalone Canvas recommendation superseded by explicit user selection; library scales/panes/navigation reduce generic work while custom quote/drawing/accessibility behavior remains application work | IS-UI-002: TradingView Lightweight Charts REQUIRED (`lightweight-charts`, documented 5.2.x API line), adapter/custom series/primitives and semantic DOM equivalents | LOW existing continuity; exact package pin, local bundling/notices, dual-quote/export/keyboard proof and measured P3 required at bootstrap | APPROVED: user explicitly requests TradingView Lightweight Charts, 21 October 2026 |
| G6-DEC-005 | FOUNDATION | Storage/migrations | SQLite+immutable Parquet: local metadata transactions plus explicit file publication; file-only references: more bespoke coordination; remote DB: unnecessary operational cost | IS-STORE-001: stdlib sqlite3, PyArrow/owned files, ordered SQL migrations, tested local active store outside synced checkout | Adds PyArrow; requires actual crash/exclusion/race tests; no physical schema or folder-adoption semantics selected | APPROVED: all remaining decisions, 22 October 2026 |
| G6-DEC-006 | FOUNDATION | Dependencies/distribution | uv/npm frozen locks: distinct ecosystems with reproducibility; loose requirements: weaker reproducibility; native installer/container: extra packaging | IS-PKG-001 / IS-BUILD-001: uv + npm, Node 24 tooling, locked source-based local release and local assets | Existing dossier commands remain usable; exact version pins/build record at bootstrap | APPROVED: all remaining decisions, 22 October 2026 |
| G6-DEC-007 | FOUNDATION | Verification/code quality | Narrow domain/workflow/storage/UI checks: evidence matched to risk; broad E2E-only suite: weak failure localization | IS-QA-001 toolchain and checks from Section 3 | Adds Python/TS dev tools; retain existing authoring checks, no mass typing/format retrofit | APPROVED: all remaining decisions, 22 October 2026 |
| G6-DEC-008 | FOUNDATION | Config/diagnostics | Local bounded structured diagnostics: inspectable with limited footprint; remote telemetry: unnecessary service/data exposure | IS-OPS-001 with approved 10 MiB × five-file log budget and 16 KiB diagnostic event limit | Tunable resource budget only; provider timing/staleness thresholds stay open | APPROVED: all remaining decisions, 22 October 2026 |
| G6-DEC-009 | CODING_PROFILE | Four coherent roots | Scope-local guides: preserve authoring/product contexts; root-wide mixed profile: imprecise applicability | IS-SCOPE-001 and all Section 7 language profiles, explicit formatter/JSX/SQLite deviations and cumulative routing in Section 11 | LOW new scopes, MEDIUM dossier Python, LOW contract Python; touched code only, no nested guide proliferation | APPROVED: all remaining decisions, 22 October 2026 |
| G6-DEC-010 | UI_STANDARDS | frontend/ | Shared semantic token map/selectors: consistent testable realization; local literals/DOM-position selectors: drifting role/state behavior | UIS-DEC-001/002 and traceable Section 6 realization rules | No approved flow/token changes; INT-002 and Data location remain affected-scope prerequisites | APPROVED: all remaining decisions, 22 October 2026 |

## 11. Activation Record and Foundation Handoff

- Gate G6 is SATISFIED for all ten decisions; this revision activates the exact approved choices and profile adaptations.
- ACTIVE coding guides exist at backend/DEVELOPMENT.md, frontend/DEVELOPMENT.md, analysis/tradingview/DEVELOPMENT.md and contract-v1.0.0/DEVELOPMENT.md. The frontend UI realization guide is frontend/UI-DEVELOPMENT.md.
- Each scope has one colocated AGENTS.md pointer. Root AGENTS.md preserves its dossier guidance and adds cumulative routing and explicit application-scope applicability. No ordinary component/model/output directory receives an extra guide.
- The original approved revision-2 source digest, user approval statements, upstream authority identities and activated artifact digests are recorded in standards-approval.json. Research dates in Section 8 remain the actual 21/10/2026 consultation date; activation does not claim a new research round.
- Standards activation creates no production source, package manifest, dependency lock, implementation brief or implementation-ledger entry. Foundation implementation state remains NOT_STARTED.
- Next: implementation-brief in FOUNDATION mode, using architecture-dossier.md, ui-dossier.md, visual-system.md, these standards and applicable scoped guides. implementation-ledger.md is absent; supply that fact rather than fabricate accepted slices. A brief must constrain bootstrap work and identify actual exclusion/durability/renderer verification before coding.
- Preserve UIADV-INT-002, UISYN-MOD-004, applicable DEFER-001–007 and ADV-VER-001. The former two prevent affected entry/folder behavior; they do not prevent preparing an unaffected foundation brief. G6 does not waive provider/numerical/platform evidence or authorize behavioral scope expansion.

### Quality-gate assessment

| Gate | Assessment |
|---|---|
| Upstream authority/platform evidence | PASS: architecture review r1 and UI review r3 permit unaffected governance; approved realization preserves FREEDOM-004 and existing semantics |
| Foundation necessity/radius/present need | PASS: Section 2 retains the three candidate tests; deferred capabilities select no speculative packages |
| Classification/strength/activation | PASS: all IS rules have a class, REQUIRED/DEFAULT strength and inherited or explicit approval provenance |
| Scoped UI traceability | PASS: active frontend/UI-DEVELOPMENT.md carries UIS-REAL-001–013 with UI-IMPL/UID/UIV/VIS provenance and explicit scoped prerequisites |
| Coding profiles/research/continuity | PASS: four coherent coding scopes, primary research/access dates, operational rules, LOW/MEDIUM continuity and approved deviations recorded |
| Human approval/cumulative routing | PASS: ten approved G6 decisions; four active coding guides, one UI guide, four minimal scoped pointers and cumulative root routing |
| Implementation/performance/durability | NOT PERFORMED: foundation briefing and actual selected-platform capability proof remain downstream |

### Verification and evidence limits

All maintained dossier Python scripts compile. The viewer regenerates with active standards, and the existing wireframe/mockup checkers verify their unchanged static design artifacts. Local document links, viewer anchors/resources, routing targets, approval rows and source/approval preservation are checked after regeneration. The viewer's only executable script remains its pre-existing authored gallery filter; captured target HTML is never embedded or executed. SHA256SUMS and ZIP contents are regenerated and checked against current bytes using README.txt exclusions.

Browser rendering was unavailable during the preceding proposal review (Chrome disconnected; headless Firefox crashed). This activation validates source/structure, not a rendered, keyboard, runtime accessibility, financial, performance or durability pass. No new browser pass is claimed.

**Handoff signal:** `STANDARDS_READY`; Foundation Sub-State `READY_FOR_FOUNDATION_BOOTSTRAP`.
