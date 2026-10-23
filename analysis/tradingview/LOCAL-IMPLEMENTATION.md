# Proposed local implementation and acceptance criteria

This document proposes an independently implemented, single-user application inspired by the inspected TradingView SPX Superchart. It is an implementation blueprint, not a claim about TradingView's internal architecture or recovered source. The initial product runs on localhost, imports user-supplied historical files, and works without network access. A licensed live-data provider adapter is a later extension.

The original anonymous captures established the chart workspace and registration gates for save, alerts, replay, Horizontal line (E13), and built-in RSI (E15); those historical results remain in the [public evidence index](evidence/index.json). Subsequent authenticated inspection demonstrated drawings, RSI, save/reload, synchronized layouts, replay, Pine compilation, and strategy reporting. It inspected alert forms and a connected paper simulator without creating alerts or submitting orders; no real broker was connected. See [authenticated findings](AUTHENTICATED-FINDINGS.md) and the [authenticated evidence index](evidence/authenticated-index.json) for A-series references and limitations. Formula equivalence remains unaudited. Local choices below remain proposed design, distinct from reference observations.

## 1. Architecture and responsibility boundaries

**Proposed stack:** React and TypeScript for application controls, Lightweight Charts for financial plotting, a local Node.js service for storage/import/background jobs, and SQLite for durable state. Pin dependencies and serve every runtime asset locally. Lightweight Charts supplies rendering and interaction primitives, but neither market data nor built-in indicators; those belong to this application. [Official product comparison](https://www.tradingview.com/charting-library-docs/latest/getting_started/product-comparison/)

Use one repository with explicit modules rather than independent microservices:

| Module             | Owns                                                          | Must not own                                                 |
| ------------------ | ------------------------------------------------------------- | ------------------------------------------------------------ |
| React workspace    | Panels, dialogs, keyboard focus, commands, active layout      | Canonical market data or authoritative cash balances         |
| Chart adapter      | Series, panes, viewport, coordinate conversion, event mapping | Domain state hidden inside renderer objects                  |
| Drawing engine     | Anchors, geometry, selection, hit tests, edit previews        | Persisting arbitrary canvas coordinates as financial anchors |
| Indicator engine   | Versioned formulas, dependency graph, computed series         | Reading data after the active replay clock                   |
| Local Node service | HTTP/WebSocket API, import, scheduling, durable transactions  | Provider secrets exposed to the browser                      |
| Market repository  | Symbols, sessions, datasets, canonical bars, revisions        | Inventing missing market observations                        |
| Simulation engine  | Replay clock, paper orders, fills, positions, accounting      | Using wall-clock quotes in a historical simulation           |
| Alert engine       | Rules, evaluation cursor, deduplication, trigger history      | Assuming a closed browser remains an executing process       |

The Node process can host these responsibilities in one executable. Separate modules keep data semantics testable without a browser. Use a browser Web Worker for long indicator recomputations and bulk drawing geometry only after measuring main-thread latency. Parse and validate large imports in a Node.js worker thread in the local service. Workers receive immutable arrays plus a generation ID; stale results are discarded after symbol, interval, or replay changes. Move no work to workers merely to add concurrency.

```text
Local files -> importer -> versioned market repository -> history/query API
                                             |              |
Provider adapter (later) -> normalized events +--------------+
                                             |
                                    clock-scoped event router
                                    /          |            \
                              indicators     alerts       paper broker
                                    \          |            /
                                 React workspace + chart adapter
                                             |
                                  SQLite workspace persistence
```

## 2. Canonical data contracts

Do not use a display label as instrument identity. `SP:SPX` and an identically named CFD are distinct instruments. Preserve provider/source identity, instrument type, quote value unit, currency where applicable, exchange, timestamp convention, session calendar, and adjustment policy. A local alias can map a provider symbol to a canonical instrument only through an explicit mapping review.

Observed network metadata in E01 (`ev_4472b012e0199b47fafc6549907cd5cc2516ea17b776c8c2c97f42d5219470fb`; [evidence index](evidence/index.json)) identified `pro_name: SP:SPX`, `full_name: SP_NAUTH:SPX`, `timezone: America/New_York`, session literal `0930-1610`, `pricescale: 100`, `minmov: 1`, `delay: 600`, `allowed_adjustment: none`, `is_tradable: false`, `value_unit_id: POINT`, and `provider_id: ice`. Preserve these as observed provider fields; normalize their meaning explicitly for a chosen dataset. Do not replace the session with generic NYSE 09:30–16:00 hours or convert POINT into an assumed USD currency. Provider calendar details and the chart's volume meaning remain unresolved by this metadata alone.

Use UTC Unix milliseconds at application/API boundaries, and ISO-8601 UTC strings for human-readable logs. A daily bar also carries its exchange-local trading date. Convert explicitly to the chart library's required representation in the chart adapter; never infer seconds versus milliseconds from digit counts. Store integer price units where practical, with decimal strings for values crossing JSON boundaries beyond safe integer range. SQLite integers and TypeScript `bigint` avoid floating-point money accumulation. Indicators may calculate in floating point but must state their output precision and comparison tolerance.

The following types are proposed contracts, not production code:

```ts
type EpochMs = number; // validated safe integer, UTC
type PriceUnits = string; // integer decimal, e.g. "612345" at scale 2
type Resolution = "1m" | "5m" | "15m" | "1h" | "4h" | "1d" | "1w";

interface Instrument {
  id: string;                    // stable local UUID
  source: string;                // "user-import" or provider ID
  sourceSymbol: string;          // e.g. "SP:SPX"
  kind: "index" | "stock" | "future" | "forex" | "cfd" | "crypto";
  valueUnit: string;             // observed SPX unit is POINT
  currency: string | null;       // only when separately established
  priceDecimalPlaces: number;
  tickSizeUnits: PriceUnits;
  quantityDecimalPlaces: number;
  volumeKind: "none" | "shares" | "contracts" | "ticks" | "provider";
  timezone: string;              // IANA, e.g. America/New_York
  calendarId: string;            // versioned session/holiday definition
  adjustment: "unadjusted" | "split" | "total-return" | "provider";
}

interface Bar {
  instrumentId: string;
  datasetRevision: string;
  resolution: Resolution;
  openTimeMs: EpochMs;
  closeTimeMs: EpochMs;          // exclusive boundary
  tradingDate: string;           // YYYY-MM-DD in exchange calendar
  open: PriceUnits; high: PriceUnits;
  low: PriceUnits; close: PriceUnits;
  volume: string | null;         // absent is not zero
  status: "open" | "final";
}

type MarketEvent = {
  id: string;
  streamId: string;
  sequence: number;              // monotonic within stream
  occurredAtMs: EpochMs;         // source event time
  receivedAtMs: EpochMs;         // local ingestion time
  origin: "import" | "live" | "replay";
  payload:
    | { type: "bar.upsert"; bar: Bar }
    | { type: "history.corrected"; revision: string; fromMs: EpochMs }
    | { type: "stream.status"; state: "ready" | "stale" | "disconnected" };
};
```

Do not claim that the inspected SPX volume is exchange-traded index volume. Import metadata must identify its meaning; show “unavailable” if absent. Validate `low <= open/close <= high`, increasing time boundaries, nonnegative volume, tick-size compatibility, duplicate keys, timezone interpretation, and conflicting revisions before commit. Reject ambiguous date formats and prompt for an explicit import mapping.

An import creates a manifest containing file SHA-256, original filename, parser version, selected timezone, column mapping, missing-value policy, source resolution, row counts, rejected rows, and dataset revision. Keep original files or immutable normalized extracts for reproducibility. Never silently fill holiday/session gaps. Aggregate larger bars from a declared base resolution using the exchange calendar, including DST and shortened sessions. Daily-to-hourly conversion is impossible and must be unavailable.

Proposed API shape: `GET /api/instruments`, `GET /api/bars?instrumentId=...&resolution=...&beforeMs=...&limit=...`, `POST /api/imports`, `GET /api/imports/:id`, and one `/api/events` WebSocket. Pagination returns an exclusive cursor plus `hasMore`; requests echo dataset revision. Live reconnect first backfills the gap, then resumes sequence-aware delivery. Corrections invalidate indicator/replay caches from the earliest affected dependency point. The documented Advanced Charts datafeed likewise distinguishes history from current-bar updates and independently scoped subscriptions; use those principles without copying its private network protocol. [Official Datafeed API](https://www.tradingview.com/charting-library-docs/latest/connecting_data/Datafeed-API/)

**Existing workspace adapter:** the ancestor trading project has Dukascopy bid/ask Parquet assets. One inspected SP500 M1 manifest identifies `USA500IDXUSD` and 8,640 rows covering 1–7 September 2026; its footer has UTC nanosecond timestamps and independent bid/ask OHLC/volume columns. Keep the raw timestamps and price sides in an import/source layer, validate any conversion into this interactive market model, and expose the chosen chart price basis. Never infer true midpoint extrema by averaging the sides' OHLC extrema. Preserve actual coverage despite monthly filenames. Existing UTC aggregation boundaries do not automatically match the SPX provider session. See [local context evidence](evidence/local-context.json).

The existing `contract-v1.0.0/` package governs completed backtest evidence, a distinct read-only use case. A future adapter for those bundles must preserve exact nanosecond time strings, knowledge-time/sequence reveal, producer binary64 values, authoritative reports, and declared indexes. It must not coerce evidence into the proposed millisecond/integer-price model or recompute stored indicators and outcomes. Keep this adapter separate from interactive calculations and simulation; the proposed contracts above do not supersede the authored run-bundle contract.

## 3. Chart, drawing, and command state

Persist application state independently of Lightweight Charts instances. Chart creation/destruction must not erase indicators or drawings. A chart record contains instrument, resolution, chart style, pane configuration, scale mode, timezone display, and viewport. Resolve viewport from stable time/price coordinates; never persist device-pixel positions.

Model drawings as versioned discriminated objects: trend line, horizontal/vertical line, ray, rectangle, text, Fibonacci retracement, brush, and position measurement. Each contains object ID, instrument scope, pane ID, financial anchors, style, visibility, lock flag, ordering, and tool-specific parameters. Distinguish a time anchor from a logical future-bar anchor so projections beyond known history survive aggregation and chart scrolling. Define whether drawings are per symbol or per layout; first release uses per-layout, per-symbol drawings.

Drawing interaction is a state machine: idle → tool armed → anchor placement → preview → committed; editing adds selected → drag preview → committed/cancelled. Escape cancels without history. Pointer capture prevents lost drags. One completed drag creates one command, not one per pointermove. Snap in screen space to nearest visible OHLC points within a documented threshold; store the resulting financial anchor. Strong magnet requires a valid candidate, weak magnet allows unsnapped placement. Hit testing, handle sizes, and line tolerances are specified in CSS pixels and tested at different pixel ratios. Series primitives offer an appropriate extension point for custom chart visualizations. [Official plugin architecture](https://tradingview.github.io/lightweight-charts/docs/5.1/plugins/intro)

Use a command journal with `execute`, `undo`, and `redo` effects over canonical state. Commands cover drawing add/edit/delete, chart style, indicator configuration, and relevant chart settings. Group compound actions transactionally. A new action clears redo. Do not include passive live ticks or viewport scrolling in undo unless expressly chosen. Persist resulting state; a bounded undo journal can be restored separately with schema/version checks. This design reproduces the observed style-change undo behavior without inferring TradingView's implementation.

Authenticated reference: a Horizontal line at 7099.39 supported undo/redo and appeared in Object tree; reload restored the drawing, then its coordinate was edited to 7100.00 and saved [A08–A09]. The edited coordinate was not independently reopened after another reload. Store editable financial coordinates independently of pixels. Two-chart interval synchronization changed both charts from daily to hourly; the two hourly charts survived saved reload [A19–A20]. Persistence of the sync policy itself was not separately retested. Persist synchronization per layout and propagate changes once. Underlying `aria-disabled` inputs still had keyboard-operable rows; reproduce coherent accessible semantics, not that inconsistency.

## 4. Indicator semantics and computation

Start with SMA, EMA, RSI, MACD, Bollinger Bands, and volume. Each definition declares formula version, inputs, source series, warm-up requirement, initialization, missing-bar policy, output names, overlay/pane placement, and incremental-update strategy. Templates reference definition versions; upgrading a formula must not silently alter a saved layout.

RSI reference inputs were 14/Close, divergence off, SMA smoothing length 14, BB standard deviation 2 (disabled), Chart calculation timeframe, and Wait for timeframe closes checked; style bands were 70/50/30 [A07]. RSI survived reload [A08]. The 15 October SPX daily data-window displayed RSI 51.94 and RSI-based MA 55.09 [A05]. These are captured outputs, not sufficient formula/warm-up fixtures.

Specify seeds mathematically. Proposed choices: SMA emits after `n` valid closes; EMA uses `alpha = 2/(n+1)` and seeds with the first `n`-close SMA; RSI uses Wilder smoothing seeded with mean gains/losses over the first `n` changes, with explicit zero-loss/flat-series rules; Bollinger Bands uses a stated population standard deviation; MACD uses the declared EMA seeds for both difference and signal. These are chosen local semantics, not verified equivalence with TradingView defaults. Verify against exported reference values before claiming parity.

Fetch prehistory for warm-up separately from the visible range. Show missing outputs before sufficient history, and identify truncated warm-up. Treat the latest open bar as provisional: recompute from the last committed state for each update rather than repeatedly adding the same bar. Commit once at close. Restarting with the same dataset must reproduce results within a documented tolerance. Pine has historical/realtime execution and rollback semantics that make this distinction necessary for faithful ports. [Official execution model](https://www.tradingview.com/pine-script-docs/language/execution-model/)

The initial system accepts built-in formulas and developer-authored TypeScript modules only. A Pine-looking editor is insufficient to claim Pine compatibility. Arbitrary user code would need isolation, resource quotas, a defined language/runtime, and a separate security review. Pine itself runs on TradingView servers and is absent from the embeddable libraries. [Pine overview](https://www.tradingview.com/pine-script-docs/welcome/)

An authored SMA20 Pine probe compiled and plotted 7738.79 [A21]; an indentation error produced CE10188 [A22], then a corrected strategy generated metrics and a trade list [A23–A24]. Observed compiler requests used `pine-facade` draft-save/translation endpoints; these are evidence, not a local integration dependency. Full parity requires diagnostics, compilation, calculation, order emulation, and reporting, separately from the editor. Treat observed report presets—bar close, four ticks/bar, one-tick execution delay, zero commission/slippage—as explicit versioned policies. No strategy-performance or historical-coverage validation followed.

## 5. Replay and separation of clocks

Replay owns a deterministic virtual clock, dataset revision, start cursor, current cursor, and speed. Its data gateway returns only bars/events observable at that cursor, including warm-up before the start. Truncate chart history, indicator inputs, comparison instruments, data-window lookups, and simulated execution through that gateway. Hiding future candles while calculations still see them is a lookahead defect.

For bar-only datasets, first release advances completed bars and states that intrabar paths are unknown. Do not fabricate tick replay. Pause, single-step, jump, restart, and return-to-live are explicit transitions. Backward seek resets and deterministically recomputes dependent state, or restores a compatible checkpoint then replays forward. Chart synchronization uses shared event time; lower-frequency charts expose only periods finalized under the selected policy.

Forward replay changed OHLC and RSI 66.57 → 61.45 [A14]; the hover-date field stayed unchanged, so it cannot identify the replay cursor. Keep cursor and hover separate. Speeds ranged 0.1–10 updates/second; exit offered optional Save Replay, and leaving unchecked restored current values [A14–A16]. Replay-session persistence is distinct from layout saving.

Use separate `live` and `replay:<sessionId>` stream IDs. Replay alerts and paper accounts are opt-in simulation resources and cannot mutate live rules/accounts. This is a deliberate local design choice. TradingView documents that ordinary server alerts, watchlist quotes, and broker/Paper Trading orders remain live during chart replay; label the difference clearly if the local product instead offers historical simulation. [Bar Replay behavior](https://www.tradingview.com/support/solutions/43000712747-bar-replay-how-and-why-to-test-a-strategy-in-the-past/)

## 6. Alerts and paper execution

Alert records contain rule version, instrument, resolution, stream scope, comparison operands, threshold, crossing direction, frequency, expiration, and enabled state. First release supports price crossings and indicator comparisons on confirmed bars. Define crossing as previous value on one side and current value on the other; equality behavior and first-sample behavior must be explicit. Record evaluation cursor and trigger ID transactionally so restart/reconnect cannot duplicate a notification. Browser notifications are delivery, not evaluation.

The observed grouped wizard supports Price or a selected Horizontal line, crossing direction/value, expiration, message, and delivery settings [A10–A12]. Price offers Once only/Every time (once per minute); line defaults to Once per bar. Model frequency by source and reference drawing identity, rather than copying a fixed threshold. The wizard was cancelled; rule creation, scheduling, notification delivery, and webhook execution remain unverified.

The Node service evaluates while running even if the browser closes. If the service or machine is stopped, realtime monitoring stops; after restart record the outage and distinguish historical catch-up triggers from timely triggers. Offline imports can support historical evaluation but cannot discover new prices. TradingView's server-side alerts continue after the webpage closes; full equivalent availability would require an always-running host. [Official alert lifecycle](https://www.tradingview.com/support/solutions/43000548327-will-alerts-work-if-tradingview-is-not-open-on-the-computer/)

Paper trading needs an explicit execution specification before implementation: accepted order types, tick rounding, quantity increments, commission, spread, slippage, trading hours, margin, shorting, and instrument tradability. SPX is an analytical index and must not automatically become an executable instrument merely because it charts successfully. Use a clearly marked synthetic simulation policy or a separately mapped tradable derivative.

The connected simulator explicitly rejected SPX: “Indices can't be traded directly” [A28]. OANDA EURUSD exposed Market/Limit/Stop, units, quote sides, TP/SL, time-in-force, and a DOM ladder [A29–A31]. Expose these from instrument/account capabilities; ladder presence does not prove fill mechanics. No orders or DOM actions were executed; private account balances are not reference fixtures.

Proposed bar-only baseline: an order submitted at a completed bar becomes eligible no earlier than the next bar; market orders fill at next open plus configured costs; limit/stop handling distinguishes gaps from intrabar touches. If stop loss and take profit both fall inside a bar, OHLC cannot establish which occurred first. Flag the fill as ambiguous and use a selected conservative policy, or require finer data. Store `executionPolicyVersion` on every fill. Never present invented fills as observed ticks. Order cancel/replace, fills, positions, cash, and realized P&L update in one SQLite transaction. Unique execution keys prevent duplicate fills after restart.

## 7. Persistence, offline operation, and local security

Use SQLite tables for instruments/calendars, datasets/imports/bars, workspaces/layouts/drawings/indicator instances, alert rules/triggers/cursors, replay sessions, paper accounts/orders/fills, and schema migrations. Every serialized document carries `schemaVersion`; every computed result carries formula/dataset/policy versions. Separate transient UI selection/hover from durable state.

```json
{
  "schemaVersion": 1,
  "workspaceId": "local-workspace-1",
  "revision": 12,
  "savedAt": "2026-10-15T09:00:00.000Z",
  "charts": [{
    "id": "chart-1", "instrumentId": "instrument-spx",
    "resolution": "1d", "style": "candles",
    "datasetRevision": "sha256:example",
    "indicators": [{"definition": "ema", "version": 1, "inputs": {"length": 20}}]
  }],
  "drawings": [],
  "executionPolicyVersion": "bar-conservative-v1"
}
```

Autosave uses a debounced transaction and a monotonic workspace revision. Show saved/saving/error state accurately. Migrations run before serving the UI, back up the previous database, and fail with recovery instructions rather than partially opening incompatible data. Keep migrations ordered and transactional where SQLite permits; test upgrade from a real previous-version fixture.

Bind HTTP/WebSocket listeners to loopback only. Verify `Host` and browser `Origin`, reject cross-origin state changes, require a per-launch local session token, and avoid permissive CORS. Keep provider credentials in the service environment or an OS credential store. Validate import paths and MIME/size limits; escape text labels and imported descriptions; apply a local-content CSP. No external analytics, CDN fonts, scripts, or startup calls are needed.

Deliver a single documented start command that opens the UI after a readiness check, reports port conflicts, and shuts down cleanly. Offline startup must work after installation with an imported fixture. Back up through SQLite's online backup mechanism or a quiescent database copy, preserving WAL consistency; export a manifest and optional source datasets. Provide an actual restore command and verify restored bars, layouts, and accounts. A raw copy of an actively written `.db` alone is not a reliable backup plan.

## 8. Acceptance matrix and staged build

These are proposed release criteria. They establish local behavior; TradingView parity requires matching captured references for the same dataset, settings, and market calendar.

| Area                                | Acceptance scenario                                                         | Required evidence                                                                                           |
| ----------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Instrument identity                 | Import SPX index and similarly named CFD                                    | Separate IDs, descriptions, sources, sessions; no silent substitution                                       |
| Import                              | Load valid, duplicate, malformed, DST and shortened-session fixtures        | Manifest totals reconcile; invalid rows reported; repeated import idempotent                                |
| Chart                               | Change daily ↔ hourly where source permits; candles ↔ line                  | Correct bars/OHLC legend; volume truthfully absent/present; undo restores style                             |
| Navigation                          | Pan, zoom, resize, reload                                                   | Stable anchored viewport, readable axes, no data corruption or duplicate subscriptions                      |
| Drawings                            | Place/edit/save/reload; undo/redo; proposed lock/hide/delete/cancel         | Match A08–A09 mechanics; separately verify remaining tools and anchors                                      |
| Indicators                          | Match A07 settings and A08 persistence; numerical fixtures/open-bar updates | Captured values alone do not establish seeds/warm-up or formula equivalence                                 |
| Scripting/reporting, if implemented | Compile, diagnose/recover, calculate, inspect trade list/properties         | A21–A24 establish mechanics; test numerical/execution policies independently                                |
| Layout synchronization              | Two charts, shared interval, save/reload                                    | Match A19–A20; no propagation loops; symbol/crosshair synchronization separately tested                     |
| Replay                              | Step and exit; proposed seek/restart/isolation tests                        | Match A14–A16; hover date separate; prove lookahead isolation independently                                 |
| Alerts                              | Match A10–A12 forms; test evaluator/reconnect/restart independently         | Creation/delivery unobserved; defined frequency and deduplication require local tests                       |
| Paper broker                        | Next-open fill, gap, cancel/replace, both-side intrabar touch               | Policy-versioned fills; ambiguity flagged; cash/positions reconcile                                         |
| Persistence                         | Crash during save, schema upgrade, concurrent tabs                          | Atomic state; migration backup; revision conflict handled explicitly                                        |
| Offline/security                    | Disconnect network and start; request API from foreign origin               | All local assets available; imported charts work; cross-origin mutation rejected                            |
| Backup                              | Back up during normal use and restore into clean directory                  | Dataset hashes and selected workspace/account totals match                                                  |
| Performance                         | 100k imported bars, four indicator panes, 100 drawings on recorded hardware | Proposed target: first viewport <2 s, interaction p95 <50 ms, no long task >200 ms during steady navigation |

Build in stages: **(1)** runnable local shell, import/validation, canonical data and candles/volume; **(2)** symbol/interval/style controls, viewport, persistence and verified indicator formulas; **(3)** core drawings, command journal, object management and keyboard behavior; **(4)** deterministic replay with isolation tests; **(5)** service-backed alerts and explicit outage reporting; **(6)** policy-versioned paper execution and accounting; **(7)** live provider integration, reconnect/corrections, additional tools and layouts. Each stage supplies a usable vertical slice plus the applicable acceptance evidence. Defer broad drawing catalogs, Pine compatibility, social feeds, screeners, and brokerage routing until their semantics and required data are separately specified.
