# UI Review

## 1. Review status

- **Target:** [ui-dossier.md](ui-dossier.md), revision 16, 20 October 2026, `READY_FOR_UI_ADVERSARIAL_REVIEW`.
- **Review:** revision 1, 21 October 2026; independent static design audit using the UI Adversary protocol and quality gates.
- **Verdict:** `REQUIRES UI REVISION`.
- **Findings:** 0 BLOCKING, 3 HIGH, 4 MEDIUM, 0 LOW.
- **Evidence confidence:** sufficient for the static findings below. Runtime behavior and the rendered HTML state specimen are evidence limited as described in Section 2.
- **Independence:** no design authority, approved visual, generator of approved visuals, or approval record was corrected by this review. Proposed staleness below applies **if corrections are accepted**, not as an unrecorded revocation of G4/G5.

## 2. Evidence set

### Canonical target and upstream authority

The complete 1,374-line UI dossier was read, including all inventories, annotations, verification properties, handoff constraints, and approval history. The complete [visual-system.md](visual-system.md), revision 2, was read. Standalone `interface-requirements.md`, `interaction-model.md`, `interface-structure.md`, `wireframe-index.md`, `mockup-prototype-index.md`, and `ui-verification-model.md` are absent. Their designated canonical replacements are UI dossier Parts I–III, Sections 15/18–19 with the JSON indexes, and Sections 20–21. Their absence is not a finding.

Relevant requirements reviewed include FR-03–FR-25, FR-27, FR-38–FR-55, CONS-01, and accepted U2/U5/U6/U12–U14. Domain checks used TR-27–TR-29, INV-03/13, PRE-02/03/06/08–10 and the scoped DM-GAP items. Architecture checks used CONTRACT-001–012/018–020, TX-001–006, CM-001–007, ORDER-005, CONC-003/004/008/012, and DEFER-001–007. Architecture was consulted for these UI-visible guarantees, not re-audited in full. The existing architecture review and ADV-VER-001 remain independent authorities/obligations.

### Visual artifacts inspected

| Artifact | Identity and approval | Actual inspection |
|---|---|---|
| WF-FRAME-001–092 | WF-SET-001-r8; G4 approved on 20 October, dossier Section 17 and frame-index.json | All 92 canonical SVGs parsed, text/control content examined, independently rendered and visually inspected in comparison sheets |
| MP-MOCK-001–092, light and dark | MP-SET-001-r3; G5 approved on 20 October, Section 21 and mockup-index.json | All 184 canonical SVGs parsed, text/control content examined, independently rendered and visually inspected alongside their wireframes |
| frame-index.json and mockup-index.json | Current set/version/state/approval crosswalks | All 92 rows in each read; all 92 source SHA-256 references independently matched |
| wireframes/index.html and mockups/index.html | Authored offline review galleries | Source structure, artifact references and all local links checked; gallery navigation is not a product prototype |
| wireframes/replay-review.html | Supplemental A32/frame-090 comparison | Source and references inspected; it does not supersede current canonical r8 files |
| MP-SPEC-001.html | Supplementary paired-theme state/visibility specimens | Complete authored HTML/CSS inspected, including eight visibility button pairs across the two themes; browser-rendered appearance/focus could not be inspected |
| Maintained previews | Derivatives, not separate approved design authority | Canonical SVGs were rendered afresh instead of relying on earlier PNGs. No conclusion assumes previews supply missing states |
| Product prototype/scenarios | Explicitly not supplied under dossier Section 18 | No MP-PROT artifact or financial interaction was inferred |
| E01/E07; authenticated A24/A29; supplemental A30/A31/A32 reference PNGs | Geometry references, not feature or calculation authority | Original local PNGs visually inspected; supplemental identities/provenance checked in reference-screenshots.json. Captured target HTML was not opened |

[Review evidence manifest](ui-artifacts/review/evidence-manifest.json) records the exact reviewed file hashes, scope, source-digest result and checker failure. Review renders were temporary inspection aids, not replacement visuals. Approval provenance is the supplied dossier/index/project ledger; original approval messages were not independently retrieved.

### Evidence limitations

- Static images establish composition, displayed meaning and designed availability; they do not establish actual command execution, focus restoration, scrolling, async recovery, numerical correctness, performance or WCAG conformance. These remain UIV-EVID-001–008 obligations. No observed user behavior or usability study is claimed.
- Chromium could not start in the sandbox (`setsockopt: Operation not permitted`); a Firefox headless fallback also exited before producing an image. Thus rendered MP-SPEC-001 focus/hover behavior is **EVIDENCE LIMITED**. All 276 canonical SVGs rendered successfully through Inkscape.
- All four visibility combinations are shown as **buttons** in MP-SPEC-001, not as complete charts with corresponding values/studies. This is relevant to UIADV-INT-001 and UIADV-DATA-001, not evidence of a working toggle implementation.
- Provider integration, precise calculation/monetary/tool conventions, technical realization and durability remain existing DEFER obligations. Their intentional deferral is not counted as a new design failure.

