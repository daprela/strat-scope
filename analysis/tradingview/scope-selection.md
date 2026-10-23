# Behavioral Scope Selection

**Status:** `SCOPE_SELECTION_REQUIRED`

**Intake outcome:** `BRIEF_BLOCKED` — foundation prerequisite unmet. This is a provisional candidate inventory for Gate G7 preparation, not `CANDIDATE_SLICES_PROPOSED` or permission to implement a behavior.

**Prepared:** 22 October 2026; implementation-brief / `SCOPE_SELECTION` mode.

**Architecture authority:** [architecture-dossier.md](architecture-dossier.md), revision 2, `IMPLEMENTATION_READY_WITH_NON_BLOCKING_GAPS`.

**Architecture approval:** G1 accepted revision 1 Parts I–II on 19 October 2026. Independent [architecture-review.md](architecture-review.md), revision 1, verdict `READY WITH NON-BLOCKING CHANGES`, has zero BLOCKING/HIGH findings. This does not expand G1 approval to Pass 2 or discharge its scoped prerequisites; ADV-VER-001 remains required verification.

**Implementation standards:** [implementation-standards.md](implementation-standards.md), revision 3, `STANDARDS_READY` / `READY_FOR_FOUNDATION_BOOTSTRAP`; G6 approval recorded in [standards-approval.json](standards-approval.json). **Not yet `READY_FOR_BEHAVIORAL_IMPLEMENTATION`.**

**Accepted implementation records considered:** None. `implementation-ledger.md` is absent; no accepted `REC-FOUNDATION`, behavioral records or supersessions exist in the supplied checkout.

**Repository context considered:** [project-state.md](../../project-state.md), Sections 1–5; root/scoped governance; backend/frontend application roots contain governance files only. The contract reference package and dossier generators are not product implementations. Repository structure establishes implementation context only; candidates below come from architecture behavior.

**UI authority:** [ui-dossier.md](ui-dossier.md), revision 35, Parts I–VI; [visual-system.md](visual-system.md), revision 7; WF-SET-001-r14 / MP-SET-001-r9, current G4/G5 approvals in [approval-r14.json](ui-artifacts/wireframes/approval-r14.json) and [approval-r9.json](ui-artifacts/mockups/approval-r9.json). Independent [ui-review.md](ui-review.md), revision 5, is `READY WITH NON-BLOCKING UI CHANGES`: zero BLOCKING/HIGH, one MEDIUM and two LOW findings. These newer UI identities supersede the historical UI revision summaries in standards/project-state, without changing approved G6 decisions.

## Gate G7 readiness

The skill requires foundation readiness before emitting `CANDIDATE_SLICES_PROPOSED`. Current standards and project state explicitly record foundation `NOT_STARTED`; an accepted foundation implementation record is missing. A behavioral selection cannot substitute for that prerequisite.

The next valid implementation handoff is implementation-brief / `FOUNDATION`, followed by governed bootstrap and implementation-gate / `REVIEW_AND_RECORD`. Once foundation acceptance establishes `READY_FOR_BEHAVIORAL_IMPLEMENTATION`, revalidate this inventory against all accepted ledger records and current upstream authorities, then present the eligible candidates at G7. This artifact does not create a foundation brief, implementation ledger, accepted record or project-state transition.

## Candidate behavioral slices

All rows are provisional and share the foundation blocker above. IDs are stable references, not priorities or a proposed execution order. No candidate is currently selected. Supporting dependencies below describe required behavior, not acceptance of a partial substitute for the named outcome. Every candidate has UI impact `REQUIRED`; its subsequent SLICE brief must extract exact approved compositions, UIV obligations and a Blast-Radius Contract.

