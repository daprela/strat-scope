# Architecture Dossier — Dukascopy Chart Workspace and Historical Trading

## 0. Dossier Status & Provenance

- **Revision:** 2 — 19 October 2026; Pass 2 completed after explicit G1 approval.
- **Active Pass:** `PASS_2_RESILIENCE_AND_VERIFICATION`.
- **Readiness Signal:** `IMPLEMENTATION_READY_WITH_NON_BLOCKING_GAPS`.
- **Project Mode:** `GREENFIELD` application design; the existing repository is an evidence/documentation dossier, not an implemented application baseline.
- **Authoritative Upstream Inputs:** [requirements-dossier.md](requirements-dossier.md), revision 14, `CONVERGED_WITH_ACCEPTED_ASSUMPTIONS`; [domain-model.md](domain-model.md), revision 1, `READY_WITH_ACCEPTED_ASSUMPTIONS`. Both reviewed completely.
- **Authority rule:** Requirements govern scope; the domain model governs semantic refinement. Older source-report architectures, stack examples, captured menus and private target endpoints are evidence/proposals only. Chronological UNK references follow the requirements Section 19 resolution register.
- **Blocking Conflicts / Gaps:** None found for boundary design.
- **Important Deferred Items:** ARCH-GAP-01–ARCH-GAP-05 and VGAP-001, isolated by DEFER-001–DEFER-007; Sections 34–35.
- **Human Gate G1:** APPROVED by the user on 19 October 2026: “I approve the boundaries proposed”. Covers revision 1 Parts I–II boundaries/contracts; new Pass 2 mechanisms are architectural proposals, not newly user-confirmed requirements.
- **Implementation readiness:** Architecture complete with scoped prerequisites. No application, live-account connection, data acquisition or integration verification was performed. Affected provider/numerical/UI details and downstream standards/implementation gates remain mandatory.

# PART I: CONTEXT, DRIVERS & DOMAIN BASELINE

## 1. Executive Summary & Problem Scope

Design one local analyst's desktop workspace for ten Dukascopy instruments, exactly M1/M5/M15/H1/H4/D1/W1/MN1, bid-default/ask-selectable bar charts, built-in studies, authored drawings, saved layouts, replay and historical simulated trading. Dukascopy live-account data and M1/H1 historical recovery extend the current market catalog while the application runs. Existing sibling ingestion outputs remain read-only. Acquired/recalculated history is retained in application-owned local files.

The principal authority split is between changing current history, historically available evidence, and each run's retained input basis. A catalog correction may improve current charts/new runs without changing a resumed run. A coherent simulated execution includes price/evidence, quantity, position/protection, commissions and USD effects. A blocked prerequisite prevents that execution rather than creating a partial monetary outcome. Authored annotations remain independent of trading history and survive rewind.

The boundaries below are logical knowledge and contract boundaries within a local application. They do not prescribe separate processes, independently deployed services, frameworks, classes, persistence engines or file layouts. Keep cross-boundary coordination explicit without imposing distributed communication. The local interaction edge, market-data edge and durable-retention capability isolate volatile representations. Deployment and technology choices remain downstream.

Excluded: actual broker orders/balances, margin/liquidation, extra slippage, scripting/Pine, alerts, external completed-run import, hosted sharing, mobile, more than two charts, additional chart periods, automatic missing-tick download and volume profiles. The application's manual backup restore is included and is distinct from external run-bundle import. [FR-26–FR-30, FR-41, FR-55, SEC-07, EVO-05–EVO-07]

## 2. Architectural Drivers (`DRV-*`)

| ID | Driver | Source Requirement / Domain IDs | Architectural Consequence |
|---|---|---|---|
| DRV-001 | Provider-qualified, side-specific, precision-preserving eight-period observations | FR-01–FR-07; BR-01–BR-04; DATA-01–DATA-08; POL-01; INV-01–INV-02 | One market-meaning owner; typed semantic basis travels with every read/result; transport cannot redefine it. |
| DRV-002 | Full dynamically discovered archive, distinct from resident working set | FR-06, FR-36, FR-52; SCALE-01–SCALE-03; EVO-01–EVO-02; TR-19 | Coverage/bounds separate from resident chart data; bounded-range reads and selective detail resolution. No hardcoded earliest date or total-history cap. |
| DRV-003 | Live/history recovery changes current data without changing saved runs or sibling inputs | FR-31–FR-35, FR-43, FR-45; CONS-04, CONS-09, CONS-16; POL-09; INV-04 | Current-catalog reconciliation, retained run basis and external source access have separate authority. |
| DRV-004 | One historical information boundary for every replay panel and decision | FR-09, FR-19–FR-23, FR-53; BR-07, BR-11; POL-03–POL-04; INV-03 | Shared historical-evidence contract and run decision ordering; neither plot cadence nor provider receipt drives execution semantics. |
| DRV-005 | Evidence hierarchy, precise eligibility/pricing and accepted approximations | FR-23, FR-37–FR-40, FR-47–FR-48, FR-51; ASM-01–ASM-02; PRE-02–PRE-08 | Separate evidence availability/resolution, event effectiveness and execution pricing; preserve assumption labels. |
| DRV-006 | Coherent hedged execution and historical USD valuation | FR-38–FR-42, FR-49–FR-50, FR-54; CONS-07, CONS-12, CONS-14; INV-05–INV-09, INV-14 | Execution owns position/protection effects; monetary meaning/sizing owns conversion/fee knowledge; run accepts a complete outcome or an explained block. |
| DRV-007 | Analysis survives rewind; saved state and backups restore coherently | FR-14–FR-17, FR-21–FR-22, FR-44–FR-45, FR-55; CONS-02, CONS-13, CONS-15; INV-12–INV-13 | Authored analysis distinct from run state; retention reports actual saved versions and retains required input evidence. |
| DRV-008 | Sole local writer, untrusted inputs and data-only provider access | AUTH-01–AUTH-03; SEC-01–SEC-07; POL-11–POL-12 | Local authority and protected provider access at explicit trust boundaries; no tenant system or brokerage capability. |
| DRV-009 | Accepted desktop performance and acquisition lifetime | FR-25, FR-34, FR-36, FR-56; SCALE-03–SCALE-05 | Routine chart reads/navigation independent of heavy tick resolution; receipt-to-display path explicit; acquire during app lifetime and catch up at startup/reconnect. |
| DRV-010 | More tick assets, longer histories and future detailed analytics/acquisition | DATA-17; EVO-01–EVO-07 | Discovery by instrument/span; detail contracts isolate local-only v1 evidence from future sources without implementing deferred features. |

## 3. Actors, Assumptions & Open Questions

### Actors

| Actor | Scope / Meaning | Authority / Responsibility | Source |
|---|---|---|---|
| Local analyst / historical simulation user | Same sole local person | Author analysis, configure simulated cash/specifications, make historical decisions, confirm destructive work, backup/restore; one writable tab | AUTH-01–AUTH-03; FR-21, FR-55; POL-11 |
| Existing ingestion process | Independent producer of sibling files | May change its own outputs; never grants this application source-file mutation authority | DATA-01, DATA-08, DATA-16; REL-01 |
| Dukascopy history/live services | External market-data authority | Supply historical M1/H1 and live-account observations/metadata; grant no simulated or actual order-routing authority | Requirements INT-05–INT-06; SEC-07; POL-12 |
| Local application runtime | Supporting lifecycle participant, not a new user role | Acquire while running; catch up at startup/reconnect; retain/recover analyst-owned work | FR-43–FR-44, FR-56; SCALE-05; OPS-03, OPS-06–OPS-07 |

No application tenant hierarchy, remote user, approver or broker execution actor is introduced. Ownership scope in this dossier means the local analyst, layout/instrument, or run, not a tenant ID.

### Assumptions (`ASM-*`)

| ID | Assumption | Upstream Status | Consequence if False |
|---|---|---|---|
| ASM-01 | Unresolved eligible SL/TP chronology after finer stored bars then available local ticks uses labelled stop-first | Explicitly accepted U4; domain Section 14 | True sequence might hit TP first; preserve approximation label. Does not supply missing entry, price or continuity. |
| ASM-02 | Eligible requested quantities fill fully, with eligible bar-limit touch at limit unless a better first eligible gap quote is established | Explicitly accepted U11; domain Section 14 | Actual broker liquidity/path may differ; preserve full-fill/bar-touch labels. Manual partial close is an explicit smaller request. |

Provider access, session/finality and numerical/tool refinements remain ARCH-GAP-01–ARCH-GAP-05. They are not silently accepted assumptions or reasons to omit required capabilities. No fresh high-consequence product ambiguity was found.

## 4. Domain Vocabulary & State Baseline

Use DC-01–DC-21, REL-01–REL-11 and PRE-01–PRE-10 from the domain model without renaming their meaning. A provider-qualified instrument differs from its alias; a side/timeframe/revision identifies a series basis; current history differs from retained run inputs; period completion differs from validation/provider finality. Nanosecond bars and millisecond ticks keep original precision and established occurrence order. Equal displayed timestamps do not prove equal events. Provider volume has unverified units and is not exchange liquidity.

| Semantic family | Authoritative baseline | Boundary treatment |
|---|---|---|
| Discovery, usable evidence, current-history correction and feed recovery | DC-01–DC-09; TR-01–TR-05; INV-01–INV-02, INV-11; HIST-01–HIST-02 | BND-001–BND-004 distinguish meaning, coverage, catalog choice and historical availability. |
| Selection, authored edits, checkpoints and interval sync | DC-10–DC-12, DC-21; TR-06–TR-11; INV-12–INV-13; HIST-07 | BND-005 owns authored work; BND-010 retains coherent selected versions; previews never become saved work. |
| Historical cursor, held events, rewind/restart/resume | DC-13–DC-14; TR-12–TR-20; INV-03–INV-04; HIST-03, HIST-08 | BND-007 owns run continuation and decision boundary; completion of an uncommitted prerequisite is not general input replacement. |
| Instructions, triggers, fills and independent exposure | DC-15–DC-18; TR-21–TR-30; INV-05–INV-10, INV-14; HIST-04–HIST-06 | BND-008 owns instruction/exposure effects; BND-009 supplies monetary decisions; coverage exhaustion never forces liquidation. |
| Monetary/specification/calculation meaning | DC-11, DC-19–DC-20; POL-06–POL-08, POL-10 | BND-009 owns unit/fee/conversion/quantity meaning; BND-006 owns study conventions. Neither invents unverified contract values. |

Historical facts survive ordinary catalog updates, position closure and replay exit. Confirmed rewind deliberately discards later active-run actions and their dependent fills/fees/account facts and reconstructs the retained prefix. It does not require permanent audit copies or automatic branches. Forward terminal order/position conditions do not prohibit reconstruction of earlier state. [Domain Sections 5 and 10; FR-21, BR-17]

## 5. Business Outcome to Responsibility Mapping

Every row includes semantic reads, changes, supporting effects and authority obligations. Detailed responsibility IDs follow in Section 6.

| Outcome / Use Case | Required Decisions | Semantic State Changes | Supporting Responsibilities | Source IDs |
|---|---|---|---|---|
| BO-01/BO-02: discover/select/navigate honest history | Qualified identity, supported side/period, usable bounds, matching requested basis | Adopt only matching valid selection; keep previous chart on failure | Read all-history bounds/ranges and metadata; derive studies; adapt labelled output; restrict untrusted input paths (RESP-001–RESP-004, RESP-008–RESP-011, RESP-024, RESP-026–RESP-027) | FR-01–FR-10, FR-52; OP-01/OP-03; INV-01–INV-02 |
| BO-03: preserve authored analysis | Valid edit versus preview/cancel, scope, writer/destructive authority | Commit/reverse layout/study/drawing edits independently of trading | Retain coherent analysis version; expose saving/error; local image export with basis, no secrets (RESP-009–RESP-010, RESP-020–RESP-024, RESP-026–RESP-027) | FR-12–FR-18, FR-44, FR-55; OP-04/OP-05/OP-13/OP-14 |
| BO-04: explore without future information | Historical availability, existing-order effectiveness, continuity before advancement | Advance coherent run/cursor; confirmed rewind reconstructs prefix | Read retained inputs, bound all panels/studies/reports, request checkpoint, retain original blocked-event context (RESP-007–RESP-008, RESP-011–RESP-014, RESP-019–RESP-021, RESP-024, RESP-026) | FR-19–FR-23, FR-42, FR-46, FR-53; OP-06/OP-11/OP-12 |
| BO-05: extend to current data | Data-only access, usable versus missing/closed interval, final/current precedence | Extend/finalize affected current history; retain source provenance | Acquire M1/H1/live facts, read session evidence, retain owned files, show partial recovery/failure; never mutate sibling/run originals (RESP-001–RESP-007, RESP-022–RESP-023, RESP-025–RESP-028) | FR-31–FR-35, FR-43, FR-56; OP-02; POL-02/POL-09/POL-12 |
| BO-06: reproducible historical practice | Eligible event/price/quantity, independent target, evidence hierarchy, complete valuation | Accept action; apply whole fill/protection/fee/USD effect or hold original event | Read retained bars/ticks/FX/specifications, record labelled result and checkpoint, present own-run report; no brokerage effect (RESP-007–RESP-008, RESP-012–RESP-023, RESP-026) | FR-27, FR-29, FR-37–FR-50, FR-54; OP-07–OP-11; INV-03–INV-10, INV-14 |

# PART II: RESPONSIBILITY BOUNDARIES, WORKFLOWS, DEPENDENCIES & CONTRACTS (PASS 1)

## 6. Responsibility Inventory (`RESP-*`) & Concern Classification

Each responsibility has one primary concern; shared policy ownership is specified in Section 7. Categories retain the protocol's distinctions even when obligations share a boundary.

| ID | Responsibility (Semantic Obligation) | Purpose | Primary Concern | Source IDs |
|---|---|---|---|---|
| RESP-001 | Establish provider-qualified instrument, side, period, precision and bucket meaning | Consistent interpretation | Domain / Business Policy | POL-01; INV-01–INV-02; DATA-07 |
| RESP-002 | Establish usable intervals, actual bounds and justified closure/gap classifications | Honest eligibility | Domain / Business Policy | POL-02; INV-11; OP-01 |
| RESP-003 | Obtain coverage and observation facts across the available archive | Full-history access independent of resident ranges | Query / Read | FR-01–FR-02, FR-06, FR-52; DATA-01–DATA-08 |
| RESP-004 | Accept only established current-history revisions and affected supported-period derivatives | Final-over-provisional current history | Semantic State Change | TR-02–TR-04; OP-02; CONS-09 |
| RESP-005 | Coordinate discovery, recovery and finalization for the current catalog | Preserve readable history during progress/failure | Application Orchestration | FR-32–FR-35, FR-43; OPS-06–OPS-07 |
| RESP-006 | Determine supplied UTC aggregation and lineage for recovered/affected bars | Preserve stored history and side semantics | Domain / Business Policy | BR-02–BR-03, BR-08; REL-03; INV-02 |
| RESP-007 | Determine historically available evidence and distinguish observed order from unresolved protective chronology | No future leakage or invented path | Domain / Business Policy | POL-03; PRE-07; ASM-01 |
| RESP-008 | Obtain bounded historical views and selective finer-bar/local-tick evidence | Same information limit for panels and simulation | Query / Read | FR-20, FR-23, FR-36; DATA-17; INV-03 |
| RESP-009 | Adopt a matching chart selection and valid arrangement/interval synchronization | Coherent one/two-chart analysis | Semantic State Change | TR-06/TR-11; OP-03; PRE-01; CONS-01/CONS-03 |
| RESP-010 | Commit, cancel or reverse valid authored settings/studies/drawings within layout/instrument scope | Independent reusable analysis | Semantic State Change | TR-07–TR-08; OP-04–OP-05; PRE-09; INV-13 |
| RESP-011 | Derive declared study outputs and unavailable/warm-up meaning | Reproducible bounded calculations | Query / Read | FR-08, FR-11–FR-12; POL-10; OP-04 |
| RESP-012 | Determine decision effectiveness and established event order | Existing eligible orders before new decisions | Domain / Business Policy | POL-04; FR-40/FR-53; CONS-10 |
| RESP-013 | Coordinate run start, advance, seek, rewind/restart and resume | One coherent historical exercise | Application Orchestration | TR-12–TR-20; OP-06/OP-11–OP-13 |
| RESP-014 | Maintain retained run basis, actions, decision boundary and blocked original-event context | Preserve run continuity | Semantic State Change | POL-09; INV-04; HIST-03/HIST-08; DATA-18 |
| RESP-015 | Accept or reject historical instructions and permitted changes with explicit targets | Valid pending instructions | Semantic State Change | TR-21–TR-24; OP-07; PRE-03/PRE-06/PRE-08 |
| RESP-016 | Determine executable side/price, protection chronology and requested full-fill effect | Honest simulation outcome | Domain / Business Policy | POL-05; TR-25–TR-26; INV-08/INV-10/INV-14; ASM-01–ASM-02 |
| RESP-017 | Apply a completely valued execution to its independent exposure, protection and USD account | Coherent quantity and money | Semantic State Change | TR-25/TR-27–TR-30; OP-09–OP-10; INV-05–INV-07/INV-09 |
| RESP-018 | Determine instrument monetary meaning, historical USD conversion, fees and permitted planned quantity | One valuation/sizing policy | Domain / Business Policy | POL-06–POL-08; PRE-04–PRE-06; OP-08; FR-41/FR-49–FR-50/FR-54 |
| RESP-019 | Interpret own-run evidence, trades and metrics without future disclosure | Reproducible reports | Query / Read | FR-20, FR-29, FR-37; OP-14; HIST-04–HIST-06 |
| RESP-020 | Coordinate autosave, coherent recovery, manual backup and replacement restore | Recover analyst-owned work | Application Orchestration | OP-13; TR-09–TR-10; FR-44/FR-55; OPS-03 |
| RESP-021 | Retain and retrieve coherent work versions and original run-input evidence | Durable, reproducible saved claims | Infrastructure-Facing | INV-04/INV-12; DATA-18; CONS-02/CONS-15 |
| RESP-022 | Retain application-owned acquisitions and read sibling evidence without altering it | Persistent local reuse within write authority | Infrastructure-Facing | FR-43; DATA-08/DATA-16; AUTH-02 |
| RESP-023 | Retain result provenance, decision/effect facts and approximation labels with their owning state | Durable evidence, distinct from debug logs | Security / Audit | FR-29/FR-37/FR-45; HIST-01–HIST-08; INV-10; SEC-04 |
| RESP-024 | Translate desktop commands and present/export coherent labelled semantic outcomes | Chart/navigation/dialog/image/report interaction | Transport / Presentation | FR-03–FR-10, FR-18, FR-24–FR-25; OP-14; SEC-02 |
| RESP-025 | Exchange and normalize only authorized Dukascopy live/history/session/specification facts | Isolate provider mechanics | External Integration | Requirements INT-05–INT-06; DATA-15; FR-31; POL-12 |
| RESP-026 | Establish local mutation, writer and destructive-action authority | Protect sole analyst's work | Security / Audit | POL-11; AUTH-01–AUTH-03; FR-21/FR-55; CONS-06 |
| RESP-027 | Enforce bounded input/write access and keep secrets/captured private data outside reports and backups | Preserve trust boundaries | Security / Audit | SEC-01–SEC-04, SEC-06–SEC-07; DATA-08 |
| RESP-028 | Govern acquisition lifetime and expose feed/recovery condition | App-running acquisition and readable degraded operation | Operational | FR-34/FR-56; SCALE-05; OPS-01/OPS-04/OPS-06 |