## 3. Executive assessment and claim map

The dossier provides strong semantic authority: nineteen tasks, fourteen journeys, eight views, explicit scope-bound confirmations, retained replay inputs, and objective verification obligations. The complete approved visual inventory is present and byte-current against its wireframes. Nevertheless, approval and source matching do not establish semantic fidelity. Important trading states reuse a generic shell without the required state meaning; destructive variants retain rewind scope; and core trading branches lack sufficient concrete realization. Broad UI implementation integration should wait for the three HIGH findings to be resolved and affected visuals reapproved.

| Area | Canonical claim / sources | Visual evidence | Verification / assessment |
|---|---|---|---|
| Goals/tasks | UIR-TASK-001–019; IF-JRN-001–014 | All eight visual groups exist | UIV-JRN-001–014; core trading realization gap ART-001 |
| Journeys/navigation | IF-NAV-001–012; IF-CONT-000 | Search, settings, work, evidence, output and return surfaces | UIV-INT-001; static return intent explicit, runtime unproven |
| Structure/hierarchy | UIS-REG-001–026; UIS-PAT-006–011 | Persistent chart, contextual drawers/docks and permitted floating exceptions | UIV-STRUCT-001; reference geometry respected |
| State/feedback/recovery | UIR-STATE-001–014; UIS-PAT-001–003 | 001–064 plus 077/091/092 | UIV-STATE-001–003; STATE-001/002 |
| Safety | IF-CONF-001–003; UIR-SAFE-001–005 | 049–056/071/078–080 | UIV-JRN-006/014; SAFE-001 |
| Adaptation | UIS-ADAPT-001–006 | 065–072; two-chart 073 | UIV-ADAPT-001; structural fallback present, runtime reachability unproven |
| Accessibility/input | UIR-A11Y-001–006; IF-A11Y family | Numeric inspector/point editor 006/074; specimen markup | UIV-A11Y-001–003; dual-series semantic gap DATA-001 |
| Visual semantics | VIS-STATE-001–015; paired role palette | Light/dark pairs and state labels | UIV-VIS-001; known failure/unknown collision STATE-002 |
| Data interpretation | UIR-INFO-001/003/007–011; VIS-DATA-001–008 | Candles/OHLC, selected targets, result and provenance surfaces | UIV-DATA-001/002; INT-001/DATA-001 |
| Visual authority | UI-ART-001–092; Sections 17/21/23 | All canonical files available and source hashes current | Semantic inconsistencies persist despite geometric equality |
| Verification | Thirty UIV properties; eight expected evidence classes | review-checks.json claims current design checks | VER-001: maintained checker cannot reproduce them after approval |
| Implementation freedom | UI-IMPL-001–012; UI-FREEDOM-001–005 | SVGs explicitly not production components | Appropriate freedom preserved; missing consequential screen decisions are not local coding freedom |

## 4. Positive evidence

| Area | Evidence | Why it matters |
|---|---|---|
| Replay disclosure | IF-JRN-012, UIS-STATE-048; WF/MP-048 explicitly withhold later times/prices/metrics | The continuity surface has a deliberate replay-safe form instead of implicitly using current quotes |
| Accepted versus executed | WF/MP-091 name O-008, say “Accepted · waiting; not filled”, retain Modify/Cancel, and disable replay-bar entry | Acceptance is not visually promoted to a fill; a selected accepted order remains inspectable |
| Evaluation exclusion | WF/MP-092 disable start/play/step/new entries and state that no fill is confirmed | This dedicated frame demonstrates the exclusion that other states should consistently retain |
| Unknown versus complete output | WF/MP-061/062/063 separate incomplete, verify-unknown and verified-complete outcomes | Export failure is independent from the retained source, with no automatic source mutation |
| Responsive structure | WF/MP-065–072 wrap the toolbar and reserve lower task space; 071/072 retain task actions; replay capsule wraps at zoom | Supported effective zoom has a concrete structural fallback. The 640px illustration is correctly not promoted to a product breakpoint or mobile requirement |
| Annotation access | WF/MP-006/074 expose object identity and editable time/price/point concepts, with preview cancellation | There is an explicit route toward the accepted keyboard drawing alternative, without treating a measurement as a trade |
| Scope restraint | Disabled future bundle launcher and screenshot-only presets; UI-DEFER-001–004 | Reference screenshots and inert review controls do not automatically grant new product or financial behavior |
| Verification honesty | Sections 20–21 distinguish required properties from future evidence | Static design checks are not described as financial, durability, performance or accessibility implementation passes |

