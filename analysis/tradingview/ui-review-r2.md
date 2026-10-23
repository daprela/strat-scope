# UI Review

## 1. Review status

- **Target:** [ui-dossier.md](ui-dossier.md), revision 24, `READY_FOR_UI_ADVERSARIAL_REVIEW`.
- **Review:** revision 2, 21 October 2026; independent static design audit of the complete current scope and earlier corrections.
- **Verdict:** `REQUIRES UI REVISION`.
- **Open findings:** 0 BLOCKING, 1 HIGH, 3 MEDIUM, 0 LOW.
- **Evidence confidence:** SUFFICIENT for static findings and artifact integrity; runtime and browser-rendered HTML remain limited below.
- **Independence:** no dossier, visual-system rule, approved SVG, approval record or visual generator was corrected. Proposed staleness applies if corrections are accepted; this review does not silently revoke recorded G4/G5 approvals.
- **History:** [revision 1 and design-owner response](ui-review-r1.md) and its [original evidence manifest](ui-artifacts/review/history/evidence-manifest-r1.json) are preserved. The dispositions below supersede their current-status implications without erasing the original audit.

## 2. Evidence set

### Canonical target and upstream authority

The complete 1,472-line UI dossier was read, including Parts I–III, the frame/mockup/registry inventories, annotations, approval history, 34 verification properties, nine expected evidence classes and implementation handoff. The complete 303-line [visual-system.md](visual-system.md), revision 7, was read, including the later explicit user overrides.

Standalone `interface-requirements.md`, `interaction-model.md`, `interface-structure.md`, `ui-verification-model.md`, `wireframe-index.md` and `mockup-prototype-index.md` are absent. Their designated replacements are dossier Parts I–III, Sections 15/18–21 and the complete JSON indexes. This established organization is not a missing-authority finding.

Requirements were consulted for FR-03–05/10–25/27/38–55, DATA-16/18, CONS-02/12–16 and accepted U12–U14. Architecture was consulted for CONTRACT-001–012/018–020, INT-001, TX-001–006, CM-001–007, FAIL-003/009–021, CONC-002–008/012, original-intent/retry/ordering rules, AC-001–018, TF-009/010 and scoped DEFER prerequisites. These are UI-visible semantic checks, not a second full architecture audit. No unprovided domain policy or provider guarantee is inferred.

### Visual artifacts inspected

| Artifact | Identity / approval | Actual inspection |
|---|---|---|
| WF-FRAME-001–106 | Current WF-SET-001-r12: 90 unchanged r11 sources and 16 r12 revisions | All 106 canonical SVGs parsed, product text/control availability examined, independently rendered through Inkscape and visually inspected in 14 contact sheets; consequential variants inspected individually |
| Wireframe approval records | Historical r11 `approval.json`; current `approval-r12.json` | All 106 current hashes match current geometry acceptance. Explicit mockup approval accepts matching geometry; no separate wireframe approval quote invented |
| MP-MOCK-001–106, both themes | MP-SET-001-r6; 212 G5-approved canonical SVGs | All 212 parsed, independently rendered and visually inspected in 27 paired-theme contact sheets; detailed state/trading/quote variants inspected individually |
| Complete JSON indexes and G5 approval | `frame-index.json`, `mockup-index.json`, `mockups/approval.json` | All 212 approved mockup hashes, 106 approved/indexed source hashes and approved/indexed VIS hashes independently match current files |
| Product crops / PNG previews | Derived review aids, not additional approved screen identities | Export/render records inspected as provenance; fresh canonical renders used instead of assuming earlier previews are current |
| Offline galleries and replay comparison | Authored HTML review navigation | Source/local references checked; historical comparison content does not override exact current approval |
| MP-SPEC-001.html | Supplementary inert paired-theme state/focus/visibility/trade specimens | Complete HTML/CSS source inspected; rendered browser/focus evidence unavailable |
| Product prototype/scenarios | None supplied or required under Section 18 | No MP-PROT financial interaction, asynchronous transition or working keyboard workflow inferred from gallery navigation |

The [revision 2 evidence manifest](ui-artifacts/review/evidence-manifest.json) pins authorities, indexes, approvals, all 318 canonical SVGs and exact finding observations. Fresh renders/contact sheets are temporary inspection aids, not replacement designs. Approval provenance is the supplied records/dossier; original conversation approvals were not independently retrieved.

### Checks and evidence limitations

