# UI Review

## 1. Review status

- **Target:** [ui-dossier.md](ui-dossier.md), revision 28, `READY_FOR_UI_ADVERSARIAL_REVIEW`.
- **Review:** revision 3, 21 October 2026; independent review of the complete approved static design and revision 2 corrections.
- **Verdict:** `READY WITH NON-BLOCKING UI CHANGES`.
- **Open findings:** 0 BLOCKING, 0 HIGH, 1 MEDIUM, 0 LOW.
- **Evidence confidence:** SUFFICIENT for static design, correction closure and artifact identity; runtime/browser limitations below.
- **Implementation scope:** unaffected scope can enter implementation governance. Resolve UIADV-INT-002 before dependent entry work. The disclosed folder contract, DEFER prerequisites and downstream gates remain applicable.
- **Independence:** no dossier, visual-system rule, approved visual, approval record or visual generator was changed. Correction directions select no replacement interaction and do not silently revoke approvals.
- **History:** [revision 2](ui-review-r2.md), [its manifest](ui-artifacts/review/history/evidence-manifest-r2.json), [revision 1](ui-review-r1.md) and its archived manifest are preserved. This review supersedes their current finding dispositions, not their historical evidence.

## 2. Evidence set

### Canonical target and upstream authority reviewed

The complete 1,496-line UI dossier was read, including Parts I–VI, current/historical approval records, inventories, compound-state annotations, 34 verification properties, nine evidence classes, prerequisites and implementation freedoms. The complete 303-line [visual-system.md](visual-system.md), revision 7, was read, including explicit later user overrides.

Standalone `interface-requirements.md`, `interaction-model.md`, `interface-structure.md`, `ui-verification-model.md`, `wireframe-index.md` and `mockup-prototype-index.md` are absent. Their designated replacements are dossier Parts I–III, Sections 15/18–21 and the complete JSON indexes. This organization is not a missing-authority defect.

[Requirements](requirements-dossier.md) were consulted for FR-03–05/10–25/27/38–55, DATA-16 and CONS-12–16. [Architecture](architecture-dossier.md) was consulted for CONTRACT-001–011/018–020, TX-001–006, CM-001–007, FAIL-012/013/015, CONC-002–004/006/008, RETRY-002–004, historical-command pseudocode and DEFER-001–007. These are UI-visible semantic checks, not a fresh full architecture/domain audit. The domain-model hash records upstream identity only.

### Visual artifacts inspected

| Artifact | Version / approval | Actual inspection |
|---|---|---|
| WF-FRAME-001–106 | WF-SET-001-r13; exact G4 hashes in `approval-r13.json` | All 106 SVGs parsed, product text/control availability extracted, independently rendered with Inkscape and visually inspected in 14 contact sheets |
| MP-MOCK-001–106, light and dark | MP-SET-001-r7; exact G5 hashes in `approval-r7.json` | All 212 SVGs parsed/rendered and visually inspected in 27 contact sheets; 015/027/077 in both themes and consequential entry/quote variants also inspected individually |
| Current indexes/revision records | Wireframe r13, mockup r7; per-artifact versions explicit | Complete indexes parsed; current approvals, source links, VIS digest and retained/changed identities checked |
| Historical approval/correction evidence | r11/r12 G4, r6 G5, revision 2 review/manifest | Recorded identities compared; archived changed r6 mockups remain historical |
| Product SVG crops/PNG previews | Derived aids, not additional approved screen identities | Export records/local references checked; fresh canonical renders used instead of assuming preview freshness |
| Offline galleries, replay comparison, MP-SPEC-001.html | Authored review navigation / inert state specimens | Source inspected and local-link checks rerun; actual browser appearance/focus unavailable |
| Product prototype / MP-PROT scenarios | None supplied or required by Section 18 | No trading, async transition or product keyboard flow inferred from gallery navigation |