## 5. Findings summary

| ID | Severity | Type | Area | Earliest owner | Finding |
|---|---|---|---|---|---|
| UIADV-SAFE-001 | HIGH | DESIGN DEFECT | Destructive scope | wireframe-designer | Restore/delete/updated-restart confirmations retain rewind-specific target fields and omit their required scope |
| UIADV-STATE-001 | HIGH | DESIGN DEFECT | State truthfulness/recovery | wireframe-designer | Concrete no-run, blocked/restricted and replacement-success frames contradict or omit their state meaning |
| UIADV-ART-001 | HIGH | READINESS GAP | Core trading realization | wireframe-designer | Claimed trading coverage lacks concrete conditional entry and valid targeted-close/modification realizations |
| UIADV-INT-001 | MEDIUM | READINESS GAP | Quote/calculation basis | interaction-flow-designer | Visibility is separated from calculation basis without a defined user-facing basis selection/readback path |
| UIADV-DATA-001 | MEDIUM | READINESS GAP | Dual-series interpretation | visual-system-designer | Showing both quote series has no defined non-color series identity or inspected complete chart specimen |
| UIADV-STATE-002 | MEDIUM | DESIGN DEFECT | Save outcome | wireframe-designer | Known save failure is displayed with publication-unknown meaning and recovery |
| UIADV-VER-001 | MEDIUM | READINESS GAP | Design verification | ui-verification-designer | Documented checker rejects the approved set before performing its checks |

## 6. Detailed findings

### UIADV-SAFE-001 — Destructive variants do not identify their actual replacement/deletion scope

- **Severity / type / area:** HIGH / DESIGN DEFECT / safety and exact scope.
- **Evidence:** UIR-INFO-014, UIR-SAFE-002/003, IF-CONF-002/003, WF-ANN-007, UIS-REG-021/022, UI-IMPL-005; inspected WF-FRAME-078–080 and MP-MOCK-078–080 in both themes. MP-078/079 line 430 and MP-080 line 450 all display `Target R-014 / v12 · Destination 09:30 UTC / R-014`.
- **Finding:** The restore frame names no backup candidate, included analysis/runs, input-completeness result or current replacement scope. The layout-deletion frame names a run/time destination rather than the selected layout. Updated-data restart names no selected new input basis or what it replaces. These are actual product fields, not just outside-product annotations. Generic “validated” or “selected updated input basis” prose does not identify those scopes. WF-ANN-007 expressly prohibits reusing rewind content for another destructive operation.
- **Consequence:** The confirmation cannot communicate the concrete work/input change being approved. A faithful implementation would reproduce an inadequate review; filling it in requires additional screen design. This is a visual-realization defect against already explicit safety authority, not a new policy requirement.
- **Minimum correction direction:** Give each operation's existing confirmation structure its actual target, version, affected/replaced content and applicable validation/new-basis information. Keep cancel and unchanged-before-publication semantics. No new confirmation layer or archive capability is requested.
- **Earliest owner:** `wireframe-designer` (current combined lifecycle: `ui-screen-designer`, LOW_FI_WIREFRAMES).
- **Affected canonical sections:** 15–16, 18–20, UID-007, UI-IMPL-005; UI-ART-078–080.
- **Stale downstream artifacts if corrected:** WF-078–080, paired MP-078–080, their previews and index/registry entries; any reused confirmation branch affected by the correction; UIV-JRN-006/014 and evidence mapping as needed. Unrelated charts, provider authority and palette remain stable.
- **Human visual reapproval required:** YES, affected G4/G5 artifacts.

### UIADV-STATE-001 — Shared shell content contradicts material trading and replacement states

