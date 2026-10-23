# Architecture Review

**Review date:** 19 October 2026  
**Review revision:** 1  
**Method:** Independent architecture-adversary review; documentation and logical failure/change attacks. No application tests or provider connection performed.

## 1. Review verdict

**Verdict:** `READY WITH NON-BLOCKING CHANGES`

| Severity | Count |
|---|---:|
| BLOCKING | 0 |
| HIGH | 0 |
| MEDIUM | 1 |
| LOW | 0 |

The architecture supplies coherent authority, historical-information, execution, retention and security constraints. No contradiction requiring a new high-consequence product decision was established. One material verification omission remains: simultaneous publication by different workflows is not explicitly tested for preservation of unrelated durable state. Existing publication/version guarantees support a correction without changing the approved boundaries. Readiness remains subject to DEFER-001–DEFER-007 and downstream standards/UI/implementation gates; this verdict neither discharges them nor certifies provider or platform feasibility.

## 2. Review scope and evidence

### Primary target

[architecture-dossier.md](architecture-dossier.md), revision 2, all 35 sections read. Its stated status is `IMPLEMENTATION_READY_WITH_NON_BLOCKING_GAPS`. G1 approval is recorded for revision 1 Parts I–II; new Pass 2 mechanisms are explicitly proposed architectural decisions. This review does not expand that approval.

### Supporting upstream artifacts

| Artifact | Available? | Stated status | Review use |
|---|---|---|---|
| [requirements-dossier.md](requirements-dossier.md) | Yes, read completely | Revision 14; `CONVERGED_WITH_ACCEPTED_ASSUMPTIONS` | Scope, accepted P1/P2/P3, authority, required behavior and evolution drivers |
| [domain-model.md](domain-model.md) | Yes, read completely | Revision 1; `READY_WITH_ACCEPTED_ASSUMPTIONS` | DC/REL/TR/INV/PRE/HIST/OP/POL semantics and DM-GAP obligations |
| `architecture-boundaries.md` | Absent | No separate artifact | Target Parts I–II contain the boundaries/contracts; no independent boundary artifact comparison possible |
| `resilience-model.md` | Absent | No separate artifact | Target Part III contains the resilience/security model |
| `verification-model.md` | Absent | No separate artifact | Target Part IV contains planned verification/diagnosis |

### Evidence limitations and target identity

Requirements/user approvals are evidenced by the supplied dossiers' provenance records, not an independently recovered interview transcript or revision-1 boundary snapshot. No upstream contradiction is inferred from an absent artifact. Source reports and captures are subordinate provenance; target HTML was not executed or embedded for this review. External API documentation referenced by the requirements was not revalidated: this review makes no new claim about actual provider capabilities. There is no implemented product to inspect or test.

SHA-256 identifies the reviewed source bytes:

```text
architecture-dossier.md  ddaea9cb64b0edeb1a2a3498d4de98cf6c1c7df6b673b69fd1b6cc1446752623
requirements-dossier.md  841570bd3457cc25a991d6b6c0fe3866b9356e9977b8a0bf490e6739d4b9f3e9
domain-model.md          8677c88b019523fa78ca029ab9d50fd8c4710fca8def4a6d28e434b6a7670554
```

The target and upstream documents were preserved unchanged. Recommendations below are not accepted architecture revisions.

## 3. Executive assessment

The strongest protection is the separation of changing current history from retained run evidence, backed by preservation of original values rather than mutable paths. Whole simulated effects, version/epoch checks, and reconciliation of uncertain publication address actual failure modes. The thirteen boundaries are logical responsibilities, with explicit exclusions and no requirement for thirteen services. A tenant platform, distributed financial transaction and permanent discarded-trade journal would add burden without a supplied driver; their absence is justified.

The remaining finding concerns proof of interactions among otherwise well-specified workflows. Separate save-regression and catalog-overlap tests could pass while an implementation still publishes an old snapshot over a newer unrelated component. Track ADV-VER-001 during verification refinement. Unaffected preparation can proceed under existing gates; live access, exact monetary conventions and platform durability remain unproven prerequisites.