## 7. Shared Knowledge Ownership

An owner defines a rule once; consumers request its decision or carry its evidence. Cross-cutting POL-10/POL-11 are allocated by their narrow subject, not copied into a universal policy engine.

| Knowledge / Rule | Upstream Owner (`POL-*`/`INV-*`/`DC-*`) | Consuming Workflows | Duplication / Leakage Risk | Architectural Treatment |
|---|---|---|---|---|
| Observation identity, side, periods/UTC, precision | Market observation meaning; POL-01, INV-01–INV-02, DC-01–DC-04 | WF-001–WF-009 | Per-panel alias/time conversions redefine data | BND-001 owns meaning; edges only adapt representations. |
| Usability/session continuity | Coverage/session evidence; POL-02, INV-11, DC-05–DC-07 | WF-001/WF-003–WF-008 | Provider flags, empty replies or weekend filters become eligibility | BND-002 decides from evidence; provider edge supplies facts only. |
| Available knowledge and intrabar resolution | Historical boundary/resolution; POL-03, INV-03/INV-10 | WF-001/WF-004–WF-009 | Latest quote leaks into watchlist/FX; tick resolver invents chronology | BND-004 owns availability and evidence hierarchy. BND-008 applies fallback only after eligibility/position checks. |
| Effective instructions and processed events | Run decision/event ordering; POL-04, INV-03 | WF-004–WF-007 | Plot update/speed becomes market ordering | BND-007 owns decision order; BND-008 consumes explicit effective boundaries. |
| Side/price and independent exposure | Execution outcome/position; POL-05, REL-08–REL-10, INV-05–INV-08/INV-14 | WF-004–WF-007 | Chart side, netting convention or stop-first supplies wrong price | BND-008 owns these rules and whole execution acceptance. |
| Specification/commission, historical USD, sizing | Monetary meaning/conversion/quantity; POL-06–POL-08, INV-09 | WF-004–WF-007/WF-009 | Sizing and execution use different fees/rates/rounding | BND-009 defines shared monetary decisions; BND-008 supplies targeted remaining quantity and accepts effects. |
| Retained input continuity | Run continuity; POL-09, INV-04 | WF-003–WF-009 | Catalog writes rewrite resumed evidence | BND-007 authorizes basis selection/replacement; BND-010 retains values, not merely mutable paths. |
| Calculation conventions and result labels | Calculation/result interpretation; POL-10, INV-10 | WF-001/WF-004–WF-009 | One generic calculator overrides distinct semantics | BND-006 owns study conventions; BND-009 monetary rounding; BND-008 execution assumption attribution. BND-007 retains selected versions; BND-012 displays without recomputation. |
| Authorship and truthful durability | Authored work/recovery authority; POL-11, INV-12–INV-13 | WF-002/WF-005–WF-009 | Save success inferred before retention; rewind deletes drawings | BND-013 decides authority; BND-005 owns analysis scope; BND-010 attests saved versions. |
| Account data-only purpose | Market-data access purpose; POL-12 | WF-003–WF-009 | Provider SDK grants broker effects or leaks credentials | BND-013 defines purpose constraint, BND-011 enforces data-only exchange; simulation sees no broker command capability. |

## 8. Cohesion Analysis & Proposed Boundaries (`BND-*`)

These thirteen logical boundaries separate distinct knowledge/reasons to change. Their count is not a deployment count. Infrastructure-facing capabilities can be implemented locally; no network between boundaries is required. Shared workflow, common storage, framework or broad noun alone is insufficient cohesion.

### BND-001 — Market observation meaning

- **Purpose:** Define consistent provider-qualified observation identity and temporal/side meaning.
- **Owned Responsibilities:** RESP-001.
- **Knowledge Owned / Protected:** DC-01–DC-04; POL-01; INV-01–INV-02; DATA-07.
- **Shared Reasons to Change:** Instrument aliases, accepted basis representations or precision/bucket conventions change.
- **Deliberate Exclusions:** Coverage verdicts (different evidence knowledge, BND-002); simulation unit/fee values (different monetary knowledge, BND-009); provider wire formats (BND-011).
- **Required Interactions:** Supplies canonical basis to BND-002–BND-009 and edges. Receives no provider/persistence dependencies.
- **Source Drivers:** DRV-001, DRV-010.

### BND-002 — Usable coverage and session continuity

- **Purpose:** Establish actual archive bounds and whether an interval is usable, a justified closure or unresolved.
- **Owned Responsibilities:** RESP-002.
- **Knowledge Owned / Protected:** DC-05–DC-07; POL-02; INV-11; PRE-02; OP-01; HIST-02.
- **Shared Reasons to Change:** Validation/coverage/session evidence improves or instrument continuity rules are refined.
- **Deliberate Exclusions:** File enumeration and acquisition (BND-010/BND-011); current value selection (BND-003); order pricing (BND-008). A filename or network response cannot make its own coverage verdict.
- **Required Interactions:** Uses BND-001 basis; accepts qualified evidence through CONTRACT-016; supplies assessments to catalog, replay evidence and monetary consumers.
- **Source Drivers:** DRV-001–DRV-005.

### BND-003 — Current-history reconciliation

- **Purpose:** Maintain the authoritative current catalog selection, finalization and affected aggregate lineage.
- **Owned Responsibilities:** RESP-004–RESP-006, RESP-028.
- **Knowledge Owned / Protected:** DC-08–DC-09; TR-02–TR-05; REL-03; OP-02; BR-08; CONS-09. Owns supplied M1→M5/M15 and H1→H4/D1/W1/MN1 recovery derivation rules under BND-001 bucket meaning.
- **Shared Reasons to Change:** Current-history precedence, overlap handling, recovered-span aggregation or acquisition lifetime changes.
- **Deliberate Exclusions:** Saved-run basis authority (BND-007); provider credentials/publication protocol (BND-011); physical retention (BND-010); absence-as-closure inference (BND-002).
- **Required Interactions:** BND-001/BND-002 for meaning/coverage, BND-011 for observations, BND-010 for retained owned history; publishes qualified catalog revisions, never pushes replacement into a run.
- **Source Drivers:** DRV-002–DRV-003, DRV-009–DRV-010.

### BND-004 — Historical evidence availability and resolution

- **Purpose:** Provide evidence only within a declared information boundary and resolve detail in the accepted hierarchy.
- **Owned Responsibilities:** RESP-007–RESP-008.
- **Knowledge Owned / Protected:** POL-03; DC-09/DC-13; INV-03; PRE-07 evidence ordering; OP-06/OP-09 evidence participation.
- **Shared Reasons to Change:** Availability semantics, additional local tick coverage or future explicitly specified detail sources change.
- **Deliberate Exclusions:** Maintaining cursor/actions (BND-007); executable side/price and eligible-position fallback decision (BND-008); network tick acquisition (excluded v1); drawing history (BND-005).
- **Required Interactions:** BND-001/BND-002 and BND-010 read capability; receives current-catalog or retained-run basis explicitly. Returns finer-bar/local-tick ordering evidence or unresolved chronology without inventing fills.
- **Source Drivers:** DRV-002, DRV-004–DRV-005, DRV-009–DRV-010.

### BND-005 — Authored chart analysis

- **Purpose:** Own valid reusable layouts, selections, study choices and layout/instrument drawings.
- **Owned Responsibilities:** RESP-009–RESP-010.
- **Knowledge Owned / Protected:** DC-10–DC-12; REL-04; TR-06–TR-08/TR-11; INV-13; PRE-01/PRE-09; OP-03–OP-05.
- **Shared Reasons to Change:** Supported analysis edits, arrangements, synchronization or annotation behavior changes.
- **Deliberate Exclusions:** Study numerical formulas (BND-006); execution and run rewind (BND-007/BND-008); pixels/control layout (BND-012); durable-write success (BND-010).
- **Required Interactions:** BND-001 and bounded BND-004 selections, BND-006 parameter validity; BND-013 mutation decisions. WF-002 coordinates retention rather than making storage part of drawing semantics.
- **Source Drivers:** DRV-001, DRV-004, DRV-007–DRV-009.

### BND-006 — Declared analytical calculations

- **Purpose:** Derive built-in study values with explicit conventions and unavailable/warm-up meaning.
- **Owned Responsibilities:** RESP-011.
- **Knowledge Owned / Protected:** DC-11; study portion of POL-10; OP-04; FR-11–FR-12.
- **Shared Reasons to Change:** SMA/EMA/RSI/MACD/Bollinger/provider-volume calculation conventions or permitted inputs change.
- **Deliberate Exclusions:** Monetary calculations (BND-009); plot rendering (BND-012); choosing future/latest evidence (BND-004); scripts (excluded).
- **Required Interactions:** Accepts already bounded labelled observations and explicit convention selection; uses BND-001 meaning. Does not reach into a feed or unbounded history to fill missing values.
- **Source Drivers:** DRV-001, DRV-004, DRV-009.

### BND-007 — Historical exercise continuity and coordination

- **Purpose:** Own each run's selected basis, historical decision boundary, retained actions and legal continuation/reconstruction.
- **Owned Responsibilities:** RESP-012–RESP-014, RESP-019.
- **Knowledge Owned / Protected:** DC-13–DC-14; POL-04/POL-09; REL-07; TR-12–TR-20; INV-03–INV-04; OP-06/OP-11–OP-14; HIST-03/HIST-08.
- **Shared Reasons to Change:** Decision ordering, retained-run basis selection, rewind/restart/resume or own-run report interpretation changes.
- **Deliberate Exclusions:** Fill/position/fee policy (BND-008/BND-009); mutable current-history reconciliation (BND-003); independent drawings (BND-005); physical checkpoints (BND-010).
- **Required Interactions:** Coordinates BND-004 evidence, BND-008 execution, BND-009 prerequisites, BND-013 authority and BND-010 retention. Exposes one bounded workspace context to BND-012. Reports interpret recorded outcomes, not a second execution engine.
- **Source Drivers:** DRV-003–DRV-008.

### BND-008 — Simulated instruction and exposure outcomes

- **Purpose:** Determine and apply complete hypothetical instruction, fill, position/protection and account effects.
- **Owned Responsibilities:** RESP-015–RESP-017; execution-owned RESP-023.
- **Knowledge Owned / Protected:** DC-15–DC-18; POL-05 and execution labels in POL-10; REL-08–REL-10; TR-21–TR-30; INV-05–INV-08/INV-10/INV-14; OP-07/OP-09–OP-10; HIST-04/HIST-06.
- **Shared Reasons to Change:** Accepted fill rules, hedging/targeted closure, protection and coherent execution acceptance change together.
- **Deliberate Exclusions:** Owning the replay clock/input selection (BND-007); reimplementing conversion/fees/sizing (BND-009); deciding provider coverage (BND-002); any broker capability (excluded).
- **Required Interactions:** Receives run-owned processed/effective event boundaries, BND-004 resolution evidence, BND-002 continuity assessments and BND-009 monetary decisions; returns complete execution effect or explained no-effect result.
- **Source Drivers:** DRV-004–DRV-006, DRV-008.

### BND-009 — Simulation monetary meaning and sizing

- **Purpose:** Own selected instrument specifications, commission, historical USD valuation and permitted quantity/risk decisions.
- **Owned Responsibilities:** RESP-018.
- **Knowledge Owned / Protected:** DC-19–DC-20; POL-06–POL-08 and monetary rounding in POL-10; INV-09; PRE-04–PRE-06; OP-08; HIST-05.
- **Shared Reasons to Change:** Instrument monetary conventions, applicable conversion evidence, commission bases or valid quantity/risk mathematics change.
- **Deliberate Exclusions:** Execution order/price discovery (BND-007/BND-008); fetching current FX to plug history (forbidden); chart appearance precision (BND-012); broker margin/balance rules (excluded).
- **Required Interactions:** Uses BND-001 meaning, BND-002 session applicability and BND-004 bounded conversion evidence; consumes run-selected specification/convention versions. Supplies the same fee/quantity/valuation semantics to sizing and execution.
- **Source Drivers:** DRV-005–DRV-006, DRV-008.

### BND-010 — Durable local evidence and work retention

- **Purpose:** Retain/recover coherent analyst work and required evidence, with truthful saved-version claims.
- **Owned Responsibilities:** RESP-003 read capability, RESP-020–RESP-022; retention portion of RESP-023/RESP-027.
- **Knowledge Owned / Protected:** DC-21; TR-09–TR-10; INV-12; HIST-07; OP-13; FR-43–FR-45/FR-55; DATA-18. Domain value selection remains with its owner.
- **Shared Reasons to Change:** Local retention formats/capabilities, coherent checkpoint recovery, portable backup and source-path handling change.
- **Deliberate Exclusions:** Financial truth or catalog conflict resolution (BND-003/BND-008/BND-009); run basis replacement authority (BND-007); credential export (forbidden); writing sibling sources (forbidden).
- **Required Interactions:** Narrow read/retain/checkpoint contracts owned by consuming semantic boundaries; BND-013 grants local mutation/restore authority. Supplies immutable selected evidence rather than promising mutable paths suffice. Backup contains necessary run inputs, not unrelated archive history.
- **Source Drivers:** DRV-002–DRV-003, DRV-007–DRV-008.

### BND-011 — Protected Dukascopy market-data exchange

- **Purpose:** Isolate authorized provider-specific data exchange and account secrets.
- **Owned Responsibilities:** RESP-025; provider portion of RESP-027.
- **Knowledge Owned / Protected:** Provider facts supporting POL-02/POL-06/POL-12; DATA-15–DATA-16; SEC-03/SEC-07. It supplies facts, not core-policy verdicts.
- **Shared Reasons to Change:** Actual live API/authentication, historical retrieval formats, asset entitlement or metadata/publication interfaces change.
- **Deliberate Exclusions:** Real order/amend/cash operations (no contract); current-catalog precedence (BND-003); session/valuation verdicts (BND-002/BND-009); TradingView private endpoints (excluded).
- **Required Interactions:** Implements normalized fact capabilities consumed by BND-003; BND-013 supplies data-only authority. Provider credentials remain protected outside browser-facing views, checkpoints, logs and exports.
- **Source Drivers:** DRV-003, DRV-008–DRV-010.

### BND-012 — Desktop interaction and disclosure

- **Purpose:** Translate accessible desktop actions and display/export truthful semantic views.
- **Owned Responsibilities:** RESP-024; presentation portion of RESP-027.
- **Knowledge Owned / Protected:** FR-03–FR-10/FR-18/FR-24–FR-25; OP-14 disclosure obligations; SEC-01–SEC-02/SEC-06.
- **Shared Reasons to Change:** Chart renderer, desktop interaction, accessibility or local image/report representation changes.
- **Deliberate Exclusions:** Determining fills, conversion, period availability or saved success (semantic owners); executing captured HTML/arbitrary scripts (forbidden); choosing a UI design/framework in this pass (downstream).
- **Required Interactions:** WF-001–WF-009 application contracts; adopts bounded basis/cursor/provenance and retained-version outcomes. Routine chart navigation must not require a tick-history resolution to finish.
- **Source Drivers:** DRV-001–DRV-002, DRV-004, DRV-007–DRV-009.

### BND-013 — Local work and data-purpose authority

- **Purpose:** Define whether a local operation may mutate, discard, restore or disclose analyst work and whether provider use is data-only.
- **Owned Responsibilities:** RESP-026; authority portion of RESP-027.
- **Knowledge Owned / Protected:** POL-11 authority portion/POL-12; AUTH-01–AUTH-03; SEC-02–SEC-04/SEC-07; FR-21/FR-55; CONS-06.
- **Shared Reasons to Change:** Local single-writer/destructive-action authority or permitted provider/disclosure purpose changes.
- **Deliberate Exclusions:** Intrinsic financial validity (BND-008/BND-009); physical writer exclusion mechanism (Pass 2); imagined users/roles/tenant platform (out of scope).
- **Required Interactions:** Supplies contextual authority decisions to mutating/export/retention/provider workflows; edges enforce purpose-specific capability exposure. Confirmation cannot legalize an invalid close or a source-directory write.
- **Source Drivers:** DRV-007–DRV-008.

## 9. Deliberate Exclusions Summary

| Related Concern | Excluded From | Why Related But Not Cohesive | Expected Owner Boundary |
|---|---|---|---|
| Provider protocol and secret handling | BND-001/BND-002/BND-003 | Observation meaning, usable evidence and current precedence do not depend on wire/API details | BND-011 |
| Final/current history versus selected run evidence | BND-007 versus BND-003 respectively | Different authority and reasons to change despite same observations | BND-003 current; BND-007 retained basis; BND-010 retention |
| Chronology, instruction effectiveness and price | Each other's owners | Available evidence cannot grant eligibility or invent executable price | BND-004 evidence; BND-007 order; BND-008 price/effects |
| Authored study settings versus numerical output | BND-006 versus BND-005 respectively | Edit lifecycle differs from formula conventions | BND-005 configuration; BND-006 calculation |
| Monetary valuation versus chart/display precision | BND-012 | Formatting is not unit/currency/rounding authority | BND-009 |
| Run rewind versus annotation undo | BND-005 versus BND-007 respectively | Distinct ownership, history and destructive effects | BND-007 trading; BND-005 analysis |
| Physical retention versus semantic truth/authority | BND-003/BND-005/BND-007/BND-008/BND-013 | Sharing a saved artifact does not merge financial, authorship and capability knowledge | BND-010 physical capability; respective owners define content/authority |
| Real orders, alerts, scripts, automatic tick acquisition | All v1 boundaries | Explicit scope exclusion/deferral, not an unfilled abstraction | None in v1 |

## 10. Application Workflows (`WF-*`)

All mutating workflows first establish sole local writer/purpose context (RESP-026–RESP-027). Read workflows establish basis and disclosure context. All recorded evidence (RESP-023) stays with its semantic owner under Section 13; no separate permanent audit subsystem is implied. Arrows here describe semantic collaboration, not dependency direction or implementation scheduling guarantees.

### WF-001 — Discover, select, navigate and read analysis

```text
search/select/range request -> establish requested basis and current/replay context
-> obtain qualified archive bounds and required range (RESP-001–RESP-003)
-> obtain only available evidence under the context (RESP-007–RESP-008)
-> adopt matching selection, or retain previous valid chart (RESP-009)
-> derive bounded study outputs (RESP-011)
-> disclose consistent chart/window/watchlist/detail labels, gaps and unavailable values (RESP-024)
```

- **Shared Responsibilities:** RESP-001–RESP-003, RESP-007–RESP-008, RESP-011, RESP-024/RESP-027.
- **Unique Responsibilities:** Selection adoption RESP-009 within this workflow and WF-002 configuration edits.
- **Coordination-Only Relationships:** Chart selection does not own archive files, historical availability, or study formulas. An empty resident range is not archive exhaustion. [OP-01/OP-03–OP-04; CONS-01]