- **Severity / type / area:** HIGH / DESIGN DEFECT / truthfulness, restriction and recovery.
- **Evidence:** UIS-STATE-026/030/032/055, UIR-INFO-006/011/015, VIS-STATE-002/007/013/014, WF-ANN-004/007, UIV-STATE-001–003; inspected WF/MP-026/030/032/055, paired themes. Architecture CONTRACT-004/007, CM-006, TX-005 govern the meaning.
- **Finding:** MP-026 says “No active run” in its task/results content while simultaneously showing `Run R-014 · Paused`, a replay cursor and an enabled Play command. MP-030 is the blocked-state realization but shows the generic order panel and a “Draft buy / Not submitted” row with no original-event block reason or resolution entry in the product. MP-032 likewise supplies no offline/restricted reason or authority recovery meaning alongside its disabled entry controls. After the rewind proposal in 049, MP-055 says the replacement is published but still displays the old 09:42 cursor, the 09:30 destination proposal, “Cancel keeps the current simulation”, and Cancel. There is no label identifying this as a historical before-snapshot.
- **Consequence:** The analyst cannot reliably identify whether there is an active run, why trading is unavailable, or which post-replacement cursor is authoritative. The completed replacement frame also suggests prepublication cancellation still applies. The declared common boundary and safe recovery require state-dependent screen content; a generator's state title or outside-product note cannot supply it.
- **Minimum correction direction:** Make the product shell, task region, actions and recovery entry coherent with each represented branch. Show a reason and permitted next step for blocked/restricted state; show the surviving state after known publication. If old evidence is intentionally retained temporarily, explicitly identify its scope and unavailable current values. Do not change architecture guarantees.
- **Earliest owner:** `wireframe-designer` / `ui-screen-designer` LOW_FI_WIREFRAMES.
- **Affected canonical sections:** 15–16, 18–22; UI-ART-026/030/032/055 and shared-shell state mapping.
- **Stale downstream artifacts if corrected:** Those four WF/paired MP sets, dependent previews/index rows and any additional state frames found to share the same contradiction; relevant UIV state reference mapping. Revision must check the shared shell across the full inventory, rather than blindly regenerate every approval.
- **Human visual reapproval required:** YES, revised G4/G5 artifacts.

### UIADV-ART-001 — Core trading branch coverage is asserted without sufficient concrete realization

- **Severity / type / area:** HIGH / READINESS GAP / task completeness and visual authority.
- **Evidence:** UIR-TASK-011–013, UIR-INFO-007–009, IF-JRN-007–009, UIS-REG-012/013, WF-DEC-005, UID-004, UIV-JRN-007–009; all 92 approved compositions inspected, especially WF/MP-025/029/068/076/090–092. PRE-06 and TR-28/29 distinguish valid partial and full closure.
- **Finding:** Entry frames 025/090 show the Market branch with selectable Limit/Stop and Risk, but there is no realized Limit/Stop entry-level field/state or Risk-% input/estimate/validation branch before replay-strip commitment. The `Price / % / Ticks / ATR` row selects a price mode; it does not itself supply an entry level. The only concrete targeted-close form is rejected frame 029; no valid selected-position close form shows remainder/protection and partial/full review. Its example requests 10,000 against a displayed 10,000 remainder yet says the amount exceeds the remainder, while its result row is a new buy draft. Pending-order frame 076 labels the order `Morning review / v12` (the layout identity), rather than its order identity, and shows no modification-draft/application endpoint. The accepted-order inspection in 091 is useful but does not provide those missing editing branches. The generic zoom “Task detail / review” action is not an inspected realization of its destination.
- **Consequence:** The inventory's stated coverage of entry, modification and independent reduction is stronger than its visual evidence. Implementers must invent consequential fields, target binding, review/co-presence and commit mapping or reuse an incorrect entry form for an existing position/order. UIV obligations describe the desired outcome but do not supply missing screen-specific design.
- **Minimum correction direction:** Supply the minimum material branch/state compositions or equally concrete annotated realizations for conditional entry/risk sizing, pending modification, and valid targeted partial/full close. Bind terms to the selected order/position and the common decision point; make synthetic examples internally coherent. Preserve existing replay-strip new-entry commitment and separate modify/cancel/close intents. Exact financial formulas and parameter bounds remain with DEFER-003/004.
- **Earliest owner:** `wireframe-designer` / `ui-screen-designer` LOW_FI_WIREFRAMES. Existing interaction authority is sufficient; this does not request a new requirements interview.
- **Affected canonical sections:** 15–16/18–20/22, UI-ART-025/029/068/076/090–092 and any added branch entries.
- **Stale downstream artifacts if corrected:** Revised/new WF branches, corresponding paired MP branches and previews, group/index/registry/UID-004 mappings and relevant UIV references. The A32-inspired shell and unrelated chart/work/continuity compositions need not change merely because trading content is clarified.
- **Human visual reapproval required:** YES, revised/new G4/G5 artifacts.

### UIADV-INT-001 — Visibility controls do not complete the calculation-basis interaction

