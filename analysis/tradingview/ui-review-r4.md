# UI Review

## 1. Review status

- **Target:** [ui-dossier.md](ui-dossier.md), revision 33, `READY_FOR_UI_ADVERSARIAL_REVIEW`.
- **Review:** revision 4, 22 October 2026; scoped independent recheck of UIADV-INT-002 and its r14/r8 descendants.
- **Verdict:** `READY WITH NON-BLOCKING UI CHANGES`.
- **Open findings:** 0 BLOCKING, 0 HIGH, 1 MEDIUM, 2 LOW.
- **UIADV-INT-002:** **OPEN — partially corrected.** Direction selection, invalidation and matching-only submission are specified and realized. Shared conditional-entry readback remains inconsistent in approved high-fidelity artifacts.
- **Evidence confidence:** SUFFICIENT for this static correction review; dynamic behavior remains EVIDENCE LIMITED.
- **Implementation scope:** unaffected scope may enter implementation governance. Correct/reapprove the affected entry mockups and independently recheck the residual before dependent entry work. Existing folder-contract, DEFER and implementation gates remain applicable.
- **Independence:** no UI authority, canonical SVG, approval, index, generator, maintained checker report, standards approval or project-state.md was changed.
- **History:** [revision 3](ui-review-r3.md) and [its exact evidence manifest](ui-artifacts/review/history/evidence-manifest-r3.json) are preserved, alongside revisions 1/2. This review supersedes current dispositions without rewriting historical evidence.

## 2. Evidence set

### Canonical target and upstream authority

The complete 1,593-line UI dossier was read, including Parts I–VI, the revision-29 transition contract, r14/r8 inventories, verification and handoff. The complete visual-system.md revision 7 was read. Standalone interface-requirements.md, interaction-model.md, interface-structure.md, ui-verification-model.md, wireframe-index.md and mockup-prototype-index.md are absent; their designated authorities are the dossier parts and JSON indexes, not missing requirements.

Requirements FR-27/38–42/47/49/50/53/54 and architecture CONTRACT-005/011, CONC-003/012, IDEM-001 and RETRY-002/003 were consulted for UI-visible semantics. This is not a new architecture, domain, numerical or complete product audit. Requirements, architecture, VIS and all 99 unaffected visual compositions retain the revision-3 evidence boundary.

### Visual artifacts inspected

| Artifacts | Version / approval | Actual inspection |
|---|---|---|
| WF-025/068/090/093–096/107–113 | WF-SET-001-r14; exact G4 approval-r14.json, 22 October | All 14 canonical SVGs parsed, independently rendered with Inkscape and visually inspected in four product contact sheets |
| Corresponding MP pairs, both themes | MP-SET-001-r8; exact G5 approval-r8.json, 22 October | All 28 canonical SVGs parsed, independently rendered and visually inspected in seven product contact sheets; 107 light, 109 dark, 110 dark and 111 light also inspected individually |
| All 113 WF / 226 MP SVGs | Current G4/G5 identities | All 339 hashes independently verified; all source mappings, paired hashes, approved VIS digest, XML safety and entry availability inspected. Compared against revision-3 manifest: exactly seven existing compositions changed and seven added; 99 remain byte-identical |
| Complete frame/mockup indexes and revision records | r14/r8 | Approval lifecycle, source/current identities and changed/retained scope checked against actual files |
| Review galleries and MP-SPEC-001 | Authored, inert navigation/specimens | Maintained local-link checks rerun; no product prototype or demonstrated async trading scenario exists |

The [current evidence manifest](ui-artifacts/review/evidence-manifest.json) pins the target, authorities, all canonical sources, 42 independent renders, observations and checker identities. Temporary PNGs/contact sheets are under `/tmp/ui-adversary-r4/`; they are inspection aids, not new approved design authority. The archived revision-3 review documents the original rendered inspection of the 297 unchanged SVGs; those were not freshly rendered this round.

### Checks and limitations