### WF-002 — Commit/cancel authored analysis and autosave

```text
layout/drawing/study/settings/sync command -> establish writer and required confirmation
-> assess supported parameters and analysis scope -> commit/reverse valid edit or cancel preview (RESP-009–RESP-010)
-> identify coherent changed analysis version -> request retention (RESP-020–RESP-021)
-> report that version's actual saving/saved/error outcome (RESP-024)
```

- **Shared Responsibilities:** RESP-009–RESP-011, RESP-020–RESP-024, RESP-026–RESP-027.
- **Unique Responsibilities:** Independent annotation and analysis edit history in RESP-010.
- **Coordination-Only Relationships:** BND-005 owns committed content; BND-010 owns retention success, not edit validity. No trading action is created by a measurement drawing. [OP-03–OP-05/OP-13; INV-12–INV-13]

### WF-003 — Startup/reconnect acquisition and current-history finalization

```text
application start/reconnect/new provider facts -> establish data-only/local retention authority
-> discover existing usable current coverage -> determine needed M1/H1 recovery spans
-> request provider observations/session/publication facts (RESP-025)
-> assess meaning, usability and continuity (RESP-001–RESP-002)
-> reconcile overlap/final versus provisional current facts and affected UTC derivatives (RESP-004–RESP-006)
-> retain application-owned history/provenance (RESP-022–RESP-023)
-> expose actual receiving/closure/recovery/stale/failure condition (RESP-028/RESP-024)
```

- **Shared Responsibilities:** RESP-001–RESP-008, RESP-022–RESP-028.
- **Unique Responsibilities:** RESP-004–RESP-006, RESP-025, RESP-028.
- **Coordination-Only Relationships:** Provider receipt supplies facts; coverage assesses; catalog selects; retention stores. No step rewrites sibling inputs or a retained run. Acquiring later history continues without disclosing it to replay. [OP-01–OP-02; FR-56; CONS-09/CONS-16]

### WF-004 — Start/advance/seek a historical exercise

```text
start/play/step/forward-seek -> establish run context and selected retained basis/settings
-> obtain next completed evidence and continuity assessment (RESP-007–RESP-008)
-> stop with reason before unresolved interval, or establish next event boundary (RESP-012–RESP-014)
-> evaluate eligible existing instructions/protection through WF-006
-> expose coherent historical cursor and bounded panels/studies/results
-> accept subsequent new decisions only after processed events; request checkpoint
```

- **Shared Responsibilities:** RESP-001–RESP-003, RESP-007–RESP-008, RESP-011–RESP-014, RESP-016–RESP-024, RESP-026.
- **Unique Responsibilities:** Run decision/event progression in RESP-012–RESP-014.
- **Coordination-Only Relationships:** BND-007 coordinates evidence and execution; playback speed/redraw does not define order. Forward seek obeys the same evaluations/gaps. At actual coverage limit preserve open positions; loading another archive range is not reaching that limit. [OP-06; TR-12–TR-14/TR-18–TR-20]

### WF-005 — Submit/modify/cancel an instruction or request targeted closure

```text
historical trading decision -> establish writable run and current decision boundary
-> obtain retained settings, selected specification, balance and target remainder
-> determine valid fixed/risk/close quantity and prerequisites (RESP-018)
-> accept valid terms/change/cancellation with after-decision effectiveness, or retain prior valid instruction and explain invalid/block (RESP-012/RESP-015)
-> retain action/effective-boundary facts and checkpoint -> disclose semantic outcome
```

- **Shared Responsibilities:** RESP-012–RESP-015, RESP-018, RESP-020–RESP-024, RESP-026.
- **Unique Responsibilities:** Instruction decision transition RESP-015, also consumed by WF-006.
- **Coordination-Only Relationships:** Sizing does not execute; acceptance cannot consume already processed events or undo past fills. Opposite entry creates an independent exposure when executed. [OP-07–OP-08/OP-10; PRE-05–PRE-06/PRE-08]

### WF-006 — Resolve and accept a complete simulated execution

```text
eligible event/instruction -> establish retained run basis and effective event context
-> verify continuity/validity -> resolve available finer stored bars then needed local ticks
-> establish observed chronology or eligible labelled stop-first (RESP-007–RESP-008/RESP-016)
-> determine executable side/price and requested quantity (RESP-016)
-> determine applicable original-event conversion, selected units, fees and USD effects (RESP-018)
-> if prerequisite absent, retain explained uncommitted original event; otherwise accept whole execution/exposure/protection/account effect (RESP-014/RESP-017)
-> retain outcome/evidence/assumptions and request checkpoint -> disclose coherent result
```

- **Shared Responsibilities:** RESP-001–RESP-002, RESP-007–RESP-008, RESP-012–RESP-014, RESP-016–RESP-024.
- **Unique Responsibilities:** Complete-effect acceptance RESP-017.
- **Coordination-Only Relationships:** BND-004 cannot decide an ineligible exit; BND-009 cannot commit an orphan fee; BND-008 cannot fetch a substitute current FX rate. ASM-01 selects unresolved protective order only; ASM-02 does not bypass gap, price or valuation rules. [OP-09–OP-10; PRE-02–PRE-07; INV-05–INV-10/INV-14]

### WF-007 — Resolve a blocked original historical event

```text
prerequisite evidence/specification becomes available -> locate retained original event and reason
-> assess continuity, historical applicability and compatibility with retained committed basis
-> retain permitted uncommitted-prerequisite completion without changing prior outcomes
-> reevaluate original event through WF-006, or remain explained blocked
-> if changed committed evidence would be required, offer deliberate updated-data restart rather than silent replacement
```

- **Shared Responsibilities:** RESP-002, RESP-007–RESP-008, RESP-012–RESP-014, RESP-016–RESP-023/RESP-026.
- **Unique Responsibilities:** None; explicit reuse prevents a second resumption pricing path.
- **Coordination-Only Relationships:** New receipt time is not new execution time/price. General catalog correction has no authority to mutate a retained basis. [OP-11; TR-15–TR-16; CONS-14–CONS-15]

### WF-008 — Rewind/restart, resume, backup or restore

```text
history/recovery command -> establish operation scope, sole writer and required destructive confirmation
-> for rewind: retain earlier actions and reconstruct dependent run prefix under the original basis
-> for explicit updated-data restart: deliberately select a new exercise basis
-> for resume: retrieve original selected evidence/settings and matching saved run
-> for backup/restore: retain/validate required run inputs and coherent analysis/run versions, excluding credentials; restore without silent merge
-> leave independent drawings unchanged by trading rewind -> checkpoint/report actual outcome
```

- **Shared Responsibilities:** RESP-007–RESP-008, RESP-012–RESP-014, RESP-016–RESP-023, RESP-026–RESP-027.
- **Unique Responsibilities:** None; reconstruction uses existing execution rules, not a parallel engine.
- **Coordination-Only Relationships:** BND-007 selects lawful run changes; BND-010 restores coherent artifacts; BND-013 controls authority. Cancelled destructive requests change nothing. Manual backup restore is not a general external run importer. [OP-12–OP-13; PRE-10; CONS-13/CONS-15]

### WF-009 — Export local chart image or own-run report

```text
local export request -> establish permitted disclosure and current/replay basis
-> obtain bounded rendered analysis or recorded own-run outcomes
-> include basis, cursor where relevant, units/currency, conventions and evidence/assumptions
-> create local image/report without credentials/private captured data -> report export outcome
```

- **Shared Responsibilities:** RESP-007–RESP-008, RESP-011, RESP-019, RESP-023–RESP-024, RESP-026–RESP-027.
- **Unique Responsibilities:** Local representation/export part of RESP-024.
- **Coordination-Only Relationships:** Export does not recompute trades against latest history or authorize hosted publication. [OP-14; FR-18/FR-20/FR-29; SEC-04/SEC-06]

## 11. Dependency Direction (`DEP-*`) & Sketch

`A -> B` means A requires B's semantic contract, not that A executes earlier. BND-010/BND-011 implement inward-defined capabilities; business rules depend on those stable capabilities, not concrete storage/provider representations. The capability arrows below name logical participants without prescribing imports or runtime topology.

```text
BND-012 Desktop edge -> application contracts of BND-003/BND-005/BND-007/BND-010/BND-013
BND-005 Authored analysis -> BND-001 Meaning, BND-004 Available evidence, BND-006 Studies, BND-013 Authority
BND-007 Run -> BND-004 Available evidence, BND-008 Execution, BND-009 Monetary decisions, BND-013 Authority
BND-008 Execution -> BND-001 Meaning, BND-002 Coverage, BND-009 Monetary decisions
BND-009 Monetary decisions -> BND-001 Meaning, BND-002 Coverage, BND-004 Bounded conversion evidence
BND-004 Available evidence -> BND-001 Meaning, BND-002 Coverage, retained-evidence read capability
BND-006 Studies -> BND-001 Meaning (bounded inputs supplied by caller)
BND-002 Coverage -> BND-001 Meaning
BND-003 Catalog -> BND-001 Meaning, BND-002 Coverage, data-fact and owned-retention capabilities
BND-010 Retention -> inward-defined read/retain/checkpoint contracts
BND-011 Provider edge -> inward-defined data-fact contracts and BND-013 data-purpose authority
BND-013 Authority -> established local work/purpose context (no market calculation dependency)
```

### Necessary Dependencies

| ID | From | To | Why Required | Knowledge Crossing |
|---|---|---|---|---|
| DEP-001 | BND-002–BND-009 | BND-001 | Same provider/basis meaning | Qualified instrument, period/side, original precision, revision |
| DEP-002 | BND-003/BND-004/BND-008/BND-009 | BND-002 | Continuity and eligibility cannot be inferred locally | Evidence-backed bounds, gaps, closure/applicability assessments |
| DEP-003 | BND-005/BND-007/BND-009 | BND-004 | Chart, run and conversion reads need the same availability semantics | Explicit current/run basis, historical boundary, bounded evidence |
| DEP-004 | BND-005 | BND-006 | Study settings need declared valid conventions/outputs | Study selection/inputs, unavailable/derived outputs |
| DEP-005 | BND-007 | BND-008/BND-009 | Coordinate execution and sizing without owning their knowledge | Effective boundary, target state, monetary prerequisites, complete effects |
| DEP-006 | BND-008 | BND-009 | Complete execution requires shared fee/valuation/quantity rules | Selected conventions, event price, requested/remaining quantity, fully valued result/block |
| DEP-007 | BND-003/BND-004/BND-007 and WF-002/WF-008 coordinators | BND-010 capability contracts | Read selected evidence; retain catalog/analysis/run work | Semantic versions/evidence/retention outcomes; no physical format |
| DEP-008 | BND-003 | BND-011 data-fact capability | Acquire required live/history metadata | Normalized M1/H1/live/session/publication/specification facts |
| DEP-009 | Mutation/disclosure/provider coordinators | BND-013 | Apply single-writer, confirmation, scope and data-only restrictions | Local actor/work scope, action purpose and confirmation decision |
| DEP-010 | BND-012 | Application contracts | Adapt user actions without duplicating domain logic | Labelled view/operation outcomes and explicit unavailable/error/saved version |
| DEP-011 | BND-010/BND-011 concrete realizations | Inward-defined consumer capability contracts | Keep physical/provider volatility outside semantic owners | Implementations satisfy normalized contracts; core has no vendor/format dependency |

### Risky Dependencies

| ID | From | To | Risk | Why Accepted | Correction Trigger |
|---|---|---|---|---|---|
| DEP-012 | BND-007 | BND-008 | Temporal coupling of cursor and whole execution outcome | Existing-before-new ordering/coherence is a product rule | If view/clock callbacks can independently mutate execution, restore exclusive run coordination; analyze failures in Pass 2. |
| DEP-013 | BND-010 | Coherent analysis/run content contracts | Representation evolution can break original-input restore | Successful saved work and reproducible backup require content retention | Before a representation change cannot read old saved versions, define compatibility/recovery in Pass 2/downstream standards. |
| DEP-014 | BND-002 | Qualified provider session evidence | Incomplete entitlement/calendar facts could stall traversal | Mandatory continuity needs instrument-specific evidence | New evidence contradicts closure assumptions: reassess affected scope; never fill gaps from silence. |

### Forbidden Dependencies

| ID | Forbidden Direction | Reason | What It Would Leak / Couple |
|---|---|---|---|
| DEP-015 | Core BND-001–BND-009 -> concrete provider/renderer/storage formats | Volatile implementation would define business meaning | SDK/session objects, plot cadence, file schemas and mutable paths |
| DEP-016 | BND-003 -> mutation of BND-007 retained basis/results | Current catalog lacks run-rewrite authority | New ticks/finality/specifications rewriting old results |
| DEP-017 | BND-012 -> unbounded latest/live reads during replay or independent trade/fee calculation | Bypasses common historical and financial authority | Future prices, inconsistent rounding, chart side as executable side |
| DEP-018 | BND-008 -> actual broker order/balance capability | Data access grants no brokerage authority | Real money/orders or account cash as simulated balance |
| DEP-019 | Any app writer -> sibling ingestion originals; any export -> credentials | Outside local mutation/disclosure purpose | Source corruption, secrets in backups/browser/reports |
| DEP-020 | Trading rewind -> BND-005 drawing deletion; study calculation -> provider acquisition | Unrelated history/knowledge ownership | Lost annotations or hidden unbounded/future input acquisition |
| DEP-021 | Provider edge -> authoritative core closure/valuation/fill verdict | Provider representation cannot bypass policy | Empty response as closure, metadata as proven contract values |

## 12. Coupling Analysis

| Parties | Coupling Type | Classification | Evidence | Boundary Consequence |
|---|---|---|---|---|
| Observation consumers/BND-001 | Business-knowledge and representation | NECESSARY | POL-01, INV-01–INV-02 | Shared semantic basis, no provider wire types. |
| BND-003/BND-007 via retained evidence | Change and data authority | NECESSARY for explicit basis selection; implicit replacement FORBIDDEN | POL-09, CONS-16 | Runs retain their own basis; catalog offers revisions only. |
| BND-004/all replay consumers | Contract and historical-time | NECESSARY | FR-20, POL-03 | Common boundary context required for every replay panel/FX/report read. |
| BND-007/BND-008 | Temporal and state | RISKY/accepted DEP-012 | POL-04, INV-05 | One run coordinator accepts complete outcomes; Pass 2 must resolve interrupted progress. |
| BND-008/BND-009 | Business-knowledge | NECESSARY | POL-05–POL-08 | Price/position owns one side, monetary decision owns other; no duplicated fee formula. |
| BND-003/BND-011 | Provider and contract | NECESSARY; provider leakage FORBIDDEN | FR-31–FR-35, UNK-19/UNK-20 | Normalize facts and retain provenance; do not import undocumented endpoints as contracts. |
| BND-002/provider session evidence | External authority | RISKY/accepted DEP-014 | DM-GAP-02 | Return unresolved when evidence insufficient, never silently share calendars. |
| BND-005/BND-007 | Workflow proximity only | UNDESIRABLE if merged | INV-13, REL-04/REL-07 | Analysis and trading histories remain independent. |
| BND-010/semantic owners | Contract evolution/durability | RISKY/accepted DEP-013 | FR-44–FR-45/FR-55 | Retention does not invent schema or reinterpret results; compatible original evidence remains an obligation. |
| BND-013/mutating coordinators | Local security scope | NECESSARY | POL-11–POL-12, CONS-06 | Bind authority to local work/action purpose; no speculative tenant layer. |

## 13. Conceptual Data Ownership (`DATAOWN-*`)

All application-owned data belongs to the sole local analyst. Writers below are semantic authorities; BND-010 is their physical retention capability, not a second truth owner. The same externally sourced fact may have a current catalog selection and a retained run copy; those selections have different authority and neither overwrites the other.

| ID | Fact / Data Family | Conceptual Owner | Source of Truth | Authority Type | Tenant / Workspace Scope | Legitimate Consumers |
|---|---|---|---|---|---|---|
| DATAOWN-001 | Provider-qualified instrument/period/side/precision meaning | BND-001 | Accepted mappings and source meaning, with absent metadata explicit | authoritative semantic interpretation; external source facts | Provider/instrument/series | BND-001 defines; all consumers read; BND-011 supplies metadata facts (BR-01, POL-01). |
| DATAOWN-002 | Original sibling observations/manifests/local ticks | External ingestion producer | Actual selected source values/provenance | external | Provider/instrument/timeframe/side/span/revision | BND-010 reads; no application writer (DATA-01/DATA-08/DATA-10). |
| DATAOWN-003 | Usability/coverage/gap/closure assessments | BND-002 | Validation and appropriate instrument/session evidence | derived | Specific series/revision/interval | BND-002 determines; BND-003/BND-004/BND-008/BND-009 read (POL-02, HIST-02). |
| DATAOWN-004 | Acquired/provisional/final current observations, precedence and aggregate lineage | BND-003 | Qualified current catalog selection and retained provider facts/derivations | authoritative catalog selection; external facts/derived aggregates | Local catalog by provider/series/revision | BND-003 changes; BND-004 reads explicit current basis; BND-010 retains (FR-35/FR-43, OP-02). |
| DATAOWN-005 | Bounded historical view and resolved evidence | BND-004 | Declared basis, availability boundary and retained evidence | derived; optional cached view has no independent authority | Current view or specific run/cursor | BND-004 determines; BND-005/BND-007/BND-009 and bounded presentation consume (POL-03). |
| DATAOWN-006 | Layouts, selections, studies' configuration, drawings, watchlist/settings | BND-005 | Analyst's committed valid authored version | authoritative | Local analyst/layout; drawing additionally instrument; at most two charts | BND-005 changes under authority; BND-010 retains; BND-012 reads (DATA-12, REL-04, OP-05). |
| DATAOWN-007 | Study convention definitions and calculated outputs | BND-006 | Declared convention plus supplied bounded input values | authoritative convention; derived outputs | Study instance/basis/boundary/convention | BND-006 defines/derives; BND-005/BND-012 consume; run retains applicable selections (POL-10). |
| DATAOWN-008 | Selected run inputs/specification/convention versions | BND-007 | Retained selected observations, ticks/FX, settings and provenance, not mutable paths | authoritative run selection of external/derived evidence | Individual run | BND-007 selects/authorizes prerequisite completion or deliberate restart; BND-010 retains; BND-004/BND-008/BND-009 read (POL-09, DATA-18). |
| DATAOWN-009 | Cursor, processed-event boundary, accepted action history, blocked-event context | BND-007 | Coherent retained run progression and decisions | authoritative | Run and established event/action order | BND-007 changes; BND-008 supplies instruction/effect facts; BND-010 retains; panels use bounded reads (POL-04, HIST-03/HIST-08). |
| DATAOWN-010 | Instructions, triggers, fills, independent positions/protection and account effects | BND-008 | Complete accepted execution and instruction transitions under run-selected basis | authoritative simulated facts; balance/remainder derived | Run/order/targeted position | BND-008 changes through run coordination; BND-007 reads/reconstructs; BND-010 retains; BND-012 reports without recomputing (INV-05–INV-10, HIST-04–HIST-06). |
| DATAOWN-011 | Editable current specifications, fees, monetary conventions and sizing/valuation decisions | BND-009 | Identified provider metadata/user overrides and selected declared conventions; historical FX facts via BND-004 | authoritative selected simulation meaning; derived monetary decisions | Local instrument settings; fixed selections per run | BND-009 defines/validates; BND-007 selects; BND-008 consumes; no retroactive run mutation (POL-06–POL-08). |
| DATAOWN-012 | Successful checkpoint and portable backup evidence | BND-010 | Successfully retained coherent version with required run inputs | authoritative retention fact; retained content preserves originating authority | Local analysis/selected runs | BND-010 attests retention and restores under authorization; semantic owners validate content (INV-12, HIST-07, OP-13). |
| DATAOWN-013 | Live access secrets and provider exchange facts | BND-011 | Protected provider setup and actual responses/receipts | external facts; protected configuration | Local data-access setup/provider account purpose | BND-011 uses secrets only; BND-003 receives normalized data; no browser/backup/report/log secret reader (SEC-03/SEC-07). |
| DATAOWN-014 | Local writer/destructive/data-purpose authority context | BND-013 | Sole analyst's local mutation scope and required confirmations | authoritative local decision | Local writable session and affected work/action | BND-013 decides; mutating/disclosure edges enforce; no tenant identity introduced (POL-11–POL-12). |