- **Severity / type / area:** MEDIUM / READINESS GAP / basis selection and interpretation.
- **Evidence:** Requirements FR-04 explicitly requires the chosen quote side to apply consistently to chart-dependent studies; UIR-TASK-001/003/005, UIR-INFO-001/003, IF-JRN-001/002, UIS-PAT-002, WF-DEC-015, Section 18 Bid/Ask propagation, UIV-INT-002; toolbar/settings/inspector realizations including 001/073/075 and the complete MP-SPEC-001 source. CONTRACT-001/018 require a declared side/basis.
- **Finding:** The late revision correctly makes Bid/Ask independent visibility controls and explicitly says they do not change the separately governed calculation basis. The preceding flows still describe choosing bid/ask for observations/calculations. No interaction rule or concrete surface identifies how that independent basis is selected or how selected-bar/study/volume values relate to it when Ask alone, both, or neither is visible. Every complete mockup depicts the default Bid basis; button-only specimens cannot answer the interpretation question.
- **Consequence:** An Ask-visible chart can retain Bid calculations legitimately, but the analyst and implementer lack a complete selection/readback contract. Implementers may couple visibility to calculation in violation of UIV-INT-002 or silently hardcode a basis. This affects the scoped chart/study work; it need not block unrelated work.
- **Minimum correction direction:** Reconcile the original side-selection task with the accepted independent visibility behavior. Identify the existing basis selection/readback path and label the scope of values/studies/volume across the four combinations. Do not make visibility alter execution prices or infer a new financial policy.
- **Earliest owner:** `interaction-flow-designer` (current lifecycle: `ux-architecture-designer`, DELTA); architecture/domain owners only if the proposed resolution changes calculation semantics.
- **Affected canonical sections:** 2–3/8/13/16/18/20/23, especially WF-DEC-015 and UIV-INT-002.
- **Stale downstream artifacts if corrected:** Affected selection/configuration/inspection flow and structural rows; relevant VIS basis labels; WF/MP toolbar, chart-heading, numeric/study/volume variants including 001/073/075; MP-SPEC-001 and UIV mappings. The shared toolbar may affect all compositions, but no unrelated recovery/business policy should change.
- **Human visual reapproval required:** DEPENDS on the accepted realization; YES for changed approved composition/content.

### UIADV-DATA-001 — Dual quote series have no canonical visual discrimination

- **Severity / type / area:** MEDIUM / READINESS GAP / data visualization and non-color identity.
- **Evidence:** WF-DEC-015 permits both series; UIR-A11Y-005, VIS-PRIN-001/006, VIS-DATA-001/002 and VIS-A11Y-003 govern source identity and redundant cues. All canonical charts show Bid-only. MP-SPEC-001 shows the both-pressed buttons but no corresponding plot/legend/numeric inspection.
- **Finding:** Hollow/filled teal/rose distinguishes financial direction. It does not distinguish a Bid candle from an Ask candle of the same direction. The visual system predates dual-series visibility and defines no quote-series distinction, overlap treatment or legend/value association for that state. The study-series palette does not implicitly define a candle-side grammar.
- **Consequence:** Displaying both series forces a new visual-semantic choice during implementation and creates a plausible risk of attributing a candle/value to the wrong quote side, particularly when the series overlap or hue is unavailable. This is a reasoned interpretation risk, not an observed user-research result.
- **Minimum correction direction:** Specify quote-side identity and legible overlap/inspection behavior in the existing visual grammar, preserving direction cues and the accepted default themes. Demonstrate both-visible with its legend/numeric association. No new theme or chart type is requested.
- **Earliest owner:** `visual-system-designer`.
- **Affected canonical sections:** visual-system data/identity rules; dossier 16/18–20/23, WF-DEC-015, UIV-DATA-001 and UIV-INT-002.
- **Stale downstream artifacts if corrected:** Affected VIS tokens/rules, quote-series WF/MP specimens and chart variants, MP-SPEC-001, indexes/registry and UIV references; both-theme rechecks. Unchanged trading eligibility, fees and retention remain stable.
- **Human visual reapproval required:** YES for changed visual direction/rules and dependent approved visuals, at their applicable gates.

### UIADV-STATE-002 — Known save failure is given unknown-publication semantics

- **Severity / type / area:** MEDIUM / DESIGN DEFECT / durability feedback and recovery.
- **Evidence:** UIR-STATE-007, UIR-ERR-004, VIS-STATE-006, UIS-STATE-015, WF-ANN-002, UIV-STATE-002; WF-FRAME-015 and MP-MOCK-015 light/dark. Architecture CM-003 and TX-004 distinguish known failure from an uncertain acknowledgement.
- **Finding:** The task footer says `Draft applied to working state; save failed for this version`, but the same product uses a question/uncertain treatment and its global footer says `Working v13 / Save outcome unknown · Reconcile >`. It never explains that these are different operations or versions.
- **Consequence:** A known failed retention needs correction/retry of retention; unknown publication first needs reconciliation. The approved frame gives incompatible recovery meanings for what appears to be the same save, weakening the exact distinction required by the dossier.
- **Minimum correction direction:** Represent either the known-failure or unknown-publication branch coherently, or explicitly identify separate operation/version scopes if both coexist. Preserve the already applied working settings; never repeat Apply as a save repair.
- **Earliest owner:** `wireframe-designer` / `ui-screen-designer` LOW_FI_WIREFRAMES; matching high-fidelity styling follows it.
- **Affected canonical sections:** 15–16/18–21; UI-ART-015 and its UIV references.
- **Stale downstream artifacts if corrected:** WF-015, both MP-015 themes, dependent preview/index entries; any added alternate save branch and its evidence mapping. Unrelated saved-version authority remains stable.
- **Human visual reapproval required:** YES, affected G4/G5 artifacts.

