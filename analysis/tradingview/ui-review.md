# UI Review

## 1. Review status

- **Target:** [ui-dossier.md](ui-dossier.md), revision 35, `READY_FOR_UI_ADVERSARIAL_REVIEW`.
- **Review:** revision 5, 22 October 2026; scoped independent recheck of UIADV-INT-002 against approved WF-SET-001-r14 / MP-SET-001-r9.
- **Verdict:** `READY WITH NON-BLOCKING UI CHANGES`.
- **Open findings:** 0 BLOCKING, 0 HIGH, 1 MEDIUM, 2 LOW.
- **UIADV-INT-002:** **OPEN — narrowed to MP-096, both themes.** The eleven corrected conditional-entry pairs pass readback inspection. The unchanged missing-SL variant still shows a proposed entry level in the ticket and absence in the capsule. Both submissions are correctly disabled.
- **Evidence confidence:** SUFFICIENT for this static design recheck; dynamic behavior remains EVIDENCE LIMITED.
- **Implementation scope:** unaffected scope may enter implementation governance. Resolve/reapprove/recheck the remaining invalid-risk readback before dependent realization is accepted. Existing folder-contract, DEFER and implementation gates remain applicable.
- **Independence:** no UI authority, canonical visual, approval, index, generator, maintained checker report, standards approval or project-state.md was changed. Only independent review/history/evidence, README and derived viewer/distribution were updated.
- **History:** [revision 4](ui-review-r4.md) and [its exact manifest](ui-artifacts/review/history/evidence-manifest-r4.json) are preserved alongside earlier reviews. Current dispositions supersede historical findings without rewriting the evidence.

## 2. Evidence set

### Canonical target and upstream authority

The complete 1,602-line dossier was read, including Parts I–VI, revision-29 entry transitions, r14/r9 inventories, verification and implementation handoff. Standalone interface-requirements.md, interaction-model.md, interface-structure.md and ui-verification-model.md are absent: their designated authorities are dossier Parts I–III and Section 20. JSON frame/mockup indexes supply the inventories in place of standalone wireframe-index.md and mockup-prototype-index.md.

Relevant visual-system.md revision-7 authority includes VIS-COLOR-016/017 and VIS-STATE-016. Requirements FR-27/38–42/47/49/50/53/54 and architecture CONTRACT-005/011, CONC-003/012, IDEM-001 and RETRY-002/003 were consulted for UI-visible meaning. This is a correction recheck, not a new full product, architecture, numerical or runtime audit. Other areas retain the prior review boundary where canonical bytes are unchanged.

### Visual artifacts inspected

| Artifacts | Version / approval | Actual inspection |
|---|---|---|
| WF-025/068/090/093–096/107–113 | r14; approval-r14.json, G4 approved | All fourteen parsed, independently rendered with Inkscape and inspected in four contact sheets |
| Corresponding MP pairs, light/dark | Current set r9; eleven revised pairs approved by approval-r9.json; 025/090/096 retain exact r8 bytes | All 28 parsed, independently rendered and inspected in seven contact sheets; 095 light, 110 dark, 111 light and 096 both themes inspected individually |
| Complete 113 WF / 226 MP inventory | Exact current G4/G5 approval records | All 339 hashes checked independently; source/index/VIS digests, inert SVG content and absence of dual-enabled entry submission checked |
| Frame/mockup indexes; revision-r9.json; approval-r8/r9.json | Eleven changed pairs; 102 retained approved pairs | Compared actual bytes with review-4 manifest: exactly 22 MP SVGs changed, no WF changed; all other 317 canonical SVGs unchanged |
| Galleries, derivatives and maintained checkers | Authored offline design evidence | Both checkers pass with report writes redirected to /tmp; current product crops and local links checked by maintained tooling |

The [evidence manifest](ui-artifacts/review/evidence-manifest.json) pins current sources, observations, 42 fresh renders, approval checks and checker identities. Inspection aids are under `/tmp/ui-adversary-r5/`; their digests are recorded but the temporary images are not packaged or new approved visual authority.

### Evidence limitations