The [revision 3 evidence manifest](ui-artifacts/review/evidence-manifest.json) pins authorities, indexes, approval records, all 318 canonical SVGs, independent checks, render coverage and observations. Fresh inspection PNGs/contact sheets are temporary aids under `/tmp/ui-adversary-r3/`, not new design authority. Source provenance is 89 r11, 15 r12 and two r13 wireframes; mockups have three revised r7 pairs and 103 unchanged r6 pairs, all included in current approval. Approval provenance is the supplied records/dossier; original conversation approvals were not independently retrieved.

### Checks and evidence limitations

- Independent SHA-256 checks match all 106 current G4 wireframes, all 212 current G5 mockups, all G5 source hashes and the approved VIS hash. No missing or stale current canonical pair was found.
- `check_wireframes.py` passes: 106 frames, eight views, 64 original state identities, material branches and 435 local links. `check_mockups.py` passes: 212 current-source SVGs, geometry/control/palette checks, approved lifecycle and 1,731 local links. Artifact checks do not prove every interaction complete.
- All 318 canonical SVGs rendered successfully. Product content is distinguished from review margins, synthetic fixtures and historical creation-round pending annotations. Exact-hash approval records govern lifecycle.
- Chrome DevTools could not connect to `127.0.0.1:9222`. HTML gallery/specimen rendering and actual Tab/focus behavior are **EVIDENCE LIMITED**; source inspection is not equivalent rendered evidence.
- Static visuals do not prove keyboard completion, focus restoration, dynamic enlargement/scrolling, async transitions, calculations, provider access, durability, performance or WCAG conformance. UIV-EVID-001–009 remain expected implementation evidence. No user-research or observed usability result is claimed.
- Original reference screenshot pixels were not re-inspected for parity in this round. Registry/links were consulted; no finding alleges screenshot-parity mismatch. Captured target HTML was neither executed nor embedded.
- Data location explicitly requires an architecture-owned ownership/validation/publication/catalog-adoption contract (UISYN-MOD-004, UI-IMPL-015). This disclosed scoped prerequisite is retained, not presented as a new UI defect. DEFER-001–007 and ADV-VER-001 remain in force.

## 3. Executive assessment and claim map

The approved r13/r7 corrections resolve all three state findings from revision 2. Unknown original-event publication blocks progression while preserving reconciliation/inspection; pending submission names its phase and original intent inside the product; known failed retention uses the existing failure grammar and preserves exact working/retained versions. The complete approved visual set is identifiable and current.

One MEDIUM interaction gap remains: opposite-side activation is not bound to the direction-specific draft being reviewed. It is explicitly isolated from affected implementation in the current handoff. Unaffected UI scope can proceed through standards/brief gates; entry behavior must first return to the UX owner. Approval of pictures does not supply that interaction decision.

| Area | Canonical claim / authority | Visual evidence | Verification / assessment |
|---|---|---|---|
| Goals/tasks | UIR-TASK-001–020; IF-JRN-001–015 | Eight views; concrete 076/093–102 branches | UIV-JRN-001–015; INT-002 scoped |
| Journeys/navigation/context | IF-NAV-001–013; IF-CONT-000; IF-REC | Drawers, settings, inline review, return paths | UIV-INT-001–003 / CONT-001; runtime restoration unproved |
| Structure/hierarchy | UIS-REG-001–026; UIS-PAT-006–013 | Persistent chart, distinct rail, bounded panels/task docks | UIV-STRUCT-001; static hierarchy coherent |
| States/recovery | UIR-STATE; UIS-STATE-001–064; WF-ANN | Revised 015/027/077 versus 007/037/092 | UIV-STATE-001–003; three state findings close |
| Safety/authority | UIR-SAFE; IF-CONF; CONTRACT-005/008/009/019 | 029/049–056/076/078–080/097/098 | UIV-JRN-006/009/014 / ACC-001 |
| Adaptation/accessibility | Accepted G2; UIS-ADAPT; IF-A11Y | 065–072, two-chart 073, point editor 074 | UIV-ADAPT/A11Y; dynamic evidence limited |
| Visual/data semantics | VIS-STATE/DATA; UIS-PAT-012 | Both themes; separate visibility/basis; dual OHLCV/volume | UIV-VIS/DATA/INT; static consistency supported |
| Artifacts/approval | Sections 17–19/21/23 | Current r13/r7 exact hashes and lineage | All 318 match; no current-source drift |
| Verification | Sections 20/21 | 34 properties, nine evidence classes | Behavior-oriented obligations; no runtime pass |
| Implementation freedom/complexity | UI-IMPL-001–016; UI-FREEDOM-001–005 | Shared shell/task families, no required product prototype | Tooling freedom separate from entry semantics |