### UIADV-VER-001 — Current approved artifact checks cannot be reproduced

- **Severity / type / area:** MEDIUM / READINESS GAP / verification evidence.
- **Evidence:** Dossier Sections 18/21 prescribe `python analysis/tradingview/check_mockups.py` and cite review-checks.json as current r3 validation. Running that exact command on 21 October exits 1 at check_mockups.py:17: `assert all(f['gate_g5'] in ('PENDING', 'STALE') for f in rows)`. All 92 current rows are `APPROVED`. The existing record nevertheless reports G5 approved and passing current checks.
- **Finding:** The maintained design-check procedure rejects the accepted lifecycle state before running its artifact checks. This does not disprove an earlier preapproval pass, invalidate actual human approval, or establish visual drift. It means the current evidence cannot be regenerated by its documented procedure.
- **Consequence:** Later review cannot reproduce the claimed postapproval consistency check, and a new run cannot distinguish approval-state incompatibility from actual design drift.
- **Minimum correction direction:** Make the design verification procedure accept and preserve the documented approval lifecycle while still detecting changed sources; rerun and record checks against the current artifact identities. Independently retain semantic review obligations, since geometric equality alone misses SAFE-001/STATE-001/ART-001. This review does not repair the checker.
- **Earliest owner:** `ui-verification-designer` (current lifecycle: `ui-screen-designer`, HIGH_FI_AND_VERIFICATION).
- **Affected canonical sections:** 18/21 and the procedure/evidence link used by UI-IMPL-011.
- **Stale downstream artifacts if corrected:** check procedure, review-checks.json and relevant evidence notes; no approved visual becomes stale solely from correcting a checker lifecycle assertion.
- **Human visual reapproval required:** NO, unless rerun checks expose actual visual/source changes.

## 7. Review-dimension coverage

| Dimension | Result | Notes |
|---|---|---|
| Requirements/traceability | FINDING | Task inventory is strong; side/basis revision is incomplete (INT-001) |
| Journeys/tasks | FINDING | Trading branches lack concrete realization (ART-001) |
| Interaction/recovery/context | FINDING | Basis readback and blocked/restricted meaning; static focus/return intent is otherwise explicit |
| Structure/information/action hierarchy | FINDING | Persistent shell is coherent; consequential trading content is incomplete within it |
| States/feedback/truthfulness | FINDING | STATE-001/002; good accepted/evaluation/output examples do not cancel them |
| Safety/irreversibility | FINDING | SAFE-001; no broker/real-cash action invented |
| Adaptive/environment | PASS for static structure; EVIDENCE LIMITED at runtime | Eight explicit zoom frames; no invented mobile or fixed breakpoint requirement |
| Accessibility/input | FINDING; runtime EVIDENCE LIMITED | DATA-001; named/anchor alternatives specified, keyboard/contrast/conformance unproved |
| Visual system/hierarchy | FINDING | DATA-001 and STATE-002; no aesthetic objection to reference-led shell |
| Data visualization | FINDING | Quote-side identity and basis scope; chart marks are schematic, not financial fixtures |
| Visual artifact coherence | FINDING | All files/hash references current; semantic coverage and content defects remain |
| Verification | FINDING | VER-001; high-risk runtime properties otherwise have explicit UIV obligations |
| Complexity/proportionality | PASS | Drawers/docks, one shared chart shell and absent product prototype are justified; no new navigation/design-system abstraction demanded |
| Implementation readiness | FINDING | Three HIGH corrections required before broad UI integration |

## 8. Change and stress attacks

### Attack A — Change the destructive operation without changing its host dock

- **Authority/driver:** IF-CONF-001–003, UIS-PAT-008, WF-ANN-007; existing restore/delete/restart capabilities.
- **Expected legitimate changes:** Target, candidate/new basis, validation, affected-work consequence and confirm verb; dependent confirmation visuals/evidence.
- **Expected stable areas:** Dock placement, context return, cancel-before-publication semantics, chart shell, provider policy and visual tokens.
- **Observed design blast radius:** 078–080 change heading/prose/verb but retain the same run/time destination tuple. The shared structure has also duplicated operation-specific meaning.
- **Assessment:** Fails exact-scope realization. Correct only affected content and dependencies, then reapprove those visuals; no entire workspace redesign is warranted.
- **Findings:** SAFE-001.