### Compact architecture claim map

| Claim / driver | Owner and guarantee | Failure consequence attacked | Planned evidence / assessment |
|---|---|---|---|
| Full archive; FR-06/FR-52 | BND-002/BND-004: discovered bounds independent of resident range | False end-of-history or fixed start date | VG-001/VG-010, AC-016, TF-001/TF-010; supported |
| Nonfuture replay; FR-20/FR-53, INV-03 | BND-004 availability; BND-007 effective/processed boundary | Future weekly values or retroactive fill | CONTRACT-012/020, AC-002/003, TF-001/002/009; supported |
| Domain outcomes; INV-05–INV-10/INV-14 | BND-008 complete effect; BND-009 shared money rules | Orphan fee, over-close, wrong side or invented FX | TX-002/006, AC-004–008, TF-002/003/004; conventions gated |
| Boundaries/dependencies; DRV-003–008 | BND-003 current selection; BND-007 run selection; inward capabilities | Catalog or infrastructure becomes execution authority | DEP-015–021, ARCHV-001/004/007; supported |
| Original evidence; FR-45/DATA-18 | BND-007 selects; BND-010 retains immutable closure | New ticks or source mutation rewrites a run | CM-005, CONC-007/010, TF-004/006/007; supported |
| Recoverable saves; INV-12 | BND-010 exact durable generation acknowledgement | Torn restore or lost acknowledged work | TX-004/005, TF-006; cross-workflow proof incomplete, ADV-VER-001 |
| Authority/secrets; POL-11/12 | BND-013 contextual authority; BND-011 data-only exchange | Foreign/stale mutation, secret leak or actual broker effect | SECR/TEN, TF-005–008, ARCHV-002/003/005; supported structurally |
| Integrations; FR-31–35 | BND-011 supplies facts; BND-002/003 qualify them | Empty response becomes closure or demo substitutes for live | EXT-001–004, TF-008, DEFER-001/002; actual evidence outstanding |
| Operability; OPS-02–07 | Semantic owners retain evidence; bounded local diagnostics | Uncertain execution/save cannot be explained | AUD, LOG, TRACE, DIAG, AUDV; supported as design |
| Proportionate complexity; local single user | Local capabilities, serialized run transitions, immutable files | Unnecessary distribution or consistency burden | ADR-001–011 tie mechanisms to stated failures; justified |

## 4. Blocking implementation gates

None identified by this review. Existing DEFER-001–DEFER-007 remain mandatory scoped prerequisites, including standards before foundation and numerical refinement before trading calculations. They must not be read as blanket permission to start every slice.

## 5. Material findings

### ADV-VER-001 — Verify preservation across different durable publication workflows

**Severity:** `MEDIUM`  
**Confidence:** `HIGH`

**Finding**  
The verification model does not explicitly exercise catalog publication against autosave or scoped run replacement and assert preservation of both workflows' unrelated durable content. This leaves a meaningful integration risk between distinct publication scopes. It is a missing proof case, not evidence that data loss is prescribed by the architecture.

**Evidence**

- Architecture Section 19 prescribes immutable candidates and an authoritative retained-generation reference. TX-003 publishes catalog/lineage/coverage; TX-004 publishes captured analysis/run versions; TX-005 replaces affected run/work state while excluding unrelated drawings.
- Section 21 CONC-005 covers older versus newer saves; CONC-006 covers overlapping catalog updates; CONC-008 covers replacement versus run/save callbacks. These do not explicitly address catalog publication against a work checkpoint or scoped replacement.
- Section 28 TF-006 requires interruptions of TX-003–TX-006 and several races, but does not name the combined interleaving or a preservation assertion for components outside the publishing workflow's scope. AC-012 focuses on crash frontiers and older saves.
- Requirements FR-43/FR-44, CONS-02/CONS-09/CONS-15 and OPS-07 require retained acquisitions and coherent saved work to survive independently. Domain INV-12 and HIST-07 protect successfully saved state.

**Property at risk**  
Publishing one component must preserve acknowledged versions of other components outside its authorized replacement scope.