- `check_wireframes.py` passes: 106 frames, eight views, 64 original state identities, material branch checks and 422 local links. `check_mockups.py` passes: 212 current-source SVGs, geometry/control/palette/source checks, 1,701 local links and approved lifecycle. These results establish the stated artifact checks; they do not establish semantic correctness of every control.
- All 318 canonical SVGs rendered independently. Product content is distinguished from review-margin titles, illustrative financial fixtures and historical pending annotations. Such annotations do not revoke exact-hash G5 approval.
- Chrome DevTools could not connect to its browser endpoint. MP-SPEC-001 rendered appearance, actual Tab focus and HTML gallery behavior are **EVIDENCE LIMITED**. Source was inspected; no finding assumes unobserved HTML behavior.
- Static visuals do not establish actual command execution, focus restoration, scrolling, text-enlargement reflow, calculations, provider access, durability, performance or WCAG conformance. UIV-EVID-001–009 remain future implementation obligations. No observed user behavior or usability study is claimed.
- Original reference PNG pixels were not re-inspected for parity in this round. Reference registry/links provide provenance; no finding alleges a mismatch against target screenshots. Captured target HTML was neither executed nor embedded.
- Data location's architecture-owned preference/validation/publication/catalog-adoption contract is explicitly missing and already blocks that setting's implementation (UISYN-MOD-004, UI-IMPL-015). This disclosed scoped prerequisite is not a new UI defect. Existing DEFER-001–007 and ADV-VER-001 remain in force.

## 3. Executive assessment and claim map

The revisions materially improve readiness. Destructive reviews identify their actual operation, trading branches have concrete forms, and visibility is separate from calculation basis with a coherent dual-quote grammar. Exact approved bytes are current. Nevertheless, one recovery endpoint still invites progression while its original execution outcome is unknown. Three narrower defects remain in save styling, processing feedback and entry-direction binding. Broad UI integration should await the HIGH correction; the MEDIUM items need resolution before their affected surfaces are implemented.

| Area | Canonical claim / authority | Visual evidence | Verification / assessment |
|---|---|---|---|
| Goals/tasks | UIR-TASK-001–020; IF-JRN-001–015 | Eight views; trading 076/093–098; folder 099–102 | UIV-JRN-001–015; original branch absence resolved; INT-002 remains |
| Navigation/interaction | IF-NAV-001–013; IF-CONT-000 | Scoped drawer/window/capsule and return surfaces | UIV-INT-001–003; runtime restoration unproved |
| Structure/hierarchy | UIS-REG-001–026; UIS-PAT-006–013 | Persistent chart and reserved full-height side panels/task docks | UIV-STRUCT-001; no material new layout conflict established |
| States/recovery | UIR-STATE-001–014; UIS-PAT-001–003 | All 64 state identities plus variants | UIV-STATE-001–003; STATE-001/002/003 |
| Safety | IF-CONF-001–003; UIR-SAFE-001–005 | 049–056/071/078–080 | UIV-JRN-006/014; original destructive-scope defect resolved |
| Adaptation/accessibility | UIS-ADAPT; UIR-A11Y; IF-A11Y families | 065–074, numeric/anchor alternatives | UIV-ADAPT-001/A11Y-001–003; runtime evidence limited |
| Visual/data semantics | VIS rules; UIS-PAT-012; UIR-INFO-018 | Both themes; 075/103–106; side-labelled candles/OHLCV/volume | UIV-VIS/DATA/INT; STATE-002 residual |
| Artifact governance | Sections 17–19/21/23 | Current r12/r6; exact-hash approval records | All hashes match; semantic defects remain |
| Verification | Sections 20/21; 34 properties, nine evidence classes | Reproducible approved-state checks | Old VER-001 resolved; no runtime pass inferred |
| Implementation freedom | UI-IMPL-001–016; UI-FREEDOM-001–005 | Static references separate from production mechanisms | Tool/framework freedom preserved; missing entry semantics are not delegated tooling choices |

### Previous finding dispositions

These are independent static design dispositions, not implementation acceptance.