### Attack B — Cross a known replacement publication boundary

- **Authority/driver:** IF-JRN-006, UIS-STATE-049/052/054/055; CM-006, TX-005.
- **Expected legitimate changes:** Authoritative cursor/generation and task outcome/actions after known success; uncertainty before reconciliation remains distinct.
- **Expected stable areas:** Drawings, retained-prefix meaning, chart identity and unaffected local work.
- **Observed design blast radius:** 055 changes the success message but retains the old cursor/proposal/cancellation content; 054 does at least expose reconciliation.
- **Assessment:** Postpublication context has not propagated through the shell. Revised state visuals/registry need reapproval, without changing architecture or the drawing model.
- **Findings:** STATE-001; successful uncertainty affordance recorded in Section 4.

### Attack C — Open trading with no run, a blocked event, or writer restriction

- **Authority/driver:** UIS-STATE-026/030/032; UIR-STATE-008/010/013.
- **Expected legitimate changes:** Mode/target truth, unavailable-command reason and allowed recovery, with coherent retained evidence preserved.
- **Expected stable areas:** Chart/analysis identity, permissible inspection, provider/execution rules and exact saved-work distinction.
- **Observed design blast radius:** 026 contradicts itself; 030/032 inherit generic entry content rather than their required explanation. Dedicated 092 demonstrates correct evaluation exclusion, so the issue is inconsistent realization rather than a missing architecture guarantee.
- **Assessment:** Revise dependent state content/availability and review shared-shell consumers; reapprove affected compositions. No runtime bypass or actual unsafe fill was observed or claimed.
- **Findings:** STATE-001, with ART-001 affecting associated task terms.

### Attack D — Ask only, both sides, then neither visible

- **Authority/driver:** Direct user-requested WF-DEC-015 and UIV-INT-002.
- **Expected legitimate changes:** Series visibility and pressed cues; defined legend/inspection association.
- **Expected stable areas:** Calculation basis unless separately selected, execution side, replay cursor, axes, drawings and context.
- **Observed design blast radius:** Button specimens cover all combinations; complete plots remain Bid-only and no independent basis path or dual-candle identity rule is supplied. This is semantic incompleteness, not missing files or a failed runtime interaction.
- **Assessment:** Clarify interaction/visual authority, then regenerate only dependent chart/value/specimen content. A toolbar correction may touch many files legitimately; it must not change trading or retention semantics. Section 23 provides the correct staleness/reapproval mechanism for accepted upstream changes.
- **Findings:** INT-001, DATA-001.

### Attack E — Effective desktop zoom and two-chart density

- **Authority/driver:** UIR-ENV-001/003, UIS-ADAPT-001–004, VIS-A11Y-004.
- **Expected legitimate changes:** Toolbar wrapping, collapsed secondary regions, reserved lower task content, capsule wrapping and readable task controls.
- **Expected stable areas:** Two charts remain retained/reachable, run/basis/target/consequence semantics and financial anchors.
- **Observed design blast radius:** 065–072 demonstrate the structural transformations, and 073 retains two chart identities with one named active chart. No forced desktop-minimum enlargement or mobile capability is inferred. Full detailed trading branches still have ART-001's limitation.
- **Assessment:** Static structural attack is contained; keyboard navigation, actual scroll extent, enlarged text and focus require UIV-EVID-006/007. No extra breakpoint, runtime test tool or replacement prototype is mandated by this audit.
- **Findings:** No independent adaptive finding; ART-001 applies to the missing detailed trading realization.

### Attack F — Move the artifact set from pending to approved

- **Authority/driver:** Actual G5 transition recorded in Section 21.
- **Expected legitimate changes:** Approval metadata/provenance and verification record.
- **Expected stable areas:** Source identity, design geometry, palette, command semantics and the ability to verify them.
- **Observed design blast radius:** The check stops at its lifecycle assertion. Independent review still matched all 92 source digests and rendered all 276 SVGs.
- **Assessment:** Verification is accidentally coupled to preapproval status. Repairing this evidence procedure alone does not invalidate visual approval; any actual source changes found later must use Section 23 staleness rules.
- **Findings:** VER-001.

## 9. Correction routing