**Concrete failure or change pressure**  
An autosave captures work against generation G. Acquisition then publishes qualified catalog C1. The autosave finishes later. A stale whole-generation publisher could reinstall C0 while correctly saving the new drawing. In reverse order, catalog publication could reinstall old analysis or a pre-rewind run. Each workflow can pass isolated atomicity tests, same-workflow stale-save tests and catalog-conflict tests while the combined implementation remains wrong. A single writable owner does not remove its asynchronous tasks.

This is a possible implementation defect the present proof plan does not directly discriminate; it is not a claim that TX-004 permits overwriting newer saved work.

**Recommended correction**  
Add deterministic publication-barrier cases for catalog versus autosave and catalog versus scoped replacement, in both completion orders, including a crash after the winning publication. Inspect the reopened catalog, analysis and run versions together. Require all acknowledged out-of-scope content to survive; a stale candidate must be rejected/reprepared or published in a way that preserves it. State how the selected publication realization satisfies this assertion. The correction need not select a database, global lock, physical reference layout or new boundary.

**Correction route**  
`architecture-verification-designer` first: add the cross-workflow property and proof obligation. Then `architecture-synthesizer` incorporates the approved clarification. If defining the proof exposes incompatible publication scopes, route that specific decision to `architecture-resilience-designer`; no requirements/domain rewrite is currently indicated. These are the invoked skill's routing labels; in this workspace the combined `system-architecture-designer` Pass 2 owns the corresponding refinement and synthesis work.

**Affected architecture sections/artifacts**

- `architecture-dossier.md` Sections 19, 21, 27–29: TX-003–005, CONC coverage, AC-012, TF-006 and ARCHV-006 as appropriate.
- Later storage standards and persistence verification evidence must carry the added obligation. No source architecture was modified by this review.

## 6. Requirements traceability review

Challenged FR-01–25/FR-27/FR-29 and FR-31–56 by capability family against Sections 2, 5–14 and 27–34. The important architecture consequences remain visible: eight periods, separate bid/ask, full archive, two charts, independent drawings, historical trading, live/backfill, coherent recovery and P3. Excluded FR-26/28 and deferred FR-30 remain excluded. No runtime dependence on captured private endpoints is introduced.

ASM-01 and ASM-02 retain their accepted limits and labels. No hardcoded September-2016 history boundary, SP500-only tick capability, margin model or implicit extra slippage became a requirement. No material orphan decision or upstream contradiction was established. Deferred details retain named owners/triggers; their absence is not evidence of completed feasibility.

## 7. Domain semantics review

Compared DC/REL/TR/INV/PRE/HIST/OP/POL with architecture Sections 4, 7, 10, 13–14 and 19–25. Triggers differ from fills; acceptance differs from effectiveness; closed/cancelled is terminal in forward history but does not prohibit confirmed prefix reconstruction. A block has original context and no partial execution. Account balance/remainder and study values are derived, while actions, input selections and execution facts retain their own authority.

Attacked stop-first before entry, TP-first evidence, worse-than-limit execution, duplicate partial closes, obsolete protection, nonpositive-balance risk sizing and current FX substitution. Explicit preconditions and shared monetary ownership resist these failures. Confirmation cannot legalize an intrinsically invalid transition.

Exact formulas/rounding remain DM-GAP-03/04 and DEFER-003/004. During replay interaction refinement, identify the selected series/period governing a user-visible single-bar step when charts differ, and preserve its relationship to run processing. The supplied sources do not establish a specific active-chart or fixed-M1 policy; this review does not invent one or treat a control choice alone as a demonstrated architecture defect.

## 8. Responsibility and boundary review

Meaning, continuity, current selection, historical availability, authored analysis, studies, run coordination, execution, monetary policy, retention, provider exchange, presentation and authority each protect named knowledge with deliberate exclusions. The highest-risk separations are BND-003 versus BND-007 and BND-005 versus BND-007. Sharing observations or participating in save/replay does not merge their authority.

