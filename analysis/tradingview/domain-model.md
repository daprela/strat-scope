# Domain Model — Dukascopy Chart Workspace and Historical Trading

**Handoff status:** `READY_WITH_ACCEPTED_ASSUMPTIONS`  
**Revision:** 1 — 19 October 2026  
**Source requirements:** [requirements-dossier.md](requirements-dossier.md), revision 14, read in full  
**Upstream convergence:** `CONVERGED_WITH_ACCEPTED_ASSUMPTIONS`  
**Scope:** One local analyst's bar-based analysis workspace, Dukascopy history/live continuity and reproducible historical simulated trading over the ten supplied instruments and exactly eight bar timeframes.

The requirements dossier is authoritative. Its source reports are provenance, not authority to import their proposed software designs. The definitions below refine accepted behavior; identity/equality arguments and derived conditions are semantic deductions, not additional product commitments. ASM-01/ASM-02 remain accepted approximations. Provider access, sessions and finality are evidence obligations, not verified facts. No account connection, market-data acquisition, application implementation or architecture selection is performed by this model.

## 1. Domain vocabulary

| ID | Term | Operational meaning | Distinguish from | Source requirement(s) |
| --- | --- | --- | --- | --- |
| DC-01 | Instrument | Continuing provider-qualified market subject, with local/provider symbols and explicit simulation specifications. | A display alias, exchange venue, equivalent-looking index or broker execution entitlement. | BR-01, BR-06, DATA-02 |
| DC-02 | Bar timeframe / bucket | M1/M5/M15/H1/H4/D1/W1/MN1 and their supplied UTC intervals. W1 starts Monday 00:00 UTC; MN1 starts on the first calendar day. | Display timezone, viewport range or execution detail; MN1 is not 30 days. | FR-07, BR-02, DATA-03 |
| DC-03 | Quote side | Bid or ask price/volume basis. Bid is the chart default; ask is selectable. | Midpoint, execution direction or account currency. | FR-04, BR-03 |
| DC-04 | Market observation | Provider-attributed bar-side OHLC/volume or quote tick at its original precision, with time, origin and revision evidence. | A calculation, invented observation or observed broker fill. | DATA-05–DATA-08, DATA-16–DATA-17 |
| DC-05 | Dataset revision / selected inputs | A particular selection of market observations and provenance used for an analysis or retained run, including applicable ticks and historical conversion evidence. | A mutable path, latest directory contents or policy settings alone. | FR-45, DATA-18, CONS-15 |
| DC-06 | Coverage | Usable observations, actual bounds, limitations and unresolved intervals for a provider/instrument/timeframe/side/revision. | First/last file labels, a continuous range or resident working set. | FR-02, FR-51–FR-52, BR-04 |
| DC-07 | Known closure / unexplained data gap | A non-trading interval supported by instrument/session evidence / an unresolved missing or unusable interval where continuity is not established. | Weekend inference, empty response or absence of ticks alone. | FR-42, FR-46, BR-09, BR-20 |
| DC-08 | Current historical catalog | The currently selected usable history, extended by acquisitions; final historical observations supersede provisional live-built observations for affected current history. | Frozen inputs of a saved run or proof of live freshness. | FR-32–FR-35, CONS-09 |
| DC-09 | Provisional candle / completed bar | A forming live-built candle / a period that has ended at the information boundary with usable required evidence. | Provider finality: period completion, validation and authoritative final publication are separate conditions. | FR-20, FR-31, FR-35, FR-51 |
| DC-10 | Layout / chart selection | Named continuing analysis arrangement / a chart's instrument, timeframe and side selection with associated presentation. | Pending selection, loaded data or replay run. | FR-03–FR-05, FR-16–FR-17 |
| DC-11 | Study instance / study output | An independently configured built-in study / its derived values for selected inputs and calculation convention. | A script, source observation or guaranteed TradingView numeric match. | FR-11–FR-12, BR-05 |
| DC-12 | Drawing / preview | Committed financially anchored annotation belonging to a layout and instrument / an uncommitted candidate edit. | Historical market evidence or a real/simulated position; measurement tools create no orders. | FR-13–FR-16 |
| DC-13 | Replay cursor / decision point | Common historical information boundary / the point after advancing completed bars and evaluating existing eligible orders at which new user decisions are accepted. | Hover time, latest-history time, wall clock or permission to reuse an already processed event. | FR-19–FR-21, FR-40, FR-53 |
| DC-14 | Trading run | Continuing hypothetical trading exercise with selected inputs, settings, retained actions, cursor and reproducible outcomes. | Current catalog, broker account or external completed-run bundle. | FR-22, FR-27, FR-29–FR-30, FR-45 |
| DC-15 | Trading action / accepted order | A user's submission, modification, cancellation or targeted close decision / a valid instruction awaiting its effective eligible evidence. | An execution, a fill at the visible close or an automatically netting opposite order. | FR-27, FR-38, FR-40, BR-17 |
| DC-16 | Stop trigger / execution | Evidence that a stop condition has been crossed / a hypothetical quantity-and-price fill with complete monetary effects and resolution evidence. | A guaranteed stop-level price or a broker-observed execution. | FR-37, FR-41–FR-42, FR-47–FR-48, FR-53 |
| DC-17 | Hedged position / protective exit | Independent exposure opened by an entry / SL or TP instruction reducing only its associated remaining exposure. | Net instrument exposure, opposite entry or annotation. | FR-38, BR-14 |
| DC-18 | Simulated USD account | Run accounting with configurable initial USD balance, executions, fees and realized results, distinct from open-position valuation. | Broker cash, instrument price/profit currency or margin account. | FR-39, FR-41–FR-42, BR-15, BR-18 |
| DC-19 | Instrument simulation specification | Selected unit/contract monetary meaning, currencies, price increment and quantity increment/minimum, including identified user overrides. | Chartability or authority to change actual broker contract terms. | FR-49–FR-50, BR-06 |
| DC-20 | Sizing / commission / conversion | Planned permitted quantity / configured execution charge / historically applicable monetary translation into USD. | Guaranteed realized loss, extra slippage or relabelling quote currency as USD. | FR-39, FR-41–FR-42, FR-49, FR-54 |
| DC-21 | Durable checkpoint / backup | Coherent last successfully autosaved analysis/run state / manually retained analysis and run inputs sufficient for coherent restoration. | Work still saving, a preview, credential export or external run-bundle import. | FR-44, FR-55, OPS-03 |

## 2. Concepts and definitions

### 2.1 Market subjects, evidence and availability

The required instrument universe is AUDJPY, EURGBP, EURUSD, GBPUSD, USDJPY, DAX, FTSE, NASDAQ, SP500 and XAUUSD. The observed provider mappings for index-related instruments are respectively DEUIDXEUR, GBRIDXGBP, USATECHIDXUSD and USA500IDXUSD; the remaining observed symbols match the local symbols (EURUSD metadata is absent in some manifests). An absent field must be reported, not repaired by assuming another product. Local NASDAQ is not an exchange venue; SP500 is not established as `SP:SPX`. [DATA-02, BR-01]

An observation's event/bucket time and the point at which its contents are available are different semantic facts. A weekly opening label does not make the week's final high/low/close knowable on Monday. Bars retain nanosecond timestamp precision and ticks retain their millisecond precision; display conversion cannot collapse distinct observations. Where source ordering does not determine chronology, do not invent a sequence. [FR-20, DATA-04–DATA-07, CONS-10]

Availability has independent dimensions: readable evidence, producer assertion (for example GOOD/COMPLETE/IN_PROGRESS), validated usability, period completion, provider finality, and usable coverage. No single producer flag answers them all. A partial edge bucket does not prove complete source coverage. Zero volume and weekend timestamps alone invalidate neither bars nor ticks and establish no closure. Side volume remains provider volume with unverified units, not exchange trades or liquidity. [FR-51, BR-04, DATA-06, DATA-09, Section 5 of requirements]

Acquisition extends the current catalog using M1/H1. Recovered M5/M15 derive from M1; H4/D1/W1/MN1 derive from H1 under the supplied UTC semantics. Only recovered/affected boundary history is completed or recalculated; unrelated stored history is retained. Current final historical data supersedes provisional live-built data, while a saved run continues using its selected evidence. September 2016 and the currently SP500-only tick inventory are dated inventory facts, not permanent domain restrictions. [FR-32–FR-35, FR-43, FR-45, FR-52, BR-08, DATA-03, DATA-15–DATA-18]