| Previous finding | Disposition | Evidence / remaining scope |
|---|---|---|
| UIADV-SAFE-001 | CLOSED | 078 names B-003, included work/input closure and replacement G-012; 079 names L-002/v12 and excluded unrelated scope; 080 distinguishes D-006→D-009 restart consequence |
| UIADV-STATE-001 | PARTIALLY RESOLVED; HIGH remains | Original 026/030/032/055 explicit mode/reason/outcome controls corrected; the shared state-availability class still fails in 077, detailed below |
| UIADV-ART-001 | CLOSED | 076 binds O-008/v2 and modification; 093–096 realize conditional/risk/invalid SL; 029/097/098 bind P-004/v3 with coherent rejected/partial/full quantities. New direction issue is INT-002 |
| UIADV-INT-001 | CLOSED | Revision 17 UX delta, Settings → Symbol basis, 075/103–106, UIV-INT-003 |
| UIADV-DATA-001 | CLOSED | VIS-DATA-009/010 and both-theme 104 show Bid-left filled / Ask-right hollow, separate OHLCV and paired volume; 103/105/106 show other modes/basis |
| UIADV-STATE-002 | PARTIALLY RESOLVED; MEDIUM remains | Working v13 / failed save v13 / retained v12 and retention-only retry corrected; high-fi unknown mark/token remain |
| UIADV-VER-001 | CLOSED | Both maintained checkers rerun successfully with approved lifecycle; exact current hashes independently confirmed; approval history unchanged |

## 4. Positive evidence

| Area | Evidence | Why it matters |
|---|---|---|
| Scope-bound destruction | WF/MP-078–080; IF-CONF-001–003 | Restore/delete/restart no longer inherit a rewind destination; validation and excluded scope are explicit |
| Replacement endpoints | WF/MP-053–055 | Unchanged, unknown and published have distinct actions; 055 names G-013/earlier cursor and uses Return rather than prepublication Cancel |
| Trade progression | WF/MP-026/030–032/091/092 | No-run has no capsule; block/unknown intent/read-only identify reasons; accepted waiting differs from evaluation |
| Concrete target operations | WF/MP-029/076/097/098 | Rejected 12,000 versus 10,000 is coherent; partial 4,000 leaves 6,000; full closure ends protection; modification names order/version |
| Quote identity | WF/MP-075/103–106; VIS-DATA-009/010 | Side identity survives without hue; basis differs from visible candles; both-hide retains values/axes/volume |
| Replay disclosure | WF/MP-048; UIV-ACC-001 | Connection inspection withholds later price/OHLC/derived evidence |
| Output uncertainty | WF/MP-061–063 | Incomplete, unknown-to-verify and verified-complete remain distinct and independent of pinned source |
| Adaptation/access | WF/MP-065–074 | Wrapped controls, reserved lower task space and point/anchor alternatives are concrete; runtime proof explicitly remains required |
| Governance restraint | Sections 18/21/23 | No unnecessary product prototype, framework or testing mechanism demanded; folder/provider/numerical prerequisites remain disclosed |

## 5. Findings summary

| ID | Severity | Type | Area | Earliest owner | Finding |
|---|---|---|---|---|---|
| UIADV-STATE-001 | HIGH | DESIGN DEFECT | Recovery / availability | wireframe-designer | Unknown original-event publication offers Start bar, Play and Step |
| UIADV-STATE-002 | MEDIUM | DESIGN DEFECT | Visual state meaning | mockup-prototype-designer | Known failed save retains unknown-publication mark/token |
| UIADV-STATE-003 | MEDIUM | DESIGN DEFECT | Processing feedback | wireframe-designer | Processing frame disables commands without pending phase/scope |
| UIADV-INT-002 | MEDIUM | READINESS GAP | Entry intent | interaction-flow-designer | Enabled Sell has undefined binding while a validated Buy draft is shown |

## 6. Detailed findings

### UIADV-STATE-001 — Unknown original-event publication offers progression