BND-007 coordinates multiple rules but does not own their formulas or file protocols. BND-010 has broad physical duties but uses narrow consumer-owned contracts; it does not choose financial truth. BND-013 is bounded local authority, not an unrestricted policy engine. No material dumping ground or unjustified deployment fragmentation was established. Implementation must preserve these distinctions without mechanically turning every boundary into a service.

## 9. Dependency and contract review

Reconstructed the Section 11 graph through CONTRACT-012–020. Provider/physical types stay outside core meaning; study computations receive bounded inputs and cannot fetch their own future data. Run/execution temporal coupling is required by existing-before-new semantics and explicitly sequenced, rather than hidden in redraw callbacks.

DEP-015–021 have planned mechanical checks ARCHV-001–007 with semantic tests for dynamic violations. No portability to every provider is promised: BND-011 isolates the chosen provider protocol while Dukascopy identity remains legitimate domain data. The implementation language/module realization still needs standards; a prose import rule is not represented as an already passing check.

## 10. Data and source-of-truth review

| Fact/concept | Claimed authority | Derived/external copies | Local scope | Review result |
|---|---|---|---|---|
| Sibling observations | External ingestion; attributed provider evidence | Immutable owned run selections | Provider/series/revision | No app writes; source stability checked during copy |
| Current qualified history | BND-003 catalog selection | Derived supported-period bars and views | Current series/revision | Final supersedes provisional only with evidence |
| Coverage/closure | BND-002 evidence-based assessment | Cached qualified results | Series/interval/revision | Empty response/weekend cannot establish closure |
| Run basis/actions/boundary | BND-007 | Retained closure and bounded views | Individual run | Current catalog cannot overwrite it |
| Execution/position/account effects | BND-008; BND-009 monetary rules | Balance/remainder/reports | Run/order/position | Whole effect; reports are not a second execution engine |
| Analysis/drawings | BND-005 committed authored version | Saved checkpoint/image | Layout/instrument | Independent from trading rewind |
| Saved/backup success | BND-010 retention fact | Exported pinned generation | Included analysis/runs | Exact-version claim; combined publication proof needs ADV-VER-001 |
| Credentials/authority | BND-011 protected setup; BND-013 current context | No backup/browser bearer copy | Local provider purpose/writer | Restored facts cannot confer authority |

Paths/hashes alone cannot preserve original values; immutable owned closure and pins explicitly address mutable sources and cleanup. Retained results remain authoritative historical simulation facts, without turning them into observed broker executions.

## 11. Transaction, failure, concurrency, and idempotency review

| Workflow | Attack | Expected guarantee | Documented behavior / result |
|---|---|---|---|
| Execution/block/resume | Price known but FX absent; resolve later | No partial effect or repricing | TX-002/006, FAIL-010/014/015 preserve original event; supported |
| Submit/close/protection | Duplicate intent; equal deliberate intent; two closes | Exactly one outcome per intent, bounded target remainder | IDEM-001/002, CONC-003/004, AC-018; supported |
| Save | Crash after content/reference but before ack; older save completes | Old-or-new coherent recovery and truthful saved label | TX-004, FAIL-012/013, CONC-005, RETRY-004; actual platform proof required |
| Rewind/restore | Late pre-replacement save/execution or stale confirmation | No resurrection; cancelled/failed preparation unchanged | TX-005, CONC-008, SECR-002/005; supported |
| Acquisition | Partial response; final/live overlap; changed source copy | Prior qualified history remains; no mixed revision | TX-003, FAIL-004–007, CONC-006; supported |
| Backup/cleanup | Delete while exporting pinned inputs | Complete snapshot or honest failure | CONC-010, FAIL-018–020; supported |
| Different publishers | Catalog versus autosave/scoped replacement | Unrelated acknowledged durable state survives | Required guarantees exist; explicit combined proof missing, ADV-VER-001 |

No distributed atomicity fiction was found. Remote data reads/subscriptions are outside local publication; their uncertainty is not repaired by repeating a simulated trade. Equal timestamp/value is not sufficient tick occurrence identity.

## 12. Security and tenant-isolation review