### 2.2 Analysis is authored work, not market history

A layout names reusable analysis containing one or two charts, their selections and arrangements, studies, presentation and drawings. Drawings belong to layout/instrument and survive interval switches and trading rewind, including annotations authored after the destination replay time. Hidden/locked flags do not remove anchors or existence. Study instances may have equal parameters yet be separately edited or removed. Outputs use SMA/EMA/RSI/MACD/Bollinger Bands/volume conventions whose initialization, missing values and precision must be declared; missing/warm-up output is unavailable, never an invented zero. [FR-08, FR-11–FR-17]

Watchlists and details reference instruments and observations; they do not own their price histories. During replay they obey the same information boundary as charts, studies and simulation. Interval synchronization changes the selected supported interval once for both charts; it does not imply that instruments, quote sides, observation timestamps or coverage are equal. [FR-09, FR-17, FR-20, CONS-03, CONS-16]

### 2.3 Run, instructions, fills and accounting

A run is the continuing historical exercise, not its current cursor or current balance. Its selected observations, conversion/tick evidence, specifications and calculation/execution/commission conventions give results meaning. New catalog history cannot silently replace them. Continuing a run with new user actions is distinct from recomputing old results against changed inputs. Explicit restart with updated data is deliberate replacement of the exercise's input basis; automatic branching or an immutable archive of every replaced run is not required. [FR-21–FR-22, FR-45, BR-19, DATA-18]

Order acceptance does not establish fill eligibility at the current visible close. Existing eligible orders are evaluated before new decisions; submissions and modifications take effect only after that decision point. A triggered stop entry becomes market-effective and uses the next eligible executable side evidence, without a newly invented delay or stop-level guarantee. The model imposes no artificial timestamp increment: source order and processed-event boundaries determine what is next. [FR-40–FR-41, FR-53, BR-11–BR-12]

Entry buys use ask and entry sells use bid; closing a long sells at bid and closing a short buys at ask. This is independent of the chart side. Limit/TP bounds and stop/market pricing differ (POL-05). Opposite entries remain separate hedged exposures. Every eligible requested execution fills the requested quantity under ASM-02; a manual partial close is a smaller explicit request, not an automatic liquidity partial. [FR-04, FR-38, FR-47–FR-48, BR-13–BR-14, ASM-02]

Every committed execution has coherent evidence, fee, position/protection and USD-account effects. A missing conversion/specification/session prerequisite is a blocked historical event, not a rejection, zero-result fill or partly applied account outcome. Resumption reconsiders that original event with its original historical pricing point. [FR-42, FR-50, CONS-07, CONS-14]

### 2.4 Planned risk and monetary meaning

Risk-percentage sizing uses the simulated USD balance, valid SL distance, instrument monetary meaning, historical conversion and configured entry/planned exit commissions. It selects the largest permitted quantity within the USD budget, rounds down to permitted increments and rejects below-minimum results. Percentage-risk sizing is unavailable at nonpositive balance; fixed sizing still obeys instrument/quantity validity with no margin rule. This budget is not an aggregate portfolio-risk cap or a bound on gap losses. [FR-39, FR-49, FR-54, BR-15, BR-22]

The three per-instrument commission choices are fixed USD per execution, USD per unit, or percentage of USD notional, all defaulting to zero. Entry and every exit execution, including a manual partial close, incur their configured charge. Separate execution charges must not be mistaken for one charge per original position. Deterministic USD/notional/quantity rounding and instrument-specific valuation conventions must be declared and retained with results; this document does not select unapproved numeric precision or infer unverified contract multipliers. [FR-41, FR-50, FR-54, BR-05]

USD account denomination does not remove the need to convert non-USD monetary outcomes. Conversion requires historical bid/ask evidence applicable to the event and known no later than it, with session/applicability justification. Merely being earlier is not sufficient authority to silently use a stale rate. Missing evidence blocks the affected operation. [FR-42, BR-18]

## 3. Identity and value semantics

These classifications express continuing business meaning, not mandated implementation types.

| Concept | Semantic kind | Identity/equality rationale | Important notes | Source requirement(s) |
| --- | --- | --- | --- | --- |
| Instrument | Identity-bearing | The same provider-qualified subject persists across aliases, new observations and specification changes. | No product equivalence inferred from a similar name. | BR-01, FR-50 |
| Layout | Identity-bearing | Rename/rearrange changes the same saved analysis; equal-looking layouts can be independently maintained. | Name is mutable, not its sole identity. | FR-16 |
| Chart within an arrangement | Identity-bearing, scoped to arrangement | A particular chart retains analysis while its selection/style changes; two equal selections remain distinct chart places. | Semantic deduction from independent versus synchronized selections; no globally independent chart lifecycle required. | FR-05, FR-17 |
| Study instance; committed drawing | Identity-bearing, scoped | Equal-looking instances can be individually changed, hidden or removed over time. | Cancelled preview has no committed drawing identity. | FR-12–FR-15 |
| Trading run | Identity-bearing | Cursor/actions/positions evolve within the same exercise, which can be resumed independently of current history. | No rule that replay exit completes or deletes it. | FR-21–FR-22, FR-45 |
| Accepted order; hedged position | Identity-bearing within run | Each is tracked through modifications, fill/closure; equal opposite or same-side entries are still independent instructions/exposures. | A targeted close must name the position semantically. | FR-27, FR-38 |
| Simulated account | Continuing accounting identity within run | Same exercise's balance changes across its executions. | No cross-run wallet or multi-account hierarchy is required. | FR-39, CONS-15 |
| Action; execution | Distinct historical occurrence | Repeated equal requests/fills at the same displayed time remain separate occurrences with different consequences. | Distinguish occurrences using retained evidence/order, not display timestamps alone; no storage key prescribed. | DATA-07, CONS-07, CONS-10 |
| Dataset revision / run-input selection | Immutable evidence value | Equal selected observations/provenance have the same evidential meaning; changing facts changes the selection. | A series bucket can retain its address while its observation version changes. | FR-35, FR-45, DATA-18 |
| Instrument specification, policy/settings selection | Value-like revision | Equal unit/currency/increment/convention values are interchangeable for the same context. | Current editing selects another value; old run-selected values remain meaningful. | FR-41, FR-45, FR-50 |
| Timeframe, quote side, monetary amount, quantity, anchor, cursor | Value-like | Relevant values and units define equality; no independent lifecycle required. | Cursor equality alone does not identify which events/actions have already been processed. | BR-02, FR-14, FR-40, FR-54 |
| Bar/tick contents; conversion evidence; study output | Value-like evidence/results | Equality includes instrument, basis, time precision, revision/provenance and relevant values. | Tick occurrences must not be deduplicated merely because displayed values/times coincide. | DATA-07, BR-05, CONS-10 |
| Coverage, readiness, remaining quantity, saving condition | Derived condition | Determined by underlying observations, actions or durability evidence. | No independent entity/status enumeration mandated. | FR-02, FR-38, FR-44, FR-52 |

## 4. Relationships and ownership

