# Requirements Dossier — Dukascopy Chart Workspace and Historical Trading

**Convergence status:** `CONVERGED_WITH_ACCEPTED_ASSUMPTIONS`  
**Revision:** 14 — 19 October 2026; requirements interview complete, packages P1/P2/P3 accepted  
**Scope of dossier:** A single-user local TradingView-inspired workspace with historical trading, Dukascopy live data when available, historical gap filling, and exactly eight supported bar timeframes over the ten supplied assets.  
**Evidence reviewed:** The user's request; the complete three source reports below; the feature inventory and anonymous/authenticated evidence registers, network summaries and local-context record; aggregation documentation and code; all current Dukascopy JSON manifests; representative bar Parquet schemas; all tick Parquet footers; and a bounded SP500 September 2026 row inspection.

This is a requirements document, not an implementation or architecture prescription. The source reports combine observations, inferences and proposals. Their proposed stack, interfaces, storage, module boundaries, algorithms and build order are not user-approved constraints. No replica has been implemented by this work.

## 1. Problem statement

Provide a familiar financial-chart analysis workspace over the user's existing historical data, extend it to current Dukascopy prices when a feed is available, and support historical simulated trading. Fill the interval between the last available history and current data through Dukascopy's historical source. Use bid prices by default with ask selectable, and retain exactly M1/M5/M15/H1/H4/D1/W1/MN1. Scripting and alerts are excluded. Reproducing TradingView's captured SPX prices or every visible menu entry is not established as a requirement.

### Evidence and precedence