Application tenants/roles and cross-tenant login tests are `NOT APPLICABLE`: one analyst is the confirmed scope. Foreign/unbound callers, second writers, cross-run targets and stale epochs remain applicable and have explicit negative plus valid-owner cases.

Attacked loopback-as-authorization, timeout-only owner takeover, path traversal, symlink/duplicate archive entries, restored bearer authority, raw provider errors and broker-capability leakage. SECR-001–008/TEN-001–004 and ARCHV-002/003/005 require denial, confinement, fresh authority and clean outputs. Security does not rely on UI flags or authentication alone. Actual origin/IPC fencing and bounded parsing must be demonstrated after stack selection. Durable domain facts and sanitized rejection diagnostics have different retention purposes; no permanent security journal is required by the supplied local scope.

## 13. External integration review

| Integration | Authority relationship | Failure/timeout | Retry/duplicate | Replaceability/evolution | Result |
|---|---|---|---|---|---|
| Sibling archive | External attributed facts, not app-owned mutable data | Unavailable/changed input explicit | Stable copy; established occurrence identity | New months/tick assets behind read capability | Structurally supported; no fresh source audit |
| Historical M1/H1 | Provider observations; core qualifies finality/coverage | Preserve history; empty/partial is not closure | Qualified read retry; content/revision reconciliation | Protocol isolated in BND-011 | Actual publication/session evidence gated |
| Live-account feed | Data-only provider purpose | Honest stale/failed/recovering; remote teardown may be uncertain | Reconcile session, revoke epoch, catch up | API/auth isolated; provider identity remains explicit | Actual API/entitlements unverified; no demo fallback |
| Local retention/export | Authoritative publication outcome | Disk-full/corruption/unknown ack cannot mean saved | Reconcile reference/artifact before retry | Format migration behind BND-010 | Platform proof gated; ADV-VER-001 applies |

TradingView private services, real brokerage, alert delivery, external run import and automatic missing-tick acquisition are `NOT APPLICABLE` to v1 runtime contracts. This review did not access any provider account.

## 14. Verification review

| High-risk property | Planned evidence | Adequacy as design | Finding |
|---|---|---|---|
| No future information or processed-event reuse | TF-001/002/009, AC-002/003, ARCHV-004 | Domain plus rendered wiring; adequate planned coverage | None |
| Exact side/limit/protection/USD effects | TF-002/003, AC-004–008, AUDV-002 | Independent arithmetic required; approved conventions first | None |
| Original run inputs and rewind scope | TF-004/006/007, AC-010/011 | Values/settings/closure tested, not only hashes | None |
| Durable saves and sole writer | TF-005/006, AC-012/013 | Real platform reopen/fencing required; mocks insufficient | None for isolated/scoped races |
| Preservation among different publishers | Current TF-006/AC-012 | Combined publication history and out-of-scope assertions not explicit | ADV-VER-001 |
| Safe authority/backup/export | TF-005/007/008, AC-013/014, ARCHV/AUDV | Scope negatives, sentinel exclusions and valid positives | None |
| Provider behavior | TF-008 plus DEFER-001/002 | Controlled adapters distinguished from real acceptance | Evidence outstanding, already gated |
| Full archive/P3 | TF-010, AC-016, recorded workload/hardware | Timing boundaries resist excluding slow reads as “preparation” | None; no benchmark run |

Broad duplicate E2E testing is not demanded. Domain, workflow, physical-storage, provider and rendered checks prove distinct failure modes. All of these are future evidence obligations, not successful test results from this review.

## 15. Observability and production-diagnosis review