## 14. Semantic Contracts (`CONTRACT-*`)

Business errors are semantic outcomes, not HTTP codes. All inputs include their relevant provider/basis/revision, local work scope, and historical boundary where applicable. Writes require authority from BND-013. Missing prerequisites differ from invalid requests, persistence failures and exhausted history.

### Application Operations

| ID | Operation | Owner Boundary | Semantic Input / Context | Semantic Outcome | Important Business Errors | Source |
|---|---|---|---|---|---|---|
| CONTRACT-001 | Discover/select/read available history | BND-005 selection; BND-004 view; BND-002 coverage | Requested instrument/period/side/range; current or retained-run basis; disclosure boundary | Matching labelled selection and actual bounds/gaps/values; failed selection retains last valid chart | Unsupported basis, unreadable/invalid range, unavailable historical value, loading, actual coverage end | OP-01/OP-03; FR-01–FR-09/FR-52; PRE-01 |
| CONTRACT-002 | Commit/cancel/undo/redo analysis edit | BND-005 | Layout/instrument/object, valid proposed parameters or cancel/reverse action, writer context | Revised committed analysis or unchanged valid prior state; separately identified save condition | Invalid parameter, locked/absent target, unsupported arrangement, missing authority/confirmation | OP-04–OP-05; FR-10–FR-17; PRE-09 |
| CONTRACT-003 | Extend/reconcile current history | BND-003 | Actual coverage, M1/H1 recovery interval/live facts, side, provenance, session/publication evidence, data-only authority | Retained current revision and affected derivatives; honest partial/unresolved/provisional state | Access unavailable, invalid facts, unresolved conflict/gap/finality, retention failure | OP-02; FR-31–FR-35/FR-43/FR-56 |
| CONTRACT-004 | Position/advance/seek/play/pause run | BND-007 | Run or start selection, retained inputs/settings, intended movement/speed, processed boundary | Coherent cursor and already-evaluated eligible outcomes, paused/blocked/coverage-limit reason | Missing retained input, unresolved continuity, incomplete evidence, invalid start; no synthetic forced closure | OP-06; TR-12–TR-14/TR-18–TR-20; PRE-02 |
| CONTRACT-005 | Submit/modify/cancel/target-close instruction | BND-007 coordinates; BND-008 owns transition | Current decision boundary, terms/type/quantity or sizing request, target position/order, retained policies | Accepted effective-after-boundary action or cancellation; invalid modification preserves valid prior order | Invalid terms/quantity/over-close, nonpending target, missing prerequisite, nonpositive-balance risk mode, authority denied | OP-07–OP-08/OP-10; PRE-03/PRE-05–PRE-06/PRE-08 |
| CONTRACT-006 | Evaluate eligible execution | BND-008 | Effective instruction/target remainder, original event/evidence, continuity decision, selected specification/fees, historical conversion | Entire labelled execution/position/protection/fee/USD effect, no trigger/fill, or explained uncommitted block | Ineligible/processed event, missing price/continuity/unit/conversion, invalid quantity/limit bound; no orphan fee/fill | OP-09–OP-10; PRE-02–PRE-07; INV-05–INV-10/INV-14 |
| CONTRACT-007 | Resolve blocked original event | BND-007 | Original blocked event/context, resolved historical prerequisite, retained basis | Reevaluate same event once under unchanged committed basis, or remain blocked | Inapplicable/future/stale evidence, changed committed basis requiring explicit restart | OP-11; TR-16; CONS-14–CONS-15 |
| CONTRACT-008 | Confirm/cancel rewind or explicit updated-data restart | BND-007 | Run/target, operation kind and confirmation; explicit updated basis only for restart | Reconstructed retained prefix or deliberate new-basis exercise; cancelled request unchanged; drawings untouched | Missing confirmation, invalid/unusable target, missing original evidence, authority denied | OP-12; TR-17–TR-18; CONS-13 |
| CONTRACT-009 | Autosave/resume/backup/restore/delete/reset local work | BND-010 retention coordination; BND-005/BND-007 validate content | Coherent committed versions, required run inputs, restore/operation scope, authority and confirmations | Actual retained version or coherent recovery/replacement; credential-free backup | Save failure/unsaved version, missing original evidence, malformed/incompatible backup, conflicting writer, no confirmation; no silent merge | OP-13; PRE-10; FR-44–FR-45/FR-55; OPS-03 |
| CONTRACT-010 | Interpret/export own chart/results | BND-012 representation; BND-007 report meaning | Bounded selected chart or recorded run results, local output request | Local image/report with units, basis, conventions/evidence labels and replay disclosure limit | Unavailable bounded values, local export failure, prohibited secret/private data disclosure | OP-14; FR-18/FR-20/FR-29; SEC-04/SEC-06 |
| CONTRACT-011 | Select/edit simulation specification, fees and sizing convention | BND-009; BND-007 retains run selection | Instrument, identified metadata/override values, commission mode, fixed/risk settings, applicable run scope | Valid explicit simulation settings, computed permitted quantity/planned risk, or explained unavailable requirement | Unknown unit/increment/minimum, invalid SL/risk budget, missing historical conversion, undocumented convention; cannot silently rewrite saved settings | OP-08; FR-39/FR-41/FR-49–FR-50/FR-54; DM-GAP-04 |

### Internal Boundary Contracts

| ID | Consumer -> Provider | Meaning Exchanged | Stability / Encapsulation Purpose |
|---|---|---|---|
| CONTRACT-012 | BND-005/BND-007/BND-009 -> BND-004 | Explicit current or retained-run basis, cursor/processed-event context, requested range/detail; returns available observations or unavailable reason with provenance | Same nonfuture rule for chart, watchlist, studies, FX and reports; no implicit latest fallback (POL-03, INV-03). |
| CONTRACT-013 | BND-007 -> BND-008 | Instruction/exposure state, effective/processed boundary and qualified evidence; returns instruction transition/complete effect or block | Run ordering independent of redraw; execution independent of provider/clock objects (POL-04–POL-05, INV-05). |
| CONTRACT-014 | BND-007/BND-008 -> BND-009 | Original event, units/specification/fees, requested or remaining quantity, planned balance/SL and applicable FX evidence; returns valued effects or valid size/block | Single monetary/rounding/quantity owner; a decision is not independent permission to commit fees (POL-06–POL-08/POL-10). |
| CONTRACT-015 | Semantic owners -> BND-010 implemented capabilities | Read qualified ranges/selected originals; retain owned observations/work/checkpoint/backup; report exactly which version succeeded or failed | Physical formats and mutable source paths cannot define truth or saved success. Required selected evidence survives source changes (FR-43–FR-45, INV-04/INV-12). |
| CONTRACT-016 | BND-003/BND-004/BND-008/BND-009 -> BND-002 | Qualified observation/validation/session facts and interval; returns usable/limited/gap/known-closure assessment and basis | Producer flags and no-response never self-authorize trading or stale conversion (POL-02, INV-11). |
| CONTRACT-017 | BND-003 -> BND-011 implemented data capability | Provider-qualified instrument, supported M1/H1 range or live/metadata request, data-only context; normalized observations, receipt/event times, session/publication/spec facts or explicit limitation | API/auth/entitlement/response details stay outside; capability exposes no real orders or balances (FR-31–FR-35, POL-12). |
| CONTRACT-018 | BND-005 and bounded view coordinator -> BND-006 | Study type/instance, declared convention/parameters and bounded labelled observations; output values with warm-up/missing meaning | No hidden acquisition or future warm-up source; convention changes explicit (FR-11–FR-12, POL-10). |
| CONTRACT-019 | Mutation/restore/export/provider workflow -> BND-013 | Local work scope, action purpose, writer and destructive confirmation context; explicit allowed/denied decision | Sole local authority distinct from intrinsic state/quantity validity and provider entitlement (POL-11–POL-12). |
| CONTRACT-020 | BND-007 -> BND-012 bounded workspace disclosure | Active historical boundary, basis, compatible panel views and save/block reasons | All replay panels carry same information limit; chart hover/latest receipt is not an alternative cursor (FR-20, CONS-16). |

## 15. External Integration Boundaries (`INT-*`)

Architecture INT IDs below are local to this dossier; each maps explicitly to the requirements integration register. Data services' external authority covers their attributed observations; this does not make every response valid, complete or final. Timeouts/retries/recovery mechanisms are deferred to Pass 2.

### INT-001 — Sibling Dukascopy archive (requirements INT-01)

- **Business Purpose:** Required initial historical bars and available local tick evidence.
- **Owning / Consuming Boundary:** BND-010 read capability; BND-003 current discovery; BND-004 selected historical reads; BND-002 usability assessment.
- **Facts Sent / Received:** Read local Parquet/manifests under `../marketDataIngestion/dukascopy/`, including monthly and all-history layouts and staged/final tick distinctions. Receive original precision, source values/status/provenance. No source writes.
- **Authority Relationship:** `authoritative` externally attributed observations; validation/coverage remain separate.
- **Provider-Specific Knowledge Kept Outside:** Filenames, schema/column-order differences, manifest path handling, staging representation and source-file access stay in the read edge. Absolute manifest paths do not grant access authority.
- **Replaceability / Evolution Driver:** Independent ingestion adds/revises months and tick assets; actual provider/series bounds stay discoverable (EVO-01–EVO-04). Saved selected evidence remains retained independently of mutable source paths.

### INT-002 — Dukascopy historical M1/H1 (requirements INT-05)

- **Business Purpose:** Fill gaps to current data and complete affected supported-period boundaries.
- **Owning / Consuming Boundary:** BND-011 exchange; BND-003 reconciliation; BND-002 continuity.
- **Facts Sent / Received:** Qualified instrument, M1/H1 interval and bid/ask request; receive provider observations and available publication/finality/session metadata. Retain origin and distinguish missing/partial/unverified facts.
- **Authority Relationship:** `authoritative` external historical source; finality requires evidence, not simply a successful response.
- **Provider-Specific Knowledge Kept Outside:** Public datafeed file conventions observed in ingestion code, compression/response formats and any chosen API mechanism stay in BND-011. Existing code is evidence of an access path, not verified publication behavior.
- **Replaceability / Evolution Driver:** UNK-20/DM-GAP-02 and future acquisition mechanisms. No claim that all provider APIs expose only M1/H1; that restriction is this release's candle-input contract.

### INT-003 — Dukascopy live-account market data (requirements INT-06)

- **Business Purpose:** Receive current observations for supported assets when available, while application is running.
- **Owning / Consuming Boundary:** BND-011 protected access; BND-003 catalog/lifecycle; BND-012 bounded display.
- **Facts Sent / Received:** Data-only subscription/access context; receive identified live observations, event/local-receipt times, asset/specification/session facts and explicit access/connection limitations. No actual orders, amendments or real-account cash.
- **Authority Relationship:** `authoritative` live-account observations for their attributed origin; provisional built bars are not final history or permission for historical future leakage.
- **Provider-Specific Knowledge Kept Outside:** Actual API/login/session/entitlement details and secrets remain at protected edge; none sent to browser-facing views/backup/report/log.
- **Replaceability / Evolution Driver:** UNK-19/DM-GAP-01 must verify actual access before acceptance. Provider failures preserve history but do not waive required live capability or authorize demo/alternate-provider substitution.

TradingView captures (requirements INT-02) remain untrusted offline design evidence, never runtime providers or executable target HTML. Real brokerage/alerts (requirements INT-04), external run bundles (INT-03) and missing-tick network acquisition (INT-07) have no v1 integration contract. Manual application backup is local work retention, not those deferred integrations.

## 16. Boundary Stress Tests

These are the designer's lightweight cohesion checks against upstream change pressure, not an independent adversarial review or a test suite.

| Change Pressure | Absorbing Boundary | Legitimate Secondary Impact | Unrelated Areas Untouched | Result / Correction |
|---|---|---|---|---|
| Ingestion adds older/newer month or replaces staged ticks with finalized month (EVO-01–EVO-02) | BND-010 read edge, BND-003 current selection | BND-002 coverage and BND-004 new-basis reads; new run selection | Existing run inputs/results, pricing and drawing semantics | PASS: DATAOWN-008/DEP-016 prohibit silent retained-basis replacement; source precision retained. |
| Another instrument gains local ticks (EVO-04, DATA-17) | BND-004 evidence lookup, BND-010 discovery | BND-002 assessed coverage; new results report actual evidence | Chart timeframes, provider network capability, exposure/account rules | PASS: no SP500 capability switch or automatic tick download. |
| Final history changes provisional weekly boundary (FR-33/FR-35, EVO-01) | BND-003 precedence/affected aggregation | BND-002 coverage, current bounded views and explicit new runs | Saved selected values/results, unrelated stored history and annotations | PASS: current selection differs from run authority. |
| Source publication or live API behavior differs from proposal (UNK-19/UNK-20) | BND-011 exchange | BND-002 evidence assessments and BND-003 qualified progress/status | Pricing, study formulas, layout edits | PASS structurally; acceptance remains open pending ARCH-GAP-01/ARCH-GAP-02. No provider protocol is assumed proven. |
| User edits commission or instrument contract values (FR-41/FR-50) | BND-009 monetary policy | BND-005 settings presentation and explicit run setting selection | Prior run results, archive data, availability rules | PASS: run-selected conventions retained; missing values remain blocked. |
| Future volume profile or detailed tick tool (EVO-05) | Future analysis capability using BND-004 evidence contracts | New volume meaning/coverage requirements and bounded view realization | Existing execution and accounting semantics | PASS: no v1 implementation; provider volume cannot silently become trade volume. |
| Future automatic missing-tick acquisition/permanent store (EVO-06) | New evidence/acquisition realization behind BND-004/BND-010/BND-011 capabilities | Explicit catalog/coverage and retained-input selection implications | Core price, independent-position and USD rules | PASS conditional on future requirements; no database/queue selected now. |
| Future extra slippage model (EVO-07) | BND-008 execution-pricing convention after new requirements | BND-007 explicit retained policy selection and result labels | Historical availability, chart periods, drawings | PASS: tick availability alone cannot enable a model. |
| Broader reference menus are requested (EVO-03) | Owning capability after new semantic requirements | Corresponding analysis/evidence contract only | Unrelated data, simulation and retention policy | PASS: captured menu presence is not a scope grant. |

## 17. Pass 1 Known Risks (`ARCH-RISK-*`)

| ID | Risk | Evidence | Consequence | Pass 2 / Upstream Owner |
|---|---|---|---|---|
| ARCH-RISK-001 | Current-catalog correction and saved-run restoration may accidentally mix bases | FR-45, CONS-15–CONS-16; DEP-013/DEP-016 | Changed outcomes or irreproducible backup | Pass 2 consistency/retention/change analysis; BND-007/BND-010 |
| ARCH-RISK-002 | Interruption between event progress and complete execution/checkpoint may duplicate or orphan effects | CONS-07/CONS-10/CONS-14; INV-05/INV-12; DEP-012 | Incorrect exposure/cash or resumed cursor | Pass 2 partial failure, concurrency, repeat safety and coherent retention |
| ARCH-RISK-003 | Unknown provider access/session/finality/applicability facts could be treated as proven | DM-GAP-01–DM-GAP-02 | Required live feature unusable or unsafe gap traversal/finalization | Integration evidence owner; Pass 2 degradation/security; ARCH-GAP-01–ARCH-GAP-02 |
| ARCH-RISK-004 | Heavy archive/tick reads could block routine chart interactions or receipt display | FR-36/FR-52/FR-56; SCALE-02–SCALE-03 | Missed accepted targets or false archive exhaustion | Pass 2 verification/diagnosis; downstream technology realization; preserve bounded capabilities |
| ARCH-RISK-005 | A late selection or second writer may replace valid displayed/saved work | CONS-01/CONS-06; INV-01/INV-12 | Mislabelled chart or lost analysis/run progress | Pass 2 concurrency/security; no writer-lock or cancellation mechanism chosen here |
| ARCH-RISK-006 | Undocumented numerical conventions or invented unit/rate values undermine sizing/fees | DM-GAP-04; POL-06–POL-08/POL-10 | Incorrect USD/risk/quantity despite structurally valid flow | Scoped numerical refinement before affected realization; ARCH-GAP-04 |
| ARCH-RISK-007 | Assumption labels may be dropped or stop-first mistaken for a price/path guarantee | ASM-01–ASM-02; INV-10 | Results falsely described as observed broker behavior | Pass 2 evidence/contract verification; BND-004/BND-008/BND-012 |
| ARCH-RISK-008 | Protected provider access and local restore may expand mutation/disclosure authority | SEC-02–SEC-04/SEC-07; POL-11–POL-12 | Source corruption, secret exposure or real brokerage capability | Pass 2 trust-boundary/replay/restore security analysis; BND-010/BND-011/BND-013 |

# PART III: RESILIENCE, CONCURRENCY, SECURITY & AUDIT MODEL (PASS 2)

## 18. Critical Resilience Workflows (`RW-*`)

Pass 2 preserves the G1-approved BND-001–BND-013 allocation. Mechanisms below are architectural decisions made in this pass; approval of Pass 1 is not represented as human approval of these new decisions. They realize existing consistency obligations without choosing a stack or physical schema.