| ID | Relationship | Business meaning | Ownership/scope rule | Source requirement(s) |
| --- | --- | --- | --- | --- |
| REL-01 | Analyst → authored analysis, runs, retained acquisitions | Sole local ownership and mutation authority. | No tenant/role hierarchy; sibling ingestion originals remain outside mutation authority. | AUTH-01–AUTH-03, DATA-08, DATA-16 |
| REL-02 | Instrument → series and current specification | Provider identity qualifies observations and contract meaning. | Series distinguish timeframe/side/revision; chartability does not supply missing specifications. | BR-01, BR-06, FR-50 |
| REL-03 | Aggregate observation → source evidence | Recovered/affected bucket derives its meaning from its actual inputs. | Preserve UTC, side and lineage; neither upsample missing data nor replace unrelated stored history. | BR-02–BR-03, BR-08, FR-33 |
| REL-04 | Layout → chart arrangement, study configuration, drawings | Continuing reusable authored analysis. | One/two charts; drawing scope is layout plus instrument across timeframes, not its creation timeframe or trade run. | FR-12–FR-17 |
| REL-05 | Watchlist/details → instrument/reference observation | Presentation of selected instrument evidence. | Replay boundary applies; no ownership of market history inferred. | FR-09, FR-20 |
| REL-06 | Replay workspace → active run boundary and charts/panels | Shared historical information limit. | Common cursor does not promise identical last observation time across instruments/periods. | FR-20, CONS-16 |
| REL-07 | Run → selected inputs, settings, actions, executions, account and positions | Evidence and outcomes of one historical exercise. | Retain until deliberate deletion; latest catalog has no authority to replace the original basis on resume. | FR-22, FR-45, DATA-18, CONS-15 |
| REL-08 | Entry execution → independent position | Filled entry creates its own exposure. | Opposite entries do not own/reduce each other. No scale-in/merge relationship is introduced. | FR-38, BR-14 |
| REL-09 | Position → optional SL/TP and targeted close requests | Protection/closure affects only remaining quantity of that position. | After partial close resize protection; full close cancels remaining protection. | FR-38, FR-54 |
| REL-10 | Execution → pricing/resolution/conversion evidence and accounting result | One coherent historical monetary outcome. | No orphan fill, fee, balance effect or protective remainder. | FR-37, FR-41–FR-42, CONS-07, CONS-14 |
| REL-11 | Backup → analysis/runs and required input versions | Reproducibility and coherent recovery. | Include necessary evidence, exclude credentials and unrelated archive obligations; not external run-bundle import. | FR-30, FR-55, DATA-18, OPS-03 |

## 5. State models

State labels below are semantic conditions, not prescribed status fields. Orthogonal conditions remain separate. Terminal means terminal along forward trading history; confirmed rewind reconstructs an earlier history rather than illegally reopening a later terminal object.

### 5.1 Evidence, coverage, feed and recovery

**Current-state semantics:** Discovery/readability/validation, usable coverage, provider assertion, provisional/final evidence and feed/recovery condition are distinct dimensions. Recovery may be pending, progressing, partially usable, complete for the requested interval, or failed. No receipt, stale receipt and proven closure are different conditions.  
**Terminal conditions:** A discovered evidence revision remains a fact even when a newer current revision supersedes it. Recovery completion is interval-specific, not proof all future history is present.

| ID | Current state/condition | Operation | Required intrinsic condition | Next state/condition | Domain effects / preserved facts | Source requirement(s) |
| --- | --- | --- | --- | --- | --- | --- |
| TR-01 | Undiscovered/unvalidated input | Establish usable coverage | Readable observations and validation evidence | Usable, limited or unreadable selection | Record actual bounds/unusable intervals; preserve source and producer assertions separately. | FR-01–FR-02, FR-51–FR-52, BR-04 |
| TR-02 | Missing historical interval | Recover historical evidence | Eligible Dukascopy M1/H1 observations, if available | Progressing/partially usable/complete, or unresolved/failed | Extend only established coverage; no-response alone proves no closure; existing history remains readable. | FR-32–FR-34, FR-43, CONS-08 |
| TR-03 | Provisional current candle/affected derivatives | Reconcile final history | Validated final historical publication evidence | Final current observation and affected derivatives | Supersede provisional current values, avoid duplicates; retain saved-run originals and unrelated stored history. | FR-33, FR-35, CONS-09, CONS-16 |
| TR-04 | Current selected catalog | Discover changed source/new ticks | Distinct provenance/observations established | Revised current catalog/coverage | Saved runs keep their selected evidence/results; new runs may select revised evidence. | FR-45, DATA-17–DATA-18, CONS-11 |
| TR-05 | Feed receipt/interruption/no observations | Reassess continuity or reconnect | Actual receipt, failure, staleness or instrument/session evidence | Receiving/stale/failed/known closure/recovering as justified | No fabricated movement; startup/reconnect catches up while app runs. | FR-31–FR-35, FR-56, BR-09, OPS-06 |

Forbidden: declaring continuous coverage from filename extrema, declaring closure from weekend/empty response, silently converting IN_PROGRESS ticks to validated complete coverage, or mutating saved-run evidence through TR-03/TR-04. [BR-04, FR-45–FR-46, DATA-06]

### 5.2 Chart selection, analysis edits and durability

**Current-state semantics:** Requested selection and successfully displayed selection are distinct. Drawing commitment, visibility and lock are independent. Durability belongs to a particular coherent version of authored work, not a permanent global saved flag.  
**Terminal conditions:** Cancelled preview creates no committed object; confirmed deletion removes the selected committed work. Supported undo/redo can restore analysis without duplicating its meaning; exact depth remains UNK-03.

| ID | Current state/condition | Operation | Required intrinsic condition | Next state/condition | Domain effects / preserved facts | Source requirement(s) |
| --- | --- | --- | --- | --- | --- | --- |
| TR-06 | Valid displayed selection; different request pending | Adopt requested selection | Matching usable instrument/timeframe/side/revision evidence | New coherent displayed selection | Failure retains last valid chart; obsolete results cannot relabel/replace current bars. | FR-02–FR-04, CONS-01 |
| TR-07 | Drawing/settings/study preview | Commit or cancel edit | Valid parameters to commit; none to cancel | Committed unsaved work, or previous valid analysis | Cancellation adds no lasting drawing/settings; invalid study inputs retain valid configuration. | FR-10, FR-12, FR-14–FR-16 |
| TR-08 | Committed drawing/study/layout configuration | Edit, hide/show, lock/unlock, remove, undo/redo | Operation applies to the selected supported object; valid committed result | Revised analysis with corresponding action meaning | Retain drawing anchors/scope; no duplicate on redo; destructive authority is separate POL-11. | FR-12–FR-17, FR-55 |
| TR-09 | Committed unsaved/saving work | Establish durable checkpoint | Successful retention of a coherent version | That version durably saved; later edits may remain unsaved | Failure preserves previous checkpoint, reports error and never claims failed work durable. | FR-16, FR-44, CONS-02 |
| TR-10 | Restart/crash or manual restore | Recover coherent analysis/run | Last successful checkpoint or valid backup with required run inputs | Coherent restored state | Saving/unsaved previews may be lost; saved work survives; do not silently merge conflicting edits. | FR-44, FR-55, CONS-15, OPS-03 |
| TR-11 | One/two charts with interval sync on/off | Select supported interval or change arrangement | At most two charts and supported interval | Independent selections or synchronized interval | One sync action, no repeated propagation; saved configuration restores. | FR-07, FR-17, CONS-03 |

### 5.3 Replay and retained trading history

**Current-state semantics:** Inactive workspace, positioned/paused, playing, coverage limit and blocked trading are behavioral distinctions. A blocked event carries a reason and historical point; play/pause alone cannot resolve it. Cursor and processed-event/action ordering together establish the decision boundary.  
**Terminal conditions:** Coverage limit is not run deletion or forced position liquidation. Exiting replay retains the run. No mandatory completed-run state or rule requiring closure of all positions is supplied.