- All 339 current G4/G5 SVG hashes, G5 source hashes, index hashes and VIS digest match. Human approval is genuine evidence of identity/acceptance, not proof of semantic consistency.
- Both maintained checkers pass. Their report writes were redirected to `/tmp/ui-adversary-r4/` to preserve design-owner evidence. Their checks cover geometry, availability and named palette cases, but miss the contradictory capsule level and the newly named selector palette cases below.
- The wireframe checker's generated G5 summary still says seven pairs are stale/seven absent. Actual G5 approval/index/files prove otherwise; that summary is not adopted as current lifecycle evidence (ART-002).
- Static SVG rendering proves no keyboard completion, focus restoration, async validation, duplicate prevention, actual reflow/scrolling, calculation, provider behavior, performance, durability or WCAG conformance. No browser/product runtime pass or user-research observation is claimed.
- No screenshot-parity finding is made; captured target HTML was neither executed nor embedded. Synthetic values need not be financially validated, but contradictory representations of the same draft remain design evidence.
- UISYN-MOD-004's folder-adoption contract, DEFER-001–007 and ADV-VER-001 remain existing scoped prerequisites, not newly invented UI findings.

## 3. Executive assessment and claim map

**UIADV-INT-002 is not fully resolved.** The UX decision is now explicit: ticket direction selection submits nothing; only the matching validated replay action can submit; relevant edits invalidate estimates; stale results cannot restore validity; unresolved submissions freeze original terms. Ready Buy/Sell, pending/invalid, collapsed and zoom endpoints demonstrate those distinctions.

However, high-fidelity conditional-entry summaries render `level Not set` beside VALID and an enabled matching submission. Six expanded specimens simultaneously show `Entry level 1.08420` in the ticket. Collapsed Sell specimen 110 retains only the contradictory `Not set` summary. This fails the correction's requirement that capsule and ticket represent the same reviewed draft. The remaining correction belongs to high-fidelity realization, not another UX interview or execution-policy decision.

Two LOW issues concern the new direction selectors' VIS palette and stale current-lifecycle summaries. Neither invalidates the supplied direction-selection contract or requires unrelated implementation to stop.

| Area | Canonical claim / authority | Visual / verification evidence | Assessment |
|---|---|---|---|
| Tasks and journeys | UIR-TASK-011/012; IF-JRN-007/008; revision 29 | 025/068/090/093–096/107–113; UIV-JRN-007/008 | Direction flow supplied; shared readback residual |
| Interaction and context | IF-BR-008a; IF-CONT-007/008; UIS-ACT-010 | Ready opposite-side restrictions; 108/109/111/113; UIV-INT-001 | Static endpoints coherent for direction/validity; runtime unproved |
| Structure and safety | UIS-REG-011/012; UIS-PAT-010; UIR-SAFE-004 | Distinct ticket selectors, capsule commits and editor | No added confirmation/netting; conditional terms conflict |
| State truthfulness | UIS-STATE-025/027/029/031 | VALID versus Not set; UIV-STATE-001/003 | INT-002 residual |
| Adaptation and accessibility | IF-A11Y-009; UIS-ADAPT-004 | 068/110/111; UIV-ADAPT-001/A11Y-001 | Editor and readable reasons present; focus/async behavior still requires runtime evidence |
| Visual semantics and data | VIS-STATE-016; VIS-COLOR-016/017; UIR-INFO-007 | Generic Select controls versus A32 selectors; retained entry levels | VIS-001; no new chart-data review implied |
| Artifact lifecycle | Sections 0/17–19/21/23; exact approvals | All 339 identities current; stale precedence/checker summary | ART-002 |
| Verification and freedom | Section 20 INT-002 expectations; UI-IMPL-006 | Explicit wrong-side no-effect, stale response/recheck/unknown obligations | Objective runtime obligations supplied; passing static checks missed actual readback defect |
| Complexity | One shared draft, existing ticket/editor | No extra view, hidden side draft or universal confirmation | Proportionate correction; no new pattern requested |

## 4. Positive evidence

| Area | Evidence | Why it matters |
|---|---|---|
| Explicit direction decision | IF-BR-008a; Section 14 revision 29 | Removes the original ambiguity between selecting direction and submitting an order |
| Symmetric availability | Buy-ready 025/068/090/093–095; Sell-ready 107/110/112 | Exactly one entry action enabled; opposite direction has an adjacent reason and enabled editor route |
| Fresh validation | 096/108/109/111/113; UIV-JRN-007/008 | Invalid/pending blocks both submissions; raw inputs retained; old estimates explicitly superseded |
| No accidental commitment | IF-CONT-008; UIV-A11Y-001; UIV-EVID expectations | Selection, Enter, return, validation completion and queued prior clicks cannot submit; authority is rechecked on fresh activation |
| Uncertainty containment | Revision-29 submission transitions; unchanged 027/031/092 | Original identity/terms frozen; no changed payload/new opposite command while unresolved; acceptance/fill/save distinct |
| Scope containment | Independent comparison against review r3 | Exactly seven revised/seven added compositions; 99 unrelated compositions and historical approvals unchanged |