- Approval proves identity/acceptance, not consistency. MP-096 legitimately retains r8 approval inside the current r9 set, but still contradicts the shared-draft contract.
- Both maintained checkers pass. The new conditional readback check covers only the eleven r9-corrected pairs; it omits the unchanged invalid-risk 096 pair. Passing that scoped check cannot establish all conditional variants are consistent.
- The wireframe checker's G5 summary still claims seven stale/seven absent pairs. Actual approval/index/file evidence establishes all 113 pairs exist and are approved. That summary is excluded from current lifecycle truth (ART-002).
- No product prototype exists. Static endpoints cannot establish keyboard completion, focus restoration, actual async invalidation/reconciliation, duplicate prevention, adaptive scrolling, financial calculations, provider behavior, durability, performance or WCAG conformance. No runtime pass or observed user behavior is asserted.
- Captured target HTML was neither executed nor embedded. Synthetic fixtures are illustrative; contradictory values for the same draft remain reviewable design evidence.
- UISYN-MOD-004, DEFER-001–007 and ADV-VER-001 remain separate prerequisites. Coordination/standards summaries predating this review do not supersede the current independent finding disposition.

## 3. Executive assessment and claim map

**UIADV-INT-002 is substantially corrected but cannot close.** All eleven renewed pairs show the same proposed conditional level, 1.08420, in capsule/ticket or the collapsed summary. Ready Buy/Sell actions match direction; pending/invalid variants block both; collapse and effective zoom preserve the editor and terms. The former VALID/Not set contradiction is eliminated in ready conditional specimens.

The retained missing-SL specimen MP-096 is also a conditional-entry draft. Its ticket shows `Entry level 1.08420`, while its capsule says `Type: Limit · level Not set`. Missing SL makes the estimate unavailable, not the already entered Limit level absent. The correction's cross-state consistency requirement therefore remains unmet in this pair. No enabled invalid submission or wrong-side execution is evidenced.

| Area | Governing claim | Evidence | Assessment |
|---|---|---|---|
| Goals/tasks/journeys | UIR-TASK-011/012; IF-JRN-007/008 | Revised 068/093–095/107–113; retained 096 | Eleven corrected pairs pass; missing-SL endpoint remains inconsistent |
| Interaction/context | IF-BR-008a; IF-CONT-007/008 | Explicit ticket selection, matching replay commit, enabled editor | Selection/commit contract remains complete; runtime evidence outstanding |
| Structure/safety | UIS-REG-011/012; UIR-SAFE-004 | One shared draft; distinct modify/close intents | No new view, confirmation, netting or execution policy required |
| States/feedback | UIS-STATE-025/027/029/031 | Pending/invalid 096/108/109/111/113 | Both actions blocked; 096 still loses proposed-level meaning |
| Adaptation/accessibility | IF-A11Y-009; UIS-ADAPT-004 | 068/110/111; UIV-ADAPT-001/A11Y-001 | Readback/editor present statically; actual focus/reflow unobserved |
| Visual semantics/data | VIS-STATE-016; UIR-INFO-007 | Side labels and selectors; entry levels | VIS-001 retained; no new chart-data finding |
| Artifacts/verification | Sections 18–23; UIV-INT-001; UI-IMPL-006 | Exact approvals; eleven-pair checker coverage | Current identities known; 096 omitted from new readback check; ART-002 report residual |
| Complexity/freedom | One shared draft; existing editor | No new navigation or confirmation | Correction remains proportionate; implementation need not invent direction policy |

## 4. Positive evidence

| Area | Evidence | Why it matters |
|---|---|---|
| Ready conditional terms | MP-068/093/094/095/107/110/112, both themes | Capsule level now agrees with the ticket or collapsed draft; readiness no longer accompanies required-level absence |
| Retained pending/invalid proposals | MP-108/109/111/113, both themes | Level 1.08420 persists while prior estimates are superseded and both submissions unavailable |
| Missing-SL restriction | MP-096, both themes | Specific SL error, unavailable estimate, both disabled submissions, editor and Cancel remain visible despite the residual readback defect |
| Symmetric commitment | Buy-ready 025/068/090/093–095; Sell-ready 107/110/112 | Only matching action enabled; opposite reason and editor route present; all 339 SVGs contain no dual-enabled entry |
| Explicit dynamic obligations | Section 14 revision 29; UIV-JRN-007/008, UIV-INT-001, UIV-A11Y-001 | Stale-result rejection, fresh activation, unresolved original terms, no implicit Enter or queued submission are specified objectively |
| Contained revision | Independent review-4 comparison; revision-r9.json | Exactly eleven MP pairs changed; all 113 WF and 102 other MP pairs retain exact identities and approval |