| ID | Current state/condition | Operation | Required intrinsic condition | Next state/condition | Domain effects / preserved facts | Source requirement(s) |
| --- | --- | --- | --- | --- | --- | --- |
| TR-12 | Replay inactive or new exercise requested | Position/start historical run | Selected usable start and retained inputs/settings | Positioned at historical boundary | Separate latest-history view; all replay panels adopt the boundary. | FR-19–FR-20, FR-45 |
| TR-13 | Positioned/paused/playing, not blocked | Play, pause, change speed, step/advance | Completed eligible next evidence; existing-order evaluation precedes new decisions | Advanced coherent cursor/outputs or paused | No future values; event order independent of playback/redraw rate. | FR-19–FR-20, FR-40, FR-53, CONS-05, CONS-10 |
| TR-14 | Advancing toward unusable/unexplained interval | Stop before unknown execution | Continuity cannot be established; backfill cannot resolve expected-session gap | Paused with gap/session reason | Preserve last coherent trading state; no execution using a later observation across the gap. | FR-42, FR-46, FR-51 |
| TR-15 | Execution requires unavailable historical conversion/specification | Hold affected execution | Required evidence absent/invalid | Blocked/uncommitted original event | No fill, fee or partial position/account effect; retain reason and event context. | FR-42, FR-50, CONS-14 |
| TR-16 | Blocked original event | Resume after resolving prerequisite | Required valid historical evidence/specification available; continuity established; retained run basis coherent | Original event eligible for coherent evaluation | Use original historical point, once; do not reprice at later receipt/cursor time or silently revise prior outcomes. | FR-42, FR-46, FR-50, CONS-14–CONS-15 |
| TR-17 | Active run, earlier target requested | Confirm or cancel rewind | Confirmation for destructive change; earlier usable target | Earlier coherent run, or unchanged original | Remove later submissions/modifications/cancellations/manual closes; recompute dependent history; retain earlier actions and all drawings. | FR-21, BR-17, CONS-13 |
| TR-18 | Active run, forward seek or restart requested | Seek under replay rules or explicitly restart | Forward movement respects event processing/gaps; updated-data restart is deliberate | Coherent sought/restarted exercise | Forward seek cannot bypass orders; explicit updated-data restart may select new inputs; no automatic branch required. | FR-19, FR-21, FR-45–FR-46, CONS-10 |
| TR-19 | Last usable evidence exhausted | Reach coverage limit | No further usable evidence in selected run inputs | Paused/coverage limit | Do not fabricate bars, fills or closure; an in-memory boundary alone is not coverage exhaustion. | FR-06, FR-19, FR-52 |
| TR-20 | Active replay or retained run | Exit replay or resume retained run | Existing saved exercise for resume | Current-history workspace or saved historical point | Exit does not destroy run; resume restores original inputs, orders, settings and results. | FR-22, FR-44–FR-45, CONS-15 |

TR-16 does not grant general authority to mix newer catalog history into a saved run. Completion of a previously uncommitted prerequisite must preserve already committed evidence/outcomes; otherwise deliberate updated-data restart remains the authorized route. The exact evidence-retention mechanism remains downstream. [FR-42, FR-45, CONS-14–CONS-15]

### 5.4 Orders, triggers and executions

**Current-state semantics:** Draft instruction, accepted instruction waiting for its eligible event, eligible pending order, stop-triggered market instruction, cancelled order, rejected request and filled order are distinct facts/conditions. Eligibility is derived from retained decision/event order. Rejection of an invalid modification does not reject or erase the previously valid order.  
**Terminal conditions:** Filled/cancelled orders do not execute again along forward history. A rejected draft has no fill; a corrected submission is a new accepted decision, not a retroactive fill. No liquidity partial-fill state is introduced.

| ID | Current state/condition | Operation | Required intrinsic condition | Next state/condition | Domain effects / preserved facts | Source requirement(s) |
| --- | --- | --- | --- | --- | --- | --- |
| TR-21 | Draft Market/Limit/Stop entry or targeted close | Accept or reject request | Valid quantity/specification and applicable instructions; closure targets remaining exposure | Accepted waiting instruction, invalid request, or blocked prerequisite | Record decision boundary; no execution from processed events. Risk mode additionally needs PRE-05. | FR-27, FR-38–FR-40, FR-49–FR-54 |
| TR-22 | Accepted waiting instruction | Establish eligibility | Next qualifying event after its effective decision boundary | Eligible pending/market instruction | New decision cannot reuse already processed close/intrabar evidence. | FR-40, FR-53, BR-11 |
| TR-23 | Eligible unfilled order/protection | Modify or cancel | Still unfilled/uncancelled when decision accepted; valid replacement terms | Revised instruction effective after decision, or cancelled | Previously evaluated fills remain; rejected modification preserves valid prior terms; cancellation cannot undo a past execution. | FR-27, FR-40, BR-12, CONS-12 |
| TR-24 | Eligible stop entry | Establish stop trigger | Eligible executable-side trigger evidence after effectiveness | Triggered market instruction | Preserve trigger fact; next eligible executable side pricing, including gaps, governs fill; no extra delay model. | FR-40–FR-41, FR-53 |
| TR-25 | Eligible market/triggered stop/limit/protective exit | Execute requested quantity | Valid price/evidence under POL-03–POL-08, complete USD meaning and no unresolved gap | Filled instruction and coherent execution | Full requested quantity under ASM-02; create/reduce only intended position, apply commission/account effects once; record evidence/assumptions. | FR-37–FR-42, FR-47–FR-48, CONS-07 |
| TR-26 | Eligible SL and TP with unresolved chronology | Resolve protective event | Finer stored bars then local ticks cannot order exits; position/eligibility and price evidence otherwise valid | Stop-first labelled result, then TR-25 if executable | ASM-01 selects ordering only; no invented entry/stop price, override of observed TP-first, or gap bypass. | FR-23, FR-37, BR-10–BR-13, ASM-01 |

Manual close requests and order modifications are decisions governed by the same after-decision effectiveness rule. Draft cancellation creates no order execution; accepted-order cancellation is retained trading history. [FR-38, FR-40, BR-17]

### 5.5 Independent positions, protection and account conditions

**Current-state semantics:** Open exposure has positive remaining quantity. Partial reduction is both a quantity condition and historical close fact; it need not be an additional status. Closed means zero remaining quantity. Account balance is derived from initial USD cash and coherent execution effects; nonpositive balance disables percentage-risk sizing without introducing margin liquidation.  
**Terminal conditions:** A fully closed position cannot be further reduced in forward history; an opposite entry creates another position. Rewind that removes a later exit reconstructs the earlier open position.

| ID | Current state/condition | Operation | Required intrinsic condition | Next state/condition | Domain effects / preserved facts | Source requirement(s) |
| --- | --- | --- | --- | --- | --- | --- |
| TR-27 | Accepted entry, no position yet for that entry | Apply entry execution | TR-25 satisfied | Independent open position | Other same/opposite positions unchanged; optional protection belongs to new position only after entry. | FR-38, BR-12, BR-14 |
| TR-28 | Open position | Execute manual partial close | Positive valid closing quantity below remaining quantity, original event eligible | Reduced open position | Realize targeted portion, apply exit commission, resize protection to remaining quantity. | FR-38, FR-41, FR-48, FR-54 |
| TR-29 | Open/reduced position | Execute full manual/protective close | Valid closing execution equals remaining quantity | Closed position, no remaining active protection | Realize remainder and exit commission once; cancel other protection. | FR-38, FR-54, CONS-12 |
| TR-30 | Coherent account at any balance | Apply coherent execution outcome | Complete valuation/conversion/fees | Revised balance/history and position/protection | No independent fee/fill application; no margin call/forced liquidation; risk mode unavailable if balance nonpositive. | FR-39, FR-41–FR-42, FR-54, CONS-07 |

## 6. Invariants