- **Severity / type / area:** HIGH / DESIGN DEFECT / state truthfulness and recovery. Residual of the earlier state-availability class, with a newly identified failing endpoint.
- **Evidence:** UIS-STATE-037 requires reconciliation before further mutation when outcome is unknown; UIS-PAT-003, WF-ANN-005, UID-005, UIV-JRN-010 and UIV-STATE-002. [WF-077](ui-artifacts/wireframes/WF-FRAME-077.svg), [MP-077 light](ui-artifacts/mockups/MP-MOCK-077.svg) and [dark](ui-artifacts/mockups/MP-MOCK-077-dark.svg) say `Publication outcome unknown` and offer `Reconcile publication`, yet have `aria-disabled="false"` for Start bar, Play and Step, with enabled glyph treatment. Architecture CONTRACT-007, TX-006, FAIL-013/015 govern the original occurrence.
- **Finding:** The unknown-resolution endpoint inherits known-resolved frame 037's progression availability. Sell/Buy are disabled, but commands that can change the run boundary remain enabled before the original whole effect/publication is established. `No automatic playback` does not reconcile the invitation to manual progression.
- **Consequence:** Following the approved availability permits a progression request against an unsettled original-event outcome; following the upstream guard makes enabled controls reject for a reason that should prevent activation. The visual and recovery authorities cannot both be realized as drawn. This is not evidence that an engine actually duplicates/skips an event.
- **Minimum correction direction:** Align 077's progression/start availability with its unreconciled state, retaining safe inspection/return and reconciliation. Distinguish known-resolved completion before enabling progression; inspect shared capsule consumers for the same error.
- **Earliest owner:** `wireframe-designer` / current `ui-screen-designer` LOW_FI_WIREFRAMES. Existing upstream semantics suffice; no architecture redesign requested.
- **Affected canonical sections:** 12 UIS-STATE-037; 16 WF-ANN-005; 18–20 UI-ART-077/UIV-JRN-010/STATE-002; 22 UID-005. Upper-level semantics need not change.
- **Stale downstream artifacts if corrected:** WF-077, both MP-077 themes, product/PNG derivatives and corresponding index/registry/hash/evidence entries. Other capsule consumers only if the shared correction changes them. Verification must cover the resolved/unknown distinction.
- **Human visual reapproval required:** YES, affected G4/G5.

### UIADV-STATE-002 — Known failed retention retains uncertainty styling

- **Severity / type / area:** MEDIUM / DESIGN DEFECT / visual semantics and durability feedback. Narrowed residual: earlier copy/recovery contradiction is resolved.
- **Evidence:** VIS-COLOR-013 is known-failure treatment; VIS-COLOR-014 assigns question mark/uncertain colors to unknown outcome; VIS-STATE-006 and UIV-STATE-002 distinguish them. [MP-015 light](ui-artifacts/mockups/MP-MOCK-015.svg) renders `? Draft applied to working state; save failed for this version` in `#6D28D9`; [dark](ui-artifacts/mockups/MP-MOCK-015-dark.svg) uses `#D8B4FE`. These are 007/077's unknown tokens. Its corrected footer says `Working v13 applied · Save FAILED v13 · Retained v12 · Retry retention (do not Apply again)`.
- **Finding:** Known-failure text/recovery are coherent, but prominent feedback still uses the canonical unknown symbol and semantic color. WF-015's corrected meaning is sufficient; this residual is high-fidelity realization.
- **Consequence:** Conflicting certainty cues weaken the difference between retrying known failed retention and first reconciling unknown publication. Reproducing the approved appearance violates the named state grammar. Explicit footer text limits impact, supporting MEDIUM rather than HIGH.
- **Minimum correction direction:** Use the existing known-failure mark/token while preserving applied working state, exact v13/v12 distinction and retention-only repair. Keep the unknown branch distinct.
- **Earliest owner:** `mockup-prototype-designer` / current `ui-screen-designer` HIGH_FI_AND_VERIFICATION. No visual-system redesign needed.
- **Affected canonical sections:** 18–21 UI-ART-015/evidence; UIV-VIS-001/STATE-002; UID-002.
- **Stale downstream artifacts if corrected:** Both MP-015 themes and product crops/previews/hash/index/registry evidence. No WF or unrelated visual becomes stale solely from this styling correction.
- **Human visual reapproval required:** YES, affected G5; no G4 reopening if source composition/meaning stays unchanged.

### UIADV-STATE-003 — Processing feedback exists only outside the product