| Scenario | Operator must determine | Available planned evidence | Assessment |
|---|---|---|---|
| Order seems duplicated or blocked | Original occurrence, applied effect, missing prerequisite, certainty | AUD-002, LOG-003, TRACE-003, DIAG-003/004 | Supported without raw financial dumps |
| Save/restore acknowledgement lost | Actual recoverable generation and authorized replacement outcome | AUD-003, LOG-005, TRACE-004, DIAG-005/006 | Reconciliation precedes another destructive action |
| No live movement/catch-up incomplete | Receipt versus display lag; access, closure, gap and recovery condition | LOG-002, MET-002/003, TRACE-002, DIAG-002/007 | No-receipt cannot become proven closure |
| Slow navigation while resolving ticks | Read/calculate/render/detail phases and accepted workload | TRACE-001–003, MET-001–005, DIAG-009 | Fix scheduling without shrinking accessible history |
| Forbidden action or malformed backup | Safe scope/reason, operation correlation, unchanged prior state | LOG-004, ALERT-004, DIAG-007/008 | No tokens/raw archive paths in diagnostics |

Local statuses are operational feedback, not excluded market-trigger alerts. Numeric stale/backoff/retention settings remain DEFER-006; no unsupported SLO is promoted to fact. A new combined publication case should inspect actual versions as ADV-VER-001 requests; logs alone would not prove preservation.

## 16. Complexity and proportionality review

| Decision | Driver / benefit | Added burden | Assessment |
|---|---|---|---|
| Thirteen logical boundaries | Protect distinct knowledge and authority | Contract discipline | Justified; no process-per-boundary requirement |
| Immutable input closure/generation publication | FR-45/55 and crash-safe saved claims | Copying, pins, integrity, cleanup, migration | Justified; entire-archive copies are not required |
| Serialized per-run effects/epochs | Async decisions, closes and replacement | Context tracking/backpressure | Justified; no extra ordering across unrelated runs |
| Independent bounded chart/detail paths | Archive size and accepted P3 | Scheduling and cache-context discipline | Justified; no fabricated fills for responsiveness |
| Local diagnostics separate from domain evidence | Explain uncertain outcomes without secrets | Bounded retention/configuration | Justified; remote telemetry and permanent journal unnecessary |

No material speculative abstraction was established. Concrete realization could still overengineer these contracts; the dossier explicitly leaves implementation structure to standards.

## 17. Change attacks

### Attack 1 — Replace staged ticks with a finalized month and add another tick asset

**Expected owner:** BND-010 source access, BND-003 current selection, BND-004 detail discovery; actual EVO-01/04 pressure.  
**Legitimate secondary changes:** Coverage/revision/occurrence evidence and new-run selection.  
**Should remain untouched:** Saved-run values/results, chart periods, execution/account policies and drawings.  
**Observed blast radius:** INT-001, CM-005, CONC-006/007 and IDEM-002/003 retain old selected values and qualify new evidence. A repeat final file cannot justify timestamp-only collapse of distinct ticks.  
**Assessment:** Contained by meaningful authority boundaries; no SP500-only or mutable-path exception found. **Related finding:** None.

### Attack 2 — Final publication revises a weekly candle while analysis autosaves

**Expected owner:** BND-003 affected aggregation and BND-010 publication; actual FR-33/35 pressure combined with ordinary FR-44 activity.  
**Legitimate secondary changes:** Current coverage/lineage and bounded current views.  
**Should remain untouched:** Saved-run basis/results and acknowledged authored work.  
**Observed blast radius:** Semantic ownership and final-over-provisional precedence contain the change. Concurrent durable publishers must still preserve each other's out-of-scope content.  
**Assessment:** Authority design survives; combined proof needs explicit coverage. **Related finding:** ADV-VER-001.

### Attack 3 — Change instrument contract values and commission conventions

**Expected owner:** BND-009, with explicit BND-007 selection; actual FR-41/50 pressure.  
**Legitimate secondary changes:** Specification editor, selected conventions, numerical fixtures and compatibility evidence.  
**Should remain untouched:** Old run outcomes, source observations, drawing ownership and period availability.  
**Observed blast radius:** DATAOWN-011, CONC-012 and CONTRACT-011/014 bind monetary results to run/event/convention versions. Missing-prerequisite completion cannot silently revalue prior executions.  
**Assessment:** Contained; exact math remains DEFER-004. **Related finding:** None.

### Attack 4 — Change provider API/session behavior or migrate retained formats