| ID / Trace | Ordered Semantic Actions | Success / Failure and Authority | External Effects / Protected Rules |
|---|---|---|---|
| RW-001 — WF-001/WF-002 selection/analysis | Qualify context → read range → derive view → adopt matching selection/edit → checkpoint | BND-005 coherent valid analysis or prior valid state; saving may fail separately | Reads and retention outside working edit; INV-01–INV-03/INV-12–INV-13, CONS-01–CONS-03 |
| RW-002 — WF-003 acquisition/finality | Discover gap → acquire facts → validate → reconcile → derive affected bars → retain → publish catalog | BND-003 qualified complete/partial revision; prior generation on failure | Remote receipt/subscription independent of local publication; INV-02/INV-04/INV-11, CONS-09/CONS-16 |
| RW-003 — WF-004–WF-006 event/execution | Establish run/basis → continuity/evidence → effective instruction/price → whole valuation → publish event effects → checkpoint | BND-007 run ordering, BND-008 coherent effects, BND-009 money; hold original event on missing prerequisite | Local reads/retention only, no broker effects; INV-03–INV-10/INV-14, CONS-07/CONS-10/CONS-14 |
| RW-004 — WF-007 blocked resumption | Locate original block → qualify compatible prerequisite → retain completion → reevaluate original event → checkpoint | Same original event once; incompatible basis remains blocked/requires restart | New receipt is not historical execution time; INV-04–INV-05/INV-09, PRE-04 |
| RW-005 — WF-008 rewind/restart/delete | Bind confirmation to scope/version → prepare reconstruction/new basis → validate → replace generation → acknowledge | Entire earlier/restarted/deleted run or original unchanged; drawings independent | No remote compensation; CONS-13, INV-13, POL-09/POL-11 |
| RW-006 — WF-002/WF-008 save/recover/backup/restore | Capture coherent versions → retain input closure → validate → publish durable generation → acknowledge; backup pins generation; restore validates replacement | BND-010 last successful coherent state survives; incomplete candidates never saved | Local file writes/export independent of logical edits; INV-04/INV-12, PRE-10, FR-55 |
| RW-007 — all mutation/acquisition | Establish owner epoch → accept purpose-bound command → recheck at publication → retain result → revoke on lifecycle change | BND-013 one writable owner; stale/foreign context denied | Remote subscription teardown can be uncertain; POL-11–POL-12, CONS-06, SEC-07, FR-56 |
| RW-008 — WF-009 export | Bind source version/boundary → derive permitted representation → write local artifact → report outcome | Complete labelled export or honest failure; source work unchanged | Export file outside run publication; INV-03/INV-10, FR-18/FR-29, SEC-04/SEC-06 |

## 19. Transaction (`TX-*`) & Consistency Model (`CM-*`)

### Publication and Retention Model

A **working version** is logically coherent state; a **retained generation** is a successfully durable recoverable version. Autosave may lag working edits. Saving/unsaved identifies newer work; saved identifies the exact retained version. A simulated execution is never partially visible even while unsaved. Crash recovery may lose the unsaved suffix, as accepted P2 permits.

Choose immutable candidate content plus one atomic retained-generation publication: stage complete content and required evidence; validate integrity/references/versions; durably retain content; atomically advance the authoritative generation reference; acknowledge only after durable publication. The chosen platform must prove old-or-new recovery. Incomplete staging never becomes active truth. After publication but before acknowledgement, inspect the retained generation instead of repeating semantic actions. Reclaim only content unreferenced by active work, retained runs/checkpoints or a pinned backup/export; current-catalog replacement alone cannot release run inputs.

Acquired/recalculated history and run evidence remain application-owned local files. Copy required selected values from externally mutable sources before claiming retained run readiness; verified immutable owned content may be shared/deduplicated. A hard link to mutable sibling files or a checksum/path without preserved values is insufficient. Validate source stability while copying; changes produce a new coherent candidate or explicit failure, never a mixed revision. Preparation may show progress without claiming saved reproducibility.

Freeze declared run instruments/series/spans, available finer-bar/local-tick/FX evidence, absence/coverage qualifications and settings/conventions. All run reads, including supporting panels, use that retained selection. Expanding it with newly arrived observations requires explicit updated-data restart except compatible completion of an originally uncommitted prerequisite. New ticks cannot silently improve old results. This is selected-input file retention, not the deferred permanent-database ingestion feature. [FR-43–FR-45, DATA-18, POL-09]

### Atomic Local Scopes

Every row follows failure → property → required guarantee → smallest mechanism → burden. Atomic scope excludes remote effects and separately written exports.

| ID | Failure / Property | Atomic Scope and Minimum Mechanism | Exclusions / Failure Consequence / Burden | Source |
|---|---|---|---|---|
| TX-001 | Partial/late selection → matching analysis | Build complete candidate; compare selection/config/cursor generation; adopt selection, labels, outputs or explicit unavailable states together. One sync action updates both chart interval selections | Reads/save/previews excluded; save failure leaves whole edit unsaved. Generation-tagged results required | CONS-01–CONS-03, INV-01/INV-13 |
| TX-002 | Interrupted event → whole simulated effect | Per-run serialized transition against expected version; publish instruction/trigger/fill, fee, exposure/protection, USD effects, processed boundary and evidence together | Acquisition/checkpoint/rendering excluded; candidate failure preserves prior prefix; missing prerequisite blocks original event without its execution effects. Identity/version bookkeeping | INV-03/INV-05–INV-10/INV-14, CONS-07/CONS-14 |
| TX-003 | Partial finalization → honest catalog | Stage verified observation content/affected derivatives; atomically publish qualified catalog generation, lineage, coverage and recovery frontier | Provider receipts, saved runs and sibling sources excluded; prepublication failure keeps prior generation; lost notification re-reads published version. Staging/reference burden | CONS-04/CONS-08–CONS-09/CONS-16, INV-11 |
| TX-004 | Crash/save error → recoverable saved state | One immutable coherent checkpoint and required input closure; durable atomic reference publication before acknowledgement | Later working edits, credentials, unfinished acquisition excluded; unknown ack reconciles actual generation. Durability proof/cleanup burden | INV-04/INV-12, CONS-02/CONS-15 |
| TX-005 | Interrupted rewind/restore/delete → all-old/all-new replacement | Prepare/validate candidate, bind confirmation to expected generation, replace whole affected active state and durable checkpoint at one generation publication; fence prior epochs | Trading rewind excludes drawings; provider setup/credentials unchanged. Unknown result reconciles before another destructive operation. Temporary-space burden | CONS-13/CONS-15, FR-55, POL-11 |
| TX-006 | Repeated prerequisite completion → same original event once | Stage compatible missing-prerequisite evidence preserving committed basis; publish its selected completion, original-event whole effect and block resolution together through TX-002 | General catalog/spec/tick refresh excluded; incompatible completion stays blocked. Compatibility/reference proof burden | TR-15–TR-16, CONS-14–CONS-15, INV-04–INV-05 |

TX-002 covers one established event/decision transition, not an entire archive/playback session. Multiple ordered events may publish a coherent successful prefix. Preserve source precision and established occurrence order. Independent equal-time instructions may use retained instruction occurrence order as a declared simulation processing convention; it cannot assert an observed market path. Unknown entry/price/continuity prerequisites remain blocked; ASM-01 applies only to its approved protective ambiguity. New decisions cannot leap beyond unfinished existing-order evaluation.

### Consistency

| ID | Failure/Race → Property / Authority | Required Consistency and Visible Lag | Mechanism / Reconciliation / Burden |
|---|---|---|---|
| CM-001 | Async result → matching basis/cursor; BND-005/BND-007 | Immediate matching context at adoption; loading/unavailable or last correctly labelled view while pending | Generation compare and coherent view envelope TX-001; discard obsolete results; context tracking |
| CM-002 | Event/decision race → coherent effects; BND-007/BND-008 | Immediate whole event outcome or explained original-event block | Per-run serialization/expected-version TX-002; re-decide conflicts; coordinator backpressure |
| CM-003 | Edits outrun save → truthful durability; BND-010 | Explicit eventual autosave, no invented save-delay guarantee; newer work remains unsaved/error | Coalesce coherent captures, monotonic version-bound acknowledgements TX-004; retain prior success; working/saved version tracking |
| CM-004 | Live/backfill overlap → qualified current data; BND-003 | Atomic published revision; staging may remain partial/provisional/recovering | TX-003 qualified generation/derivatives, re-read overlaps; staging and conflict qualification burden |
| CM-005 | New catalog versus resumed run → original basis; BND-007 | Zero automatic substitution of committed inputs/settings/results | Owned immutable closure and version-bound reads; validate before resume; missing evidence blocks; retention space burden |
| CM-006 | Rewind/restore versus async progress → coherent replacement | Old state remains during preparation/cancel; successful replacement advances epoch, drawings independent | Expected-version confirmation and TX-005; reject stale candidates; temporary duplicate content |
| CM-007 | Heavy tick/save work versus current display → FR-36/SCALE-03 | Live display within 1 second of local receipt; durable history may lag explicitly; replay remains bounded | Independently scheduled bounded display/read path, qualified TX-003 persistence; measure lag, never conceal dropped continuity. Scheduling burden |

No distributed transaction, remote broker compensation, outbox or delivery queue is justified: provider interactions are reads/subscriptions and money effects are local simulation. Rewind is an authorized reconstruction, not compensation for a real order.

## 20. Stepwise Partial-Failure Matrix (`FAIL-*`)

SUCCEEDED means known completion, FAILED means known absence of successful completion, NOT_ATTEMPTED means not reached, UNCERTAIN means unknown external/publication outcome. Later steps are NOT_ATTEMPTED unless stated. A prepared candidate has no active effects before publication.

| ID | Workflow / Failure Frontier | Prior SUCCEEDED | FAILED / UNCERTAIN; Later NOT_ATTEMPTED | User/Invariant Outcome and Safe Recovery |
|---|---|---|---|---|
| FAIL-001 | RW-001 context/parameter check | Request received | Validation FAILED; read/edit/save NOT_ATTEMPTED | Prior valid analysis intact; correct input/authority, no automatic resubmit |
| FAIL-002 | RW-001 read/calculate/adopt | Context qualified, perhaps range read | Read/calculation FAILED or adoption obsolete; publish NOT_ATTEMPTED | Keep last labelled valid view; retry read only in valid generation |
| FAIL-003 | RW-001 saved notification | Working edit and durable checkpoint published | UI acknowledgement FAILED | Re-read exact retained version; never replay edit to repair status |
| FAIL-004 | RW-002 provider request | Gap qualified | Request FAILED or response UNCERTAIN; validate/publish NOT_ATTEMPTED | Existing history readable; gap unresolved; retry qualified read, never infer closure |
| FAIL-005 | RW-002 decode/validate | Response received | Validation FAILED; derivatives/publish NOT_ATTEMPTED | Reject unusable candidate, prior catalog intact; response success is not validity |
| FAIL-006 | RW-002 aggregate/stage | Qualified facts, perhaps some staged content | Candidate completion FAILED; publication NOT_ATTEMPTED | Report partial progress, retain prior qualified generation; reuse verified spans and re-decide overlaps |
| FAIL-007 | RW-002 publish catalog | Complete candidate retained | Publication/ack UNCERTAIN after crash | Inspect active reference/closure: old or complete new revision; no blind duplicate append |
| FAIL-008 | RW-002 receipt→display | Actual local receipt | Display FAILED/late; retention independently succeeds/fails | Explicit display/stale limitation, measured target violation; rebuild current bounded view, catch up qualified history |
| FAIL-009 | RW-003 continuity/evidence | Prior coherent event prefix | Next prerequisite FAILED/unresolved; price/commit NOT_ATTEMPTED | Pause before unknown interval; resolve backfill/session evidence, no later-price bypass |
| FAIL-010 | RW-003 price/quantity/valuation | Eligible event, perhaps pricing candidate | Spec/FX/price requirement absent; effect publication NOT_ATTEMPTED | Original-event block, no fill/fee/exposure/USD partial effect; resume only compatible original event |
| FAIL-011 | RW-003 construct/version-check | Whole candidate computed | Candidate FAILED or version obsolete; publish NOT_ATTEMPTED | Prior whole state intact; re-read/re-decide, no blind effect retry |
| FAIL-012 | RW-003 logical publish→save | Whole working event published | Checkpoint FAILED or not yet attempted | Coherent working result unsaved; crash may lose unsaved suffix; retry checkpoint, not execution |
| FAIL-013 | RW-003/RW-006 durable acknowledgement | Required content retained | Durable reference/ack UNCERTAIN | Saving/unknown until reference inspected; reconcile same operation before retry |
| FAIL-014 | RW-004 prerequisite compatibility | Block located, new fact acquired | Applicability/compatibility FAILED; effect NOT_ATTEMPTED | Preserve block/prior results; correct prerequisite or explicit restart |
| FAIL-015 | RW-004 apply completion | Compatible evidence staged | Transition FAILED or rewind invalidates epoch; publish NOT_ATTEMPTED | Original block or newer state remains; discard stale callback; same original identity on valid retry |
| FAIL-016 | RW-005 confirm/prepare | Target selected, perhaps confirmed | Authority/version/reconstruction FAILED; replacement NOT_ATTEMPTED | Original run/drawings unchanged; fresh confirmation if affected version changed |
| FAIL-017 | RW-005 replacement ack | Complete validated candidate staged | Replacement UNCERTAIN | Resolve whole old/new generation and epoch before another destructive command |
| FAIL-018 | RW-006 retain evidence | Coherent capture obtained | Copy/integrity/reference FAILED; publish NOT_ATTEMPTED | No save/backup success; prior checkpoint safe, source untouched; no mutable-path fallback |
| FAIL-019 | RW-006 backup write | Selected generation/closure validated | Export FAILED/UNCERTAIN; active work unchanged | Partial output not valid backup; verify integrity or retry same pinned generation |
| FAIL-020 | RW-006 restore validation | Backup read/staged | Path/schema/content/coherence FAILED; replacement NOT_ATTEMPTED | Existing work intact; reject candidate, no partial merge or credential restore |
| FAIL-021 | RW-007 owner acquisition/recheck | Request/task prepared | Owner acquisition FAILED or stale epoch; mutation NOT_ATTEMPTED | Read-only/denied; stale work cannot upgrade authority by retry |
| FAIL-022 | RW-007 stop/reconnect | Local session revoked | Remote teardown UNCERTAIN; late receipts possible | Fence/drop old callbacks; reconcile remote session if supported; fresh catch-up detects losses |
| FAIL-023 | RW-008 export write/ack | Permitted bounded snapshot prepared | Output FAILED/UNCERTAIN; no run mutation | Verify complete artifact or regenerate same snapshot; no false complete-export claim |

## 21. Concurrency & Race Analysis (`CONC-*`)

One writable tab does not eliminate async races. The authoritative local mutation capability must exclude other owners and reject stale epochs at publication, including queued saves/acquisition callbacks. Use exclusive ownership plus changing owner/run/restore epochs; a timeout alone cannot grant a second writer while the old writer can publish. Technology selection must prove exclusion across supported tabs/processes.

| ID | Competing Operations / Bad Interleaving → Property | Guarantee / Minimum Mechanism | Conflict Outcome / Burden |
|---|---|---|---|
| CONC-001 | Two tabs/processes both observe free owner → CONS-06/INV-12 | Exclusive mutation owner and publication fencing across all writes | Loser read-only/denied; no timeout-only takeover; lifecycle/owner proof burden |
| CONC-002 | Selection A resolves after B under B labels → INV-01 | Selection/config/cursor generation checked on complete adoption TX-001 | Discard obsolete A; cancellation optional; carry context on every result |
| CONC-003 | Step/play/seek versus new action reuses processed event → INV-03 | One per-run sequencer, effective boundary/expected version TX-002 | Re-read/re-decide; no retroactive modification; backpressure burden |
| CONC-004 | Close versus protection/two closes share stale remainder → INV-05–INV-07 | Same run scope and target remainder/version validation | One ordered transition wins; next sees current exposure/invalid target; no duplicate close |
| CONC-005 | Older save finishes after newer save/edit → INV-12 | Ordered checkpoint generation publication, exact-version acknowledgements | Drop/coalesce stale saves; never regress retained reference or mark newer work saved |
| CONC-006 | Backfill/finality/live overlap or source changes while copied → INV-02/INV-11 | Stable-source validation, expected catalog generation and precedence re-evaluation TX-003 | Reconcile from current revision; unresolved differing final facts explicit conflict, not timestamp-only last-writer wins |
| CONC-007 | Run snapshot/resume versus new ticks/catalog/spec edits → INV-04 | Owned immutable selected evidence closure and run convention version | New catalog affects new selection only; source-copy change retries coherently |
| CONC-008 | Rewind/restore versus play/resume/save callback resurrects discarded exit → CONS-13/CONS-15 | Expected generation plus owner/run/restore epoch at publication TX-005 | Drop stale results; changed destructive target requires fresh confirmation; epochs propagate into persistence |
| CONC-009 | Delayed provider response after stop/revocation → POL-11–POL-12/FR-56 | Recheck acquisition epoch, runtime authority and data-only purpose | Drop stale callback; fresh startup/reconnect catch-up; no inherited stale authority |
| CONC-010 | Backup/read/cleanup versus deletion reclaims referenced inputs → INV-04/INV-12 | Pin coherent retained generation and input closure; reclaim only unreferenced owned content | Export complete snapshot or fail honestly; reference/pin accounting burden |
| CONC-011 | Duplicate sync/third-chart command → CONS-03/FR-17 | One expected-version layout command, coherent max-two arrangement transition | Duplicate returns original result; third chart rejected semantically |
| CONC-012 | Old monetary task versus changed run/settings → INV-04/INV-09 | Bind result to run basis/event/specification/convention versions | Re-decide current authorized context; never revalue prior results silently |

Run ordering is scoped per run; catalog revision conflict checks cover affected series/overlap. Do not impose extra global market chronology across unrelated instruments/runs.

## 22. Idempotency (`IDEM-*`), Retry (`RETRY-*`), Ordering (`ORDER-*`) & Timeouts

### Idempotency

Assign logical command identity when first accepting that intent; transport retries reuse it. Two deliberate equal user actions are distinct occurrences. Scope includes local work, owner epoch, resource/run/layout and run/restore epoch. Same identity/different canonical semantic payload is a conflict. Retain operation outcomes with the state they protect; recovered older checkpoints do not silently retransmit lost unsaved commands from the UI.

| ID | Duplicate → Property | Identity / Minimum Mechanism | Repeat / Conflict / Coverage and Burden |
|---|---|---|---|
| IDEM-001 | Repeated edit/instruction → no duplicate intent | Accepted command occurrence + work/resource/epoch, outcome retained with transition | Return original result/version; changed terms under same identity rejected. Covers action/effective boundary/creation/deletion; outcome-mapping burden |
| IDEM-002 | Reevaluated/resumed event → INV-05 | Run epoch + established event occurrence + instruction/target/protection + effect role; applied result in same transition | Return existing whole effect, no new fee/position. Conflicting evidence under selected basis rejected/restart; trigger/fill roles distinct; no timestamp/value-only tick dedup |
| IDEM-003 | Repeat bar response → unique qualified catalog | Provider/instrument/period/side/bucket + revision/provenance; content compare before publication | Equal values reuse content; differences become explicit revision/conflict under precedence; covers lineage/coverage, not arbitrary tick collapse |
| IDEM-004 | Lost save/rewind/restore ack → no repeated replacement | Captured source/target generation + operation occurrence + owner/run/restore epoch, outcome with generation | Reconcile/return matching published generation; changed target under same identity rejected. Requires outcome retention through uncertain completion |
| IDEM-005 | Repeated export → no false output success | Request occurrence + pinned source generation + local artifact identity | Verify complete matching artifact then return; conflicting request needs new intent. Partial artifacts validated, source unchanged |

### Retry Strategy