| ID | Invariant | Why violation is invalid | Applies to | Source requirement(s) |
| --- | --- | --- | --- | --- |
| INV-01 | Display/calculation instrument, timeframe, side and revision agree with their actual selected evidence. | Otherwise another instrument/basis is falsely presented. | Analysis, reports, simulation | BR-01, BR-05, CONS-01 |
| INV-02 | Bar selections use exactly the eight accepted periods and supplied UTC boundaries; bid/ask remain separate. | Unsupported periods, shifted buckets or mixed sides change observation meaning. | History, aggregation, charts | FR-04, FR-07, FR-33, BR-02–BR-03 |
| INV-03 | Replay values and executions use no observations beyond their historical information boundary or already processed events as if new. | Such results contain future knowledge or retroactive execution. | All replay panels/decisions | FR-20, FR-40, FR-53, CONS-10 |
| INV-04 | A saved run's committed results and selected original inputs/conventions are coherent and remain unchanged by catalog updates/resume. | Mixing revisions invalidates reproducibility. Explicit rewind/restart follow their own transitions. | Saved run | FR-45, FR-50, DATA-18, CONS-15–CONS-16 |
| INV-05 | Every committed execution has matching quantity, position/protection, fee and fully valued USD effects exactly once. | An orphan, duplicate or unvalued fill contradicts the account/exposure history. | Execution and account | FR-42, CONS-07, CONS-12, CONS-14 |
| INV-06 | For each position, remaining quantity equals its entry quantity less its targeted executed closures, never negative. | Opposite entries cannot consume it; over-closure creates unauthorized exposure. | Position | FR-38, BR-14 |
| INV-07 | Active protection belongs to an entered, open position and covers no more than its remaining quantity; full closure leaves none active. | Exits before entry or after closure create impossible exposure. | SL/TP and position | FR-38, FR-54, BR-12 |
| INV-08 | Buy limit/TP fill price is no higher than its limit; sell limit/TP fill price is no lower. | Worse execution violates the limit promise; stop instructions have no such guarantee. | Limit executions | FR-47, BR-21 |
| INV-09 | Accounting currency is USD; instrument currencies/unit meaning are preserved and required conversion is historical and applicable. | Relabelling or fabricated/future conversion produces false money. | Account/results/sizing | FR-39, FR-42, FR-50, BR-18 |
| INV-10 | Resolution evidence and accepted assumption labels remain attributable to the outcome. | A policy approximation cannot become a claimed observed sequence/liquidity fill after restore/export. | Executions/results | FR-29, FR-37, FR-48, ASM-01–ASM-02 |
| INV-11 | Current coverage claims contain only established usable observations/known closures; unresolved intervals remain explicit. | Apparent continuous history would authorize fabricated traversal. | Catalog/recovery | FR-46, FR-51–FR-52, CONS-08 |
| INV-12 | Durably saved state denotes a coherent successfully retained version; saved replay cursor/actions/positions/account/settings agree. | A success label without recoverable corresponding facts is false. | Analysis/run checkpoints | FR-44, CONS-02, CONS-15 |
| INV-13 | Drawing anchors retain their layout/instrument scope across timeframe changes, navigation and trading rewind. | Trading history does not own independent authored annotations. | Committed drawing | FR-14, FR-21 |
| INV-14 | Eligible requested executions fill their requested quantity under the declared full-fill assumption. | Unrequested liquidity partials introduce an excluded execution model. | Entry/exit execution | FR-48, ASM-02 |

## 7. Transition preconditions

| ID | Operation | Precondition | Why required | Related invariant/policy | Source requirement(s) |
| --- | --- | --- | --- | --- | --- |
| PRE-01 | Adopt chart selection | Requested tuple and usable loaded evidence match; period supported. | Protect last valid chart from failed/late selection. | INV-01–INV-02 | FR-02–FR-04, CONS-01 |
| PRE-02 | Advance/seek/evaluate trading event | Valid completed bar/valid tick, eligible event order and no unresolved intervening gap/session uncertainty. | Readability or producer COMPLETE alone is insufficient. | INV-03, INV-11; POL-02–POL-04 | FR-42, FR-46, FR-51, FR-53 |
| PRE-03 | Execute instruction | Instruction effective before relevant unprocessed event; usable side/price evidence and quantity/specification available. | Avoid retroactivity, wrong side and invented fills. | INV-03, INV-05; POL-04–POL-05 | FR-40, FR-47–FR-50, FR-53 |
| PRE-04 | Commit monetary outcome/resume blocked event | Required historical USD conversion and session applicability established at the original event. | A blocked fill cannot become partly committed or move to a later price. | INV-05, INV-09; POL-07 | FR-42, CONS-14 |
| PRE-05 | Accept percentage-risk size | Positive balance; valid SL and monetary specification/conversion/commission; permitted size within budget and at least minimum. | Planned loss cannot be computed from absent values or nonpositive balance. | POL-06–POL-08 | FR-39, FR-49, FR-54 |
| PRE-06 | Accept fixed quantity or close quantity | Valid permitted quantity/increment; close additionally targets an open position and does not exceed remainder. | Quantity validity is independent of margin; fixed mode needs no invented solvency rule. | INV-06–INV-07; POL-08 | FR-38, FR-50, FR-54 |
| PRE-07 | Apply stop-first | Eligible exits of an entered position; unresolved ordering after finer bars then available local ticks; no known TP-first or gap block. | ASM-01 only resolves a limited ordering ambiguity. | INV-10; POL-03–POL-05 | FR-23, FR-37, BR-10–BR-12 |
| PRE-08 | Modify/cancel accepted order | Still pending at decision point; changed terms valid and effective after that point. | Processed fills cannot be undone by a later request. | INV-03; POL-04 | FR-40, FR-53, CONS-12 |
| PRE-09 | Commit authored edit | Valid supported parameters/anchors; cancelled preview excluded. | Preserve prior valid analysis on invalid input/cancel. | INV-12–INV-13 | FR-10, FR-12, FR-14–FR-16 |
| PRE-10 | Restore backup/resume saved run | Required retained input versions/settings and internally coherent state available. | Mutable file paths or conflicting edits cannot prove reproducibility. | INV-04, INV-12; POL-09–POL-11 | FR-44–FR-45, FR-55 |

Confirmation and write authority for destructive changes are POL-11, not intrinsic lifecycle preconditions. Text parseability/file-format validation is input validation (SEC-02), not an invariant that an order remains permanently draft or rejected. Quantity increments, limit bounds and unit validity carry business meaning and are modeled separately. Performance thresholds in SCALE-03 are quality constraints, not perpetual domain-state invariants.

## 8. Authorization and business-policy distinctions

| Policy ID | Decision | Knowledge required | Domain lifecycle rule kept separate | Consumers | Source requirement(s) |
| --- | --- | --- | --- | --- | --- |
| POL-11 | May this local action alter, discard or restore work? | Sole analyst's mutation authority, one writable tab, confirmation for deletion/reset/rewind; application-owned versus sibling inputs. | Correct prior state, permitted quantity and rewind recomputation remain intrinsic rules. Confirmation alone cannot legalize invalid execution. | Authored edits, trading actions, rewind, deletion/reset, backup/restore, acquisition retention | AUTH-01–AUTH-03, FR-21, FR-55, DATA-08, DATA-16, CONS-06 |
| POL-12 | Does provider access authorize this effect? | Live-account market-data purpose only; no actual order or real-balance authority. | Simulated order eligibility and USD accounting are independent of account entitlements. | Live/history use and all simulation actions | FR-31, BR-06, SEC-03, SEC-07 |

No approver hierarchy, subscription entitlement, tenant role or real broker execution permission is invented. Protected credentials and untrusted imported labels cannot grant domain authority; backups/reports exclude credentials. [AUTH-01–AUTH-03, SEC-02–SEC-04]

## 9. Invalid states

| Invalid state / fact combination | Violated rule | Why contradictory | Prevention/detection responsibility at semantic level |
| --- | --- | --- | --- |
| Chart says SP500/bid/H1 but contains another subject/ask/revision. | INV-01, PRE-01 | Labels and evidence disagree. | Chart-selection adoption and result provenance |
| Replay cursor is midweek; study/watchlist uses that week's final high/close or a live quote. | INV-03 | Later knowledge is exposed. | Historical availability policy across every consumer |
| New market/modified order fills on the just-processed visible close. | INV-03, PRE-03, POL-04 | Effect precedes accepted decision. | Effective-order/event ordering |
| COMPLETE producer flag plus unreadable interval is reported as continuous tradeable coverage. | INV-11, PRE-02 | Producer assertion is not validation. | Coverage/eligibility assessment |
| Empty/weekend interval is called a known closure without session evidence. | POL-02, INV-11 | Missing observations cannot establish non-trading. | Session/gap classification |
| Conversion paused; fill exists but fee/USD/position effect is absent. | INV-05, INV-09 | Partial execution outcome has no coherent monetary meaning. | Complete-execution acceptance |
| Blocked event resumes at today's/newer market price. | PRE-04, TR-16 | It becomes a different historical event. | Blocked-event context and resumption |
| Saved run results use old bars but newly arrived ticks/specification/fee convention. | INV-04 | Mixed evidence rewrites selected history. | Retained run basis |
| Opposite entry reduces an existing position. | INV-06, REL-08 | Hedging was selected; entry is not a targeted close. | Position identity and closure semantics |
| Closed position has active SL/TP, negative remainder or another executed close. | INV-06–INV-07 | Exits exceed or outlive exposure. | Position/protection transitions |
| Buy limit fills above limit or sell TP below limit. | INV-08 | Bound violated; applying stop pricing to a limit is invalid. | Execution-pricing policy |
| Both exits unordered; ASM-01 invents an entry, stop-level quote or fills across an unresolved data gap. | PRE-07, POL-03–POL-05 | Ordering fallback cannot supply other prerequisites. | Intrabar resolution and pricing |
| Risk-sized quantity rounded above planned budget, or risk sizing accepted with nonpositive balance. | PRE-05, POL-08 | It is not the agreed sizing decision. Actual later gap loss may still exceed budget. | Planned-risk sizing |
| One request has an automatic liquidity partial fill without an explicit smaller manual close request. | INV-14 | Excluded queue/liquidity model introduced. | Full-request execution assumption |
| Confirmed rewind removes exit action but retains its commission/closed state. | CONS-13, TR-17, INV-05 | Trading facts do not describe the retained history. | Run reconstruction |
| Cancelled rewind changes cursor, or trading rewind deletes annotations. | TR-17, INV-13 | Confirmation/scope semantics violated. | Rewind policy and drawing ownership |
| Saving failed but the changed state is labelled saved, or restore loses successfully saved matching orders. | INV-12 | Durability claim lacks coherent evidence. | Checkpoint/recovery semantics |
| 100k loaded bars are exhausted and older available history is called unavailable. | FR-52, TR-19 | Resident benchmark is falsely treated as archive bounds. | Coverage/navigation semantics |