**Expected owner:** BND-011 for provider protocol; BND-010 for format migration. These are dossier CHG-002/004 pressures, not a requirement to support a second provider now.  
**Legitimate secondary changes:** Normalization/coverage evidence, protected setup, old-format compatibility and actual durability tests.  
**Should remain untouched:** Core fills, hedging, USD-account meaning and historical-information rules.  
**Observed blast radius:** CONTRACT-015/017 and DEP-015 isolate mechanics; historical inputs/settings must retain meaning through migration. New evidence that invalidates guarantees explicitly reopens readiness.  
**Assessment:** Structurally contained; feasibility remains evidence limited. **Related finding:** None.

## 18. Positive architecture evidence

- Current catalog selection cannot automatically mutate saved runs; retained values, absence/coverage qualifications and conventions protect more than path identity.
- ASM-01 cannot invent an entry, price, continuity or observed chronology; ASM-02 does not authorize over-close or worse-than-limit execution.
- Missing original-event conversion blocks the whole effect; receipt time cannot become a new historical fill time.
- A lost save acknowledgement calls for reference inspection rather than replaying a trade or edit.
- Confirmed rewind reconstructs the prefix and removes dependent later effects while preserving independent drawings.
- Sole-writer enforcement includes publication fencing across supported tabs/processes; restore cannot import command authority.
- Controlled fixtures cannot certify actual live entitlements, provider finality or physical-storage durability. Those proofs remain separate.
- P3 preserves both full archive access and honest timing boundaries; heavy tick resolution cannot dictate routine chart responsiveness.

## 19. Recommended correction order

1. Refine the Pass 2 verification model for ADV-VER-001 with combined publication interleavings and explicit reopened-state assertions. Clarify scope preservation alongside the proof; revisit resilience only if a contradiction emerges.
2. Incorporate the accepted correction in the canonical dossier and downstream persistence standards/brief. Preserve the requirements/domain authorities and G1 boundary scope.
3. Review the corrected property-to-test mapping; later require actual selected-platform evidence. Discharge each existing DEFER prerequisite before its affected work, independently of this finding.

No new requirements interview, replacement domain model or wholesale boundary redesign is recommended.

## 20. Residual risks and evidence limitations

| Risk/limitation | Why it remains | Implementation consequence / required evidence |
|---|---|---|
| Actual live API/auth/assets unavailable | No account integration performed | DEFER-001 requires discovery before affected enablement/acceptance; historical mode is not a waiver |
| Session/finality/FX applicability facts unverified | Instrument-specific external evidence absent | DEFER-002: affected traversal/valuation/finalization remains unresolved until justified |
| Numerical/study/tool/control conventions unfinished | Deliberate scoped downstream refinements | DEFER-003–005: approve conventions and independent examples before affected briefs; include replay step-control semantics |
| Atomic publication and physical sole-writer capability unproven | Stack/platform not selected | DEFER-007 and TF-006 require actual capability evidence before depending on it; ADV-VER-001 adds combined histories |
| Scheduling/backoff/resource bounds and P3 unmeasured | No implementation/hardware benchmark | DEFER-006, TF-010; do not invent provider deadlines or claim measured performance |
| No separate upstream resilience/verification artifacts or approval snapshot | Canonical dossier consolidates them | Internal-consistency review is possible; independent cross-artifact/approval-history comparison is evidence limited |
| Simulated full-fill/bar-touch/stop-first differs from reality | Explicitly accepted ASM-01/02 | Preserve labels and limitations; no broker-parity claim |

These limitations remain visible; none was converted into a new product requirement or an already passing test.

## 21. Final implementation-readiness statement

**Can implementation AI follow the reviewed architecture without inventing a high-consequence decision? YES, within the dossier's explicitly gated scope.** It can follow named semantic authorities, complete-effect/publication rules and failure/security guarantees, and must stop affected work at its documented DEFER prerequisite rather than guess. ADV-VER-001 is a non-blocking verification correction to track. This is readiness for governed downstream preparation and eligible slices, not unconditional authorization for every feature, actual provider feasibility, physical durability certification or production release.