| Candidate ID | Behavioral slice | Intended outcome | Why this is one coherent slice | Architecture sources | Existing implementation context |
|---|---|---|---|---|---|
| `SC-001` | Discover and navigate qualified local chart history | Search/select instrument, period and quote display; pan/zoom/go to supported ranges; inspect correctly labelled values, actual bounds, gaps and unavailable sides while retaining the previous valid chart on failure | One request-to-adopted-chart reading journey; archive extent remains independent of resident bars and viewport navigation does not advance replay | WF-001; OP-01/03; CONTRACT-001/012/020; BND-001/002/004/005/012 | No accepted product realization. Requires qualified archive reads, matching-context adoption and approved paired Bid/Ask rendering; see scoped prerequisites |
| `SC-002` | Configure and recover an authored chart workspace | Apply/cancel presentation settings; create/name/restore one/two-chart layouts and supported interval sync; autosave/resume the exact committed analysis version | One authored workspace lifecycle with preview, commit, failure and recovery; durable success is separate from a valid working edit | WF-002/008; OP-03/04/13; CONTRACT-002/009/015/019; BND-005/010/012/013 | None. Needs chart selection context from SC-001 or an accepted equivalent; shared recovery overlaps SC-011 and must be reused rather than implemented twice |
| `SC-003` | Add and manage bounded analytical studies | Add/configure/hide/remove approved built-in studies in overlays/panes, showing declared input basis, warm-up and missing values; retain valid configuration after invalid edits | One study instance lifecycle from configuration to bounded output and saved configuration | WF-001/002; OP-04; CONTRACT-002/018; BND-005/006/012 | None. Requires chart/workspace behavior and scoped DEFER-003 conventions before briefing; no future inputs or TradingView formula-parity assumption |
| `SC-004` | Author and retain financially anchored drawings | Create/cancel/select/edit/hide/lock/delete core drawings; inspect objects and undo/redo supported analysis edits within layout/instrument scope | One annotation lifecycle whose retained financial anchors and edit history survive trading rewind | WF-002/008; OP-05; CONTRACT-002/009; BND-005/010/012; IMPL-010 | None. Requires chart/workspace behavior and approved tool/undo conventions under DEFER-003/005; never creates trading instructions |
| `SC-005` | Catch up and finalize current Dukascopy history | On startup/reconnect, acquire missing M1/H1 and live facts, reconcile final/provisional observations, retain owned history and affected derivatives, and explain actual progress/failure | One acquisition-to-published-current-history lifecycle; sibling archive and retained runs stay intact | WF-003; OP-02; CONTRACT-003/016/017; INT-002/003; BND-002/003/010/011/013 | None. Provider/session/finality and bounded-runtime evidence required under DEFER-001/002/006; ADV-VER-001 applies to catalog publication races |
| `SC-006` | Start and traverse a historical exercise | Start/resume, play/pause/step and seek forward with retained inputs, one historical disclosure boundary, event evaluation and explained continuity/coverage stops | One replay progression lifecycle; all panels and eligible existing instructions observe the same processed boundary | WF-004/008; OP-06/13; CONTRACT-004/009/012/013/020; BND-004/007/008/010/012 | None. Requires chart/retention behavior and eligible-execution integration; cannot authorize playback that skips existing instructions or advances through unresolved gaps |
| `SC-007` | Configure simulation terms and inspect permitted sizing | Set scoped balance, instrument specifications/overrides, fees and fixed/risk sizing; show valid quantity/planned risk or an explicit missing prerequisite without revaluing saved runs | One simulation configuration-to-sizing use case with one monetary policy owner | WF-005; OP-08; CONTRACT-011/014; BND-007/009/012 | None. Scoped monetary conventions and independent examples under DEFER-004 are mandatory; sample mockup values are not financial defaults |
| `SC-008` | Manage historical instructions and complete simulated outcomes | Submit Market/Limit/Stop entries and SL/TP, modify/cancel pending orders, and partially/fully close a targeted position; evaluate eligible events into complete fill/protection/fee/USD effects or an explained block | One decision-to-outcome trading lifecycle; acceptance alone is not a completed trade and opposite entries preserve independent exposures | WF-005/006; OP-07/09/10; CONTRACT-005/006/013/014; BND-004/007/008/009 | None. Requires writable replay, sizing and retained evidence. SC-006 and SC-008 are coupled through WF-006; a later brief must include missing support or refine selection explicitly, never assume it exists. DEFER-002/004 and affected UI findings apply |
| `SC-009` | Resolve a blocked original historical event | Explain the original event and missing prerequisite; accept compatible completion and reevaluate that same event once, or remain blocked/offer explicit updated-data restart | One blocked-event recovery use case reusing execution rather than introducing a second pricing path | WF-007; OP-11; CONTRACT-007/012/013/014; BND-004/007/008/009/010 | None. Requires accepted replay/execution/block context; original event timing, committed basis and prior outcomes must be preserved |
| `SC-010` | Rewind or deliberately restart a historical exercise | Confirm the exact affected run/scope, reconstruct the retained prefix or explicitly choose a new basis; cancel without change and preserve independent drawings | One destructive historical timeline change with coherent replacement and scope-bound confirmation | WF-008; OP-12; CONTRACT-008/009/019; RW-005; BND-007/010/013 | None. Requires replay/execution/recovery behavior. No discarded-trade journal or silent latest-history rebinding; ADV-VER-001 applies to scoped replacement races |
| `SC-011` | Back up and restore coherent local work | Back up required analysis/run versions and original input closure; validate and confirm replacement restore, deletion or reset, with exact recovery and denied/failed outcomes | One local work protection/replacement lifecycle; restore never silently merges or imports arbitrary external runs | WF-002/008; OP-13; CONTRACT-009/015/019; RW-006; BND-005/007/010/013 | None. Requires actual work to protect and proven retention/authority capabilities. Reuse accepted autosave/resume from SC-002/006; verify actual storage/process recovery and preserve unrelated acknowledged state |
| `SC-012` | Export the intended local chart image | Export bounded selected chart/studies/drawings and labels, including current/replay basis and actual local artifact outcome | One chart snapshot-to-local-image journey, separate from report meaning | WF-009; OP-14; CONTRACT-010/012/020; BND-007/012 | None. Requires chart and any exported study/drawing/replay behavior; scoped DEFER-003 output conventions and complete custom-layer capture must be resolved |
| `SC-013` | Inspect and export own-run results | Inspect recorded orders/fills/positions/fees/USD effects and metrics, then export an own-run report with original conventions/evidence and historical boundary | One recorded-results interpretation/export use case; reports consume recorded outcomes rather than recalculate against latest history | WF-009; OP-14; CONTRACT-006/010/020; RESP-019/023/024; BND-007/012 | None. Requires accepted simulated results; monetary/metric/output conventions under DEFER-003/004 apply. External run-bundle import remains excluded |