- **Severity / type / area:** MEDIUM / DESIGN DEFECT / pending feedback and unavailable-action explanation.
- **Evidence:** UIS-STATE-027 requires visible pending estimate/request/evaluation and scope; UIR-FEED-001/002, VIS-STATE-002/003, WF-ANN-004, UIV-JRN-008 and UIV-STATE-001. [WF-027](ui-artifacts/wireframes/WF-FRAME-027.svg) and [MP-027](ui-artifacts/mockups/MP-MOCK-027.svg), both themes, disable Start bar/Play/Step/Sell/Buy. Product content is the ordinary order ticket/account placeholders/results table, without sizing/submitting/evaluation phase, pending occurrence or unavailable-action reason. Processing title and annotation are outside the product. Frame 092 has explicit evaluation feedback but does not retire 027 from the current registry.
- **Finding:** This canonical pending realization communicates unavailable commands without the required phase/reason at use. Binding placeholder financial values at runtime would not supply the missing processing explanation.
- **Consequence:** Pending submission/evaluation cannot be distinguished from invalid draft/general restriction in this realization. Implementation must add consequential feedback or choose a replacement endpoint without that decision being recorded. No actual execution bypass or observed user failure is asserted.
- **Minimum correction direction:** Give retained 027 named phase/scope and unavailable-action reason, or explicitly retire/remap it to a coherent endpoint and specify the remaining compound pending branches. Preserve prior terms and separate accepted/filled/save meaning.
- **Earliest owner:** `wireframe-designer` / current `ui-screen-designer` LOW_FI_WIREFRAMES; interaction/structure already requires the feedback.
- **Affected canonical sections:** 15–16 WF-027/WF-ANN-004; 18–20 UI-ART-027/UIV-STATE-001/JRN-008; 22 UID-004.
- **Stale downstream artifacts if corrected:** Revised WF-027, both MP-027 themes and derivatives/index/registry/evidence; or lifecycle/coverage mappings if retired. Other pending endpoints only if their content/mapping changes.
- **Human visual reapproval required:** YES for revised G4/G5 content; mapping-only retirement needs explicit canonical lifecycle review.

### UIADV-INT-002 — Opposite-side activation is not bound to the displayed draft

- **Severity / type / area:** MEDIUM / READINESS GAP / entry intent and review continuity.
- **Evidence:** UIR-INFO-007, UIR-SAFE-004, IF-JRN-007/008, IF-CONT-000 and UIS-ACT-010 require reviewable direction/levels/size/risk. UIS-PAT-010 and WF-DEC-005/013 assign final new-entry commitment to the replay bar. WF/MP-[093](ui-artifacts/mockups/MP-MOCK-093.svg)/[094](ui-artifacts/mockups/MP-MOCK-094.svg)/[095](ui-artifacts/mockups/MP-MOCK-095.svg), both themes, show `Direction: Buy`, conditional level, estimates and `Valid draft: use replay-bar Buy to submit`. Both Buy and Sell remain enabled; Buy is marked selected. Frame 068 has a Buy Limit summary with the same dual availability. No rule defines Sell's effect in this state.
- **Finding:** It is unspecified whether Sell changes the draft for review, submits opposite-side terms from those fields, or invokes an independent shortcut draft. Level/SL validity and risk sizing depend on direction, so a Buy validation/estimate cannot silently establish valid Sell terms.
- **Consequence:** Plausible implementations give different intent/commit sequences: an action could submit a direction different from the displayed reviewed terms, or turn an advertised final submission into selection. Architecture can reject invalid terms but cannot decide this missing interaction. No actual wrong-side fill is claimed.
- **Minimum correction direction:** Define opposite-side activation's relation to the draft, side-specific validation/estimate invalidation and final commitment; align readback/availability across detailed forms and capsule. Preserve the no-universal-extra-confirmation rule and separate entry/modify/close intents; no replacement layout prescribed.
- **Earliest owner:** `interaction-flow-designer` / current `ux-architecture-designer` DELTA. Architecture only if a proposed correction changes execution/eligibility policy.
- **Affected canonical sections:** IF-JRN-007/008, UIS-PAT-010, WF-DEC-005/013/019, entry realizations 025/068/090/093–096, UIV-JRN-007/008 and UID-004.
- **Stale downstream artifacts if corrected:** Accepted IF/UIS clarification and demonstrably dependent trading WF/MP/capsule variants, UI-ART/UID/UIV/preview/index entries. Trace actual shared consumers; unrelated recovery/quote/settings and financial rules remain stable.
- **Human visual reapproval required:** DEPENDS; YES for changed approved content, availability or action semantics.

## 7. Review-dimension coverage