## 5. Findings summary

| ID | Status / severity | Type | Area | Current owner | Finding |
|---|---|---|---|---|---|
| UIADV-INT-002 | OPEN — MEDIUM, narrowed | READINESS GAP | Shared conditional draft/readback | ui-screen-designer HIGH_FI_AND_VERIFICATION | MP-096 retains level 1.08420 in ticket but Not set in capsule |
| UIADV-VIS-001 | OPEN — LOW, carried forward | DESIGN DEFECT | Visual-role conformance | Same high-fi owner | Generic Select Buy/Sell still omit canonical side palettes |
| UIADV-ART-002 | OPEN — LOW, partly corrected | READINESS GAP | Lifecycle summaries | ui-screen-designer synthesis/finalization; checker maintainer | Dossier Section 0 corrected; wireframe checker G5 summary still obsolete |

Previously closed STATE-001/002/003, SAFE-001, ART-001, INT-001, DATA-001 and VER-001 retain their dispositions. No new finding ID is needed for the same conditional-readback defect surviving in a missed branch.

## 6. Detailed findings

### UIADV-INT-002 — Missing-SL variant still disagrees about the retained Limit level

- **Status / severity:** OPEN — MEDIUM; scope reduced to MP-MOCK-096 light/dark and dependent evidence. Original opposite-side ambiguity and all eleven renewed readbacks are corrected.
- **Type / area:** READINESS GAP; draft continuity, state truthfulness and implementation-review consistency.
- **Evidence:** UIR-INFO-007; IF-BR-008a; Section 14 revision 29, “Draft and validation identity” and invalid-input transition; UIV-INT-001; UI-IMPL-006 require the same proposed conditional level through pending/invalid validation. [MP-096 light](ui-artifacts/mockups/MP-MOCK-096.svg) and [dark](ui-artifacts/mockups/MP-MOCK-096-dark.svg) show ticket `Direction: Buy · Type: Limit`, `Entry level 1.08420` and `ERROR: required SL missing; estimate unavailable`; capsule shows the same R-014/EURUSD/completed 09:42 Buy draft but `Type: Limit · level Not set`. Both Buy/Sell have `aria-disabled="true"`. The actual render confirms both readbacks coexist. WF-096 uses proposed price placeholders rather than declaring absence. revision-r9.json excludes 096; its exact r8 bytes remain approved. check_mockups.py's new 22-SVG readback coverage likewise excludes it.
- **Finding:** A missing SL correctly invalidates sizing/submission, but the capsule incorrectly erases the retained entry-level meaning. Validation status and raw proposed values are separate facts under the approved UX contract.
- **Consequence:** An implementation copying this endpoint can make the same shared draft appear populated in the ticket and empty in the capsule when an unrelated required field is invalid. Recovery/context preservation and later conformance review become inconsistent across error variants. Disabled actions contain commitment risk, so no BLOCKING/HIGH severity or actual trade failure is inferred.
- **Minimum correction direction:** Reconcile proposed-level readback for 096 in both themes while preserving the missing-SL reason, invalid/superseded estimate, disabled submissions and editable retained inputs. Extend the conditional-readback evidence to this retained invalid branch; distinguish absent required entry level from absent SL. No formula or new UX policy is required.
- **Earliest owner:** `mockup-prototype-designer`, current consolidated `ui-screen-designer HIGH_FI_AND_VERIFICATION`.
- **Affected canonical sections:** Parts V–VI, MP/UI-ART-096, UID-004, UIV-INT-001 evidence and UI-IMPL-006 realization. Existing normative contract is sufficient.
- **Downstream stale if corrected:** MP-096 pair, actual dependent product SVG/PNG previews, gallery/index/digests, scoped revision/check/render evidence and independent review evidence. Trace actual output changes before widening scope; eleven corrected pairs and unrelated sources should retain bytes.
- **Human visual reapproval:** YES, scoped G5 for changed 096 content. G4 stays valid if WF bytes/semantics remain unchanged. Historical approval records stay immutable.