## Scoped prerequisites carried into selection

- **All candidates:** accepted foundation record and behavioral readiness; current active standards and scoped guides; applicable sole-writer/origin/epoch, retention, diagnostic, performance and accessibility obligations. G6 approves choices, not physical capability. DEFER-007 platform proof and ADV-VER-001 are not discharged by a candidate inventory.
- **History/replay/acquisition:** DEFER-002 forbids invented session closure, publication finality or FX applicability; missing facts remain unresolved/blocked. SC-005 additionally requires DEFER-001 protected actual provider evidence. Controlled fixtures cannot certify live acceptance.
- **Studies, drawings, ranges and exports:** identify approved scoped conventions under DEFER-003 before the affected brief. DEFER-005 interaction/default/undo obligations must be matched to the current UI authority rather than guessed.
- **Sizing/trading/results:** DEFER-004 exact monetary/notional/quantity conventions and independent examples are required before affected calculation briefing. Decimal representation alone does not discharge these semantics.
- **Trading UI:** current UI review revision 5 narrows UIADV-INT-002 to MP-096 light/dark missing-SL draft readback. Resolve the pair, scoped G5 and independent recheck before dependent realization is accepted. UIADV-VIS-001 also requires existing Buy/Sell selector palettes and affected reapproval. Do not copy contradictory approved illustrative endpoints into product behavior. UIADV-ART-002 is a checker lifecycle-summary residual; exact approvals remain the source of visual identity. Unaffected work is not globally blocked by these findings.
- **Runtime:** DEFER-006 resource/timing/backoff choices require their owning standards/integration/performance evidence; this inventory supplies no new numerical thresholds.

## Completed or unavailable capabilities

| Capability | Reason excluded from current candidates | Evidence |
|---|---|---|
| Foundation/tooling bootstrap | `OTHER_EXPLICIT_REASON`: mandatory predecessor, not a behavioral G7 candidate; must use FOUNDATION mode | Standards Document Status and Section 11; project-state Sections 3/5; no accepted foundation record |
| Settings / Data location adoption | `OTHER_EXPLICIT_REASON`: UI exists but architecture ownership, validation/publication and catalog-adoption contract is missing; do not invent a candidate from UI alone | ui-dossier Section 23, UISYN-MOD-004; UI-IMPL-015; ui-review revision 5 Section 9. Route to system-architecture-designer before affected briefing; this does not exclude qualified reads from an established input root |
| Scripting/alerts, brokerage effects, mobile and external run-bundle import | `NO_LONGER_SUPPORTED_BY_CURRENT_ARCHITECTURE`: outside the current v1 scope; this label denotes current exclusion, not a claimed historical implementation | Architecture Sections 1/9/15 and WF-008; standards Section 1 |

No behavioral capability is excluded as `ALREADY_IMPLEMENTED`; no accepted implementation record supports that claim.

## Selection

**Selected slice:** `NONE`

**Selected candidate ID:** `NONE`

**Selection evidence:** `Awaiting explicit human selection` after foundation readiness is established and this inventory is revalidated. The request to generate this document is not a slice selection.

**Gate G7:** `NOT REACHED` — foundation prerequisite unmet. No `CANDIDATE_SLICES_PROPOSED` or `READY_FOR_IMPLEMENTATION` signal is emitted.

## Refresh conditions

Refresh when accepted foundation evidence establishes behavioral readiness, or any of the following materially changes the candidate set or its eligibility:

- approved architecture or explicit project scope, including the missing Data location contract;
- accepted implementation records, supersessions or completed capabilities;
- relevant UI authority, approval identities or independent finding dispositions;
- a prior candidate is superseded, overlaps an accepted realization, or is no longer coherent;
- prerequisite refinements materially change an affected candidate's scope.

Read every accepted REC entry and respect supersessions before reissuing candidates. Reuse accepted support behavior; combine or refine coupled candidates explicitly before a SLICE brief. Do not refresh mechanically after every slice if the remaining set stays current. Do not rank or select candidates without explicit project/human authority.