| Dimension | Result | Notes |
|---|---|---|
| Requirements/traceability | PASS with scoped prerequisite | Twenty tasks mapped; folder architecture contract explicitly gates that setting |
| Journeys/tasks | FINDING | Concrete branches now present; opposite-side intent INT-002 remains |
| Interaction/recovery/context | FINDING | STATE-001 / INT-002; return/focus rules otherwise explicit; runtime limited |
| Structure/information/action hierarchy | PASS for static design | Chart-led shell, current side-panel bounds and scoped review/forms |
| States/feedback/truthfulness | FINDING | STATE-001/002/003; no blanket rejection of all state authority |
| Safety/irreversibility | FINDING in progression/entry scope | SAFE-001 closed; STATE-001/INT-002 affect bounded practice decisions, not invented real-cash trading |
| Adaptive/environment | PASS for structure; EVIDENCE LIMITED at runtime | Eight zoom realizations and two-chart identity; no mobile or fixed-breakpoint mandate inferred |
| Accessibility/input | PASS for specification; EVIDENCE LIMITED at runtime | Keyboard/anchor/numeric alternatives and non-color quote cues; conformance remains unproved |
| Visual system/hierarchy | FINDING | STATE-002 violates an existing mark/token rule, not aesthetic preference |
| Data visualization | PASS for static semantics | Dual-quote gap resolved; fixtures do not prove financial paths/formulas/volume units |
| Visual artifact coherence | FINDING | All approved bytes current; named endpoint content/availability/styling conflicts persist |
| Verification | PASS for specified obligations | Approved-lifecycle checks reproducible; semantic findings remain despite artifact passes; runtime proof still future |
| Complexity/proportionality | PASS | Shared shell/drawers/docks and no product prototype justified; no extra navigation/framework abstraction demanded |
| Implementation readiness | FINDING | HIGH STATE-001 prevents broad integration; MEDIUM corrections before affected-scope reliance |

## 8. Change and stress attacks

### A — Known resolution becomes unknown publication

- **Authority/driver:** Actual 037/077 split; UIS-STATE-037, TX-006, FAIL-013.
- **Legitimate changes:** Outcome certainty, allowed progression, reconciliation and affected visual/UIV evidence.
- **Stable areas:** Original occurrence/basis/coherent prefix, drawings, safe inspection/return.
- **Observed blast radius:** Explanation/action changes, but 077 inherits 037's enabled Start bar/Play/Step. Trade-entry exclusion does propagate.
- **Assessment / findings:** State-dependent availability fails; correct/reapprove the endpoint and actual shared dependencies without changing financial policy. STATE-001.

### B — Known failed save replaces unknown acknowledgement

- **Authority/driver:** 007 versus corrected 015; CM-003, VIS-STATE-006.
- **Legitimate changes:** Known-failure mark/token and retention-only recovery, exact working/retained versions.
- **Stable areas:** Already applied configuration, no repeat Apply, unrelated plot/entry semantics.
- **Observed blast radius:** Low-fi text/footer correction propagates; high-fi feedback keeps uncertain question mark/color.
- **Assessment / findings:** Semantic text propagation succeeds; state-role styling does not. Affected G5 correction only if source remains unchanged. STATE-002.

### C — Conditional Buy draft, then Sell

- **Authority/driver:** Supported conditional/risk entry; IF-JRN-007/008; 068/093–096.
- **Legitimate changes:** Declared direction, side-specific level/SL validation and affected estimate before commitment.
- **Stable areas:** Run/completed boundary, retained inputs, hedging, units, separation from modification/closure and chart visibility.
- **Observed blast radius:** Both commits enabled against Buy-labelled terms; opposite activation/validation sequence undocumented.
- **Assessment / findings:** Shared capsule distributes an undefined interaction. Resolve once, then trace affected visuals/UIV; unrelated quote/backup artifacts remain valid. INT-002.

### D — Pending request/evaluation in trading

- **Authority/driver:** UIS-STATE-027, WF-ANN-004.
- **Legitimate changes:** Named phase/scope and unavailable-action reason; old coherent terms/results identified.
- **Stable areas:** Basis/cursor, execution-versus-save meaning, chart-led structure.
- **Observed blast radius:** 027 disables capsule commands but retains generic entry content; 092 already demonstrates explicit evaluation copy.
- **Assessment / findings:** Geometry/currentness checks cannot expose a missing phase. Correct/retire that endpoint and preserve compound-branch verification. STATE-003.

### E — Ask only, both, neither, independent calculation basis