Every retry rule identifies the property risk, smallest safe action and added burden. Stop when context/authority is obsolete, request cancelled, prerequisite needs evidence/user action, or provider instructs rate limiting. No arbitrary attempt count, delay or timeout is invented; concrete bounded/cancellable scheduling is selected under DEFER-006.

| ID | Failure/Action → Property | Classification / Guarantee | Trigger, Stop and Final Outcome / Burden |
|---|---|---|---|
| RETRY-001 | Transient local/provider history read → correct basis | safe as-is for read; normalize facts via IDEM-003 | Retry still-valid read, honor rate-limit instructions; stop invalid/permanent denied/cancelled. Remain unavailable/error with preserved history; bounded progress burden |
| RETRY-002 | Command response lost → no duplicate action | requires idempotency/dedup IDEM-001 | Same logical intent and valid epoch only; return existing outcome or explicit unknown, never fresh intent identity. Retained-outcome burden |
| RETRY-003 | Version conflict/late result → no stale mutation | re-read/re-decide | Fresh facts/decision; confirmation renewed when meaning/target changes. Drop obsolete candidate, not blindly reapply effects |
| RETRY-004 | Durable publication unknown → truthful saved state | reconcile first after UNCERTAIN, IDEM-004 | Inspect active reference/integrity; published means acknowledge, absent means same still-current candidate may retry; ambiguous/corrupt pauses writes. Recovery-inspection burden |
| RETRY-005 | Missing FX/spec/session/ordering prerequisite → no invented effect | no automatic execution retry; prerequisite-driven reevaluation IDEM-002 | Only compatible resolved fact and current epoch allow original event; remain explained blocked or deliberate restart. Original-event retention burden |
| RETRY-006 | Live session interrupted/unknown subscription → bounded feed lifecycle | reconcile first, epoch-bound callbacks and proven-occurrence dedup | Reconcile previous session if possible, revoke old epoch, establish fresh session/catch-up; stop denied/cancelled/rate-limited. No demo/false continuity; provider evidence burden |
| RETRY-007 | Known failed checkpoint/export → preserve coherent work | safe retry immutable captured content; publication/output dedup IDEM-004/IDEM-005 | Reuse verified content, stop obsolete context/persistent storage error; prior checkpoint valid, new work unsaved, incomplete output not success. Staging-space burden |
| RETRY-008 | Destructive intent cancelled/denied/stale → no unauthorized repetition | no automatic retry | Fresh valid intent/authority/confirmation required; preserve old work; never replay old confirmation into new epoch |

### Ordering and Timeout Rules

| ID | Failure Scope → Property | Required Order / Minimum Guarantee | Late/Uncertain Outcome and Burden |
|---|---|---|---|
| ORDER-001 | Per-run scrambled/reused events → INV-03/INV-05 | Preserve established occurrence order/precision; existing eligible events before new decisions; seek same transitions as stepping | No invented timestamp increment/redraw order; stale version rejected; retain sequencing evidence |
| ORDER-002 | Per instruction trigger/fill → POL-04–POL-05 | Acceptance → effectiveness after decision → trigger if applicable → next eligible executable evidence; no added delay/slippage | No processed-event fill; unresolved chronology labelled/blocked under approved limits; trigger fact does not itself establish fill |
| ORDER-003 | Per affected catalog revision partial derivatives → INV-11 | Validate/retain observations and affected derivatives before qualified publication; final precedence current only | Late provisional facts cannot overwrite final history; re-evaluate obsolete responses |
| ORDER-004 | Per saved/replacement generation ack loss → INV-12 | Durable content → durable atomic reference → exact-version saved acknowledgement | Resolve uncertainty before repeat; older save cannot regress retained reference |
| ORDER-005 | Historical view mixed panels → CONS-05/CONS-16 | One context generation; unavailable/slow panels explicit within same boundary | Never earlier cursor labels with later values; obsolete callbacks discarded |
| ORDER-006 | Remote/local timeout → correct uncertainty | Missing read response means unavailable facts, provider processing/session may be UNCERTAIN; mutation timeout UNCERTAIN unless nonpublication proven | No cross-boundary rollback assumption; reconcile RETRY-004/RETRY-006; values require evidence |

## 23. External Dependency Failure Model (`EXT-*`)

| ID | Dependency / Authority | Degradation and Timeout | Retry, Duplicate, Rate-Limit and Outage / Trust Rule |
|---|---|---|---|
| EXT-001 | INT-001 sibling archive, external observation facts | Missing/unreadable/changed input unavailable; unrelated retained runs unaffected; no source writes | RETRY-001, stable-source copy, schema/precision/coverage validation. Equal-time ticks distinct unless occurrence identity proves duplication; confined paths, no source substitution |
| EXT-002 | INT-002 historical M1/H1, externally attributed facts | Preserve prior catalog; partial/empty response not closure/finality; remote read outcome can be uncertain | RETRY-001/IDEM-003, validate requested span/side and provider feedback; show unresolved gaps, pause affected trading; no recovery-time guarantee; ARCH-GAP-02 evidence required |
| EXT-003 | INT-003 live-account data-only feed | Receiving/closure/stale/failed/recovering distinct; missing receipt not price movement; remote teardown may be uncertain | RETRY-006, acquisition epochs and actual occurrence identity; catch up from last usable boundary, honor access/rate limits. No demo/broker balance/order fallback; required live acceptance still gated |
| EXT-004 | BND-010 local storage/export, authoritative local publication | Disk-full/corrupt/missing content/unknown durability prevents new saved claim; keep valid prior generation | RETRY-004/RETRY-007; inspect reference/closure before new writes; work coherent but unsaved, resume missing originals blocked. Prove platform durability, no unverified filesystem promise |

## 24. Security Under Resilience Pressure (`SECR-*`) & Scope Isolation (`TEN-*`)

The sole analyst need not log into an invented application account. Unauthenticated negative verification means an unbound/foreign caller without local mutation capability. A browser/loopback realization enforces origin/capability isolation; localhost alone grants no authority. A desktop realization enforces equivalent IPC/capability isolation. Standards select realization, not the security obligation.

| ID | Boundary / Abuse Mode | Required Guarantee / Failure Handling |
|---|---|---|
| SECR-001 | Foreign/unbound caller or second writer forges mutation context | Purpose/work-bound owner capability checked at acceptance and publication; stale/retried context denied with no mutation, never upgraded automatically |
| SECR-002 | Delayed destructive command reuses confirmation after target change | Bind confirmation to action/target/expected generation/epoch; reject stale confirmation, no automatic destructive retry |
| SECR-003 | SDK brokerage capability/credentials leak through errors | Protected data-only edge exposes no order/amend/cash command; sanitize error mapping; no raw credentials/session payload in browser/log/audit/export |
| SECR-004 | Manifest/backup/captured label grants arbitrary path/code | Canonical read/write root confinement, reject escaping symlinks/archive paths and ambiguous duplicate entries, bounded parser resources, labels as text; invalid candidate never active; captured HTML/scripts never executed |
| SECR-005 | Restore resurrects old live writer/session command authority | Backup excludes credentials/bearer capabilities; content validated then fresh owner/restore epoch; historical action facts not reissued as transport commands; stale callbacks fenced |
| SECR-006 | Cross-run target/evidence/cache substitution | Validate run/basis/epoch/position chain on every result/action; cache key includes basis/convention/boundary; wrong scope denied even if target ID exists |
| SECR-007 | Acquisition publishes after stop/revocation | Recheck acquisition epoch/runtime purpose at publication; drop late callbacks, fresh startup/reconnect catch-up; already published qualified facts remain valid |
| SECR-008 | Future/private data leaks through export/diagnostic/latest cache | Bounded replay disclosure at edge; no implicit latest lookup; secret/private captures excluded, diagnostic context sanitized; unavailable output fails honestly |

No application tenants/admin overrides exist (AUTH-01–AUTH-03). TEN IDs specify analogous local ownership isolation rather than a new tenant platform. Literal cross-tenant login/role tests are inapplicable; foreign/wrong-work/run/layout negative tests are required.

| ID | Scope Origin / Tampering Mode | Required Binding / Callback and Cache Rule |
|---|---|---|
| TEN-001 | Local capability versus attacker-selected workspace/path | Authoritative owned roots/owner epoch, not payload path, determine resource access; no remote/admin override |
| TEN-002 | BND-007 run context versus transplanted position/event/FX | Bind full run/basis/epoch/target chain; stale pre-rewind or cross-run callback rejected; retry cannot change scope |
| TEN-003 | BND-005 layout/instrument versus equal-looking drawing ID | Layout/instrument lookup and financial anchors; timeframe switch/rewind cannot write unrelated annotations |
| TEN-004 | Restored retained generation versus escaping paths/current-catalog substitution | Stage in owned confinement, validate closure/integrity/semantic scope before replacement; fresh authority, no credentials/capabilities imported |

## 25. Audit Semantics (`AUD-*`) & Sensitive Data

Audit here is required durable domain/provenance evidence, not a new permanent security journal or remote telemetry system. Retained facts are immutable within their selected version; authorized rewind removes later active-run facts under BR-17, and reset/deletion follows POL-11. No hidden permanent discarded-trade archive or indefinite rejected-action log is required. Minimal current operation outcome evidence for uncertain-publication reconciliation stays with its generation; bounded local diagnostic logs remain separate.

Record relevant local actor/epoch (no provider account identity), work/run/layout target, logical occurrence, historical event/effective boundary, basis/version/conventions, semantic outcome and correlation. Wall time never substitutes for historical event time.

| ID | Durable Evidence / Owner | Required Facts and Failure/Retry Visibility | Exclusions |
|---|---|---|---|
| AUD-001 | Inputs/current generation, BND-003/BND-010 | Provider/basis/precision/version, origin/lineage, validation/coverage/finality evidence; partial recovery not complete, repeats not duplicate bars, selected run references remain original | Secrets, private captured content, unsafe path disclosure |
| AUD-002 | Actions/triggers/execution/block, BND-007/BND-008 | Target/effective/processed occurrence, side/price/quantity, observed versus ASM labels, selected spec/FX/fee/rounding and whole effects; duplicate same outcome, block no fill, rewind discards suffix | Actual-broker claims, invented chronology, zero-profit placeholders |
| AUD-003 | Saved/backup/restore/replacement, BND-010 | Source/target generation, included closure/integrity, operation outcome/confirmation scope; unknown publication reconciles, failed candidates not active | Credentials/tokens/previews/unrelated archive; no permanent discarded-run journal |
| AUD-004 | Authored analysis, BND-005/BND-010 | Committed layout/instrument object settings/anchors, meaningful undo/redo; cancelled previews absent, failed save not saved, drawing independent of rewind | Claims user annotations are discovered market facts |

Rejected/unauthorized requests mutate no domain history; sanitized LOG-004 can explain rejection without inventing accepted trading facts. A saved current block includes HIST-08 original context; indefinite block-history retention is unnecessary.

| Sensitive Data | Allowed Use / Required Exclusions |
|---|---|
| Provider credentials/session material | Protected BND-011 setup/runtime only; never browser-facing views, checkpoint/backup/report/log or raw retry errors |
| Captured private identities/figures/DOM | Offline untrusted reference only; no product execution/embedding/private fixtures |
| Analyst layouts/actions/results | Local owned work and explicit local export; no remote telemetry by default, no raw financial-history diagnostic dumps |
| Market/spec/FX evidence | Qualified values only to legitimate scoped consumers; preserve precision; no whole dataset logging/current-rate substitution |
| Writer capability/confirmation context | Trusted local authority/edge only; bearer material absent from backup/provider/export; restored facts never grant authority |

## 26. Change-Impact Analysis (`CHG-*`) & Architecture Corrections (`RCORR-*`)

| ID | Pressure / Absorbing Boundary | Legitimate Secondary Impact | Unrelated Areas Untouched / Correction |
|---|---|---|---|
| CHG-001 | Longer history/new local ticks/finalized month; BND-010/BND-003/BND-004, EVO-01–EVO-04 | TX-003 source stability, CM-005 selected retention, IDEM-003 occurrence handling; TF-002/TF-004 | Existing run facts/settings, drawings/fill policies unchanged; no correction |
| CHG-002 | Changed API/session/publication/access facts; BND-011/BND-002/BND-003 | EXT-002–EXT-003, SECR-003, TF-008 actual evidence gate | Execution/monetary rules unchanged; missing facts block rather than relax; no correction |
| CHG-003 | Instrument/fee/numerical convention edits; BND-009/BND-007 | CM-005/CONC-012, retained-version compatibility, TF-003/TF-004 | Prior results/archive unchanged; no correction |
| CHG-004 | Storage representation migration; BND-010, DEP-013 | TX-004–TX-005 durability, closure/backup compatibility, TF-006/TF-007 | Semantic owners unchanged; migrate original values/results without reexecution against latest data; no correction |
| CHG-005 | Renderer/interaction scheduling; BND-012/BND-005/BND-006 | TX-001 context guards, bounded scheduling, TF-009/TF-010 | Event order, accounting/retained evidence unchanged; no correction |
| CHG-006 | Future profiles/tick-download/slippage/external-run import; EVO-05–EVO-07/FR-30 | New requirements/evidence/security review at owning capability | No v1 feature activation by incidental capability; no correction in v1 |

No RCORR entry is needed: Pass 2 adds guarantees/mechanisms within approved ownership. New implementation evidence that invalidates a guarantee must explicitly reopen the owning artifact and readiness; approval cannot conceal a later structural correction.

# PART IV: VERIFICATION STRATEGY & PRODUCTION OPERABILITY (PASS 2)

## 27. Verification Goals (`VG-*`) & Semantic Acceptance Criteria (`AC-*`)

These are required future implementation proofs, not tests run by this documentation task. Property → concrete defect → direct observable evidence → narrowest boundary governs selection; no arbitrary coverage percentage or live-provider-only business verification is imposed.

| ID | Property / Upstream Source | Defect and Observable Proof | Narrowest Boundary / Criticality |
|---|---|---|---|
| VG-001 | Honest identity/UTC/precision/coverage; INV-01–INV-02/INV-11, FR-51–FR-52 | Mislabelled/wrong-side/false continuity/resident cap; exact qualified values/bounds/gap decisions | Domain + source contract; critical |
| VG-002 | Historical boundary/decision effectiveness; INV-03, FR-20/FR-40/FR-53 | Future weekly high/latest watchlist/FX/visible-close fill; bounded views/effective event outcomes | Domain/workflow; critical |
| VG-003 | Coherent price/hedging/protection/USD/sizing; INV-05–INV-10/INV-14 | Worse limit/invented stop price/over-close/bad fee/partial effects; exact whole outcomes/evidence | Domain; critical |
| VG-004 | Retained basis/prefix reconstruction; INV-04, CONS-13–CONS-16 | New ticks/settings rewrite run or orphan exit after rewind; original-value/state comparisons | Workflow; critical |
| VG-005 | Saved meaning/old-or-new recovery; INV-12, FR-44–FR-45/FR-55 | Lost acknowledged save/mixed restore/missing inputs; real reopen and closure inspection | Persistence integration; critical |
| VG-006 | Local authority/scope/data-only purpose; POL-11–POL-12, SEC-02–SEC-04/SEC-07 | Foreign/stale/wrong-run mutation or secrets/broker effects; denied effects and clean output | Workflow/contract; critical |
| VG-007 | Repeat/failure/order rigor; CONS-07/CONS-10/CONS-12 | Duplicate fill/save regression/late callback; controlled failure frontier/barrier evidence | Workflow + real persistence for physical risk; critical |
| VG-008 | Provider normalization/degradation; FR-31–FR-35/FR-56 | Demo substitution/false closure/finality/concealed outage; qualified normalized facts/status | Contract + actual-provider acceptance; critical for affected integration |
| VG-009 | Authored analysis/accessible interaction; FR-10–FR-18/FR-24–FR-25, INV-13 | Invalid preview persists/duplicate redo/sync/drawing lost; semantic state plus keyboard/focus outcomes | Domain/workflow + selective rendered E2E; important |
| VG-010 | P3/full archive; SCALE-03, FR-36/FR-52/FR-56 | Tick stall/archive cap/exceeded latency; hardware/workload/timing and range-read evidence | Performance integration/selective E2E; important |
| VG-011 | Durable labels/secret-free exports; INV-10, FR-18/FR-29/FR-55 | Approximation as observed/backup missing inputs/secrets exposed; artifact/evidence inspection | Contract/persistence integration; critical |

| ID | Initial Context / Trigger | Expected Semantic Outcome | Required Evidence / Source |
|---|---|---|---|
| AC-001 | Valid chart, failed or late different-basis request | Prior correctly labelled view retained; obsolete result cannot adopt current labels | View/context generation comparison; VG-001, CONS-01 |
| AC-002 | Cursor inside W1/MN1, later/live observations arrive | Later high/low/close/study/watchlist/detail/FX/report hidden, unavailable explicit | Every bounded consumer's values; VG-002, FR-20 |
| AC-003 | Submit/modify at processed boundary, change playback speed/forward seek | Eligible later event only; identical retained actions/inputs reproduce; cancellation cannot undo filled history | Effective/event identity and outcomes; VG-002/VG-007, ORDER-001–ORDER-002 |
| AC-004 | Eligible unresolved SL/TP after finer bars/local ticks | Labelled stop-first only within PRE-07; known earlier TP wins; missing entry/price/gap not invented | Evidence hierarchy and retained labels; VG-003, ASM-01 |
| AC-005 | Gap-crossed long SL versus buy limit/TP; chart side toggled | Long close uses bid; buy limit never above limit and better eligible gap quote honored; chart side changes no fills | Exact executable side/price/provenance; VG-003, POL-05/INV-08 |
| AC-006 | Opposite entries then targeted partial/full close | Independent hedges; only target reduced, fee per execution, protection resized/cancelled; over-close rejected | Whole quantity/account effects; VG-003, INV-05–INV-07/INV-14 |
| AC-007 | Risk SL/fee/increments then nonpositive balance/missing units/FX | Largest valid quantity within planned budget rounded down; below minimum rejected; invalid/missing prerequisite blocked; fixed mode no margin check | Independent declared-convention arithmetic; VG-003, FR-49–FR-50/FR-54 |
| AC-008 | Event lacks historical conversion/session evidence, later prerequisite arrives | No partial effects; compatible resolution uses original time/price once; current-rate substitution forbidden | Whole blocked/prior/result comparison; VG-003/VG-004, CONS-14 |
| AC-009 | Empty/weekend/zero volume versus known closure/unexplained gap | Preserve valid rows; no absence-only closure; unresolved gap pauses, known closure follows gap-price policy | Coverage/continuity evidence; VG-001/VG-008, FR-46/FR-51 |
| AC-010 | New final/current bars/ticks/specs after saved run | Original observations/settings/results unchanged on resume; explicit restart may select new basis | Retained precision/convention/value comparison; VG-004, FR-45 |
| AC-011 | Cancel/confirm rewind after exit with independent drawing | Cancel unchanged; confirm retained prefix/open exposure, no removed later fee/exit, drawing unchanged | Cursor/action/effect/anchor comparison; VG-004/VG-009, CONS-13 |
| AC-012 | Crash each write/publication/ack frontier; old save finishes late | Coherent old/new saved generation, acknowledged work survives, unsaved suffix may be lost; no retained-version regression | Actual-storage reopen/closure checks; VG-005/VG-007, TX-004 |
| AC-013 | Unbound/foreign caller, second writer, stale restore callback, wrong-run target | Denied without effect; retry cannot upgrade authority; current owner positive case works | State unchanged/sanitized reason; VG-006, SECR-001/SECR-005–SECR-006, TEN-001–TEN-002 |
| AC-014 | Unsafe/corrupt/missing-input backup or credentials/capabilities in restore | Reject unsafe/incomplete artifact, preserve old state; valid backup restores original content under fresh owner | Artifact/reference validation; VG-005/VG-006/VG-011, TEN-004 |
| AC-015 | Provider timeout/rate-limit/denied entitlement, reconnect duplicates | History readable, honest stale/recovering/gap state; no demo/broker effect; qualified duplicate-free catalog | Controlled responses and protected-edge operation inspection; VG-008, EXT-002–EXT-003 |
| AC-016 | Pan beyond 100k resident set while selective ticks/live receipt active | Complete archive accessible; accepted two-chart workload meets P3 | Recorded hardware/readiness/timing boundaries; VG-010, SCALE-03 |
| AC-017 | Keyboard study/drawing/settings/sync/export; invalid/cancel preview | Named/focused usable controls, valid prior state retained, no duplicate redo/sync, max two charts; local image labelled | Semantic assertions plus rendered wiring; VG-009/VG-011, FR-24 |
| AC-018 | Same intent/event retry versus deliberate equal second action/conflicting payload | Same identity same original effect; new intent distinct; conflicting identity rejected, no timestamp-only tick collapse | Operation/effect state comparison; VG-007, IDEM-001–IDEM-005 |