## 10. Historical facts

| ID | Historical fact | Created by | Preserved through | Relationship to current state | Source requirement(s) |
| --- | --- | --- | --- | --- | --- |
| HIST-01 | Selected observation values, original precision, revision/origin and lineage | Discovery/acquisition and input selection | Save/resume/backup and later catalog corrections | Current latest value may differ; saved run evidence does not automatically change. | FR-35, FR-45, DATA-07–DATA-08, DATA-18 |
| HIST-02 | Provider status and validation/coverage evidence | Input assessment | Retained provenance needed for selected results | IN_PROGRESS/COMPLETE describes producer evidence, not the current tradeable state by itself. | FR-51, BR-04, DATA-06 |
| HIST-03 | User decision and its effective event boundary/terms | Accepted submit/modify/cancel/manual-close action | Forward run continuation, autosave/restore | An old accepted request may now be filled/cancelled; its terms are not current pending quantity. | FR-40, FR-44, FR-53 |
| HIST-04 | Stop trigger, execution price/quantity and resolution evidence/assumption | Trigger/evaluate/fill transitions | Run save/resume, report and backup | Trigger does not by itself establish fill; closed position does not erase its entry/exit evidence. | FR-29, FR-37, FR-41, FR-48 |
| HIST-05 | Selected conversion evidence, contract/cost conventions and coherent USD effects | Complete execution | Run continuation/resume despite new metadata | Current rate/settings cannot reinterpret an already valued result. | FR-41–FR-42, FR-45, FR-50 |
| HIST-06 | Entry quantity and each targeted executed reduction | Entry/close execution | Partial/full closure and run recovery | Remaining quantity is derived; an earlier partial close is not the current position state. | FR-38, CONS-12 |
| HIST-07 | Successfully retained coherent analysis/run checkpoint | Successful autosave | Crash/restart and later failed save attempts | Current edits may be newer/unsaved; last success is still recoverable. No indefinite checkpoint archive required. | FR-44, CONS-02, OPS-03 |
| HIST-08 | Original blocked-event context, missing prerequisite and explanatory reason | Holding affected event | Prerequisite resolution until coherent resumption | Block is a current impediment; it is not a rejected market order or completed zero-profit fill. No indefinite diagnostic history is mandated. | FR-42, FR-50, CONS-14 |

Preservation is explicitly scoped. Confirmed rewind discards later trading actions **and their dependent execution/fee/account facts from the active run** and reconstructs the retained prefix. No permanent audit copy or automatic branch of discarded trading history is required. Retained earlier facts keep their selected input basis; drawings are not part of this deletion. Deliberate reset/deletion or updated-data restart may replace the exercise under POL-11. Ordinary catalog corrections, closing a position, exiting replay and reopening the run cannot erase/rewrite its evidence. [FR-21–FR-22, FR-45, FR-55, BR-17, CONS-13]

## 11. Business operations

| ID | Operation | Semantic owner | Important intrinsic rules | Separate policy/context needed | Resulting domain effect | Source requirement(s) |
| --- | --- | --- | --- | --- | --- | --- |
| OP-01 | Establish usable history and actual bounds | Coverage | Distinguish validation, gaps and producer assertions; preserve originals. | POL-01–POL-02, POL-11 | Qualified selection with actual limitations. | FR-01–FR-02, FR-51–FR-52 |
| OP-02 | Extend/reconcile current historical evidence | Current catalog | M1/H1 acquisition basis, supplied UTC derivatives, affected boundaries only, no duplicates. | POL-01–POL-02, POL-09, POL-12 | Retained current coverage extended/finalized without rewriting runs. | FR-32–FR-35, FR-43, CONS-09 |
| OP-03 | Choose chart analysis basis and synchronize interval | Chart selection/layout | Match displayed evidence; at most two charts, supported interval. | POL-01, POL-03 | Coherent independent/synchronized selection. | FR-03–FR-07, FR-17 |
| OP-04 | Configure studies and interpret derived values | Study instance/calculation convention | Declared inputs/warm-up/missing handling; invalid change retains valid configuration. | POL-01, POL-03, POL-10 | Meaningful derived outputs and persisted authored choices. | FR-08, FR-11–FR-12 |
| OP-05 | Commit/edit/cancel/reverse annotation or presentation | Authored analysis | Preserve financial anchors, scope and valid previous state; no duplicate redo. | POL-11, applicable tool bounds | Committed analysis or no preview effect. | FR-10, FR-13–FR-16 |
| OP-06 | Position, advance or seek replay | Run's historical decision boundary | Completed evidence, existing orders before new decisions; no future data. | POL-02–POL-05 | Consistent cursor, panels and evaluated orders. | FR-19–FR-20, FR-53 |
| OP-07 | Submit/modify/cancel historical instruction | Order | Quantity/terms valid; after-decision effectiveness; no retroactive cancellation. | POL-04–POL-08, POL-11–POL-12 | Accepted revised instruction, cancellation, invalid request or explained block. | FR-27, FR-40, FR-49–FR-54 |
| OP-08 | Determine permitted planned quantity | Sizing decision | Largest valid quantity within planned USD risk including fees, or valid fixed amount. | POL-06–POL-08 | Quantity/planned risk or specific invalid/missing-input outcome. | FR-39, FR-49, FR-54 |
| OP-09 | Resolve and execute eligible historical instruction | Execution outcome | Finer bars then local ticks as needed; complete valuation; requested full fill. | POL-02–POL-07; ASM-01–ASM-02 | Coherent labelled fill/position/account effects or no committed fill. | FR-23, FR-37, FR-41–FR-42, FR-47–FR-48 |
| OP-10 | Reduce selected exposure partially/fully | Hedged position | Reduce only target; resize/cancel protection, charge exit fee. | POL-04–POL-07, POL-11 | Remaining exposure and USD result agree. | FR-38, FR-41, FR-54 |
| OP-11 | Resolve blocked historical event | Original event context | Establish missing prerequisite at original point; preserve prior committed outcomes. | POL-02, POL-07, POL-09 | Original event can proceed coherently once. | FR-42, FR-46, CONS-14 |
| OP-12 | Rewind retained exercise or restart deliberately | Run | Recompute retained prefix; drawings independent; explicit updated-data restart. | POL-09, POL-11 | Coherent earlier/restarted run or unchanged cancelled request. | FR-21, FR-45, CONS-13 |
| OP-13 | Retain, resume or restore coherent authored work/run | Durable checkpoint/backup | Retain required original run inputs, matching cursor/orders/settings; exclude previews/credentials. | POL-09–POL-11 | Recoverable state with truthful durability. | FR-16, FR-22, FR-44–FR-45, FR-55 |
| OP-14 | Present/export analysis image or own-run results | Selected analysis/result | Identify basis, policy, units/currency and approximations; replay disclosure limit applies. | POL-01, POL-03, POL-10–POL-12 | Local image/report; no hosted publication or external-run importer implied. | FR-18, FR-20, FR-29–FR-30, SEC-04 |

## 12. Shared policies