### Previous finding dispositions

These are independent static-design dispositions, not implementation acceptance.

| Finding | Current disposition | Independent evidence |
|---|---|---|
| UIADV-STATE-001 | CLOSED | WF/MP-077 disable Start bar, Play, Step, Sell and Buy; visible reason names reconciliation. Evidence inspection, Reconcile publication and Return paused remain. Known-resolved 037 permits manual progression. WF-ANN-005, UID-005, UIV-JRN-010/STATE-002 agree |
| UIADV-STATE-002 | CLOSED | Both MP-015 themes use × and VIS-COLOR-013; working v13 / failed save v13 / retained v12 and retention-only repair preserved. Unknown 007/077 retain ? and VIS-COLOR-014. No WF revision required |
| UIADV-STATE-003 | CLOSED | WF/MP-027 show submission I-009, R-014, decision 09:42, submitted terms, retained records, no advance/new entry and acceptance/fill unconfirmed separately from save. 092 remains evaluation; WF-ANN-004 distinguishes estimate-only pending |
| UIADV-INT-002 | OPEN — MEDIUM | Opposite-side binding gap reproduced in unchanged 068/093–095 and acknowledged by Sections 0/17/18/23/25; no upstream interaction correction supplied |
| UIADV-SAFE-001 / ART-001 / INT-001 / DATA-001 / VER-001 | Remain CLOSED | Operation-specific destructive reviews, concrete trading branches, separate calculation basis, dual-quote grammar and reproducible approved-lifecycle checks retained; revision 2 records original closures |

## 4. Positive evidence

| Area | Evidence | Why it matters |
|---|---|---|
| Unsettled original outcome | 031/077 versus 037; UIV-JRN-010 / STATE-002 | Unknown no longer invites progression; original event and safe reconciliation survive |
| Submission versus evaluation | 027 versus 092; WF-ANN-004 | Product feedback names phase/identity without implying execution or saving |
| Retention certainty | 015 versus 007/077; VIS-STATE-006 | Known failure and uncertainty now differ in text, marks, colors and recovery |
| Scoped destruction | 049–056/078–080; IF-CONF | Restore/delete/restart name actual scope; stale/preparing/unchanged/unknown/published remain distinct |
| Target operations | 029/076/097/098 | Order/version and position/remainder explicit; over-close preserves exposure; partial/full close remain targeted |
| Quote interpretation | 075/103–106; VIS-DATA-009/010 | Visibility/basis independent; UTC slots, OHLCV and volume preserve side identity without hue alone |
| Replay disclosure/output | 048/060–063 | Later price facts withheld; output pinned; unknown artifact requires verification |
| Adaptive continuity | 065–074; UIS-ADAPT | Concrete task docks and numeric/anchor alternatives; runtime proof explicitly remains required |
| Scoped governance | r13/r7 revisions and approvals | Two WF files and three MP pairs changed; unrelated approved bytes retained |

## 5. Findings summary

| ID | Severity | Type | Area | Earliest owner | Short finding |
|---|---|---|---|---|---|
| UIADV-INT-002 | MEDIUM | READINESS GAP | Entry intent / validation / commitment | interaction-flow-designer; current route ux-architecture-designer DELTA | Enabled Sell has undefined binding while a validated Buy draft is shown |