## 5. Findings summary

| ID | Severity | Type | Area | Earliest current correction owner | Finding |
|---|---|---|---|---|---|
| UIADV-INT-002 | MEDIUM | READINESS GAP | Shared entry draft/readback/commit | mockup-prototype-designer; current ui-screen-designer HIGH_FI_AND_VERIFICATION | Direction contract corrected, but valid conditional capsule says level Not set |
| UIADV-VIS-001 | LOW | DESIGN DEFECT | Visual-system conformance | mockup-prototype-designer; current ui-screen-designer HIGH_FI_AND_VERIFICATION | New generic ticket selectors omit the mandated Buy/Sell palette |
| UIADV-ART-002 | LOW | READINESS GAP | Canonical lifecycle summaries | ui-synthesizer; current ui-screen-designer synthesis/finalization | Current precedence and checker G5 summaries still claim missing/stale pairs |

Previously closed STATE-001/002/003, SAFE-001, ART-001, INT-001, DATA-001 and VER-001 remain closed. Relevant canonical bytes are unchanged from the archived revision-3 review. These are design-review dispositions, not implementation acceptance.

## 6. Detailed findings

### UIADV-INT-002 — Direction contract supplied; shared conditional-entry readback remains inconsistent

- **Status / severity:** OPEN — MEDIUM; original direction ambiguity corrected, minimum shared-draft realization incomplete. No actual wrong-side execution is evidenced.
- **Type / area:** READINESS GAP; review continuity, displayed terms and commitment readiness.
- **Evidence:** UIR-INFO-007, UIR-SAFE-004, IF-BR-008a; Section 14 revision 29 “Draft and validation identity” / “Co-presence and access”; UI-IMPL-006; UIV-JRN-007/008 and UIV-INT-001. Approved MP-068/093/094/095/107/112 in **both themes** show ticket `Entry level 1.08420`, capsule `Type: Limit [or Stop] · level Not set`, `VALID` and an enabled matching Buy/Sell. MP-110 both themes collapses the ticket but retains `level Not set`, VALID and enabled Sell. Corresponding WF sources retain `[price]` / `[price input]`, without asserting absence. MP-108/109/111/113 similarly replace the proposed retained level with Not set during invalidation. The high-fi fixture substitution maps `[price]` to `Not set` while `[price input]` becomes `1.08420` (build_mockups.py fixture mapping); this is provenance, not production-code review.
- **Finding:** The selected side now matches its submission action, but the summary at commitment does not truthfully represent the shared conditional draft. Required price-level absence conflicts with readiness; expanded ticket and capsule disagree. The collapsed variant cannot expose the required level through its promised readback.
- **Consequence:** An implementation following the approved mockup could show an unset required limit/stop level as executable, or disagree about whether ticket and capsule share the terms being submitted. The corrected UX forbids that ambiguity. Synthetic fixtures do not excuse a literal absence/readiness contradiction.
- **Minimum correction:** Make conditional-entry capsule and ticket show the same proposed level and validation context. Use consistent illustrative values or explicit placeholders without turning a required set value into absence. Preserve retained proposed levels during pending/invalid states; if truly absent, keep both submissions unavailable with a reason. Add design-check evidence that compares these readbacks, then independently recheck.
- **Earliest current owner:** `mockup-prototype-designer`, current consolidated `ui-screen-designer HIGH_FI_AND_VERIFICATION`. The UX contract and low-fi structure already supply the decision; do not reopen direction policy or monetary formulas.
- **Affected canonical sections:** Parts V–VI; MP/UI-ART entry rows, UID-004, UI-IMPL-006 and associated UIV evidence. No new upstream semantic rule is required.
- **Downstream stale if corrected:** affected MP pairs, product crops/PNGs/galleries, mockup index/digests, revision/check records and reviewed evidence. Start with 068/093–095/107–113, include other actual capsule consumers only where the shared fixture correction changes them. Unrelated 99 compositions remain stable.
- **Human visual reapproval:** YES, scoped G5 for changed approved content. G4 remains valid if WF bytes/semantics do not change. Current approvals remain historical fact until owning-stage revision; this review does not revoke or rewrite them.