These policies describe independently meaningful domain knowledge. Multiple consumers do not imply common software ownership or a proposed module.

| Policy ID | Rule/concept described | Legitimate consumers | Duplication risk | Conceptual owner | Source requirement(s) |
| --- | --- | --- | --- | --- | --- |
| POL-01 | Provider/basis/time semantics: explicit instrument/side/timeframe/revision, UTC buckets, source precision, no invented midpoint or provider substitution. | Discovery, selection, aggregates, studies, data window, reports, simulation | Same number appears to mean different instrument/time/side. | Market observation meaning | FR-04, FR-07, BR-01–BR-05, DATA-07 |
| POL-02 | Usability and session continuity: validated evidence; preserve otherwise valid zero-volume/weekend rows; known closure needs evidence, unexplained gaps block trading. | Coverage discovery, recovery, replay advancement, pricing, conversion applicability | A workflow bypasses gap pause or treats producer flag/silence as closure. | Coverage and instrument/session evidence | FR-42, FR-46, FR-51–FR-52, BR-04, BR-09, BR-20 |
| POL-03 | Historical availability and evidence resolution: common cursor, period availability, finer stored bars before needed local ticks; label unresolved eligible protective order as ASM-01. | Charts, studies, watchlists/details, data window, order resolution, replay reports | Future leakage or a tick-only/SP500-only path; fallback masquerades as observation. | Historical information boundary / resolution evidence | FR-20, FR-23, FR-37, BR-07, BR-10, DATA-17 |
| POL-04 | Decision effectiveness: evaluate existing eligible orders before new decisions, never reuse processed evidence; stop trigger becomes market instruction. | Replay play/step/seek, submissions, modifications, cancellations, close requests, restore/re-evaluation | Different speed or workflow changes fills or cancels history retroactively. | Run decision/event ordering | FR-40, FR-53, BR-11–BR-12, CONS-10 |
| POL-05 | Executable side and price: buy ask/sell bid; next eligible market evidence or next side-specific bar open; gap SL first executable side, limits/TP at limit or better with better first eligible gap quote honored. No extra slippage/delay. | Entry, stop trigger, SL/TP, manual closure, planned execution explanation | Chart side changes execution, SL given limit guarantee, worse limit price, invented ticks. | Execution-pricing meaning | FR-04, FR-40–FR-41, FR-47, BR-13, BR-16, BR-21 |
| POL-06 | Instrument monetary meaning and execution charges: selected editable specs; fixed USD/execution, USD/unit or percent USD notional; zero default, entry/exit charges. | Sizing, entries/exits/partial closure, notional and USD reporting | Inconsistent multipliers or charge once per position instead of execution. | Instrument specification and selected commission convention | FR-41, FR-49–FR-50, BR-06 |
| POL-07 | Historical USD valuation: currency/direction/applicability and nonfuture evidence; missing required inputs hold original event without partial effects. | Sizing, commissions requiring notional conversion, realized results, account/reports, blocked-event resumption | Current or stale substituted rate, false USD amount or repriced resumption. | Historical monetary conversion | FR-42, BR-18, CONS-14 |
| POL-08 | Permitted quantities and planned risk: instrument increment/minimum; targeted closes bounded by remainder; positive-balance risk sizing includes fees and rounds down. | Entry acceptance, fixed/risk sizing, order changes, partial/full closure/protection | Rounding differs by workflow or invalid close becomes opposite exposure. | Quantity validity / planned-risk budget | FR-38–FR-39, FR-49–FR-50, FR-54, BR-22 |
| POL-09 | Selected-run continuity versus current history: freeze original inputs/conventions/results; confirmed rewind changes retained history, deliberate updated-data restart changes basis. | Catalog finalization, run resume/re-evaluation, rewind/restart, backup/restore | New evidence silently changes an old result or removed exit persists. | Trading run evidence continuity | FR-21–FR-22, FR-35, FR-45, DATA-18, CONS-13–CONS-16 |
| POL-10 | Declared calculation/rounding and evidence labels: no invented zero/warm-up output, deterministic numerical conventions, full-fill/bar-touch ASM-02 and stop-first ASM-01 identified. | Studies, sizing, fills/fees, re-evaluation, data window/reports/export | Consumer-specific rounding, approximations presented as broker facts. | Calculation/result interpretation | FR-08, FR-11, FR-29, FR-37, FR-41, FR-48, FR-54, ASM-01–ASM-02 |
| POL-11 | Local authorship, destructive-action authority and durability claims. | See Section 8; analysis/run autosave and recovery | A second writer overwrites work, failed save claimed durable, source files edited. | Analyst-owned work and recovery authority | FR-44, FR-55, AUTH-02, CONS-02, CONS-06 |
| POL-12 | Data access is not brokerage/credential export authority. | Live/history use, simulation, backup/report/image export | Real cash/order effects or leaked secrets through simulated workflows. | Market-data access purpose | SEC-03–SEC-04, SEC-07 |

POL-03 establishes which evidence can settle ordering; POL-04 establishes instruction effectiveness; POL-05 establishes executable pricing. None subsumes the others. Full-fill ASM-02 changes the requested-quantity outcome, not chronology, eligibility, gap handling or available quote evidence.

## 13. Rule ownership map

```text
Instrument and market observation meaning (POL-01, POL-06)
  owns knowledge of: provider identity, quote/UTC basis, selected unit and contract meaning
  consumed by: coverage, chart selection, calculation, sizing, execution and reports

Coverage and session evidence (POL-02)
  owns knowledge of: usable intervals, actual bounds, established closures and unexplained gaps
  consumed by: discovery, recovery, replay, execution and historical conversion

Historical information boundary (POL-03)
  owns knowledge of: cursor-available facts, period completion, evidence versus ordering approximation
  consumed by: every replay panel, calculation and intrabar outcome resolution

Run decision/event ordering (POL-04)
  owns knowledge of: processed events, instruction effectiveness and existing-before-new decisions
  consumed by: submissions/changes/closes, play/step/seek and coherent reconstruction

Execution outcome (POL-05 through POL-08, POL-10)
  owns knowledge of: requested quantity, executable side/price, fee and historical USD effects
  consumed by: entry, protection, manual closure, account and result interpretation

Independent position (REL-08/REL-09, INV-06/INV-07)
  owns knowledge of: entry exposure, targeted reductions, remaining protection and closure
  consumed by: close requests, protective execution, account reconciliation and rewind

Trading run evidence continuity (POL-09)
  owns knowledge of: retained input/policy basis, actions/outcomes, permitted rewind/restart changes
  consumed by: resume, catalog correction, results and backup/restore

Authored analysis and durable work (POL-11)
  owns knowledge of: layout/instrument drawing scope, valid edits and coherent saved-version claims
  consumed by: chart editing, autosave/recovery, destructive actions and backup/restore

Market-data purpose (POL-12)
  owns knowledge of: data-only account access, absence of real-order/cash authority
  consumed by: live/history access, simulation and export/backup
```

These are semantic ownership statements, not architectural boundaries, dependencies or proposed classes.

## 14. Assumptions and conditional semantics

| Assumption | Affected model elements | Consequence if false |
| --- | --- | --- |
| ASM-01 — user accepted U4: unresolved eligible SL/TP ordering after usable finer stored bars and local ticks uses labelled stop-first. | TR-26, PRE-07, INV-10, HIST-04, POL-03/POL-10, OP-09 | Actual sequence may have reached TP first. Retained result remains a policy approximation; no claim to recover missing chronology, entry or stop price. |
| ASM-02 — user accepted U11: eligible requests fill fully without liquidity/queue partials; eligible bar-limit touches use limit price unless a better first-eligible gap quote is established. | TR-25, TR-28, INV-08/INV-10/INV-14, HIST-04, POL-05/POL-10, OP-09/OP-10 | Actual broker may fill less, later or not at all. Results remain labelled simplified simulation; explicit manual partial closure remains supported. |

Neither assumption overrides valid observed order, instruction eligibility, instrument/quantity validity, conversion prerequisites, historical cursor or unresolved-gap pauses. No fixed-M1 execution baseline, guaranteed zero price movement, market-volume semantics or broker liquidity assumption is added.

## 15. Ambiguities and domain-model gaps