### UIADV-VIS-001 — Generic direction selectors still bypass the side palette

- **Status / severity / type:** OPEN — LOW; DESIGN DEFECT; carried forward from revision 4 and confirmed in inspected current artifacts.
- **Evidence:** VIS-STATE-016 includes sidebar direction selectors; VIS-COLOR-016/017 and UI-IMPL-014 require Buy #14532D on #DCFCE7, Sell #7F1D1D on #FEE2E2 in both themes. MP-025/068/093–096/107–109/111–113 retain neutral Select Buy/Sell controls with blue selection. MP-090 and capsule submission controls retain side roles. Current maintained palette check still omits Select labels.
- **Finding / consequence:** A repeated selector family contradicts explicit approved visual roles and can propagate conformance drift. Named sides/selection remain readable, so this is not a task blocker or observed usability failure.
- **Minimum correction / earliest owner:** Apply existing side roles and check this label family; `ui-screen-designer HIGH_FI_AND_VERIFICATION`. Do not change selector-versus-submission semantics.
- **Affected sections / downstream stale:** Twelve affected MP/UI-ART pairs, actual derivatives, indexes/hashes and check evidence. No WF/VIS redesign required.
- **Human visual reapproval:** YES, scoped G5 for changed content; G4 unaffected.

### UIADV-ART-002 — Wireframe check still reports obsolete G5 lifecycle

- **Status / severity / type:** OPEN — LOW, PARTIALLY CORRECTED; READINESS GAP.
- **Evidence:** Dossier revision-35 Section 0 current-authority precedence now correctly identifies all 113 current pairs, eleven renewed r9 pairs and 102 retained pairs. The fresh redirected check_wireframes.py report still says “Seven r7 entry pairs STALE_SOURCE and seven added frames PENDING STAGE 2D”. approval-r14/r9.json, indexes and actual files establish current G4/G5 identity and acceptance.
- **Finding / consequence:** The current checker summary can misroute downstream work to completed propagation or cast doubt on identifiable approvals. Exact records resolve the fact; no new visual-approval deficiency is inferred.
- **Minimum correction / earliest owner:** Reconcile the maintained derived G5 summary with actual lifecycle while preserving historical records; checker maintainer / current `ui-screen-designer` synthesis/finalization.
- **Affected sections / downstream stale:** Derived wireframe lifecycle report, viewer/package if its content changes. Section 0's original residual is resolved; no further correction there is requested.
- **Human visual reapproval:** NO for report/documentation-only changes without visual or semantic changes.

## 7. Review-dimension coverage

| Dimension | Result | Scope / limitation |
|---|---|---|
| Requirements/traceability | PASS for correction | Shared-draft preservation already explicit; no new requirement invented |
| Journeys/tasks | PARTIAL PASS / FINDING | Eleven renewed endpoints corrected; 096 error branch missed |
| Interaction/recovery/context | PARTIAL PASS / FINDING | Direction/commit/recovery contract explicit; retained-level inconsistency in 096 |
| Structure/information hierarchy | PASS for inspected scope | Existing ticket, capsule and editor preserve task organization |
| States/feedback/truthfulness | FINDING | Missing SL and absent entry level conflated only in 096 readback; both submissions blocked |
| Safety/irreversibility | PASS statically | No enabled invalid entry, added confirmation or changed destructive semantics |
| Adaptive/environment | PASS statically / EVIDENCE LIMITED dynamically | 068/110/111 retain corrected terms/editor; no actual reflow test |
| Accessibility/input | PASS as specification / EVIDENCE LIMITED dynamically | Named selection, disabled reasons, fresh commit and focus obligations; runtime unobserved |
| Visual system/hierarchy | FINDING retained | VIS-001 selector palettes |
| Data visualization | No new chart-data finding | Unchanged chart semantics; conditional terms covered by INT-002 |
| Visual artifact coherence | FINDING | Exact current approvals established; retained content and checker-summary residuals |
| Verification | PARTIAL PASS | Objective UIV obligations present; new readback checker omits retained invalid-risk branch |
| Complexity/proportionality | PASS | Existing shared draft/editor; no new views or confirmation requested |
| Implementation readiness | PASS in unaffected scope | Narrow invalid-risk realization still needs correction/reapproval/recheck |