### UIADV-VIS-001 — Generic ticket direction selectors bypass the canonical side palette

- **Severity / type / area:** LOW; DESIGN DEFECT; visual-system consistency. Labels/selection markers preserve direction and prevent this from being a task blocker.
- **Evidence:** VIS-STATE-016 explicitly includes sidebar direction selectors; VIS-COLOR-016/017 and UI-IMPL-014 prescribe Buy `#14532D` on `#DCFCE7`, Sell `#7F1D1D` on `#FEE2E2`, in both themes. MP-025/068/093–096/107–109/111–113 have neutral `Select Buy` / `Select Sell` controls (24 SVGs, 48 controls), using theme text/surface and blue selection. MP-090's named Buy/Sell direction controls and capsule actions retain the mandated colors. Actual rendered artifacts were inspected. The maintained palette check recognizes Buy/Sell/Buy direction/Sell direction, omitting the new Select labels.
- **Finding / consequence:** One repeated direction-selector family has a different visual-role realization from the explicit approved system; copying these artifacts propagates conformance drift while current checks report success. This is an authority contradiction, not a new aesthetic preference or observed user confusion.
- **Minimum correction:** Apply the existing side roles while preserving distinct Select labels, selected/focus markers and non-submission semantics; verify the newly named selector family.
- **Earliest owner:** `mockup-prototype-designer`, current `ui-screen-designer HIGH_FI_AND_VERIFICATION`; no VIS redesign needed.
- **Affected sections / downstream stale:** affected MP/UI-ART rows, paired derivatives, indexes/hashes/check evidence and approval scope. No geometry, interaction or WF change required.
- **Human visual reapproval:** YES, scoped G5 for the changed 12 pairs. G4 unaffected.

### UIADV-ART-002 — Current lifecycle summaries contradict the approved r8 evidence

- **Severity / type / area:** LOW; READINESS GAP; canonical handoff/lifecycle consistency.
- **Evidence:** Section 0's **Current-authority precedence** says Parts V–VI remain PENDING STAGE 2D, seven r7 pairs STALE_SOURCE and seven added pairs absent. Sections 18/21/23/25, the complete current indexes, G4 approval-r14.json and G5 approval-r8.json instead establish all 113 current pairs approved. check_wireframes.py's report G5 field repeats the superseded missing/stale claim despite passing r14 checks; the redirected fresh report reproduces it. This is distinct from explicitly historical revision-29 handoff prose or frozen creation-round SVG margins.
- **Finding / consequence:** Current precedence/check summaries can wrongly direct downstream work back to an already completed stage or cast doubt on the actual approved evidence. Exact hashes and later explicit approval resolve the fact, so no new visual approval deficiency or blocking finding is inferred.
- **Minimum correction:** Reconcile the current precedence statement and maintained check-report summary with actual r14/r8 lifecycle, retaining historical records and the distinction between approval, independent finding status and runtime evidence.
- **Earliest owner:** `ui-synthesizer`, current `ui-screen-designer` synthesis/finalization; checker maintainer for its derived summary.
- **Affected sections / downstream stale:** Section 0, checker-generated lifecycle summary and derived viewer/distribution. Historical revision records and approvals remain unchanged.
- **Human visual reapproval:** NO for documentation/report-only correction with no canonical SVG or semantic change.

## 7. Review-dimension coverage

| Dimension | Result | Scope / limitation |
|---|---|---|
| Requirements/traceability | PASS for correction | Revision-29 contract traced to valid-term review and existing semantic commands |
| Journeys/tasks | FINDING | Shared conditional terms remain contradictory (INT-002) |
| Interaction/recovery/context | PARTIAL PASS / FINDING | Selection/invalidation/commit/uncertainty specified; capsule readback residual |
| Structure/hierarchy | PASS for inspected scope | Existing ticket/editor/commit surfaces; no replacement view required |
| States/feedback/truthfulness | FINDING | VALID/Not set conflict; pending/error endpoints otherwise distinct |
| Safety/irreversibility | PASS with entry residual | No extra confirmation/netting; no destructive-scope change |
| Adaptive/environment | PASS statically / EVIDENCE LIMITED dynamically | 068/110/111 preserve direction/editor; collapsed required-level readback fails |
| Accessibility/input | PASS as specification / EVIDENCE LIMITED dynamically | Named selection, matching availability, no implicit Enter, announcement/return obligations; no runtime proof |
| Visual system/hierarchy | FINDING | New generic selector palette (VIS-001) |
| Data visualization | No new chart-data finding | Chart semantics unchanged; conditional financial terms covered by INT-002 |
| Visual artifact coherence | FINDING | Content contradictions despite matching hashes; lifecycle summary drift (ART-002) |
| Verification | PARTIAL PASS | Objective behavioral obligations supplied; passing static checks miss readback/palette cases |
| Complexity/proportionality | PASS | One shared draft and existing editor; no new navigation/confirmation demanded |
| Implementation readiness | PASS in unaffected scope | Dependent entry realization still requires correction/reapproval/recheck |