## 6. Detailed findings

### UIADV-INT-002 — Opposite-side activation is not bound to the displayed draft

- **Severity:** MEDIUM, retained from revision 2. This is a contained interaction gap in hypothetical trading, explicitly excluded from affected implementation until resolved. It does not undermine corrected recovery or require unrelated work to stop; no actual wrong-side execution is evidenced.
- **Type:** READINESS GAP, not an observed usability result.
- **Area:** Interaction, review continuity and side-dependent estimate validity.
- **Evidence:** UIR-INFO-007, UIR-SAFE-004, IF-CONT-000, IF-JRN-007/008 and UIS-ACT-010 require reviewable direction/terms/risk and a current valid decision. UIS-PAT-010 and WF-DEC-005/013/019 place final new-entry commitment on the replay strip. [WF-093](ui-artifacts/wireframes/WF-FRAME-093.svg), [MP-093 light](ui-artifacts/mockups/MP-MOCK-093.svg) / [dark](ui-artifacts/mockups/MP-MOCK-093-dark.svg), and 094/095 in both themes show `Direction: Buy`, direction-dependent entry/SL/estimate fields and `Valid draft: use replay-bar Buy to submit`; both Buy and Sell have `aria-disabled="false"`. Buy has the selected marker. 068 retains the Buy Limit summary and dual availability. 096 disables both for invalid risk, but does not define the valid opposite-side transition. Sections 0/17/18/23/25 explicitly retain the unresolved decision.
- **Finding:** It is unspecified whether Sell changes the draft for review, submits opposite-side terms from that draft, or uses a separate shortcut intent. Buy-specific level/SL validation and estimated risk cannot silently establish valid Sell terms. Architecture accepts explicit semantic commands; it cannot select this missing UI sequence.
- **Consequence:** Dependent entry implementations could disagree about direction, validation/estimate invalidation and commit timing. An activation could commit a different direction from the reviewed terms, or act as selection despite its documented submission role. The approved picture does not resolve that choice.
- **Minimum correction direction:** Specify opposite-side activation's relationship to draft, side-specific validity/estimate invalidation, reviewable readback and final commitment. Bind capsule and detailed ticket to that contract and add the observable UIV obligation. Preserve distinct entry/modify/close and the no-universal-extra-confirmation rule. No policy/layout is selected by this review.
- **Earliest owner:** `interaction-flow-designer`; current consolidated route `ux-architecture-designer` DELTA. Use `architecture-workflow` only if the chosen correction changes execution/eligibility policy.
- **Affected canonical sections:** IF-JRN-007/008, IF-CONT-007/008, UIS-PAT-010, UIS-ACT-010, WF-DEC-005/013/019, UID-004, UIV-JRN-007/008 and Section 23 entry handoff.
- **Stale downstream artifacts if corrected:** Actual dependent entry WF/MP/UI-ART compositions, beginning 025/068/090/093–096; trace shared capsule consumers before widening scope. Changed content/availability invalidates corresponding crops/previews, indexes, hashes and UIV evidence. Unrelated event recovery, retention, quote, folder and backup designs do not become stale merely because this finding exists.
- **Human visual reapproval required:** DEPENDS on correction; YES for changed approved content, availability, selection or commitment semantics. Record changed authority and affected G4/G5 scope before implementation relies on it.

## 7. Review-dimension coverage