| Reference | Source | Authority and limitation |
| --- | --- | --- |
| U1 | User request in this conversation | This version uses `../marketDataIngestion/dukascopy/`, ten assets, M1/M5/M15/H1/H4/D1/W1/MN1 and partial SP500 ticks. |
| U2 | User's first interview answers | Include historical trading; exclude scripting and alerts; one local user; Dukascopy live connection when available; automatic historical gap filling from M1/H1; existing stored timeframes only; default bid with ask selectable. |
| U3 | User's second interview answers | Permit backfill to complete affected existing boundary candles; use live-account data; render charts from available historical bar timeframes; reserve ticks for resolving intrabar orders/stops and future tick-dependent analysis; expect tick history for additional assets later. No fixed-M1 execution baseline was accepted. |
| U4 | User's third interview answers | Inspect finer stored bars first, then local ticks if still needed. If available evidence cannot establish stop-loss versus take-profit order, apply a labelled stop-first result. Use local ticks only now; automatic missing-data download and permanent local database updates are future-version work. This defers tick acquisition, not the already-required M1/H1 historical gap filling. |
| U5 | User's fourth interview answers | Include Market/Limit/Stop entries, SL/TP, order modification/cancellation and full/partial manual closure. Opposite entries open independent hedged positions. No margin checks; simulated balance and position sizing are configurable. A stop-loss crossed by a gap fills at the first available executable bid/ask, even when worse than the stop price. Currency, costs, sizing modes and remaining fill rules were not selected. |
| U6 | User's fifth interview answers | New orders/modifications become effective only after the current replay decision point; market orders use the next available bid/ask or next bar open when bar-only. Offer fixed quantity and percentage risk from SL distance. Account currency is fixed USD and cannot be changed; commissions are configurable and default zero. No additional slippage is applied without tick data; optional tick-dependent slippage may be useful but its model is not chosen. Rewind removes subsequent trading actions after confirmation. |
| U7 | User's sixth interview answers | Defer all extra slippage modelling. Confirm per-instrument commission choice among fixed USD per execution, USD per unit and percentage of USD notional, default zero and charged on entry/exit including partial closures. Request clarification of why a USD account needs conversion; no missing-conversion policy has been accepted. |
| U8 | User confirmation after currency-conversion explanation | If required historical conversion to the USD account is unavailable, pause the affected execution with an explanation. Do not invent a conversion rate or record an incorrect USD result. |
| U9 | User's persistence answers | Retain downloaded M1/H1 and recalculated candles in application-owned local files for reuse, leaving sibling ingestion files unchanged. Autosave layouts, drawings and replay trading progress, including positions, pending orders and settings, and resume after restart. Saved runs retain original inputs/results when new data arrives; updated history is used for new runs or an explicit restart. |
| U10 | User's source/replay answers | Final Dukascopy historical bars replace provisional live-built bars for current history and new runs; saved runs retain original inputs. Pause replay trading with an explanation at unexplained gaps during expected trading hours when backfill cannot resolve them; traverse known market closures normally. Watchlists, details and synchronized charts follow the historical replay cursor and must not reveal later/live prices. |
| U11 | User's fill/sizing answers | Limit entries and TP fill at requested price or better, never worse; a better first eligible quote after a gap is used, while a bar touch fills at the limit with evidence labelled. Assume full simulated fills without liquidity-driven partial fills; manual partial closure remains. Risk-percentage sizing includes configured entry/exit commission and rounds down to permitted increments within planned risk, rejecting quantities below minimum; gaps may exceed planned loss. Instrument value/price/quantity specifications are visible/editable, populated from Dukascopy metadata where available, with trading paused when required values are missing. |
| U12 | User's first-version boundaries | Drawings are layout/instrument-scoped, persist across timeframe changes and remain unchanged by trading rewind. Trading uses validated completed bars/valid ticks, unusable intervals are reported as gaps and valid zero-volume/weekend rows are preserved. Desktop mouse/keyboard with at most two simultaneous charts is sufficient; mobile is excluded. External completed-run bundle import/viewing is deferred to deliver v1 sooner; the application's own trading results/reports remain. |
| U13 | User's closure-package response and history clarification | Accept P1 execution and P2 recovery. Require complete available history with discovered asset/provider bounds; 100k is an in-memory benchmark, not a lookback cap. P3's remaining targets are subsequently accepted in U14. |
| U14 | User's final package acceptance | Accept P3's remaining performance/runtime targets after clarification that the 100k figure is an in-memory benchmark only. P1, P2 and P3 are all accepted. |
| S1 | [REPLICATION-ANALYSIS.md](REPLICATION-ANALYSIS.md) | Complete original analysis: workspace, functional inventory, E01–E18 observations, data semantics, proposed scope and residual unknowns. |
| S2 | [AUTHENTICATED-FINDINGS.md](AUTHENTICATED-FINDINGS.md) | Complete authenticated update: A01–A35, including successful RSI/drawing/persistence/layout/replay/compiler/report workflows. Supersedes earlier account-gate conclusions for those tested workflows only. |
| S3 | [LOCAL-IMPLEMENTATION.md](LOCAL-IMPLEMENTATION.md) | Complete independent implementation proposal and acceptance matrix. Proposed product behavior is a candidate requirement until accepted. |
| S4 | [FEATURE-INVENTORY.json](FEATURE-INVENTORY.json), [anonymous register](evidence/index.json), [authenticated register](evidence/authenticated-index.json) | 180 captured menu rows across 11 groups; 53 scenarios / 450 steps. Menu presence and inspection activity do not establish behavior or release scope. |
| S5 | [network summary](evidence/network-summary.json), [Pine network summary](evidence/authenticated-network-summary.json), [local context](evidence/local-context.json), [cleanup notes](evidence/authenticated-cleanup.json) | Bounded historical evidence. Private endpoints are not integration contracts; old local paths and coverage are superseded by U1 and the present inventory. |
| D1 | `../marketDataIngestion/dukascopy/` inspected 19 October 2026 | 7,281 bar manifests with corresponding Parquet files; 42 tick manifests and 48 tick Parquet files. Metadata establishes declared coverage, not exhaustive row quality or continuity. |
| D2 | `../marketDataIngestion/aggregate-instructions.md`, `dukascopy/aggregate_m1_bidask.py`, `dukascopy/aggregate_h1_bidask.py` | Current aggregation semantics: M5/M15 from M1; H4/D1/W1/MN1 from H1; UTC boundaries; existing output timestamps retained by default. Old documentation paths omit the current `dukascopy/` directory. |
| D3 | `../marketDataIngestion/dukasCopyIngestionTicks.py` | Tick timestamp/schema and in-progress daily-part/finalized-month conventions. Inspected as source text; no ingestion was run. |
| D4 | `../marketDataIngestion/dukasCopyIngestion_m1_concurrent.py`, `dukasCopyIngestion_h1_concurrent.py` | Existing downloaders use Dukascopy's public datafeed with separate BID/ASK M1 daily and H1 monthly candle files. This is repository evidence for the proposed historical access path, not proof of live access or publication latency. |
| W1 | [Dukascopy historical-data overview](https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/overview-historical-data/) | Official documentation checked 19 October 2026: JForex IHistory supports historical access and distinguishes demo/live real-time ticks. U3 selects live-account data; exact API/setup verification remains UNK-19. |
| W2 | [Dukascopy IHistory reference](https://www.dukascopy.com/client/javadoc/com/dukascopy/api/IHistory.html) | Official API reference describes multiple history methods. It does not establish that every Dukascopy interface is limited to M1/H1. U2/D4 constrain this version's historical candle inputs to M1/H1. |
| W3 | [Dukascopy market-order execution](https://www.dukascopy.com/wiki/en/forex-cfds/orders/market-order/), [maximum slippage](https://www.dukascopy.com/wiki/en/forex-cfds/orders/market-order-with-slippage/) | Official documentation checked 19 October 2026: order execution depends on conditions when an order reaches the market and available liquidity. Inference for this replica: quote ticks alone cannot recover a hypothetical order's actual broker slippage. Any execution-delay/extra-cost model must be explicitly defined and labelled, not claimed as observed execution. |

U14 completes acceptance of P1/P2/P3. U13 requires full dynamically bounded history, with 100k bars solely an in-memory benchmark. U1–U12 establish the data, feature, execution and persistence decisions recorded below. The source table retains chronological statements for provenance; later user decisions and the current requirements supersede earlier provisional choices. Convergence retains the explicitly accepted simulation approximations ASM-01/ASM-02; it does not claim observed broker execution or completed implementation. No live connection, data download or sibling-data modification was performed while preparing this dossier.

Provenance distinguishes user-confirmed requirements, supplied-source behavioral baseline and explicit simulation assumptions. The baseline details within selected chart/indicator/drawing families come from S1–S3, not recovered source or numerical-parity proof. Remaining visual/parameter details are non-blocking downstream design work (Section 18). No architecturally significant unknown remains unaccepted. Provider/API feasibility must still be verified before live integration is accepted; requirements convergence is not an integration test result.

## 2. Business outcomes

| ID | Outcome | Success evidence / unacceptable failure | Status / provenance |
| --- | --- | --- | --- |
| BO-01 | Analyze the existing Dukascopy history through a TradingView-inspired workspace. | All ten assets and eight supplied timeframes are discoverable; no external price source is required to use those files. | KNOWN — U1 |
| BO-02 | Make financial data identity and limitations visible. | A user can distinguish SP500 provider history from `SP:SPX`, bid from ask, historical latest from live, and absent from zero. Mislabelled instruments or invented history are unacceptable. | SUPPLIED-SOURCE — S1–S3 correctness baseline |
| BO-03 | Preserve reusable analysis work. | Saved chart configuration, studies and drawings survive restart or expose a recoverable save error. | SUPPLIED-SOURCE — S2 A05–A09, A19–A20; S3 |
| BO-04 | Explore historical decisions without future information. | Replay calculations and any included simulation use only information available at the replay cursor. | SUPPLIED-SOURCE — S2 A13–A16; S3 |
| BO-05 | Continue from stored history to current Dukascopy data without concealing gaps. | Recover M1/H1 history, reconcile supported periods, expose closure/recovery/failure states and preserve readable existing data. | KNOWN — U2/U10/U14 |
| BO-06 | Practice historical trading without real brokerage effects. | Historical orders and results are explicitly simulated; execution and accounting rules are inspectable. | KNOWN inclusion — U2; detailed policies UNK-16 |

## 3. Scope

### Confirmed scope and constraints

- DATA-01–DATA-03: the existing Dukascopy files are the required market-data foundation; support the ten assets and eight supplied bar timeframes.
- Partial SP500 ticks describe the inspected inventory, not a permanent capability limit. Use available ticks for intrabar order/stop resolution, and support additional tick assets as their data becomes available. No tick-driven chart rendering or tick chart timeframe is required.
- Intrabar resolution uses available finer stored bars first, then local ticks if necessary. If evidence still cannot determine SL/TP order, use a labelled stop-first result. No missing ticks are downloaded in this version; their acquisition and permanent local database updates are future work. M1/H1 historical bar gap filling remains in scope.
- One local user; connect to Dukascopy live-account market data when available and query historical data to fill the gap to current data. Historical candle acquisition uses M1/H1; other supported periods may need recalculation for the recovered interval. U3 permits completing affected existing boundary candles while preserving older history.
- Exactly M1/M5/M15/H1/H4/D1/W1/MN1; no extra chart timeframes, including custom, second, tick-count or range intervals. Chart rendering uses bars; ticks supply detailed evidence for eligible operations.
- Stored timeframes are the historical basis; no blanket replacement by M1-derived history. Default bid prices, with ask selectable; no midpoint chart mode in this version.
- Historical simulated trading is included. Scripting and alerts are excluded. Live data access does not authorize real brokerage or live paper execution.
- Historical trading includes Market/Limit/Stop entries, optional SL/TP, modifying/cancelling orders and full/partial manual position closure. Opposite entry orders create independent hedged positions; closing a position is a distinct targeted action. Balance and position sizing are configurable; no margin checks or margin-based forced liquidation are required.
- The simulated account is USD only. Starting balance, fixed quantity and risk-percentage sizing are configurable; commission is configurable with default zero. New orders/modifications take effect after the replay decision point. Rewind removes subsequent trading actions only after confirmation. Bar-only execution applies no additional slippage; observed bid/ask and gap prices still apply.
- No extra slippage model is included, even when local ticks exist. Commission can be configured per instrument as fixed USD per execution, USD per unit or percentage of USD notional, charged separately on entry and exit executions including partial closures. All modes default to zero.
- If historical conversion required for a USD execution/account result is unavailable, pause the affected execution and explain the missing rate. Do not use a fabricated, unit-for-unit or current-day substitute rate.
- Acquired M1/H1 and recalculated higher candles are retained in application-owned local files across launches; existing sibling ingestion files remain unchanged. Autosave committed layouts/drawings/replay trading progress and restore them after restart. Existing saved runs retain original data/results; updated history applies to new runs or an explicit restart, not a silent recalculation.
- Final historical bars take precedence over provisional live-built bars in current history/new runs, without changing saved-run inputs. Replay trading pauses at unexplained unresolved market-hour gaps; known closures are traversed normally. All replay workspace panels follow the historical cursor rather than exposing later/live prices.
- Limit entries/TP execute at the requested price or better, with evidence labelled. Eligible simulated orders fill fully, without a liquidity/queue partial-fill model. Risk-percentage sizing includes configured entry/exit commission, rounds quantity down within permitted increments and rejects below-minimum size. Instrument contract/unit values and price/quantity increments are explicit and editable; missing required values pause trading.
- V1 is desktop mouse/keyboard with a maximum of two charts and no mobile support. Drawings belong to their layout/instrument and remain across timeframe switches and trading rewind. Trade only on validated completed bars/valid local ticks; do not discard otherwise valid rows solely for zero volume or weekend timestamps. External completed-run bundle import/viewing is deferred.
- All available history is accessible; no 100k-bar lookback/retention limit and no fixed earliest date. Discover earliest/latest coverage per provider, asset, timeframe and side. September 2016 describes the present inventory, not a product constant. The 100k figure is an in-memory performance working set, not a requirement to keep the whole archive resident.
- P1 execution-edge and P2 recovery/conflict defaults are accepted by U13; P3 quality/runtime targets are accepted by U14. Full history remains independent of the resident working-set benchmark.
- The task is requirements preparation. No current mandate selects a framework, renderer, language, database, API shape or deployment topology.

### First-version scope — feature families confirmed by U2

Instrument search/watchlists; candles/line/provider-volume; navigation/data window; settings/themes; built-in indicators; core drawings/object management; named saved layouts and two-chart interval synchronization; local image export; historical replay/trading; live Dukascopy data and historical gap filling. The following supplied-source tool/study baseline stays within those selected families. Exact visual/parameter realization is downstream design work, while the accepted data/trading/recovery/runtime rules are binding.

### Release boundaries and supplied-source baseline

| Capability family | Source coverage / data fit | Proposed disposition |
| --- | --- | --- |
| Historical paper trading | Forms inspected; fills unverified. Bars can support declared approximations; ticks cover only part of one instrument. | Included — U2; execution/accounting policies UNK-12/UNK-16. |
| Alerts and notification evaluation/delivery | Reference forms inspected; delivery unverified. | Excluded — U2; no background alert service or notification integration required. |
| Pine editor, arbitrary scripts and scripted strategy execution | Successful reference probes, but no recovered compiler or general parity evidence. | Excluded — U2. Historical trading results do not imply script execution. |
| Completed backtest run-bundle viewing | Existing separate `contract-v1.0.0/` contract; distinct from this version's own historical trading reports. | Deferred — U12. Do not implement external run-bundle import/viewing in v1. |
| Additional chart styles | 21 entries inventoried; only candles-to-line change exercised. | Defer beyond candles and line until selected and semantically specified. |
| Full drawing catalog | Lines/channels/pitchforks, Fibonacci/Gann, patterns/Elliott/cycles, forecasting/profiles, shapes and annotations inventoried; one horizontal-line lifecycle verified. | Core subset below; larger catalog remains selectable expansion. |
| Tick/second/custom/range intervals | Visible reference menus exceed the eight supplied bar timeframes. | Excluded — U2; retain only the eight supplied chart timeframes. |
| Volume profiles and other tick-dependent analysis | U3 plans volume profiles for a future version. Quote ticks and side volumes do not establish exchange trades, aggressor side or order-book depth. | Future scope, not this release; future profiles require explicit volume semantics and sufficient input data. |
| News, options, corporate events/fundamentals, calendar, screeners, AI/social/community | Separate datasets/services; most deep workflows uninspected. | Defer; never populate with invented or captured historical demo content. |
| Dukascopy live quotes and historical gap filling | Required by U2/U3, extending the initial stored dataset using live-account data. | Included; exact API/setup and source reconciliation remain UNK-19/UNK-20. |
| External alert delivery and scripting | Explicitly unnecessary in U2. | Excluded. |
| Real brokerage, cloud sharing, hosted snapshots | Outside the selected local historical-trading/data-access scope. | Not included in v1; live-account access is market data only. |
| TradingView authentication, subscription gates and upgrade/publish actions | Reference account/UI behavior, not needed to read local data. | Proposed exclusion. |

## 4. Actors

| Actor / system | Relationship and responsibility | Status |
| --- | --- | --- |
| Local analyst | Sole user; selects history/live views, configures and saves analysis and performs historical simulated trading. | KNOWN — U2; no shared/tenant roles required. |
| Existing ingestion process | Produces/revises sibling inputs independently; originals remain unchanged by this application. | KNOWN — U9; saved runs retain original selected observations/specifications. |
| Dukascopy market-data services | Live-account observations and historical M1/H1 gap filling, as well as provenance of supplied files. | KNOWN required dependency — U2/U3; API/setup and reconciliation details UNK-19/UNK-20. |
| Historical simulation user | The same sole analyst; submits simulated orders in historical replay. | KNOWN — U2; execution rules UNK-16. |
| Run-bundle producer | No integration in this release; separate externally produced evidence is deferred. | Future actor only — U12. |

## 5. Important terminology

| Term | Operational meaning | Distinction |
| --- | --- | --- |
| Asset / instrument | A named local series with provider-qualified identity. | `SP500` / `USA500IDXUSD` is not proven identical to `SP:SPX`; `NASDAQ` is not the NASDAQ venue identifier for stocks. |
| Bar timeframe | M1=minute, M5=5 minutes, M15=15 minutes, H1=hour, H4=4 hours, D1=day, W1=week, MN1=calendar month. | MN1 is not one minute or a fixed 30-day duration. |
| Coverage | Actual usable observations and known gaps for a particular instrument, timeframe, side and dataset version. | File name, first/last span and GOOD/COMPLETE status do not prove continuous usable observations. |
| Bid / ask | Separate price-side OHLC and volume observations. | An average of side highs/lows is not the true high/low of a midpoint tick series. |
| Volume | Provider-supplied side volume, whose units/meaning require confirmation. | It is not established as exchange-traded index volume, executed order flow or liquidity depth. |
| Latest historical | Last available record in the selected dataset. | Neither a current live quote nor proof the market is open. |
| Display timezone | How a user reads timestamps. | It does not change the UTC bucket boundaries of stored bars. |
| Replay cursor | Historical information boundary. | Independent of mouse hover date, wall clock, visible range and latest stored record. |
| Completed bar | A bar whose period has ended at the information boundary and whose required data is usable. | An existing W1/MN1 row may contain observations from after a replay cursor inside that period. |
| Paper simulation / run evidence | Newly calculated hypothetical execution / authoritative output from an existing completed run. | These have different data authority and must not be conflated. |
| Chart period / execution detail | The selected one of eight bar periods / finer observations used to establish historical order events within a bar. | Using ticks for fill evidence does not add a tick chart or require rendering every tick. |
| Hedged position / targeted closure | An independent long or short position / an explicit action reducing a selected position. | A new opposite-side entry does not silently close an existing position. |
| Account currency / instrument profit currency | The fixed USD unit of combined account balance and reporting / the currency in which an instrument's price change initially yields a monetary result under its contract. | USD account reporting does not turn EURGBP quotes into USD prices or make GBP profit equal the same numeric amount in USD. |

## 6. Functional requirements

User-confirmed requirements carry U references; `SUPPLIED-SOURCE` entries define the bounded behavioral baseline within the selected chart/analysis families. Exact visual and formula/parameter realization remains downstream design work; no numerical TradingView parity is promised. Acceptance examples describe observable outcomes, not implementation choices.

### Dataset access and selection

- **FR-01 — KNOWN, U1:** Discover all ten supplied instruments with all eight available bar timeframes from the current data root. Locate monthly and all-history files without manually selecting every month.
- **FR-02 — SUPPLIED-SOURCE, D1/S3:** Expose each selection's provider identity, timeframe, quote side, actual coverage, quality limitations and historical-data status. Distinguish missing data, invalid data, exhausted history and loading.
- **FR-03 — SUPPLIED-SOURCE, S1 E02/E18:** Search the local instrument catalog by local symbol, provider symbol and descriptive name. Forex, index-related and commodity grouping must not imply unavailable Stocks/Crypto/Options catalogs. A failed selection retains the last valid chart.
- **FR-04 — KNOWN, U2:** Default chart prices to bid and offer ask as an explicit selectable alternative; no midpoint mode. Show the chosen side in the legend/data window and apply it consistently to chart-dependent studies. Chart side does not change the execution side of a simulated buy/sell.

### Chart workspace

- **FR-05 — SUPPLIED-SOURCE, S1 E01/E09:** Display candles and line views with readable time/price axes, crosshair, selected-bar OHLC and provider-labelled volume when available. Switching styles retains instrument, interval and analysis state.
- **FR-06 — KNOWN full-history scope, U13; navigation detail S1/S3:** Support pan, zoom, resize, go-to-date and return-to-latest-history across all available history. Moving beyond an in-memory working set makes earlier/later available observations accessible; never report end-of-history merely because 100k bars are loaded. Preserve financial anchors and do not invent observations beyond actual source coverage.
- **FR-07 — KNOWN timeframe set, U2:** Offer exactly M1/M5/M15/H1/H4/D1/W1/MN1, including after live/backfill updates. No additional timeframes. Visible-range presets state range/timeframe and must use one of these eight periods; no unsupported 30-minute or 2-hour substitution from the reference.
- **FR-08 — SUPPLIED-SOURCE, S1 E01/E17:** Provide a readable data window for selected-bar time, OHLC, quote side, volume and study outputs. Missing/warm-up values remain unavailable rather than zero.
- **FR-09 — KNOWN replay clock, U10; supplied-source watchlist baseline S1:** Provide a local watchlist over available assets and basic details from local metadata. During replay, metrics use only cursor-available observations, not later/live prices. Identify timeframe, side and reference observation; missing historical values remain unavailable. Editing/order/appearance details are downstream UI work; reference parity is not independently verified.
- **FR-10 — SUPPLIED-SOURCE, S1 E07/E18:** Configure light/dark appearance, chart/grid/crosshair presentation, candle colors, price precision and display timezone. Cancel discards a settings preview; applying retains a valid configuration. Display precision must not replace stored values.

### Indicators, drawings and persistence

- **FR-11 — SUPPLIED-SOURCE, S3; RSI workflow S2 A05–A08:** Provide SMA, EMA, RSI, MACD, Bollinger Bands and volume presentation. Each supported calculation declares its inputs, initialization, warm-up, missing-data behavior and precision. Captured RSI 51.94 on SPX is not a fixture for different Dukascopy data.
- **FR-12 — SUPPLIED-SOURCE, S2 A07/S3:** Add/remove studies, use overlays or separate panes, edit supported inputs/style/visibility and save those choices. Invalid inputs retain the previous valid configuration and identify the problem.
- **FR-13 — SUPPLIED-SOURCE, S3; horizontal line S2 A08–A09:** Provide trendline, horizontal/vertical line, ray, rectangle, text, Fibonacci retracement, brush and long/short position measurement. Measurement drawings do not create orders. Exact geometries and configuration bounds remain UNK-04.
- **FR-14 — KNOWN scope/rewind, U12; tool detail S2/S3:** Drawings belong to their layout and instrument, persist across timeframe switches and remain unchanged by trading rewind. Create/select/edit/hide/lock/delete supported financially anchored tools and list them in an object tree. Preserve anchors across zoom, resize and restart. Rewinding trading does not remove later annotations or claim that user-authored drawings are historically discovered facts.
- **FR-15 — SUPPLIED-SOURCE, S1 E08/E09/E18; S2 A08:** Undo/redo supported chart edits and drawing changes with a meaningful action label. Cancelling an uncommitted drawing creates no lasting object; redo after undo creates no duplicate. Exact history depth is UNK-03.
- **FR-16 — KNOWN autosave/restore, U9; layout detail S2:** Create, name, autosave and restore layouts containing instrument/timeframe/side, chart presentation, studies, drawings and arrangement. Show saving/saved/unsaved/error truthfully. A failed save must not be reported as durable success. Committed drawings and settings participate in autosave; previews/cancelled edits do not become saved analysis.
- **FR-17 — KNOWN limit, U12; synchronization detail S2:** Provide one-chart and two-chart desktop arrangements, at most two charts in v1, with explicit interval synchronization. Without sync, charts retain their own selection; with sync, both adopt a supported interval once and remain usable after save/reload. All replay charts obey the common historical cursor; larger arrangements are deferred.
- **FR-18 — SUPPLIED-SOURCE, S1 E17/S3:** Export a local chart image including intended chart/studies/drawings/legend. Hosted links and social publication are separate unselected integrations.

### Historical replay

- **FR-19 — SUPPLIED-SOURCE, S2 A13–A16/S3:** Select a historical start within usable coverage; play, pause, step one completed bar, change playback speed, restart and seek. Display the cursor explicitly and keep it separate from hover time.
- **FR-20 — KNOWN, U10; visibility detail S3:** All replay workspace charts, synchronized charts, watchlists, details, studies, comparisons, data-window values and simulation use information available at the historical cursor. Do not display later/live prices in these panels. Completed higher-timeframe OHLC remains hidden until its period is available; no future high/low/close may enter a replay calculation. Timeframe/coverage differences do not authorize using later observations to populate an empty value.
- **FR-21 — KNOWN, U6/U12/U13:** Confirm rewind, remove subsequent trading actions and recompute account/positions at the earlier cursor. Cancelling preserves cursor/state. Retain earlier actions, including entries that should be open again; drawings remain unchanged. Respect the FR-53 event-before-new-decision boundary so same-cursor actions cannot execute against already-processed events. Identical retained inputs/actions/policies reproduce results.
- **FR-22 — KNOWN, U9/U12/U13:** Autosave replay trading progress and resume at the saved historical point after restart with positions, pending orders and settings. Replay progress is distinct from the latest-history view. Exiting replay identifies the return to current history without destroying the saved run. Drawings obey FR-14; concurrent editing is bounded by FR-55's single-writer rule.
- **FR-23 — KNOWN, U3/U4/U12:** Resolve intrabar order/stop outcomes with available finer stored bars before local ticks. If usable evidence cannot establish SL/TP order, apply labelled stop-first. Charts remain bar-based; no tick redraws/timeframes. Discover usable tick coverage per asset/date, not SP500-only. Use local ticks only; validated eligibility is FR-51, and fill policies are FR-38/FR-40/FR-47/FR-48/FR-53.

### Accessibility and failures

- **FR-24 — SUPPLIED-SOURCE, S1/S3:** Provide named controls, keyboard-operable commands/dialogs, clear focus, non-color-only status and readable numerical values outside the plot. Keyboard and pointer affordances must agree; do not reproduce the reference's contradictory disabled-switch semantics.
- **FR-25 — KNOWN desktop scope, U12; adaptation detail S1/S3:** Support desktop mouse/keyboard and at most two charts; no mobile/touch support is required in v1. Keep core chart selection/navigation usable as panels resize. Missing/corrupt files, end of history, invalid settings and failed saves have distinct actionable messages. Exact desktop minimum dimensions remain a UI-detail question rather than a mobile requirement.

### Historical trading and excluded/conditional features

- **FR-26 — EXCLUDED, U2:** Alerts and their evaluation, scheduling, trigger history and external delivery are not required in this version. This retained ID records the explicit scope decision.
- **FR-27 — KNOWN, U2/U5–U14:** Historical trading supports Market/Limit/Stop entries, optional SL/TP, modification/cancellation and targeted full/partial closure. Opposite entries hedge. Balance and fixed/risk-based sizing are configurable without margin checks; account currency is USD. SL gaps use first executable side prices, limits/TP are requested price or better, and new decisions take effect after the replay point. Apply the detailed execution/recovery rules below; no extra slippage or real order routing.
- **FR-28 — EXCLUDED, U2:** No scripting editor, Pine compatibility or arbitrary script execution is required in this version. Built-in indicators remain in scope.
- **FR-29 — SUPPLIED-SOURCE historical-results detail:** Historical trading results should expose input dataset, execution policies, units/currency, trades and metrics reproducibly. Scripted strategy execution/reporting is excluded. A chart value unit must not be relabelled as an accounting currency.
- **FR-30 — DEFERRED, U12:** External `contract-v1.0.0` completed-run import/viewing is excluded from v1; the application's own historical trading results/reports remain. A future feature must obey the authored contract's producer-authoritative numbers, exact timestamps and knowledge-time reveal. No current schema aliases or external run reader are required.

### Live market data and historical continuity — KNOWN inclusion, U2

- **FR-31:** Connect to Dukascopy live-account market data when available for the supported assets (U3); do not substitute demo feed observations. Live bars identify instrument, quote side, event time and provisional/final status. No live observation is allowed into historical simulation after its replay cursor.
- **FR-32:** Detect the gap between available history and current market data, request Dukascopy historical M1/H1 for the missing interval, and extend usable history. Show progress, unresolved gaps and failures; a network response with no records is not by itself proof of market closure.
- **FR-33:** Calculate recovered/live candles in the existing M5/M15/H4/D1/W1/MN1 periods, preserving separate bid/ask sides and UTC bucket semantics. Complete affected boundary candles, such as a weekly candle spanning a recovered interval, without adding periods or wholesale-replacing older supplied history. Final/current history and saved-run correction precedence is FR-35/FR-45; provider publication evidence is Section 18.
- **FR-34 — KNOWN, U2/U10/U14:** Distinguish current feed receipt, scheduled closure/no observations, recovery, stale data and connection failure. Preserve readable stored history and never fabricate weekend/outage movement. Meet the one-second local-receipt display target; source publication/session evidence must be verified under Section 18. No provider outage recovery deadline is promised.
- **FR-35 — KNOWN precedence, U10:** Resume from the last usable historical boundary after a live interruption and reconcile overlapping observations without duplicate bars or concealed discontinuity. When final Dukascopy historical bars become available, replace provisional live-built bars in application-owned current history and recompute affected supported-timeframe derivatives. New runs use that finalized history; saved runs keep their original inputs/results under FR-45. Publication lag, partial recovery and closure-detection evidence remain UNK-20.
- **FR-36 — KNOWN, U3/U14:** Keep routine bar-chart drawing/navigation independent of large tick-history inspection. Tick-dependent order resolution may expose loading/unresolved state; do not invent a fill for responsiveness. Use the accepted SCALE-03/P3 response targets; full archive navigation is FR-52.
- **FR-37 — KNOWN, U4:** Identify each fallback result as a stop-first simulation assumption rather than observed event ordering. Record the resolution evidence (bar timeframe or local ticks), relevant coverage limitation and chosen policy with the trading result so it remains distinguishable after save/reload or export. Actual observed SL/TP order takes precedence whenever usable finer evidence establishes it.
- **FR-38 — KNOWN, U5/U13:** Manage each hedged position independently. Opposite entries hedge; a targeted close reduces only that position. Partial closure resizes SL/TP to remaining quantity; full closure cancels its protective exits. Reject over-closure/invalid quantity rather than closing another position or creating an unintended opposite position.
- **FR-39 — KNOWN, U5/U6/U11:** Provide configurable simulated starting balance in fixed USD and both fixed-quantity and percentage-of-balance risk sizing using the SL distance. Include configured entry/exit commission in planned risk and round quantity down to the instrument's permitted increment; reject below-minimum quantities. The user cannot change account currency. No margin-based rejection/liquidation applies. Actual losses may exceed planned risk through a gap. Required unit values/increments are explicit under FR-50; unknown historical USD conversion pauses the affected execution under FR-42.
- **FR-40 — KNOWN, U6/U13:** New orders/modifications cannot execute against an already-visible close or processed intrabar events. Market orders use the next available eligible executable bid/ask, or next available bar's side-specific open for bar-only evidence. No invented regularly timed quote. Existing orders are evaluated before new decisions at a cursor (FR-53); limits use FR-47 and stops become market orders after triggering.
- **FR-41 — KNOWN, U6/U7/U13:** Per-instrument commission can be fixed USD per execution, USD per unit or percent USD notional; default zero, charged on entry/exit including partial closures. No additional slippage or execution-delay model applies, with or without ticks. Preserve observed spread/next-event/gap effects. Apply instrument specifications, historical USD conversion and deterministic documented quantity/notional/fee rounding.
- **FR-42 — KNOWN, U8/U13:** Use historical bid/ask conversion evidence known at or before the event, never future observations. Missing required historical/session data pauses the affected execution with its instrument/event, conversion and time explained. Keep it uncommitted; do not create an unvalued fill, incorrect USD result or partial account update. Unit-for-unit, present-day or silently substituted stale rates are unacceptable. Once resolved, resume the blocked event at its original historical point, not a later market price.
- **FR-43 — KNOWN, U9:** Retain acquired M1/H1 bars and recalculated supported-timeframe candles in application-owned local files for reuse after restart. Record provenance and usable coverage; do not modify existing sibling ingestion files. This file retention is included now and does not implement the deferred automatic tick-download/permanent-database mechanism.
- **FR-44 — KNOWN, U9/U13:** Autosave committed layouts, drawings and replay trading state, including cursor, actions, positions, orders and settings. Restore the coherent last successfully autosaved state after crash/restart. Show saving/unsaved/error truthfully: work still shown as saving/unsaved and previews may be lost in a crash; successfully saved work must survive coherently. Backup/restore is FR-55.
- **FR-45 — KNOWN, U9:** Preserve the original selected market observations and settings/results of each saved trading run when newer history, ticks or corrections arrive. Reopening/resuming must not silently re-evaluate against changed inputs. Updated history is used for new runs or when the analyst explicitly restarts with updated data. Retaining only mutable source-file paths is insufficient to promise unchanged historical inputs; the retention mechanism is left to design.
- **FR-46 — KNOWN, U10:** If replay trading encounters an unexplained gap during expected trading hours that historical backfill cannot resolve, pause it with an explanation before executing across the unknown interval. Preserve the current coherent simulated state; do not invent bars or silently fill orders using observations after that interval. Traverse known market closures normally, applying the existing next-available-price and gap-fill rules. A market closure must be established from appropriate instrument/session evidence, not merely an empty response or a weekend timestamp.
- **FR-47 — KNOWN, U11:** Limit entries and take-profits fill at the requested limit price or better, never worse. If the first eligible executable quote after a gap is already better, use that quote. Otherwise an eligible bar touch can fill at the limit; identify its bar-based evidence/assumption rather than claiming an observed tick. Buy-side limits use ask evidence and sell-side limits use bid evidence. A known data gap pause overrides assumed touch execution; order eligibility must precede the touch.
- **FR-48 — KNOWN, U11:** Assume full requested-quantity fills for eligible simulated orders; do not model liquidity-driven automatic partial fills or queue priority. Manual partial position closure remains supported and fills the requested closing quantity under the same simulation assumption. Report the simplified execution policy; do not describe it as reconstructed broker liquidity.
- **FR-49 — KNOWN, U11:** Percentage-risk sizing must calculate the largest valid permitted quantity not exceeding the selected USD balance-risk budget under planned SL execution and configured entry/exit commissions. Round down to the allowed quantity increment and reject a result below minimum. Show the resulting quantity and planned risk. Missing/invalid SL, required unit values or currency conversion cannot be replaced with invented sizing inputs; gaps may increase actual loss beyond the planned amount.
- **FR-50 — KNOWN, U11:** Expose editable simulation specifications for each instrument: quantity/contract unit and monetary value, price increment and permitted quantity increment/minimum. Populate from Dukascopy metadata where available and identify any user overrides. Pause trading if required values are unknown. Saved runs retain the selected specification with their settings; later metadata/override changes do not silently change their results. These are simulation specifications, not authority to alter the real broker account.
- **FR-51 — KNOWN, U12:** Permit trading only on validated completed bars and valid local tick evidence. Preserve source files; report invalid/unusable intervals and apply existing gap-pause rules instead of silently trading through them. Preserve otherwise valid zero-volume/weekend rows; neither characteristic alone proves invalidity or market closure. Forming live candles may be displayed as provisional but are not finalized historical evidence before they become available at the replay cursor.
- **FR-52 — KNOWN, U13:** Expose complete available history for each provider/asset/timeframe/side, including current data back to September 2016 and any shorter/longer histories or extensions. Discover coverage from observations/metadata; no hardcoded global start date, rolling-year restriction or total-bar navigation/retention cap. Report actual bounds/gaps. An in-memory working set is separate from the accessible archive; full history need not be simultaneously resident.
- **FR-53 — KNOWN, U13/P1:** Advance completed bars; evaluate eligible existing orders before accepting new decisions at a cursor. New submissions/modifications cannot act on events already processed at that decision point. A triggered stop entry becomes a market order using next eligible executable side pricing, including gaps; existing evidence and unresolved-gap rules still apply.
- **FR-54 — KNOWN, U13/P1:** Apply deterministic documented USD/quantity rounding; reject invalid/over-close quantities and disable percentage-risk sizing at nonpositive balance. Fixed sizing remains subject to valid quantity/instrument checks and no margin model. Protective exits cannot exceed remaining position size or outlive full closure.
- **FR-55 — KNOWN, U13/P2:** Permit one writable tab. Confirm destructive deletion/reset. Provide manual backup/restore of analysis and saved trading runs with required input versions, excluding credentials. A backup need not copy the whole external market archive, but must retain the inputs required by its included runs. Restore coherent state rather than silently merging conflicting edits.
- **FR-56 — KNOWN, U14/P3:** Meet the accepted desktop working-set/response targets in SCALE-03. Acquisition runs while the application is running, with catch-up on startup/reconnect; no always-on acquisition while closed is required. Expose progress/provider delays/failure and keep available history readable. Provider network availability/publication delay has no guaranteed recovery time; this does not relax the one-second local-receipt display target.

## 7. Business rules

- **BR-01 — SUPPLIED-SOURCE, S1–S3/D1:** Identify an instrument by provider/source and symbol; never silently substitute `SP:SPX`, OANDA EURUSD, an exchange index or a futures contract for a Dukascopy asset.
- **BR-02 — SUPPLIED-SOURCE, D1/D2:** Preserve supplied UTC bucket semantics. Display timezone changes labels only. W1 opens Monday 00:00 UTC; MN1 opens on the first calendar day; edge buckets can contain partial source coverage.
- **BR-03 — KNOWN data constraint, U2/U3:** Never claim upsampled missing observations. Stored periods remain the historical basis; recovered/live aggregates preserve separate sides, UTC boundaries and lineage, and complete affected boundary candles without wholesale replacement. Final/current versus saved-run precedence is FR-35/FR-45.
- **BR-08 — KNOWN, U2/U3:** Use stored historical timeframes as supplied; do not introduce extra timeframes or replace all history with new M1 aggregations. Gap filling/live maintenance may add candles and complete affected existing boundary candles in the same eight periods while preserving older history.
- **BR-09 — KNOWN, U2:** No live feed at a particular time is an expected condition, including closed-market periods. It does not imply that every missing interval is a weekend/closure, that all assets share a session, or that historical retrieval has failed.
- **BR-04 — KNOWN eligibility, U12:** GOOD/COMPLETE is a bounded producer assertion, not continuity proof. Preserve otherwise valid zero-volume/weekend rows; report unusable intervals as gaps and never infer closure from absence alone.
- **BR-05 — SUPPLIED-SOURCE, S3:** All results identify the selected data, price basis and relevant calculation/policy version. Different provider history is not expected to reproduce captured TradingView numbers.
- **BR-06 — SUPPLIED-SOURCE, S1/S2; U5/U6 constraints:** Chartability does not establish simulated instrument sizing or value-per-point. Establish contract multipliers, quantity increments and executable capabilities; U5 excludes margin checks and U6 fixes account currency to USD. Do not import real-account balances or broker execution permission.
- **BR-07 — KNOWN, U10:** Replay uses one historical information boundary across charts and supporting panels. No live/latest-history watchlist or details exception is included. Missing historical values are unavailable, not replaced with current quotes; live ingestion may continue without exposing its later observations to the replay workspace.
- **BR-10 — KNOWN, U3/U4:** Tick support is a capability of an instrument's available data, not a special SP500-only execution mode. Missing ticks never justify claiming an observed intrabar path. If the SL/TP ordering remains unknown after inspecting available finer bars and local ticks, use stop-first and label it as an assumption. This ordering decision does not fix an unknown stop fill price or override evidence of an earlier actual TP event.
- **BR-11 — KNOWN, U10/U13:** Intrabar order evaluation cannot reveal later observations to earlier decisions. Advance completed bars, evaluate existing eligible orders, then accept new decisions. Already processed observations cannot be reused as if they occurred after a new decision.
- **BR-12 — KNOWN, U4/U13:** Stop-first applies only to eligible protective exits when SL/TP ordering is unresolved. It cannot invent an entry, apply a stop before entry or override a data-gap pause. Existing orders are evaluated before new decisions, so subsequent cancellation/modification cannot retroactively alter an already processed fill.
- **BR-13 — KNOWN, U5:** If an eligible stop-loss is crossed by a price gap, fill at the first available executable quote side after the gap, even when worse than the stop level. Use bid when closing a long and ask when closing a short. When bar data supplies the execution approximation, identify that evidence rather than claiming a captured tick. ASM-01 settles ambiguous SL/TP ordering, not guaranteed stop-level pricing.
- **BR-14 — KNOWN, U5:** Opposite entry orders hedge; they do not net, reduce or automatically reverse existing positions. Manual partial/full closure must identify the position being reduced. Closing semantics and order quantity validation remain explicit and are not margin checks.
- **BR-15 — KNOWN, U5/U6:** No margin requirement, margin-call policy or margin-driven forced liquidation applies. Account currency is USD, balance and fixed/risk-based sizing are configurable, and commission defaults to zero. Fractional quantities, contract increments and nonpositive/insufficient-balance behavior remain explicit sizing/account policies; no margin model is inferred.
- **BR-16 — KNOWN, U6/U7:** Zero additional slippage is not a guarantee of execution at the submitted/reference/stop price. Historical spread, subsequent quote movement and gaps affect the baseline executable price. All extra slippage/delay modelling is deferred; tick use for intrabar resolution does not enable an additional charge or adverse price shift.
- **BR-17 — KNOWN, U6:** A confirmed rewind discards later order submissions, modifications, cancellations and manual closures in the active run; recalculate dependent fills, positions and USD account history at the new cursor. No automatic branch is required. UI cancellation must preserve the original run; handling of unrelated drawings remains separate.
- **BR-18 — KNOWN, U8:** A fixed USD account does not redefine an instrument's price/profit currency. Convert monetary outcomes using applicable historical data; a missing required rate blocks the affected execution until the condition is resolved. The blocked outcome must not be mislabelled as insufficient margin, a market rejection or a successful zero-profit fill.
- **BR-19 — KNOWN, U9:** Changing the current historical catalog must not rewrite a saved run's original price/rate/tick evidence or completed results. Keep its selected input revision and execution/commission settings on resume. User-requested edits/rewind follow their explicit rules; restarting with updated history is a deliberate action, not an automatic side effect of acquiring data.
- **BR-20 — KNOWN, U10:** A known market closure and an unexplained market-hour data gap have different trading consequences. First-available-price execution across a known closure remains allowed; it is not a workaround for unresolved missing observations during an expected trading session. Stop-first ambiguity handling does not override FR-46's gap pause.
- **BR-21 — KNOWN, U11:** A stop is not a limit: gap-crossed SL uses the first executable side price, while limit/TP pricing is bounded by requested price or better. Finer-bar/tick evidence establishes event ordering where available; full-fill and bar-touch policies remain explicitly labelled assumptions when liquidity/path evidence is absent.
- **BR-22 — KNOWN, U11:** Risk percentage is a planned loss budget against simulated USD balance, including configured entry and planned exit commission. Rounding must not increase the permitted quantity above that budget. It is not a guarantee that actual losses, gap execution or repeated hedged exposures stay within that amount.

## 8. Lifecycle/state requirements

- Dataset access distinguishes discovery/validation, usable/limited coverage, unreadable data and changed source versions. Current-catalog updates do not change a saved run's selected inputs/results; invalid intervals remain visible and pause trading under the agreed policies.
- Chart selection must distinguish pending selection from successfully loaded data; a late result cannot label another asset's bars as current.
- A drawing preview can be committed or cancelled. Locked/hidden drawings persist without losing their financial anchors.
- Analysis edits may be unsaved, saving, saved or failed. Only successful persistence is durable; crash/restart expectations are UNK-14.
- Replay may be inactive, positioned, playing, paused or at its coverage limit. Cursor, configuration and any simulated outcomes require explicit restart/seek policies. These are behavioral distinctions, not a designed formal state machine.
- Tick months are producer-marked COMPLETE or IN_PROGRESS. Daily `.parts` files are staging material, not independently proven completed months.
- Historical simulation distinguishes drafts, eligible accepted orders, triggered entries, cancellation/rejection, fills and position/account history. Stop entries become market orders after trigger; subsequent decisions cannot retroactively act on an evaluated interval.
- Independently open long/short positions support targeted partial/full closure. Resize protective quantities after partial closure, cancel them after full closure, reject invalid/over-close requests and reconcile the account once per execution.
- U6 confirms that removing later trading actions on rewind restores earlier position/order conditions and recomputes dependent account history. A later exit removed by rewind cannot leave the earlier position permanently closed. Rewind confirmation is distinct from resetting an entire run or changing drawings.
- An event missing required historical USD conversion remains paused/uncommitted at its historical point, with the last committed state coherent. After the required condition is resolved, resume that original event rather than using a later price.
- Live observations can belong to a forming candle; label them provisional until finalized. Final historical bars supersede provisional current-catalog data, without changing a saved run's selected observations or results. Validate provider finality/publication evidence before accepting integration.
- Recovery can be pending, progressing, partially usable, complete or failed. Do not represent partial history as continuous; unresolved market-hour gaps pause replay trading, while established closures traverse normally.

## 9. Authorization requirements

- **AUTH-01 — KNOWN, U2:** One local analyst uses the application; no shared-user or tenant roles are required. Provider account identity, if necessary for live access, does not introduce application tenants or permission to route real orders.
- **AUTH-02 — KNOWN, U9/U13:** The sole local analyst owns application analysis and retained acquisition files. Consuming sibling ingestion data grants no authority to mutate it; deletion/reset of saved work requires confirmation and backups exclude credentials.
- **AUTH-03 — outside v1:** No shared-user/tenant or remote collaboration authority is required. Adding it later requires new ownership and permission requirements; no role matrix is invented for this release.

## 10. Data requirements

### Required inventory

**DATA-01 — KNOWN, U1/D1:** Use repository-relative `../marketDataIngestion/dukascopy/` (currently `/mnt/data/gdrive/trading/marketDataIngestion/dukascopy/`). Do not reuse the obsolete path without the `dukascopy/` component from older dossier evidence. The sibling datasets are inputs, not files to redistribute in the dossier ZIP.

**DATA-02 — KNOWN, U1/D1/U3/U11:** The initial universe is below; current SP500-only tick files are not a permanent capability restriction. Additional local tick assets are discoverable. Use explicit verified/editable instrument specifications for simulated monetary/quantity meaning and pause if required values are missing; do not infer executable product equivalence from a chart label.

| Local asset | Dukascopy identifier observed in manifests | Category |
| --- | --- | --- |
| AUDJPY | AUDJPY | Forex |
| EURGBP | EURGBP | Forex |
| EURUSD | EURUSD; absent in some manifests | Forex |
| GBPUSD | GBPUSD | Forex |
| USDJPY | USDJPY | Forex |
| DAX | DEUIDXEUR | Index-related |
| FTSE | GBRIDXGBP | Index-related |
| NASDAQ | USATECHIDXUSD | Index-related |
| SP500 | USA500IDXUSD | Index-related |
| XAUUSD | XAUUSD | Commodity / gold |

**DATA-03 — KNOWN, U1/D1:** Support all eight stored bar timeframes, with the following inspected inventory. Counts/row totals are from all manifests, not a full Parquet row audit.

| Timeframe | Directory under data root | Parquet / JSON pairs | Declared rows, all assets | Storage and lineage |
| --- | --- | ---: | ---: | --- |
| M1 | `dukascopy_m1_bidask/` | 1,211 | 45,185,760 | Monthly; source history. SP500 has one extra October file. |
| M5 | `dukascopy_m5_bidask/` | 1,210 | 9,033,120 | Monthly; M1 aggregation. |
| M15 | `dukascopy_m15_bidask/` | 1,210 | 3,011,040 | Monthly; M1 aggregation. |
| H1 | `dukascopy_h1_bidask/` | 1,210 | 883,680 | Monthly; separately stored source history. |
| H4 | `dukascopy_h4_bidask/` | 1,210 | 220,920 | Monthly; H1 aggregation. |
| D1 | `dukascopy_d1_bidask/` | 1,210 | 36,820 | Monthly; H1 aggregation. |
| W1 | `dukascopy_w1_bidask/` | 10 | 5,270 | One all-history pair per asset; H1 aggregation. |
| MN1 | `dukascopy_mn1_bidask/` | 10 | 1,210 | One all-history pair per asset; H1 aggregation. |

Monthly layout: `<directory>/<SYMBOL>/<YYYY>/<SYMBOL>_<YYYY>_<MM>_<TIMEFRAME>_bidask.{parquet,json}`. W1/MN1 layout: `<directory>/<SYMBOL>/<SYMBOL>_<TIMEFRAME>_bidask.{parquet,json}`.

**DATA-04 — KNOWN source fact, D1:** All assets have monthly files from September 2016 through September 2026. M1/M5/M15 begin 1 September 2016, with latest September observations ending on day 7 for DAX/EURGBP/EURUSD/FTSE/GBPUSD/NASDAQ/SP500, day 8 for USDJPY, and day 9 for AUDJPY/XAUUSD. SP500 M1 additionally reaches 16 October 2026 23:59 UTC; that does not establish continuity across the September/October boundary. H1 reaches 30 September 2026 23:00, H4 20:00, and D1 00:00 for all assets. W1 opening labels span 29 August 2016–28 September 2026; MN1 labels span September 2016–September 2026. These are opening-time extrema, not proof of complete periods.

**DATA-05 — KNOWN source fact, D1:** Representative bar schemas use UTC nanosecond timestamps, independent bid/ask OHLC binary64 values and side-volume float32 values. Column order differs between source and aggregate files; consumers must respect names and declared types. This sample does not prove schema uniformity in every file.

**DATA-06 — KNOWN source fact, D1/D3:** Tick data lives in `dukascopy_ticks_monthly/SP500/<YYYY>/`. There are 41 finalized monthly Parquet files, September 2016–January 2020; one February 2020 IN_PROGRESS manifest and seven daily Parquet files under `SP500_2020_02_ticks.parts/`. All 48 footers total 25,615,026 rows. Finalized observations span 1 September 2016 06:00:00.941 UTC–31 January 2020 21:14:57.962 UTC; staged observations extend through 9 February 2020 23:59:56.857 UTC. Tick schemas use UTC **milliseconds**, bid, ask and side volumes. No exchange order book or aggressor-side trade field was observed. A span is not a continuity guarantee, and COMPLETE is not independent download-quality verification.

**DATA-07 — KNOWN preservation constraint, U9/U13:** Preserve source precision and price sides. Display conversion cannot collapse distinct tick observations or alter a saved run's input facts. Respect established source order where present; if evidence does not establish SL/TP chronology, use labelled ASM-01 rather than claim an observed path. Mathematical ordering/rounding must be deterministic and documented.

**DATA-08 — KNOWN, U9/U13:** Retain file/version provenance for saved/replayed calculations and report missing metadata. A stale absolute manifest path is neither execution authority nor a write target; only application-owned acquisitions/state may be written.

**DATA-09 — KNOWN observation; policy unresolved:** A bounded SP500 September 2026 row inspection found 8,640 M1 rows, 720 H1 rows and 30 D1 rows; respectively 2,192, 218 and 4 rows had zero bid volume, and all three samples included weekend rows. No sampled bid-close values were null. These observations do not establish fabricated data, exchange sessions, full quality, or a justified deletion/filtering policy.

**DATA-15 — KNOWN, U2/D4:** Acquire missing historical candle observations from Dukascopy using M1/H1 as this version's source periods. Existing ingestion code constructs separate BID/ASK M1 daily and H1 monthly public datafeed requests. Publication delay, recent incomplete periods, response limits and actual live-feed agreement have not been verified. This is an interface-scoped input constraint, not a claim that all Dukascopy APIs expose only two periods.

**DATA-16 — KNOWN, U2/U9:** New live/backfilled data retain Dukascopy identity, time, side, origin and provisional/final distinction. New/affected supported-timeframe aggregates retain input provenance. Store acquired history in application-owned local files and retain it across launches. Existing sibling ingestion datasets remain unchanged; no shared-directory mutation is required or authorized by these requirements.

**DATA-17 — KNOWN, U3/U4:** Tick availability is evaluated per instrument and time span. Support future supplied tick assets without a SP500-only product restriction. Preserve distinction between observed tick evidence and bar-based approximations; report the evidence used to resolve an intrabar event. Only local ticks are used in this release; automatic missing-tick download and permanent-database updates are deferred. Future volume-profile support is a separate feature, not part of this release.

**DATA-18 — KNOWN, U9/U13:** Retain selected historical observations, applicable local tick/FX evidence and policy/instrument settings with each saved run. Do not substitute new catalog data. Runs retain required inputs until deliberate deletion; confirm destructive delete/reset. Manual backups include required run-input versions but no credentials, and restored runs must remain reproducible.

| ID | Data category | Authority / ownership | Classification | Retention/privacy |
| --- | --- | --- | --- | --- |
| DATA-10 | Supplied market observations/manifests | Existing local ingestion outputs, provider provenance | Required initial basis — U2; read-only sibling inputs — U9 | Acquisitions retained separately; saved-run inputs preserved; validated trading eligibility under FR-51. |
| DATA-11 | Calculated studies/metrics | Declared local calculations using chosen input/policy | Derived; never substitute for producer facts | Reproducibility expected; retention UNK-14. |
| DATA-12 | Layouts, drawings, watchlists, settings | Analyst-authored state | Authoritative user work | Layouts/drawings/settings autosaved — U9; delete/export/backup scope UNK-14. |
| DATA-13 | Replay position and historical simulated orders/accounts | Selected replay/simulation inputs and declared policies | Required simulation history — U2; not broker facts | Autosave/resume original run data/results — U9; confirmed rewind rules U6. |
| DATA-14 | Optional completed-run bundles | Contract-defined producer | Producer-authoritative evidence | Preserve exact values, times, knowledge/sequence reveal and declared indexes if selected. |

## 11. External integrations

| ID | System | Role and direction | Failure / replaceability expectation |
| --- | --- | --- | --- |
| INT-01 — KNOWN, U1 | Existing Dukascopy directory | Required inbound historical source | Missing files cannot cause source substitution; report affected coverage, preserve other usable data and apply OPS-02/gap-pause rules. |
| INT-05 — KNOWN, U2 | Dukascopy historical M1/H1 source | Required inbound gap filling | Preserve existing readable history on failure; expose unresolved spans. Actual access path supported by D4; publication/overlap rules UNK-20. |
| INT-06 — KNOWN, U2/U3 | Dukascopy live-account market-data feed | Required inbound current observations when available | Expected closure and unexpected outage must be distinguished; live-account identity confirmed, API/setup verification UNK-19. Market-data access never authorizes broker orders. |
| INT-07 — deferred, U4 | Historical tick acquisition and permanent database update | No automatic missing-tick network acquisition in this release | Future missing-data downloads and permanent local database updates are a change driver, separate from required current M1/H1 bar backfill. |
| INT-02 — SUPPLIED-SOURCE constraint | TradingView evidence | Offline reference material only | No runtime dependence on its private WebSocket, Pine/compiler, account, logo, news or quote services; actual market input is the specified Dukascopy data. |
| INT-03 — deferred, U12 | Existing run-bundle contract | No external run-bundle import/viewing in v1 | Future compatibility remains governed by the existing authored contract; own replay reports remain in scope. |
| INT-04 — scope resolved, U2 | Real broker execution / external alert delivery | Not required; live market data is separately included in INT-06 | No real order routing or alert delivery is required. |

## 12. Consistency requirements

These consistency obligations realize the selected data/trading/persistence behaviors. They specify business-visible coherence rather than transaction or retry mechanisms.

- **CONS-01:** Instrument, interval, side and revision labels must agree with displayed bars and dependent calculations after rapid selection changes. Obsolete results must not replace current results.
- **CONS-02:** Restore one coherent saved analysis state. Failed saves retain the prior successful state and expose unsaved work. Crash recovery is the last successful autosave; still-saving/unsaved work and previews can be lost (U13/P2).
- **CONS-03:** Interval synchronization must not repeatedly propagate one user action or duplicate chart state. A chart that cannot support a selected interval exposes that limitation explicitly.
- **CONS-04:** Discovery/backfill cannot duplicate observations or silently replace conflicting selected values. Use validated eligible sources and final-over-provisional current history; preserve original saved-run inputs/results.
- **CONS-05:** A replay step exposes mutually consistent bar/study/cursor state and uses no future information. Gaps and unequal timeframe coverage remain visible.
- **CONS-06:** Permit one writable tab; other tabs cannot overwrite its work. Source updates must not mix revisions in a resumed saved run.
- **CONS-07 — selected trading outcome:** Re-evaluation/restart cannot duplicate fills. Fill, remaining position/protection, commission and USD-account effects reconcile as one business outcome. Alerts are excluded; no transaction/retry mechanism is prescribed.
- **CONS-08 — selected data outcome:** Backfill/reconnection cannot duplicate bars or silently conceal conflicting observations. Partial recovery retains usable history with explicit progress/failure and unresolved-gap state.
- **CONS-09 — KNOWN, U2/U3/U9/U10:** Preserve supplied stored-timeframe history; final Dukascopy history supersedes provisional live-built data in application-owned current history, with affected supported-period derivatives updated. Do not wholesale rebuild unrelated stored history or alter saved-run original inputs/results.
- **CONS-10 — selected event-order outcome:** Apply historical events once in established order; process eligible existing orders before new cursor decisions. Do not claim a tick path when evidence cannot order it; use labelled ASM-01 for unresolved SL/TP chronology. Chart redraw cadence must not change fills/accounting.
- **CONS-11 — KNOWN, U4/U9:** Identical selected inputs/policies reproduce the same labelled stop-first result on reload. Newly available ticks are a catalog revision, not authority to rewrite a saved run's evidence/results.
- **CONS-12 — KNOWN, U5/U13:** Modifying/cancelling/closing cannot duplicate execution or affect the wrong hedged position. Fill, remaining size, protective exits and account result agree; existing orders are evaluated before subsequent cursor decisions, which cannot cancel a fill retroactively.
- **CONS-13 — KNOWN outcome, U6:** Confirmed rewind makes cursor, retained trading actions, orders, positions and account history agree at the new historical point. Cancelled rewind changes none of them. No removed later action may survive as an orphaned fill, commission or balance adjustment.
- **CONS-14 — KNOWN, U8/U13:** Paused conversion cannot leave a fill missing its matching position/commission/USD effects. Resume the original historical event after resolution, once, without moving it to a later price.
- **CONS-15 — KNOWN outcome, U9:** Saved cursor, actions, orders, fills, positions, USD account history, settings and selected input revision restore coherently. Concurrent arrival of new catalog history must not cause a resumed run to mix old results with new inputs or lose its saved orders.
- **CONS-16 — KNOWN outcome, U10:** Finalizing current history can update only the current catalog and newly selected runs, not the original inputs of a resumed saved run. Synchronized replay panels must agree on the historical information boundary even when instruments/timeframes have different observation times or coverage limits.

## 13. Security requirements

- **SEC-01 — KNOWN repository constraint:** Captured target DOM/text is untrusted evidence. Do not execute or embed captured target HTML in the product or dossier viewer.
- **SEC-02 — SUPPLIED-SOURCE, S3:** Treat data files, manifests, labels and imported analysis as untrusted inputs; malformed content cannot execute code or authorize arbitrary file access.
- **SEC-03 — SUPPLIED-SOURCE, S3/U2:** No TradingView credentials or copied session cookies are required. If Dukascopy access needs credentials, protect them from browser exposure, exported layouts, logs and dossier artifacts. No credential has been requested in chat or inspected. Account access is for data, not real trading.
- **SEC-07 — KNOWN authority boundary, U3:** A Dukascopy live account supplies market-data access only for this version. Historical simulation must never submit or amend actual broker orders or use live-account balances as simulated cash. Credentials are supplied during application setup, not embedded in requirements.
- **SEC-04 — local trust boundary, U2/U13:** Protect the sole analyst's local data and mutation authority; no remote/shared/tenant access is part of v1. Imported/captured content cannot grant write authority, and credentials are excluded from backups and report exports.
- **SEC-05 — scope resolved, U2:** Arbitrary user scripts and external webhook/alert delivery are excluded, so this version does not require their execution or delivery permissions.
- **SEC-06 — KNOWN source handling:** Do not propagate private captured account figures or script/account identities into product fixtures. Existing masked derivatives are not byte-identical original evidence.

## 14. Scale/performance drivers

| ID | Dimension | Evidence / accepted target | Status |
| --- | --- | --- | --- |
| SCALE-01 | Market universe | Ten assets × eight bar timeframes; 7,281 bar Parquet/manifest pairs | KNOWN — D1 |
| SCALE-02 | History volume | 45.19 million declared M1 rows; 25.62 million tick footer rows; approximately ten years of bar file periods | KNOWN metadata totals; not all data must be loaded at once |
| SCALE-03 | Accepted resident benchmark and response targets | Two charts, 100k resident bars/chart; four study panes and 100 drawings total. Initial viewport <2 seconds once inputs are local/ready; interaction p95 <50 ms; live display within 1 second of local receipt. Record desktop hardware during validation. All available archive history remains navigable without date/row/retention caps. | KNOWN — U13/U14; performance benchmark, not a mandated cache size/architecture. |
| SCALE-04 | Users/charts/device | One local user; at most two simultaneous charts; desktop mouse/keyboard, no mobile | KNOWN — U2/U12 |
| SCALE-05 | Acquisition lifetime/provider recovery | Acquire while the app runs; catch up at startup/reconnect. No 24/7 closed-app acquisition or guaranteed provider outage/publication recovery time. Show progress/failure and keep existing history usable. | KNOWN — U14; provider/session evidence verified before implementation acceptance. |

## 15. Operational requirements

- **OPS-01 — KNOWN boundary, U2:** One local-user application uses network access for Dukascopy live/history data. Existing local history remains readable when data services are unavailable; no requirement for fully offline operation of every workflow is asserted.
- **OPS-02 — selected failure outcome, U10/U12:** Missing/unreadable/corrupt data identifies the affected selection/reason without corrupting unrelated saved work. Preserve originals and use reported-gap/pause behavior; do not repair shared ingestion inputs silently.
- **OPS-03 — KNOWN, U13/P2:** Manual backup/restore includes analysis and saved trading runs with required input versions, excluding credentials. Crash recovery restores the last successful autosave; unsaved/saving work and previews may be lost. Single-writer behavior and destructive-action confirmation bound editing conflicts; run reproducibility must survive restore.
- **OPS-04 — selected data outcome, U9/U10:** Changed/incomplete data cannot masquerade as an unexplained market event. Expose producer status and actual coverage; a stopped historical dataset does not establish market closure or freshness.
- **OPS-05 — excluded, U2:** No alert-monitoring, scheduling or notification delivery availability requirement applies.
- **OPS-06 — KNOWN, U2/U14:** Fill the history-to-current gap, including after interruption, while the app runs and on startup/reconnect. Preserve separate session/closure/recovery/failure states; no fabricated bars. Provider publication/network recovery has no guaranteed duration; keep usable history readable and show progress/failure.
- **OPS-07 — KNOWN, U9:** Reuse retained application-owned history after restart and resume the last saved replay trading progress without requiring a repeat download of unchanged acquired bars. Data acquisition or autosave failure must not alter the sibling ingestion originals or corrupt a previously saved run.

## 16. Evolution/change drivers

- **EVO-01 — KNOWN, D1/D3:** Ingestion is adding files and tick history is incomplete. Additional months and transition from daily staging parts to finalized tick months must not silently change the selected analysis inputs.
- **EVO-02 — KNOWN, U9/U13:** New longer/shorter asset/provider histories must be discoverable without hardcoded dates and without changing saved-run meaning. This does not add another provider/live implementation to v1; future providers retain explicit identity and compatible coverage discovery.
- **EVO-03 — KNOWN scope pressure, S1–S3:** The reference inventory is much wider than the dataset-backed baseline. Scope additions need explicit data/semantic requirements rather than enabling an icon as evidence of completeness.
- **EVO-04 — KNOWN, U3:** More assets will have tick data in future. Required tick-data discovery and intrabar order resolution must work for those assets based on available coverage, rather than special-casing SP500. This does not automatically add new chart periods or require all assets to possess ticks.
- **EVO-05 — KNOWN future direction, U3:** Volume profiles and other tools that require detailed data are planned for later versions. Current tick consumption is restricted to necessary intrabar execution detail; future analytics require their own data semantics and acceptance criteria.
- **EVO-06 — KNOWN future direction, U4:** A future mechanism will download missing data, including missing tick evidence, and update a permanent local database. Current missing-tick handling is local-only with labelled stop-first fallback for unresolved SL/TP order. This future requirement does not select the database, physical schema or synchronization mechanism, and does not defer this version's existing M1/H1 gap-filling requirement.
- **EVO-07 — KNOWN deferral, U7:** Extra slippage modelling is deferred entirely. A future version may separately specify an execution model if requested; local tick availability alone does not justify enabling it now.

## 17. Confirmed assumptions

User-confirmed decisions are requirements in their owning sections. The two assumptions below remain deliberate simulation approximations, explicitly accepted with their consequences; they are not unaccepted product unknowns. Neither claims recovered real-market execution, and no fixed-M1-only execution baseline is required.

| ID | Assumption | Why needed | Consequence if false | Acceptance |
| --- | --- | --- | --- | --- |
| ASM-01 | When eligible SL and TP ordering remains unknowable from usable finer stored bars and local ticks, apply stop-first and label the result. | The available historical data may not establish the intrabar path. | Simulation may report a stop loss where a true tick sequence would have shown take-profit first; results must remain identifiable as policy-based. | Explicitly accepted by user — U4. Does not override established ordering or determine unknown fill prices. |
| ASM-02 | Eligible orders fill fully without liquidity-driven partial fills/queue simulation; eligible bar-based limit touches fill at the limit when no better first-eligible gap quote is established. | This version lacks reliable historical book/queue evidence but must support deterministic historical trading. | A real broker might fill less, later or not at all; simulation fills remain identifiable as policy/evidence-based approximations. | Explicitly accepted by user — U11. Manual partial closure remains supported; never overrides order eligibility, limit bounds or unresolved-data-gap pauses. |

## 18. Unresolved non-blocking questions

| ID | Question | Why non-blocking / owner |
| --- | --- | --- |
| UNK-01 | Exact visual similarity, typography, colors and panel dimensions? | S1/S2 screenshots constrain later UI work; user/UI design before final visual acceptance. |
| UNK-02 | Initial chart symbol, timeframe, theme and watchlist order? | User-configurable defaults do not currently change high-level semantics. |
| UNK-03 | Undo depth and keyboard shortcuts beyond observed commands? | Bounded UI behavior; settle before interaction implementation. |
| UNK-04 | Precise drawing parameters, indicator input bounds, export resolution and range-preset mappings? | Requires UX/domain refinement within an accepted feature subset. Unsupported periods must already remain explicit. |
| UNK-05 | Custom watchlists/templates and additional chart/sync styles? | Can remain deferred if baseline scope is accepted. |
| UNK-19 | Verify exact live-account API/authentication and account-specific asset access. | Implementation evidence obligation, not an unresolved product/API-mechanism requirement: live-account feed is mandatory and must be verified before enabling live mode. Failed access leaves historical mode usable with an explicit live limitation; it does not authorize demo substitution or waiving live integration. Owner: integration discovery before implementing/accepting live access. |
| UNK-20 | Verify per-instrument session/closure evidence and historical publication/retrieval completion behavior. | Product precedence, gap pauses, history scope, original-event resumption and P3 runtime limits are explicit. Provider details require integration evidence; never infer closure from silence or authorize unexplained-gap trading. Owner: integration validation before accepting live/backfill behavior. |

## 19. Blocking architectural unknowns

**None.** All architecturally significant product decisions identified during elicitation are resolved, explicitly deferred from v1, or covered by accepted assumptions ASM-01/ASM-02. UNK-19/UNK-20 remain provider-specific evidence obligations in Section 18; they do not waive required live/backfill behavior or claim that access has been tested.

### Resolution register

| Stable question ID | Final disposition | Authority |
| --- | --- | --- |
| UNK-10 | Historical trading included; scripting/alerts excluded. | U2 |
| UNK-11 | One local user, local application with Dukascopy live/history network access. | U2 |
| UNK-12 | Completed-bar replay; evaluate existing orders before new decisions; next-event eligibility; one historical clock; confirmed rewind removes subsequent actions. | U6/U10/U13 |
| UNK-13 | Exactly eight stored periods; bid default, ask selectable; complete recovered boundary candles without wholesale history replacement. | U2/U3 |
| UNK-14 | Layout/instrument-scoped drawings survive trading rewind; autosave/resume; one writable tab; confirm delete/reset; manual backup/restore and last-successful-autosave crash recovery. | U9/U12/U13 |
| UNK-15 | Validated completed bars/valid local ticks; report unusable intervals; preserve otherwise valid zero-volume/weekend rows and source originals. | U12 |
| UNK-16 | USD, hedging, no margin, configurable balance/sizing/specifications, commission bases, risk rounding/costs, fill policies, nonfuture conversion and blocked-event resumption as specified in FR-27/FR-38–FR-54. | U4–U13; ASM-01/ASM-02 |
| UNK-17 | External completed-run import/viewing deferred; own trading results retained. | U12 |
| UNK-18 | P3 accepted: complete dynamically bounded history; 100k resident bars/chart is a benchmark only; agreed desktop latency/runtime targets below. | U13/U14 |
| UNK-19 | Live-account/API access is an implementation validation obligation, with explicit historical-mode fallback on access failure and no demo/provider substitution. | U3; Section 18 evidence boundary |
| UNK-20 | Final history precedes provisional data; unexplained gaps pause trading; known closures traverse normally; provider-specific closure/publication evidence remains for integration validation. | U10/U13/U14 |
| UNK-21 | Retain acquired history in application-owned local files, leaving sibling ingestion files unchanged. | U9 |
| UNK-22 | Local ticks only; missing-tick acquisition/permanent database updates deferred. | U4 |
| UNK-23 | All extra slippage modelling deferred; spread/gaps/next-event prices still affect baseline fills. | U7 |

### Accepted closure packages

| Package | Accepted requirements | Practical limit |
| --- | --- | --- |
| P1 — execution, U13 | Completed-bar advancement; existing orders before new decisions; triggered stops become market orders; SL/TP resized after partial closure and cancelled on full closure; reject invalid/over-close quantity; no percentage-risk sizing at nonpositive balance; nonfuture bid/ask conversion; pause missing conversion/session data and resume the original historical event after resolution. | No fills against processed history or invented rates. Stop gaps can worsen price. Fixed quantity still requires valid inputs, with no margin model. Mathematical rounding is deterministic and documented. |
| P2 — recovery, U13 | Single writable tab; delete/reset confirmation; manual analysis/run backup and restore with required input versions and no credentials; last-successful-autosave crash recovery. | Unsaved/saving work and previews may be lost; successfully saved state must remain coherent. Backup need not include unrelated market history, but must retain inputs required by included runs. |
| P3 — quality/runtime, U14 | Two desktop charts; benchmark 100k resident bars per chart, four study panes and 100 drawings across the workspace; initial viewport <2 seconds once inputs are local/ready; interaction p95 <50 ms; live display within 1 second of local receipt. Acquire while the app runs; catch up on startup/reconnect. Record benchmark hardware. | All available archive history remains accessible beyond the resident set, with no hardcoded dates or retention cap. No 24/7 acquisition while closed or guaranteed provider outage/publication recovery time. Show progress/failure without making existing history unusable. |

### Integration evidence boundary

Verify the actual Dukascopy live-account API/authentication, supported instrument access, session/closure metadata and history publication behavior before accepting live/backfill implementation. This requirements handoff does not authorize account connection, expose credentials, select an API mechanism, or claim tested entitlements. If required access fails, preserve usable history and explain the live limitation; do not substitute demo/another provider or declare the required live feature complete. These are implementation feasibility/acceptance checks against explicit requirements, not unresolved product scope.

## 20. Requirements contradictions and resolutions

| ID | Conflict / source | Resolution | Status |
| --- | --- | --- | --- |
| CON-01 | Old dossier/ancestor instructions omit `dukascopy/` in dataset paths. U1 and current files include it. | Use current U1/D1 root; keep historical evidence unchanged. | Resolved |
| CON-02 | Reference SPX and local USA500IDXUSD are different provider identities. | No equivalence/copied calendar is assumed; explicit editable simulation specifications define units/value and missing required values pause trading. | Resolved identity/specification policy — U3/U11 |
| CON-03 | Earlier anonymous RSI/drawing/layout gates versus later successful authenticated workflows. | S2 supersedes only the tested account-gated conclusions. Neither implies complete numerical or workflow parity. | Resolved |
| CON-04 | Broad reference menus versus finite first-version scope. | U2 includes historical trading and excludes alerts/scripting; no automatic full parity commitment. | Resolved feature boundary |
| CON-05 | Stored timeframes have unequal coverage and final/live values can disagree. | Keep stored-history basis, fill gaps/complete affected boundaries, use final-over-provisional current history and freeze saved-run inputs. | Resolved policies — U3/U9/U10 |
| CON-06 | Local proposal's example Resolution type omits MN1, but U1 mandates monthly data. | MN1 is a required timeframe. Example implementation types are not requirements authority. | Resolved |
| CON-07 | Source aggregation preserves UTC boundaries; reference SPX uses a New York session. | Preserve supplied UTC semantics and identify the provider; no claim of matching session-based SPX bars. | Resolved |
| CON-08 | Producer statuses are GOOD/COMPLETE, but month spans can be incomplete and some rows have zero volume/weekend timestamps. | U12 requires validated eligible data and reported unusable intervals; otherwise valid zero-volume/weekend rows are preserved. Status labels alone never establish continuity. | Eligibility policy resolved — U12 |
| CON-09 | Reference website may retain live panels during replay; U2 requires live data and historical trading in one product. | U10 selects a common historical cursor for all replay panels, including watchlists/details; later/live quotes remain hidden. Alerts are excluded. | Resolved — U10 |
| CON-10 | Suggested millisecond application model versus nanosecond bars and exact completed-run contract. | Preserve source precision; external completed-run viewing is deferred by U12 and any future implementation retains contract authority. No application time representation mandated here. | Resolved — U12 |
| CON-11 | Earlier offline-only proposal versus U2 live connection and history API catch-up. | U2 supersedes offline-only scope. Local saved history remains the initial foundation; network inputs extend it. | Resolved |
| CON-12 | U2 permits recalculation for gap filling but says use stored timeframes as supplied. | U3 confirms retaining exactly eight periods and preserving existing history except newly recovered/affected boundary bars. | Resolved — U3 |
| CON-13 | U2 describes historical M1/H1-only inputs; official JForex history documentation describes broader capabilities. | Treat M1/H1 as this version's chosen candle-acquisition contract, supported by existing downloaders, rather than a provider-wide limitation. Exact live access remains separate. | Scope distinction resolved; access UNK-19 |
| CON-14 | Fixed-M1 execution was proposed, but U3/U4 require bar rendering and selective detailed evidence. | Use finer available stored bars before local ticks; labelled stop-first only if eligible SL/TP ordering remains unknown. P1 supplies the remaining cursor/execution rules. | Resolved — U4/U13; ASM-01 |
| CON-15 | Present tick files only cover SP500 versus U3 future tick assets. | Inventory stays a dated observation; tick capability is based on asset/date coverage and must support future additions. Volume profiles remain future scope. | Resolved — U3 |
| CON-16 | U2 requires M1/H1 gap filling; U4 defers missing-tick downloads/permanent database updates; U9 requires retained acquisition files. | Current M1/H1 bar acquisition and file-based reuse are in scope; store in application-owned local files without changing sibling data. Automatic missing-tick acquisition/permanent database mechanism remains future work. | Resolved scope/ownership — U4/U9 |
| CON-17 | Reference broker capabilities include margin/leverage, but U5 selects no margin checks. | Historical simulation omits margin-based rejection/liquidation; configurable balance and position sizing remain required. Live-account access does not import real account constraints or balances. | Resolved — U5 |
| CON-18 | Stop-first assumption can be misread as a guaranteed stop-price fill. | U4 selects event ordering when unknown; U5 separately requires gap-crossed SL at first executable bid/ask, even at a worse price. | Resolved — U4/U5 |
| CON-19 | Opposite-side order could be interpreted as a closing trade. | U5 selects independent hedging for entries; full/partial manual closure explicitly targets an existing position. | Resolved — U5 |
| CON-20 | Earlier question proposed configurable account currency; U6 explicitly fixes USD. | USD is the sole accounting currency and cannot be changed. Non-USD instrument results need historical conversion, not relabelling; U8 pauses the affected execution if conversion is unavailable. | Currency and missing-rate behavior resolved — U6/U8 |
| CON-21 | U6 considers optional slippage with ticks; U7 explicitly defers it entirely. Gap SL pricing and next-event fills can still be worse than the reference price. | No added slippage/delay model in this release. Retain historical spread, gaps and next-event movement in baseline pricing; local ticks remain intrabar evidence, not an automatic execution adjustment. | Resolved — U5–U7 |
| CON-22 | Rewind could preserve or branch later trades, changing account outcomes. | U6 requires confirmation, removal of subsequent trading actions and recomputation at the earlier cursor; no automatic branch required. | Resolved — U6 |
| CON-23 | Current catalog corrections could silently alter resumed simulation outcomes. | U9 preserves each saved run's original selected data and results. Updated history is used for new runs or an explicit restart, not automatic recalculation. | Resolved — U9 |
| CON-24 | Provisional live-built bars can disagree with later final history. | U10 selects final Dukascopy history for current history/new runs. Apply corrections in application-owned history while preserving sibling originals and saved-run input revisions. | Resolved precedence — U9/U10 |
| CON-25 | Next-available-price gap fills might otherwise execute across unexplained missing market-hour observations. | U10 pauses trading at unexplained unresolved gaps; only known market closures retain normal next-available-price traversal. A labelled stop-first assumption cannot authorize crossing an unresolved data gap. | Resolved — U10 |
| CON-26 | Supported manual partial closure could be confused with automatic liquidity-based partial fills. | U11 includes targeted manual partial closure but assumes full fills for each eligible requested execution; no automatic liquidity/queue model is included. | Resolved — U11/ASM-02 |
| CON-27 | Risk percentage could omit commission or round quantity above the intended budget. | U11 includes configured entry/exit commission and downward increment rounding, rejecting below-minimum quantities. Gaps can still exceed planned loss. | Resolved — U11 |
| CON-28 | Reference captures include narrow/mobile-like layouts and larger chart menus, but U12 prioritizes v1. | Desktop mouse/keyboard only, at most two charts; no mobile or external completed-run import required now. | Resolved — U12 |
| CON-29 | 100k bars/chart might be mistaken for a history cap. | Complete available history has dynamic provider/asset/timeframe/side bounds. 100k is resident working-set benchmark only, without hardcoded dates or retention limits; P3 targets accepted separately. | Resolved — U13/U14 |

## 21. Quality-gate review and handoff

| Gate | Final assessment — revision 14 |
| --- | --- |
| Problem/scope | PASS — single-user desktop charting, historical trading, required live/backfill and explicit v1 deferrals. |
| Actors/authority/tenancy | PASS — one local analyst; live-account access is data only; no real orders, shared tenants or concurrent writers. |
| Business semantics | PASS — explicit evidence precedence, order/hedging/fill/sizing/cost/clock/rewind rules; accepted approximations remain labelled. Mathematical definitions/rounding and tool parameters must be documented in downstream design. |
| Data authority | PASS — full dynamically discovered history, unchanged sibling originals, application-owned acquisitions, final-over-provisional current history and frozen saved-run inputs/results. |
| Integrations | PASS for requirements — provider identity, direction, authority and failure behavior specified. Actual API/account/session/publication evidence is required before implementation acceptance, not claimed by this dossier. |
| Consistency/failure | PASS — coherent fills/positions/accounting, duplicate prevention, replay isolation, gap/conversion pauses, original-event resumption, autosave/rewind and backup/crash boundaries. |
| Security | PASS for scope — untrusted evidence/imports; protect local analysis and credentials; no secrets in backups, no captured HTML execution and no real broker order authority. |
| Scale/quality | PASS — P3 explicitly accepted. Two desktop charts, 100k resident bars/chart benchmark with complete historical navigation, four study panes/100 drawings, measurable viewport/interaction/local-feed targets and bounded acquisition lifetime. |
| Evolution | PASS — longer/shorter provider/asset histories, additional local tick assets, future profiles, missing-data/permanent database mechanisms and later external-run import recorded without adding them to v1. |
| Assumptions/contradictions | PASS — ASM-01 and ASM-02 explicitly accepted; contradiction register records final precedence. Remaining UI/parameter details and provider evidence obligations are visible and non-blocking for requirements handoff. |
| Architecture leakage | PASS — no framework, service/module decomposition, physical database, API endpoint, deployment or retry design mandated. Existing local source paths and user-selected application-owned file retention are constraints. |
| Convergence | CONVERGED_WITH_ACCEPTED_ASSUMPTIONS — no unaccepted architecturally significant product unknowns remain. Simulation assumptions are ASM-01/ASM-02. |

**Handoff:** Ready for conditional domain modeling under ASM-01 and ASM-02, followed by architecture/UI design using the explicit v1 scope and requirements IDs. Preserve all accepted data/trading/recovery rules and full-history coverage. Resolve Section 18's non-blocking design details at their owning stage and verify provider feasibility before accepting live integration. No application has been implemented, no architecture stack selected, and no live account connected by this requirements task.