Other product categories retain revision-3 dispositions for the 99 byte-identical compositions; this scoped recheck does not claim a fresh exhaustive audit or runtime acceptance.

## 8. Change and stress attacks

| Attack / governing driver | Legitimate changes | Expected stable areas | Actual outcome / blast radius |
|---|---|---|---|
| Valid Buy → attempt Sell; valid Sell → attempt Buy (IF-BR-008a) | Explicit ticket selection followed by fresh validation; matching action only | Run/boundary, raw inputs, independent positions | Static availability symmetric; no dual-enabled entry in any canonical SVG. Dynamic no-effect remains UIV evidence |
| Change side/risk/fixed inputs; late prior validation (IF-CONT-007/008) | Pending/invalid state, superseded estimates, fresh review | Raw proposed levels; prior accepted orders; no implicit command | 108/109/111/113 disable both and name pending/invalid. Contract rejects late results; MP retained-level readback still Not set (INT-002) |
| Collapse Sell ticket or use effective desktop zoom (UIS-ADAPT-004) | Reflow/collapse, same summary/editor, meaningful focus return | Shared direction/terms/boundary/validity | 068/110/111 keep editor/reasons; 110 enables Sell with required level Not set (INT-002). No mobile/breakpoint mandate inferred |
| Lost matching-submit response (IDEM-001; RETRY-002/003) | Freeze original submitted identity/terms and reconcile | Original payload, retained records; distinct modify/close | Normative transitions/UIV forbid payload changes, duplicate intent and queued clicks; unchanged 027/031/092 keep prior restrictions. Runtime unobserved |
| Apply r14/r8 correction without unrelated drift | Seven revised/seven added compositions and dependent evidence | Other 99 compositions, VIS, historical approvals | Hash comparison confirms containment; selector palette and current summary defects are local. Corrections need scoped G5, not blanket G4 invalidation |

## 9. Correction routing

| Finding | Current owner | Required revision | Downstream stale / reapproval |
|---|---|---|---|
| INT-002 residual | ui-screen-designer HIGH_FI_AND_VERIFICATION | Shared proposed-level/readiness readback; targeted design-check evidence | Actual affected MP pairs/derivatives/indexes; scoped G5, then independent recheck; no UX-policy change |
| VIS-001 | Same high-fi owner | Apply existing side palettes to Select controls and verify that family | 12 MP pairs and derivatives; scoped G5; no WF/VIS redesign |
| ART-002 | ui-screen-designer synthesis/finalization; checker maintainer | Current precedence and G5 report summaries | Documentation/derived reports/viewer/package; no visual reapproval |

Existing UISYN-MOD-004 remains with system-architecture-designer before the Data location brief. DEFER-001–007 and ADV-VER-001 retain their owners/triggers. No design correction was performed in this independent review.

## 10. Implementation-readiness conclusion

Unaffected scope may proceed through applicable implementation governance. **UIADV-INT-002 remains an entry prerequisite**, now requiring scoped high-fidelity correction rather than another UX decision. No BLOCKING/HIGH finding remains. The two LOW findings do not require unrelated work to stop.

All 113 WF / 226 MP SVGs are present, identifiable, source-current and explicitly G4/G5 approved. Approval does not eliminate the documented content contradictions. Objective corrected UX/UIV constraints exist, so the owner can repair the realization without inventing direction policy, calculations, extra confirmations or new capabilities. Runtime verification and existing upstream prerequisites remain separate obligations.

## 11. Final verdict

`READY WITH NON-BLOCKING UI CHANGES`