This recheck does not reopen an exhaustive product audit for the 102 unchanged compositions or claim runtime acceptance.

## 8. Change and stress attacks

| Attack / driver | Legitimate changes | Expected stable areas | Actual outcome |
|---|---|---|---|
| Ready Buy ↔ Sell, opposite action attempted; IF-BR-008a | Explicit ticket selection, fresh validation, matching commit | No implicit command, unchanged run/boundary | Ready endpoints retain matching-only availability; runtime no-effect evidence remains required |
| Direction/fixed/risk edits; stale validation result | Pending/invalid status and superseded estimate | Raw proposed levels and existing orders | 108/109/111/113 now retain 1.08420; normative late-result rejection unchanged |
| Valid risk proposal → remove required SL; IF-JRN-007 / UIV-INT-001 | Block both, explain missing SL, invalidate estimate | Proposed Limit entry level and shared draft identity | 096 blocks correctly but capsule says Not set while ticket keeps 1.08420: INT-002 remains |
| Collapse ticket / effective desktop zoom; UIS-ADAPT-004 | Reflow/collapse and reachable editor | Direction, proposed terms, validity, run/boundary | 068/110/111 correct in both themes; no new mobile/breakpoint requirement inferred |
| Unknown matching submission; IDEM-001 / RETRY-002/003 | Freeze and reconcile original request | Original identity/terms; distinct modify/close | Contract/UIV remain explicit; unchanged 027/031/092 retain prior reviewed restrictions; runtime unobserved |
| Apply shared readback correction without unrelated drift | Correct actual conditional consumers and evidence | All WF, VIS and unrelated MP/approval history | Exactly eleven pairs changed; containment succeeds, but unchanged 096 demonstrates selection of changed files is not complete semantic coverage |

## 9. Correction routing

| Finding | Earliest current owner | Minimum revision | Downstream stale / reapproval |
|---|---|---|---|
| INT-002 residual | ui-screen-designer HIGH_FI_AND_VERIFICATION | Consistent retained entry level in missing-SL 096; cover retained invalid branch in evidence | 096 pair and actual derivatives/indexes/checks; scoped G5, then independent recheck; no new UX/G4 decision |
| VIS-001 | Same high-fi owner | Apply existing Buy/Sell palettes to Select family | Twelve MP pairs and actual derivatives; scoped G5; G4/VIS unchanged |
| ART-002 residual | Checker maintainer / ui-screen-designer synthesis | Current G5 report summary | Derived report/viewer/package; no visual reapproval |

UISYN-MOD-004 remains with system-architecture-designer before the Data location brief. DEFER-001–007 and ADV-VER-001 retain owners/triggers. No design correction was performed in this independent review.

## 10. Implementation-readiness conclusion

Unaffected scope may proceed through applicable implementation governance. **UIADV-INT-002 remains an affected-scope prerequisite, narrowed to the invalid-risk missing-SL readback in MP-096 both themes.** No BLOCKING/HIGH finding remains. The two LOW findings retain their independent scope.

All 113 WF / 226 MP SVGs are present, source-current, identifiable and explicitly G4/G5 approved. Eleven renewed conditional pairs now satisfy the reviewed readback correction. The remaining discrepancy can be corrected under the existing UX/UIV authority without inventing direction policy, formulas, confirmation or a new capability. Static checker success does not waive it. Applicable runtime verification and upstream prerequisites remain mandatory.

## 11. Final verdict

`READY WITH NON-BLOCKING UI CHANGES`