P3 thresholds: initial ready-local viewport **<2 seconds**, interaction **p95 <50 ms**, live display **within 1 second of local receipt**. Benchmark two charts with 100k resident bars each, four study panes and 100 drawings total on recorded desktop hardware. “Ready-local” does not exclude range read/calculation/render work after a request by relabelling it cache preparation. Network publication lag is separate from local receipt→display timing; no guaranteed provider recovery deadline is introduced.

## 28. Risk-Based Test Families (`TF-*`)

Use controlled clocks/responses, explicit publication failure hooks and barrier-controlled races, not sleep-based tests. Verify actual storage with the chosen platform. Domain expected examples/property assertions must not mirror implementation calculations. Supply approved scoped conventions before affected numerical tests; their absence is a slice prerequisite, not a guessed fixture.

| ID | Goals → Defect / Direct Proof | Boundary and Cases | Proves / Intentional Limit |
|---|---|---|---|
| TF-001 | VG-001/VG-002 → wrong basis/future knowledge; exact qualified values/decisions | Domain: eight UTC periods including MN1/week boundaries, bid/ask/precision, completed versus final, missing/warm-up, flags/readability, closure versus empty/weekend, cursor-limited panels/FX | Policies, not actual provider truth or UI wiring |
| TF-002 | VG-002/VG-003 → invalid price/chronology/effects; exact whole outcome | Domain: ORDER-001–ORDER-002, finer bars before local ticks, equal-time distinct occurrences, actual TP-first versus ASM-01, eligibility, better-limit/gap SL/stop trigger, hedging/protection/manual/full fills; negative missing entry/price/continuity | Execution/invariants, not broker liquidity reconstruction or transport/storage |
| TF-003 | VG-003 → wrong monetary risk/fees; independent arithmetic | Domain: three commission modes/zero default/entry/every partial exit, applicable historical nonfuture bid/ask FX, stale/future rate rejection, minimal/increment/max-budget quantity, nonpositive balance | Monetary rules under approved numerical convention, not invented contract values |
| TF-004 | VG-004/VG-007 → basis mixing/wrong rewind; retained evidence/state comparison | Workflow: catalog/tick/spec updates after snapshot, unchanged resume, compatible block completion versus restart, cancelled/confirmed rewind, CONC-007/CONC-008/CONC-012, FAIL-009–FAIL-017 | Ownership/orchestration, not physical durability |
| TF-005 | VG-006/VG-007 → stale/foreign/duplicate mutation; no-effects and barrier proof | Workflow: CONC-001–CONC-005/CONC-008–CONC-009/CONC-011–CONC-012; IDEM-001–IDEM-004; RETRY-002–RETRY-008; FAIL-001/FAIL-011/FAIL-014–FAIL-017/FAIL-021–FAIL-022; unbound/foreign/second-owner/wrong-run/old-epoch negative plus valid owner | Coordination/authority; actual physical owner exclusion additionally TF-006 |
| TF-006 | VG-005/VG-007 → torn/lost/regressed save; actual reopen/closure proof | Persistence integration: interrupt TX-003–TX-006 at every stage/after publication-before ack; disk full/corrupt/missing inputs, older save completion, writer handover, source copy changes/cleanup pinning; CONC-001/CONC-005–CONC-010, FAIL-006–FAIL-007/FAIL-012–FAIL-020 | Actual chosen-platform durability/fencing, not untested remote-filesystem or malicious OS guarantees |
| TF-007 | VG-005/VG-006/VG-011 → unsafe/incomplete output; artifact/restore inspection | Persistence/contract: secrets/tokens absent; archive traversal/symlink/duplicate-entry/resource limits; missing originals/precision/convention round-trip; partial/uncertain export; IDEM-005, FAIL-018–FAIL-020/FAIL-023 | Backup/export/restore, not external completed-run import |
| TF-008 | VG-008/VG-001 → provider mismatch/false closure; normalized facts/status | Contract: schema/column names/precision, partial/duplicate/overlap/rate-limit/timeout, live session epochs, denied/no demo; FAIL-004–FAIL-008/FAIL-022; RETRY-001/RETRY-006; ORDER-003/ORDER-006; actual-account/session/publication proof separately DEFER-001–DEFER-002 | Controlled adapter behavior, synthetic fixtures cannot certify real entitlements/calendar/publication |
| TF-009 | VG-002/VG-009/VG-011 → rendered context/keyboard wiring; visible bounded state | Selective E2E: rapid selection, two-chart replay/watchlist/window/studies, draw/save/reload/rewind, focus/names, truthful save/errors, local image/report labels; FAIL-002–FAIL-003/FAIL-008/FAIL-023, ORDER-005 | Cross-boundary wiring/accessibility; arithmetic remains TF-002/TF-003 |
| TF-010 | VG-010 → measured stall/history cap; timing/range record | Performance integration/selective E2E: accepted hardware/workload, ready-local initial view, interaction p95/concurrent tick/live display, archive both directions beyond resident set, startup/reconnect catch-up | P3 on recorded hardware; no universal hardware/provider recovery-time guarantee |

All FAIL-001–FAIL-023, CONC-001–CONC-012, IDEM-001–IDEM-005, RETRY-001–RETRY-008 and ORDER-001–ORDER-006 are assigned above. Wrong-local-work/run/layout tests supply actual isolation proof in this single-user product; no nonexistent tenant login matrix is fabricated.

## 29. Mechanical Architecture Checks (`ARCHV-*`) & Audit Verification (`AUDV-*`)

Concrete tooling follows language/module standards; the required constraints are explicit now.

| ID | Rule / Violation Shape | Enforcement / Limit |
|---|---|---|
| ARCHV-001 | DEP-015/DEP-011: core imports concrete provider/storage/renderer types | Automated import/dependency rules at semantic scopes; dynamic leaks also need contracts/tests |
| ARCHV-002 | DEP-018/DEP-021/SEC-07: provider grants broker commands/balances | Data capability allowlist and controlled attempted-operation recording; actual SDK encapsulation/integration still reviewed |
| ARCHV-003 | DEP-019/TEN-001/TEN-004: write/source/path/secret escape | Root confinement and path/symlink/archive escape tests, backup/export content exclusions; arbitrary OS tampering outside scope |
| ARCHV-004 | DEP-016/DEP-017/CONTRACT-012/CONTRACT-020: implicit latest replay reads | Explicit basis/boundary contract checks, forbid provider reads from panels/report, wrong-context cache tests; parameter presence alone not correctness |
| ARCHV-005 | TX-002/CONC-001/CONC-008/TEN-002: bypass fenced mutation | Restrict mutation entrypoints, expected owner/run/restore context required through publication; physical exclusion tested TF-006 |
| ARCHV-006 | INV-04/INV-12/CONTRACT-015: broken retained references/precision | Validate complete required content closure and original-value/version-compatible round-trip; integrity alone not source correctness |
| ARCHV-007 | DEP-020/INV-13: rewind mutates drawings or study acquires data | Dependency/effect-shape rules forbid those capabilities; dynamic/semantic behavior tested separately |

| ID | Audited Action | Required Fact / Failure / Retry Proof | Exclusion Proof |
|---|---|---|---|
| AUDV-001 | AUD-001 provenance | Lineage/side/precision/bounds through partial/duplicate/finalization/source change; run values original | Secret/private sentinel values absent from retained provenance/diagnostics |
| AUDV-002 | AUD-002 execution/block/rewind | Effective event/whole effects/ASM labels after save/export; duplicate no new effect; block no partial fill; authorized suffix removed | No broker account/cash or fabricated observed ordering |
| AUDV-003 | AUD-003 save/replacement/backup | Saved generation matches closure; uncertain publication reconciles once; incomplete/unsafe artifact rejected | Sentinel credentials/tokens/raw login payload absent; no extra permanent discarded-trade journal |
| AUDV-004 | AUD-004 authored work | Anchors/config round-trip; preview/rejection no accepted fact; drawing survives trading rewind | No private captured account/script fixtures/results |

## 30. Diagnostic Observability (`LOG-*`, `MET-*`, `TRACE-*`, `ALERT-*`)

The sole analyst is the operator. Provide local inspectable diagnostics/status, not remote telemetry or market-trigger alerts. Use bounded reason codes; opaque local work/run/operation/generation identities may correlate logs/traces but never metric labels. Exclude secrets/raw datasets/full financial histories. Standards select bounded diagnostic retention; domain-evidence retention remains independent.

| ID | Diagnostic Question | Boundary / Required Context | Prohibited Fields |
|---|---|---|---|
| LOG-001 | Why was a view adopted/discarded? | BND-005/BND-012 context generation, safe requested basis/boundary identity, adoption/load outcome, trace | Raw arrays/HTML/private captured content |
| LOG-002 | Why is recovery/staleness unresolved? | BND-003/BND-011 acquisition epoch, safe instrument/period/side/span, normalized coverage/finality/access reason, candidate/published generation | Credentials/raw provider response/headers/account identity |
| LOG-003 | Why did event stop/repeat/lose ack? | BND-007/BND-008/BND-010 opaque event/run/operation identity, basis/convention, expected/current version, block/duplicate/publication phase, known/uncertain outcome | Raw trade/cash/position dumps or invented conversion values |
| LOG-004 | Why was mutation/restore/export denied? | BND-013/BND-010/BND-012 purpose, safe scope category, epoch/confirmation/validation reason, operation correlation | Tokens, backup contents, credentials, untrusted raw paths |
| LOG-005 | What generation can recover? | BND-010 candidate/active generation, reference/integrity/durability phase, working/saved version, safe error category | Secret config, raw blocks, unrelated private paths |

| ID | Type / Operational Question | Signal and Bounded Dimensions | Threshold / Action |
|---|---|---|---|
| MET-001 | Metric: local viewport/interaction slow? | Duration distribution by bounded phase/view-mode | <2s initial ready-local viewport, p95 <50ms interaction on SCALE-03 workload |
| MET-002 | Metric: receipt→display slow? | Duration/status by provider capability; receipt/event times distinct | Within 1 second local receipt; retain violations, network publication separate |
| MET-003 | Metric: acquisition progressing/limited? | Phase/duration/failure/rate-limit category and qualified pending spans | No invented recovery SLO; expose progress/error and provider feedback |
| MET-004 | Metric: saves lag/fail/unknown? | Checkpoint duration/failure, working-versus-retained progress, publication condition | No invented save delay; truthful unsaved/error, reconcile uncertainty before unsafe writes |
| MET-005 | Metric: detail resolution loading or blocked? | Phase/duration, bounded block/duplicate/conflict reasons | Explain missing prerequisite versus heavy read; no arbitrary block timeout |
| TRACE-001 | Trace: selection/range path | Read→calculate→context-check→adopt; LOG-001/MET-001, context identity | No raw arrays; isolate slow/stale phase |
| TRACE-002 | Trace: acquisition/display path | Receipt→validate→derive→retain→publish/display; LOG-002/LOG-005/MET-002–MET-003 | Receipt/history times separate; no raw provider secrets |
| TRACE-003 | Trace: run/block/resume path | Eligibility→resolution→valuation→whole effect→checkpoint; LOG-003/LOG-005/MET-004–MET-005 | Original occurrence/generation, no confidential financial payload |
| TRACE-004 | Trace: restore/export/owner path | Validate→authority→publish→ack; LOG-004/LOG-005, operation generation | No credentials/capability material |
| ALERT-001 | Local status: save failed/publication uncertain | Known save/error phase and exact version | Show immediately when known; inspect generation/correct storage, no false saved claim |
| ALERT-002 | Local status: event blocked | Original event/instrument and missing gap/FX/spec/evidence | Resolve prerequisite or deliberate restart; play cannot bypass |
| ALERT-003 | Local status: denied/disconnected/stale/partial provider | Qualified condition/reason and preserved history | Explain limitation, no demo/recovery deadline |
| ALERT-004 | Local status: stale authority/confirmation/invalid backup | Sanitized deny/validation reason | Preserve work; fresh valid intent/action, no destructive autoretry |

These are operational UI statuses, not excluded trading alerts FR-26. Numeric stale thresholds, diagnostic retention limits and scheduler/timeout settings remain VGAP-001/DEFER-006. Until instrument evidence exists, no receipt means freshness unknown/no recent receipt, never proven closure.

## 31. Production Diagnosis (`DIAG-*`) & Redundancy Review

| ID / Operator Question | Authoritative State / Evidence | FAILED versus UNCERTAIN / Safe Recovery |
|---|---|---|
| DIAG-001 — Why did selection/sync not change? (RW-001) | BND-005 requested/adopted context, AUD-004, LOG-001/LOG-005, TRACE-001, MET-001 | Invalid/obsolete adoption known failed; unknown saved label resolved by generation. Keep last valid view, issue fresh request, no relabelling old arrays |
| DIAG-002 — Is catch-up complete? (RW-002) | Published catalog/gaps/lineage AUD-001, LOG-002/LOG-005, TRACE-002, MET-002–MET-003 | Remote read may be uncertain; active reference resolves local truth. Empty not closure; retry qualified rate-limited read/staged reconciliation, preserve history |
| DIAG-003 — Did order execute twice? (RW-003) | Run epoch/processed boundary, AUD-002 effect identity, LOG-003, TRACE-003, MET-005 | Duplicate display/ack not second effect; unknown retained publication inspected first. Re-render/reconcile same result, no ad hoc fee/corrective broker trade |
| DIAG-004 — Why still paused? (RW-004) | Original HIST-08/AUD-002 block, basis/prerequisite decision, LOG-003/TRACE-003 | Missing/inapplicable evidence known block; completion publication can be uncertain. Validate original-time evidence, same occurrence once or explicit updated-data restart |
| DIAG-005 — Did rewind/restore/delete succeed? (RW-005) | Active epoch/generation, AUD-003, LOG-004/LOG-005, TRACE-004 | Prepublication failure leaves old state, postpublication ack uncertain until inspected. Resolve old/new whole generation before another destructive command |
| DIAG-006 — What saved work/backup survives? (RW-006) | Last valid generation/closure AUD-003, working indicator, LOG-005/MET-004 | Failed content never saved; unknown ack resolved by reference/integrity. Recover coherent generation, validate backup closure, retry retention not execution |
| DIAG-007 — Why read-only/late feed receipt? (RW-007) | Owner/acquisition epoch/runtime, LOG-002/LOG-004, TRACE-004 | Local owner decision known, remote teardown possibly uncertain. Exclude prior owner before handover, fence late callbacks, fresh catch-up |
| DIAG-008 — Is export complete/permitted? (RW-008) | Pinned source version, AUD-002/AUD-004, artifact integrity, TRACE-004 | Incomplete write failed, lost ack uncertain until artifact verified. Verify/regenerate same bounded snapshot; no rerun against latest data |
| DIAG-009 — Why missed P3? | TRACE-001–TRACE-003, MET-001–MET-005, recorded hardware/workload/read/tick phases | Separate absent provider receipt from slow local read/render/save. Fix scheduling/range path without reducing history scope, skipping valuation or exposing future values |

Domain TF-001–TF-003 prove policies; workflow TF-004/TF-005 prove cooperation/authority; TF-006 proves actual storage/exclusive publication that mocks cannot. TF-008 controlled normalization does not replace real provider access/session evidence. TF-009 adds only visible/keyboard wiring, not duplicated arithmetic; TF-010 measures workload. ARCHV prevents structural drift and AUDV checks retained evidence; neither substitutes for semantics. This designer's checks are not an independent architecture-adversary review.

# PART V: DECISIONS, SEMANTIC PSEUDOCODE, AI IMPLEMENTATION HANDOFF & READINESS (PASS 2)

## 32. Architecture Decision Log (`ADR-*`) & Evaluated Alternatives

CONFIRMED means upstream/user approved. PROPOSED means the architectural choice made here for downstream conformance, not optional permission for coding AI to guess differently; changing it requires an explicit architecture revision. New Pass 2 choices are not retrospectively human-approved by G1.