| Dimension | Result | Notes |
|---|---|---|
| Requirements/traceability | PASS | Twenty tasks/fifteen journeys; folder architecture contract remains scoped upstream work |
| Journeys/tasks | FINDING | INT-002; no new missing primary journey established |
| Interaction/recovery/context | FINDING | Entry binding unresolved; event/save corrections close; runtime focus limited |
| Structure/hierarchy | PASS for static design | Chart-led shell, bounded panels, separate target operations |
| States/feedback/truthfulness | PASS for static design | STATE-001/002/003 close; compound branches still need implementation evidence |
| Safety/irreversibility/permissions | PASS with scoped entry exception | Destructive scopes/writer restrictions present; INT-002 prerequisite for entry |
| Adaptive/environment | PASS statically; EVIDENCE LIMITED dynamically | Eight zoom variants/two-chart context; no mobile or fixed-breakpoint mandate inferred |
| Accessibility/input | PASS as specification; EVIDENCE LIMITED dynamically | Named keyboard/numeric/anchor paths and non-color semantics; no conformance claim |
| Visual system/hierarchy | PASS for inspected SVGs | Corrected certainty cues; paired-theme user overrides retained |
| Data visualization | PASS statically | Side/basis/UTC/provenance coherent; fixtures prove no numerical/high-density runtime behavior |
| Visual artifact coherence | PASS | All 318 current approved SVGs inspected; no source drift; historical margins do not change approval |
| Verification | PASS with correction dependency | Behavior-oriented high-risk obligations; selected INT-002 sequence must update acceptance property |
| Complexity/proportionality | PASS | Shared task families justified; no extra panels/prototype/framework demanded |
| Implementation readiness | PASS in unaffected scope | Resolve INT-002 before dependent entry work; preserve folder/DEFER/governance gates |

## 8. Change and stress attacks

### A — Known resolution becomes unknown publication

- **Authority/driver:** Actual 037/077 split; UIS-STATE-037, WF-ANN-005, CONTRACT-007/TX-006.
- **Expected legitimate changes:** Outcome wording, allowed progression, reconciliation and affected approval/UIV evidence.
- **Expected stable areas:** Original occurrence/basis/prefix, safe inspection/paused return; no automatic play.
- **Observed blast radius:** 077 disables Start/Play/Step/Sell/Buy with an adjacent reason; 037 retains manual progression. Source and both themes match renewed exact approvals.
- **Assessment / findings:** Contained and coherent; STATE-001 closes. Unrelated entry/quote/settings need no revision.

### B — Known failed retention replaces unknown acknowledgement

- **Authority/driver:** 015 versus 007/077; CM-003, FAIL-012/013, VIS-COLOR-013/014.
- **Expected legitimate changes:** Failure mark/token and retention-only recovery, exact working/saved versions.
- **Expected stable areas:** Applied settings/prior checkpoint; no repeated Apply/trade effect.
- **Observed blast radius:** Both MP-015 themes corrected; unchanged WF-015 remains sufficient. Error × and v13/v12 differ from uncertain ? and reconciliation.
- **Assessment / findings:** Scoped propagation/reapproval succeeds; STATE-002 closes.

### C — Estimate, submission and evaluation pending

- **Authority/driver:** UIS-STATE-027, UIR-FEED-001/002, WF-ANN-004, UIV-JRN-008.
- **Expected legitimate changes:** Actual phase/draft/request/event identity, terms and unavailable-action reason.
- **Expected stable areas:** Last coherent records, basis/boundary and acceptance/fill/save distinctions.
- **Observed blast radius:** 027 names original submission I-009 and blocks entry/advance; 092 retains evaluation; annotation separates estimate-only pending without inventing a submitted request.
- **Assessment / findings:** Static correction coherent; STATE-003 closes. Dynamic compound-branch walkthrough remains required, not passed here.

### D — Valid conditional Buy draft, then Sell

- **Authority/driver:** Supported conditional/risk entry; IF-JRN-007/008; 068/093–096.
- **Expected legitimate changes:** Direction, side-specific level/SL validity and estimate/readback before commitment.
- **Expected stable areas:** Run/completed boundary, retained inputs, USD/units, hedge policy, separate modify/close.
- **Observed blast radius:** Both commitments enabled against Buy-labelled terms; opposite-side transition remains undocumented.
- **Assessment / findings:** INT-002 remains. Resolve once upstream, trace actual descendants; independent quote/recovery/backup remain stable.

### E — Ask only, both, neither and independent calculation basis