| Finding | Earliest owner / current skill route | Required revision | Downstream stale if accepted | Reapproval |
|---|---|---|---|---|
| SAFE-001 | wireframe-designer / ui-screen-designer LOW_FI | Operation-specific confirmation content | WF/MP-078–080, dependent registry/previews/UIV links | Affected G4/G5 |
| STATE-001 | wireframe-designer / ui-screen-designer LOW_FI | State-dependent shell/task content and recovery | WF/MP-026/030/032/055 and other proven shared dependencies | Affected G4/G5 |
| ART-001 | wireframe-designer / ui-screen-designer LOW_FI | Concrete trading branches, correct target binding/examples | Revised/new trading WF/MP and UID/UIV/index mappings | Affected/new G4/G5 |
| INT-001 | interaction-flow-designer / ux-architecture-designer DELTA | Calculation-basis selection/readback contract | Affected IF/UIS/VIS/chart/value/specimen/UIV references | Depends on accepted UI change |
| DATA-001 | visual-system-designer | Non-color quote-side/overlap/inspection grammar | Dependent dual-series WF/MP/specimen/registry/UIV | Applicable visual gate and affected G4/G5 |
| STATE-002 | wireframe-designer / ui-screen-designer LOW_FI | Coherent known-failure/unknown-save branch | WF/MP-015 and dependent references | Affected G4/G5 |
| VER-001 | ui-verification-designer / ui-screen-designer HIGH_FI | Reproducible approved-set checks | Check record/procedure/evidence notes | No visual reapproval by itself |

Full finding IDs are UIADV-prefixed as in Section 5. Coordinate INT-001/DATA-001 before regenerating dependent charts. Regenerate high-fidelity artifacts only after their governing low-fidelity/semantic correction is settled. Route an actual domain/security/data-authority change to `architecture-workflow`; none is proposed here because existing architecture correctly defines the relevant guarantees. Apply dossier Section 23 to explicitly identify stale UI-ART entries and affected approvals when an upstream correction is accepted. Do not overwrite the design inside this review.

## 10. Implementation-readiness conclusion

Broad UI implementation integration should not proceed until **UIADV-SAFE-001, UIADV-STATE-001 and UIADV-ART-001** are corrected and the dependent visual artifacts reapproved. Independently governed foundation or unaffected work may proceed through its own standards/brief gates, with explicit exclusions for these defective UI surfaces. This audit itself grants no implementation authorization.

Approved visual authority is complete as an inventory and current by recorded source digest. It is insufficiently coherent for the affected behavior. Existing UI-IMPL/UIV constraints are useful, but an implementation brief for confirmations, affected trading states or trading-entry/modification/closure paths cannot yet extract a complete screen realization without additional design. The four MEDIUM issues must be tracked and resolved before their affected work relies on them. Existing DEFER-001–007 and ADV-VER-001 remain in force; this review neither expands them nor discharges them.

## 11. Final verdict

`REQUIRES UI REVISION`

## 10. Design-owner response — 21 October 2026 (not an independent re-review)

The original audit, evidence hashes and verdict above remain historical and unchanged. WF-SET-001-r9 is proposed for human G4 review; ui-dossier.md revision 17 Section 16 maps each correction. All 92 old compositions carry a revised shared basis label, so their paired r3 mockups and previews are stale. Fourteen new low-fi branches have no high-fi counterpart yet.

| Finding | Owner response / evidence | Remaining closure condition |
|---|---|---|
| UIADV-SAFE-001 | Operation-specific scopes in WF-078–080 | G4, paired mockups/G5, independent recheck |
| UIADV-STATE-001 | Coherent no-run/blocked/restricted/replaced/unknown shell and actions; WF-026/030–032/053–055 | Same; runtime behavior remains expected evidence |
| UIADV-ART-001 | WF-029/068/076 and new 093–098 supply concrete entry/risk/modification/close branches | Same; extend UIV/registry in Stage 2D |
| UIADV-INT-001 | ux-architecture-designer scoped delta in dossier Parts I–III; WF-075/103–106 | G4 and Stage 2D readback/visibility specimens |
| UIADV-DATA-001 | visual-system revision 3 VIS-DATA-009; WF-104 plot and side-labelled inspector | G4, both-theme high-fi/contrast review and G5 |
| UIADV-STATE-002 | WF-015 explicitly shows known failed retention v13 vs working v13 / saved v12; WF-007 retains unknown branch | G4 and corrected paired high-fi styling/G5 |
| UIADV-VER-001 | Checker accepts APPROVED lifecycle, retains source hashes and explicitly reports stale pairs without claiming current source geometry; report rerun against r9 | Tool defect corrected; full current-source evidence awaits Stage 2D regeneration. No human visual gate inferred from checker success |

The user-requested Settings / Data location addition is WF-099–102 and UIR-TASK-020 / IF-JRN-015. The application preference ownership/publication contract is explicitly handed to architecture before implementation. This response proposes corrections; it does not close findings on the independent reviewer's behalf or claim high-fi or runtime completion.