| ADR | Decision / Status | Sources / Alternatives / Consequences |
|---|---|---|
| ADR-001 | Thirteen logical boundaries/Part II contracts — CONFIRMED at G1 | User approval of revision 1; BND-001–BND-013. Reject merging merely by workflow/storage; no separate-process commitment |
| ADR-002 | Exclusive local owner, per-run serialized transitions, version/epoch fencing — PROPOSED | CONS-06/CONS-10/CONS-12, TX-001–TX-002, CONC-001–CONC-012. Reject UI-only flag/redraw execution/timeout-only takeover; runtime must prove exclusion |
| ADR-003 | Immutable owned evidence closure and atomic retained-generation publication — PROPOSED | FR-43–FR-45/FR-55, TX-003–TX-006. Reject mutable paths/in-place mixed generations and unnecessary whole-archive backups; requires staging/integrity/compatibility/cleanup |
| ADR-004 | Coherent working state distinct from exact saved checkpoint — PROPOSED realization of CONFIRMED P2 | FR-44, CONS-02/CONS-15, CM-003. Reject accepted edit as automatic durability; unsaved suffix may be lost, acknowledged generation survives |
| ADR-005 | Current catalog versus retained run; narrow original-event completion — CONFIRMED policy, PROPOSED TX-006 realization | FR-35/FR-42/FR-45, POL-09. Reject silent new ticks/rates/spec replacement; compatible prerequisite completion preserves committed outcomes |
| ADR-006 | Whole local simulated effects, no broker compensation — CONFIRMED scope, PROPOSED TX-002 realization | INV-05, SEC-07. No remote money effect justifies distributed transaction/outbox; whole effect or block, no margin/liquidation/real cash |
| ADR-007 | Retained logical intent/effect identity; reconcile uncertain publication before retry — PROPOSED | IDEM-001–IDEM-005, RETRY-001–RETRY-008. Reject timestamp-only dedup/blind timeout retry; equal deliberate actions remain distinct |
| ADR-008 | Shared bounded evidence contracts, independent routine chart path — PROPOSED realization | FR-20/FR-23/FR-36/FR-52, BND-004, CM-001/CM-007. Reject latest-cache replay, SP500-only detail, history cap; detail loading cannot invent fills |
| ADR-009 | Protected data-only provider edge and evidence gates — CONFIRMED scope, PROPOSED isolation | POL-12, SEC-03/SEC-07, ARCH-GAP-01–ARCH-GAP-02. Reject demo/TradingView private runtime endpoints; required live/backfill still needs actual acceptance evidence |
| ADR-010 | Domain/provenance evidence and bounded local diagnostics, no permanent discarded-trade journal — PROPOSED realization | HIST-01–HIST-08, BR-17, AUD-001–AUD-004. Reject remote audit/telemetry platform; authorized rewind removes later active facts |
| ADR-011 | Narrow property verification plus selective E2E/performance — PROPOSED | VG-001–VG-011, TF-001–TF-010. Reject live-provider-only rules and broad duplicate E2E; storage/provider actual proofs distinct |
| ADR-012 | Stack/numerical/study/tool/provider tuning — DEFERRED with named prerequisites | DEFER-001–DEFER-007, DM-GAP-01–DM-GAP-05. No affected slice may silently guess; architecture readiness is not product completion |

## 33. Architecture-Level Semantic Pseudocode

Candidate preparation can use bounded asynchronous reads; publication rechecks authority/context. No framework, physical schema, API endpoint or vendor call is implied. Persistence failure is never repaired by executing an already coherent working trade/edit again.

```text
acceptHistoricalCommand(command, context):
    require currentLocalWriterAndRunEpoch(context)
    enter runTransitionOrder(command.run)
    if existingLogicalOutcome(command.identity):
        require sameSemanticPayload(command)
        return originalOutcome
    run = readCoherentWorkingRun()
    require expectedVersionAndDecisionBoundary(command, run)
    require eligibleExistingEventsProcessedBeforeNewDecision(run)
    quantity = monetaryPolicy.decide(command, run.selectedConventions)
    candidate = instructionPolicy.acceptOrReject(command, quantity, run)
    if rejectedOrMissingPrerequisite(candidate):
        return explainedNoEffect
    recheckAuthorityAndExpectedVersion()
    publishWholeWorkingTransition(candidate)  # TX-002, IDEM-001
    requestAutosaveOfCoherentVersion()
    return outcomeWithActualSavedCondition

advanceEstablishedEvent(context):
    require currentLocalWriterAndRunEpoch(context)
    enter runTransitionOrder(context.run)
    run = readCoherentWorkingRun()
    evidence = historicalEvidence.nextAvailable(run.retainedBasis, run.processedBoundary)
    continuity = coverage.assess(evidence, run.retainedSessionEvidence)
    if unresolvedContinuityOrActualCoverageLimit(continuity):
        publishCoherentPauseWithoutNextEventEffects()
        return explainedPauseOrCoverageLimit
    eligible = runOrdering.effectiveExistingInstructions(run, evidence)
    resolution = historicalEvidence.finerStoredBarsThenNeededLocalTicks(eligible, evidence)
    pricing = executionPolicy.eligibleSidePriceAndProtectiveOrder(eligible, resolution)
    if unresolvedNonFallbackPrerequisite(pricing):
        retainOriginalBlockedEventWithoutItsEffects()
        requestAutosaveOfCoherentVersion()
        return explainedBlock
    money = monetaryPolicy.valueWholeEffect(pricing, run.selectedConventions,
                                            boundedOriginalEventConversionEvidence)
    if missingOrInapplicablePrerequisite(money):
        retainOriginalBlockedEventWithoutItsEffects()
        requestAutosaveOfCoherentVersion()
        return explainedBlock
    candidate = executionPolicy.applyWholeEffect(run, pricing, money)
    require candidateInvariantsAndEvidenceLabels(candidate)
    recheckAuthorityAndExpectedVersion()
    publishWholeEffectAndProcessedBoundary(candidate)  # TX-002, IDEM-002
    exposeCommonBoundedWorkspaceContextOrUnavailableValues()
    requestAutosaveOfCoherentVersion()
    return coherentOutcome

resumeBlockedEvent(context, prerequisite):
    block = readOriginalBlockInCurrentRunEpoch()
    require historicalApplicabilityAtOriginalEvent(prerequisite, block)
    require preservesCommittedBasisAndOutcomes(prerequisite, block)
    stageVerifiedOwnedPrerequisiteEvidence()
    reevaluateSameOriginalOccurrenceAndPublishCompatibleCompletion()  # TX-006
    # incompatible prerequisite stays blocked; changed committed basis needs restart

publishCheckpoint(capturedWork):
    require coherentCapturedVersionsAndAuthority(capturedWork)
    retainVerifiedImmutableRequiredInputClosure(capturedWork)
    require allOriginalValuesAndReferencesRecoverable()
    require notSupersededAndCurrentOwnerRestoreEpoch()
    durablyPublishSingleGenerationReference(capturedWork)  # TX-004
    if publicationUncertain:
        reconcileActiveReferenceAndIntegrityBeforeRetry()
    acknowledgeOnlyExactSuccessfullyRetainedVersion()

replaceRunOrRestore(request):
    require currentWriterAndConfirmationForExactScopeVersion(request)
    pinCurrentRetainedGeneration()
    candidate = reconstructPrefixOrStageValidatedRestore(request)
    require noUnauthorizedDrawingOrCredentialEffects(candidate)
    require coherentInputClosureAndIntrinsicInvariants(candidate)
    recheckConfirmationAuthorityAndExpectedGeneration()
    fenceAffectedPendingEpochsAtReplacement()
    publishCompleteReplacementAndRetainedGeneration(candidate)  # TX-005
    reconcileBeforeRepeatIfAcknowledgementUncertain()

reconcileCurrentHistory(facts, acquisitionContext):
    require currentDataOnlyAcquisitionContext(acquisitionContext)
    qualified = normalizeAndValidateUntrustedFacts(facts)
    continuity = coverage.assessWithInstrumentSessionEvidence(qualified)
    candidate = catalog.reconcileCurrentRevision(qualified, continuity)
    deriveOnlyRecoveredAndAffectedSupportedUtcBuckets(candidate)
    retainVerifiedOwnedObservationContent(candidate)
    recheckAuthorityAndExpectedCatalogGeneration()
    publishQualifiedCatalogAndLineage(candidate)  # TX-003, IDEM-003
    # never replace retained run selections or mutate sibling sources
```

A compound advance may publish a coherent established-event prefix, but a blocked execution has no part of its effect and new decisions cannot leap beyond unfinished existing-order processing. No step assumes a provider receipt or durable file publication rolls back with working memory.

## 34. AI Implementation Handoff (`IMPL-*`, `FREEDOM-*`, `DEFER-*`)

### Non-Negotiable Implementation Constraints

| ID | Category / Rule and Source |
|---|---|
| IMPL-001 | Domain/boundary: preserve DC/INV/PRE/POL and approved BND-001–BND-013/contracts; respect DEP-015–DEP-021, no concrete provider/storage/render types inward. |
| IMPL-002 | Data: ten initial instruments/eight periods, bid default/ask selectable, UTC/original precision/established occurrences. Discover full actual bounds; no hardcoded start/history/retention cap (FR-01/FR-04/FR-07/FR-52). |
| IMPL-003 | Authority: sibling inputs read-only, owned acquisition files; retain selected original values/evidence/settings/limitations before claiming reproducible save, not mutable paths (TX-003–TX-004, CM-005). |
| IMPL-004 | Replay: all panels/studies/FX/reports/execution use explicit retained basis/common boundary, higher-period completion enforced, no latest fallback (CONTRACT-012/CONTRACT-020). |
| IMPL-005 | Execution: existing eligible events before new decisions; next-event side/stop/limit rules; finer bars before needed local ticks; eligible ASM-01 only and full-fill ASM-02 with labels. No invented entry/price/path (POL-03–POL-05, ORDER-001–ORDER-002). |
| IMPL-006 | Money/exposure: independent hedged targets, whole fee/protection/position/USD effect or original-event block, shared BND-009 valuation/risk; no margin/liquidation/extra slippage/real cash (TX-002/TX-006, INV-05–INV-10/INV-14). |
| IMPL-007 | Concurrency: authoritative sole writer, owner/run/restore epoch at publication, expected version, scoped fresh confirmation; forbid UI-only flag/timeout-only takeover/restored authority (CONC-001–CONC-012). |
| IMPL-008 | Durability: immutable complete content, durable atomic generation reference, exact saved acknowledgement; failed save/restore keeps prior saved version, reconcile uncertainty before retry (TX-004–TX-005, CM-003). |
| IMPL-009 | Repeat/order: IDEM-001–IDEM-005/RETRY-001–RETRY-008/ORDER-001–ORDER-006; same intent original outcome, deliberate equal actions distinct, conflicting identity rejected; no time-only tick dedup. |
| IMPL-010 | Authored/reconstruction: layout/instrument drawings independent of trading rewind; confirmed prefix reconstruction removes dependent later effects; no permanent discarded-trade journal required (INV-13, TX-005, AUD-002/AUD-004). |
| IMPL-011 | Security: protected data-only live-account edge; no demo/broker effects; confined untrusted file/backup/label parsing, secrets/tokens absent from browser/log/export/backup; fresh restore authority (SECR-001–SECR-008, TEN-001–TEN-004). |
| IMPL-012 | Recovery: backup required run-input closure and coherent analysis; stage/validate before replacement, no silent merge/latest substitution for missing originals (PRE-10, TX-005, AUD-003). |
| IMPL-013 | Verification: required VG/AC/TF/ARCHV/AUDV evidence, deterministic barriers/frontiers and actual platform durability; domain rules cannot rely only on rendered/live tests. |
| IMPL-014 | Performance/runtime: full archive/routine chart independence; measure P3 recorded workload/hardware; acquisition while app runs, catch-up startup/reconnect, truthful progress/failure, no invented provider deadline (CM-007, TF-010). |
| IMPL-015 | Operability/readiness: safe local diagnostics tied to DIAG, evidence distinct from logs, no market alerts/remote telemetry; honor scoped DEFER prerequisites and later lifecycle gates. |

### Allowed Implementation Freedom

| ID | Local Choice / Conditions |
|---|---|
| FREEDOM-001 | Internal helpers/names/private values within boundary; preserve ownership, precision, determinism and dependencies. |
| FREEDOM-002 | Bounded indexes/cache/task scheduling; context-aware keys, complete archive accessible, P3 met without skipping financial/continuity checks; no mandated resident cap. |
| FREEDOM-003 | Immutable content encoding/compression/integrity and publication realization; standards select technology and prove old-or-new recovery, compatibility and safe roots; no physical schema prescribed. |
| FREEDOM-004 | Browser/native interaction and local capability transport; UX/standards choose while preserving protected secrets, one writer and origin/IPC isolation; no deployment inferred. |
| FREEDOM-005 | Test/diagnostic/static-check tooling; produce required semantic evidence, deterministic races and bounded local diagnostics. |

### Deferred Decisions and Prohibited Invention

| ID | Decision / Owner and Trigger | Prohibited Invention / Affected Work Gate |
|---|---|---|
| DEFER-001 | ARCH-GAP-01 actual API/auth/entitlements; protected integration discovery before live acceptance | No connection by this document, credentials in chat/docs, demo substitute or completed-live claim; independent historical slices can proceed, required live remains delivery scope. |
| DEFER-002 | ARCH-GAP-02 instrument sessions/finality/publication/FX applicability; integration validation before affected traversal/finalization | No guessed calendar/closure/stale rate from silence/weekend; absent evidence unresolved/blocked. Controlled policy work possible; actual acceptance waits. |
| DEFER-003 | ARCH-GAP-03 study/tool/input/export/range conventions; domain/calculation/UX before affected slice brief | No assumed numeric TradingView parity, unsupported periods or guessed accepted parameter bounds; brief names approved scoped conventions first. |
| DEFER-004 | ARCH-GAP-04 exact USD/notional/quantity precision/valuation; scoped domain/monetary refinement before trading calculation slice | No coding-agent ad hoc rounding/multipliers/FX applicability. Document delegated conventions/independent examples, pause missing required values; blocks affected slice authorization, not ownership design. |
| DEFER-005 | ARCH-GAP-05 UI/default/undo realization; UX/UI before affected interaction work | No invented tenant/shared-user model, enlarged chart/sync catalog, optional scope or visual-parity claim. |
| DEFER-006 | VGAP-001 timeout/backoff/staleness, diagnostic resource bounds, scheduler values; standards/integration/performance evidence | No arbitrary SLO/threshold/attempt counts here; finite/bounded cancellable runtime configuration honors provider feedback and P3; silence never closure. |
| DEFER-007 | Stack/renderer/process/storage realization; standards before foundation, implementation brief before coding | No mandatory stack from old blueprint or logical boundary count; prove actual TX-004/TX-005/single-writer platform capability first, no untested filesystem durability claim. |

Downstream sequence: standards choose technology against capability guarantees; UX/UI prepares interaction/visual authority; scoped domain/integration refinements discharge relevant prerequisites; implementation briefs authorize foundation or one behavioral slice with explicit sources/validation. This dossier does not authorize production coding, provider connection, external publication or presume approval at later human gates.

## 35. Conflicts, Gaps & Final Completeness Verdict

### Cross-Artifact Conflicts and Upstream Modifications

No blocking requirements/domain contradiction or required upstream rewrite was found. No SYN-CONFLICT/SYN-MOD or RCORR entry is fabricated. Requirements Section 19 resolves legacy UNK references. Parts I–II preserve approved ownership/contracts; only status/provenance records approval. Parts III–V add resilience obligations within them.

### Architecture, Resilience and Verification Gaps

| ID | Severity / Missing Information | Owner and Next Action / Implementation Impact |
|---|---|---|
| ARCH-GAP-01 | IMPORTANT, scoped integration evidence: actual live API/auth/per-asset access; UNK-19/DM-GAP-01 | Integration discovery validates protected edge; DEFER-001 gates live acceptance, no substitute/waiver. Independent slices remain usable. |
| ARCH-GAP-02 | IMPORTANT, scoped integration evidence: sessions/publication/finality/FX applicability; UNK-20/DM-GAP-02 | Integration validation supplies appropriate facts; DEFER-002 gates affected acceptance, absent facts unresolved/blocked. |
| ARCH-GAP-03 | IMPORTANT, scoped realization: study/tool/export/range conventions; DM-GAP-03 | Domain/calculation/UX refine before affected brief; DEFER-003 prevents coding guesses. |
| ARCH-GAP-04 | IMPORTANT, scoped realization: exact monetary/notional/quantity precision/valuation; DM-GAP-04 | Domain/monetary refinement documents delegated rules/examples; DEFER-004 gates affected trading slice, unknown values pause. |
| ARCH-GAP-05 | OPTIONAL architecture gap: UI/default/undo details; DM-GAP-05 | UX/UI establishes bounded realization under DEFER-005; no scope/ownership expansion. |
| VGAP-001 | OPTIONAL architecture configuration gap: provider timing/staleness, diagnostic resource bounds/scheduling | Standards/integration/performance chooses bounded values under DEFER-006; status/action rules already explicit, P3 targets unchanged. |

No resilience boundary decision is left undefined: TX/CM/FAIL/CONC/IDEM/RETRY/ORDER/EXT/SECR/TEN/AUD specify guarantees and minimum mechanism classes. Remaining IMPORTANT items are prerequisites for **named affected slices/acceptance**, isolated under DEFER. They do not mean all trading/live/UI implementation can begin today. A prerequisite exposing incompatible semantics or infeasible guarantees must revise the owning authority/readiness before affected coding.

### Quality-Gate Review

| Skill Gate | Assessment / Evidence |
|---|---|
| 1–8 Pass 1 | Preserved PASS: authoritative inputs/accepted assumptions; traced semantic responsibilities, nine concern categories, cohesion/exclusions, ownership/contracts and classified dependencies. Pass 1 scope restraint applies to Parts I–II; new mechanisms explicitly Pass 2. |
| 9 Partial failure | PASS: RW-001–RW-008 ordered actions and FAIL-001–FAIL-023 distinguish SUCCEEDED/FAILED/NOT_ATTEMPTED/UNCERTAIN; no remote rollback fiction. |
| 10 Problem before pattern | PASS: TX-001–TX-006/CM-001–CM-007 tie actual failures/properties to minimum mechanisms and burdens; no unjustified distributed infrastructure. |
| 11 Concurrency/repeat/provider | PASS: CONC-001–CONC-012, IDEM-001–IDEM-005, RETRY-001–RETRY-008, ORDER-001–ORDER-006, EXT-001–EXT-004 define scopes/conflicts/identity/uncertainty/degradation. |
| 12 Security/scope/audit | PASS: SECR-001–SECR-008/TEN-001–TEN-004/AUD-001–AUD-004 adapt to local user, fresh restore authority, data-only provider and scoped evidence retention; no invented tenants/journal. |
| 13 Property before test | PASS: VG-001–VG-011 → AC-001–AC-018 → TF-001–TF-010 narrow evidence; Section 31 explains justified redundancy. |
| 14 Negative/resilience proof | PASS: foreign/unbound/unauthorized/wrong-scope/stale context negative plus valid owner; deterministic barriers/frontiers cover all failure/race/retry/order groups, actual storage proof separate. |
| 15 Constraints/operability | PASS: ARCHV-001–ARCHV-007/AUDV-001–AUDV-004 and LOG/MET/TRACE/ALERT/DIAG answer concrete local questions, exclude secrets/high-cardinality metric IDs; accepted numeric targets only. |
| 16 Handoff consistency | PASS with scoped non-blocking gaps: ADR/statuses, semantic pseudocode and IMPL/FREEDOM/DEFER align; coding agents cannot guess affected deferred prerequisites. |

### Completeness Verdict and Approval Record

- **Pass 1 Status:** `BOUNDARIES_READY_FOR_RESILIENCE`; G1 **APPROVED** by the user on 19 October 2026: “I approve the boundaries proposed”. Covers revision 1 Parts I–II, not new Pass 2 mechanisms or later gates.
- **Pass 2 Final Status:** `IMPLEMENTATION_READY_WITH_NON_BLOCKING_GAPS`; core structure, resilience, security, verification, diagnostics and handoff complete, with ARCH-GAP-01–ARCH-GAP-05/VGAP-001 isolated under DEFER-001–DEFER-007.
- **Meaning:** Ready for downstream standards/UI/governed implementation preparation under constraints; not a built/tested product, proven provider feasibility, selected stack, completed affected refinement or release acceptance.
- **Independent review:** Not performed by this designer. Architecture-adversary may review the canonical dossier separately; self-checks are not independent approval.