- **Authority/driver:** UIS-PAT-012, explicit user direction, VIS-DATA-009/010.
- **Expected legitimate changes:** Visible series/slots and side-labelled readbacks/volume; separate Apply changes basis.
- **Expected stable areas:** UTC bucket, cursor, axes/drawings, study identity, execution-side policy, retained inputs.
- **Observed blast radius:** 103–106 preserve named basis independent of visibility. Both uses filled-left Bid/hollow-right Ask with separate OHLCV/volume; neither retains axes/numeric context.
- **Assessment / findings:** No new static defect. Missing-side/async/high-density runtime evidence remains UIV work; no display threshold invented.

### F — Desktop effective zoom and return

- **Authority/driver:** Accepted 1280×800 baseline; UIS-ADAPT, UIS-PAT-013; 065–074.
- **Expected legitimate changes:** Wrapping/collapsing, reserved scrollable task docks and reachable actions; explicit active chart.
- **Expected stable areas:** Chart/run/target, anchors, terms/consequence/reason and return origin; no auto-play.
- **Observed blast radius:** Eight variants preserve chart above task space; settings remains an allowed overlay; desktop panels share bounds. 073 retains chart identities; 074 exposes numeric points/anchors.
- **Assessment / findings:** Static containment supported; actual enlargement, keyboard completion and focus restoration EVIDENCE LIMITED. INT-002 applies to 068; no independent adaptive finding.

### G — Scoped correction/finalization preserves unrelated approval

- **Authority/driver:** Actual r13/r7 revisions; Section 23 staleness model.
- **Expected legitimate changes:** WF-027/077; MP-015/027/077; dependent derivatives, mappings/UIV and renewed approvals.
- **Expected stable areas:** Other 104 wireframes/103 mockup pairs, VIS rules and historical approvals.
- **Observed blast radius:** Independent comparison against revision 2 confirms exactly those canonical changes; current sources/VIS match approval and retained pairs remain identical. Both checkers accept finalized lifecycle.
- **Assessment / findings:** Scope/provenance contained. Future INT-002 changes must name actual stale descendants; no blanket visual invalidation.

## 9. Correction routing

| Finding / prerequisite | Earliest owner | Required revision | Downstream stale | Reapproval |
|---|---|---|---|---|
| UIADV-INT-002 | interaction-flow-designer / ux-architecture-designer DELTA | Direction/draft/validation/readback/commit contract; IF/UIS and UIV/UID handoff | Actual entry WF/MP/UI-ART descendants and derivatives, starting 025/068/090/093–096; trace capsule consumers | Affected G4/G5 if approved semantics/content/availability change |
| Existing UISYN-MOD-004, not new finding | architecture-workflow / system-architecture-designer | Folder ownership/validation/publication/catalog-adoption contract before setting's brief | 099–102 and UIV-JRN-015 only if new authority changes documented semantics | Depends on resulting UI change |

STATE-001/002/003 require no further design correction on this evidence. Closure does not waive implementation verification. DEFER-001–007 and ADV-VER-001 retain existing owners/triggers. This review edits no upstream authority or visual lifecycle record.

## 10. Implementation-readiness conclusion

Unaffected UI scope may enter implementation governance with **UIADV-INT-002 explicitly excluded from dependent entry work**. No BLOCKING or HIGH finding remains. The MEDIUM gap requires an upstream UX decision before its affected brief, dependent visual revision and implementation; a coding agent must not choose it as local freedom. This scoped readiness neither approves unresolved entry semantics nor waives G6/G7.

The complete static visual authority is available, current and G4/G5 approved. Later briefs/reviews can consume unaffected scope's objective UIR/IF/UIS/VIS/UID/UIV constraints. The three corrected states no longer require choosing between inconsistent approved endpoints. Runtime conformance, financial/provider evidence, persistence proof, folder contract and applicable existing prerequisites remain downstream obligations.

## 11. Final verdict

`READY WITH NON-BLOCKING UI CHANGES`