No blocking identity, lifecycle, invariant or ownership gap was found against revision 14. The following refinements/evidence obligations remain visible; they do not silently acquire invented answers. IMPORTANT means necessary before accepting affected behavior, not an unresolved product-scope blocker.

| ID | Gap/ambiguity | Affected semantics | Severity | Required upstream clarification / owner |
| --- | --- | --- | --- | --- |
| DM-GAP-01 | Exact live-account API/access and per-asset entitlement unverified (UNK-19). | TR-05, POL-12; ability to receive required live observations | IMPORTANT, integration evidence | Verify access before live acceptance; failed access preserves historical mode, without demo substitution or waiving required live capability. No new product decision assumed. |
| DM-GAP-02 | Per-instrument sessions, conversion applicability and history publication/finality evidence unverified (UNK-20). | TR-02/TR-03/TR-14/TR-16, POL-02/POL-07 | IMPORTANT, integration evidence | Establish authoritative session/finality/applicability facts before enabling affected traversal/finalization; otherwise remain unresolved/blocked. |
| DM-GAP-03 | Precise study initialization/formulas/input bounds, drawing parameters and export/range details remain UNK-04. | DC-11/DC-12, TR-07, POL-10 | IMPORTANT for affected realization, non-blocking for boundary design | Declare calculation conventions and valid tool parameters within accepted subset before implementation; do not assume TradingView parity or introduce extra periods. |
| DM-GAP-04 | Deterministic USD/notional/quantity rounding details and instrument-specific numerical valuation conventions must be documented; no numeric precision or unverified contract value selected here. | PRE-04–PRE-06, POL-06–POL-08/POL-10 | IMPORTANT for affected realization, delegated by FR-41/FR-50/FR-54 and requirements quality gate | Document numerical rules and retain selected conventions; source/validate instrument values with identified overrides. Missing required values block trading. A contradiction to accepted risk/limit bounds returns upstream. |
| DM-GAP-05 | Exact undo depth/commands, defaults, visual realization and optional expanded watchlists/templates remain UNK-01/UNK-02/UNK-03/UNK-05. | TR-08/TR-11, authored analysis | OPTIONAL domain refinement / downstream UI | Settle bounded interaction defaults and accepted parameters; no expansion of scope or new ownership model inferred. |

Source volume units remain unverified (requirements terminology/DATA-09); present them as provider-supplied units without claims about exchange execution or liquidity. This is a limitation of evidence, not permission to invent volume meaning. Stable IDs referring to earlier UNK items in historical dossier prose follow the final Section 19 resolution register; for example UNK-14/UNK-16 are resolved, not newly reopened here.

## 16. Domain-model challenge findings

| Finding | Evidence | Resolution/status |
| --- | --- | --- |
| One “complete” flag would confuse elapsed period, usable coverage and provider finality. | FR-20/FR-35/FR-51; DATA-04/DATA-06 | Corrected: orthogonal conditions in DC-09 and Section 5.1; opening labels cannot reveal completed higher-period values early. |
| Stop-first can incorrectly become an entry/path/price invention. | BR-10–BR-13, ASM-01 | Corrected: PRE-07 and TR-26 limit it to eligible protective chronology; POL-05 separately determines price. |
| Next-price execution across unknown data can bypass a mandatory pause. | FR-40 versus FR-46, BR-20 | Corrected: PRE-02/PRE-03 require continuity first; established closure alone permits normal gap traversal. |
| “USD account” can hide missing conversion and partial fill/account updates. | FR-42, BR-18, CONS-14 | Corrected: TR-15/TR-16 and INV-05/INV-09 hold the entire original event until valued, without inventing a rate. |
| Immutable history can accidentally forbid required rewind; rewind can accidentally preserve orphaned exits. | FR-21/FR-45, BR-17, CONS-13 | Corrected: preserve against catalog changes; deliberately discard later active-run facts and recompute the retained prefix. No extra audit retention/branch invented. |
| Resolving a blocked prerequisite can be mistaken for general saved-run input replacement. | FR-42/FR-45, CONS-14–CONS-15 | Clarified after TR-16: uncommitted prerequisite completion preserves prior basis/outcomes; changed-data re-evaluation requires deliberate restart. Mechanism deferred. |
| Position lifecycle can be conflated with a measurement drawing or opposite order. | FR-13–FR-14/FR-38, BR-14 | Corrected: separate identities/ownership; targeted reductions only, drawings survive trading rewind. |
| Manual partial close can be misread as liquidity partial fill. | FR-48, ASM-02 | Corrected: full fill of each requested quantity; protection and fee follow each explicit partial-close execution. |
| A terminal closed/cancelled state can wrongly remain terminal after destructive rewind reconstructs an earlier history. | Requirements Section 8; FR-21 | Clarified: terminal only within forward retained history; reconstructing earlier state is not a new forward reopen transition. |
| The same timestamp may be treated as sufficient evidence/order identity. | DATA-07, FR-40, CONS-10 | Corrected: original precision and established occurrence order are retained; no invented chronology where evidence is insufficient. |
| Resident working set can become a lookback cap; SP500 tick inventory can become a permanent capability gate. | FR-52, DATA-17, EVO-02/EVO-04 | Corrected: coverage derives from actual per-series evidence; full archive remains accessible; ticks are per instrument/span. |
| Broker constraints, automatic liquidation, forced closure at coverage end or external-run ingestion might enter by convention. | BR-15, FR-19/FR-30/FR-54, SEC-07 | Excluded: no supported transition/authority for those additions. No invented run-completion lifecycle. |
| Numerical/tool details could be silently asserted as verified semantics. | Requirements Section 18 and quality gate; FR-11/FR-41/FR-54 | Preserved as DM-GAP-03/DM-GAP-04 with declared-convention obligations; no unapproved formula/precision selected. |
| Semantic owners can turn into speculative implementation boundaries. | Skill scope and requirements quality gate | Reviewed: no modules, schemas, transport shapes, SDK, concurrency mechanism or deployment is selected. File-retention constraints are upstream requirements only. |

### Quality-gate review

| Skill gate | Assessment |
| --- | --- |
| 1. Upstream readiness/traceability | PASS conditionally — full revision 14 read; requirement IDs retained; no source proposal overrides it. |
| 2. Vocabulary | PASS — DC-01–DC-21 distinguish basis, evidence, state, history and decisions. |
| 3. Identity/value | PASS — continuing identity/value equality justified; no storage-derived identities. |
| 4. Relationships/ownership | PASS — REL-01–REL-11; scope/cardinality only where supported; no tenant hierarchy. |
| 5. State model | PASS — TR-01–TR-30 cover legal effects, blocks, recovery and terminal limits; no unsupported completion/liquidation states. |
| 6. State versus history | PASS — HIST-01–HIST-08, explicit catalog-change and destructive-rewind distinctions. |
| 7. Rule classification | PASS — invariants, operation preconditions, authority/policies, input validation and quality constraints separate. |
| 8. Invalid states | PASS — concrete contradictory combinations linked to responsible semantics. |
| 9. Operations | PASS — OP-01–OP-14 describe business effects and owners, not technical mutation. |
| 10. Shared policies | PASS — POL-01–POL-12 identify knowledge, consumers and duplication risks. |
| 11. Architecture leakage | PASS — no unmandated architecture, persistence shape, mechanism or framework choice. |
| 12. Gaps/contradictions | PASS conditionally — ASM-01/ASM-02 preserved; non-blocking refinements and integration evidence obligations explicit; no new blocking contradiction found. |
| 13. Downstream readiness | `READY_WITH_ACCEPTED_ASSUMPTIONS` — conditional on ASM-01/ASM-02, with affected-behavior obligations in Section 15. |

## Handoff note

Ready for boundary design only under named accepted assumptions **ASM-01 and ASM-02**, using requirements revision 14 and this model's semantics/traceability. Preserve evidence-versus-approximation labels, original saved-run inputs, after-decision effectiveness, coherent USD outcomes, closure-versus-gap rules, and independent authored drawings. DM-GAP-01/DM-GAP-02 require provider evidence before live/backfill acceptance; DM-GAP-03–DM-GAP-05 remain scoped downstream refinements under the dossier's delegation. These obligations do not claim that live access, numerical parity or an implementation has been verified.