- **Authority/driver:** UIS-PAT-012; explicit user direction; VIS-DATA-009/010.
- **Legitimate changes:** Visibility/slots and side-qualified OHLCV/volume; separate basis Apply changes study inputs.
- **Stable areas:** UTC bucket identity, replay boundary, executable-side rules, axes/drawings and saved-run inputs.
- **Observed blast radius:** 103–106 retain named basis/non-color identity; neither-visible preserves context. Shared basis-label propagation is legitimate dependency scope.
- **Assessment / findings:** Static change contained; INT-001/DATA-001 close. Missing-side/async/high-density behavior still needs UIV evidence. NONE open for this attack.

### F — Desktop zoom and all-panel sizing

- **Authority/driver:** Accepted 1280×800 baseline, UIS-ADAPT family, latest UIS-PAT-013.
- **Legitimate changes:** Wrapped controls, collapsed secondaries, scrollable task detail and matching desktop panel bounds; zoom docks remain docks.
- **Stable areas:** Target/cursor, accessible primary operations, financial anchors, retained two-chart context.
- **Observed blast radius:** 065–072 reserve lower task space; 16 r12 revisions distinguished from 90 unchanged approvals; paired themes match sources; 073 names both chart identities.
- **Assessment / findings:** Static structure/approval scope contained. Enlarged-text scrolling, full keyboard completion and task reachability remain UIV-EVID-006/007. INT-002 applies to 068; no independent adaptive finding established.

### G — Change destructive operation and finalize approval

- **Authority/driver:** IF-CONF-001–003; actual r12/r6 approval; previous lifecycle-check failure.
- **Legitimate changes:** Scope/candidate/consequence/verb and approval evidence.
- **Stable areas:** Scope/version binding, cancel-before-publication, source/VIS identity and check reproducibility after approval.
- **Observed blast radius:** Restore/delete/restart now use distinct scope tuples; approved-state checkers run; all current hashes match; historical records remain distinct.
- **Assessment / findings:** SAFE-001/VER-001 close. Section 23 can expose future stale descendants without blanket invalidation. Successful checks do not cancel semantic findings. NONE open for this attack.

## 9. Correction routing

| Finding | Earliest owner / current route | Required revision | Downstream stale if accepted | Reapproval |
|---|---|---|---|---|
| STATE-001 | wireframe-designer / ui-screen-designer LOW_FI | 077 state-specific capsule availability | WF-077, paired MP-077, derivatives/registry/hash/UIV evidence; other consumers only if changed | Affected G4/G5 |
| STATE-002 | mockup-prototype-designer / ui-screen-designer HIGH_FI | Known-failure mark/token | Paired MP-015 and derivatives/registry/hash evidence; no automatic WF change | Affected G5 |
| STATE-003 | wireframe-designer / ui-screen-designer LOW_FI | 027 pending feedback or explicit retirement/remapping | Revised WF/MP-027 and dependencies, or lifecycle/coverage authority | Affected G4/G5 if visuals change |
| INT-002 | interaction-flow-designer / ux-architecture-designer DELTA | Draft direction/opposite activation/validation/commit contract | Dependent IF/UIS and entry WF/MP/UIV/UID mappings including 068/093–096; trace shared consumers | Depends; changed semantics/visuals require affected gates |

IDs abbreviate Section 5. Route to the earliest stage that must change, not automatically to higher authority. Existing architecture defines original-event ordering and valid side-specific terms; no replacement architecture/interface is authored here. UISYN-MOD-004 separately routes the disclosed folder contract to `system-architecture-designer` / `architecture-workflow` before that setting's brief. Apply Section 23 staleness rules to actual UI-ART dependencies and renewed approval. This audit does not edit their lifecycle records.

## 10. Implementation-readiness conclusion

Broad UI implementation integration should wait for **UIADV-STATE-001** to be corrected and dependent visual authority reapproved. Otherwise implementation must choose between the governing unknown-publication restriction and approved enabled progression. Resolve the three MEDIUM findings before their affected state/entry surfaces rely on the design. Independently governed unaffected work may proceed through standards/brief gates with explicit exclusions; this audit itself neither authorizes implementation nor waives G6/G7.

The complete visual inventory is available, identifiable, approved and byte-current. The issue is semantic consistency of named endpoints, not missing G5 approval. Later briefs/reviews have useful objective UIV constraints but cannot reproduce those affected realizations coherently without the corrections. Data location remains additionally gated by its disclosed architecture contract. DEFER-001–007 and ADV-VER-001 remain scoped prerequisites. No provider, calculation, performance, durability or accessibility pass is claimed.

## 11. Final verdict

`REQUIRES UI REVISION`
