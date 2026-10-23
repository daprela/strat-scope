# Authenticated TradingView inspection — 16 October 2026

The logged-in session allowed direct verification of workflows that stopped at registration in the original investigation. **Drawings, RSI, save/reload, two-chart interval synchronization, historical replay, Pine compilation, and strategy reports now have working reference evidence.** Alert configuration and paper-trading interfaces were inspected; alert delivery and order execution were not exercised.

This update supplements the [original analysis](REPLICATION-ANALYSIS.md) and changes its coverage conclusions. The [local implementation guide](LOCAL-IMPLEMENTATION.md) incorporates the resulting behavioral requirements. The proposed local application is still an independent reconstruction; this investigation did not recover TradingView's source or build the application.

## Session, method, and evidence boundaries

REA discovered the user's existing authenticated chart tab. A second tab in the same browser shared its authentication. The generic SPX chart link initially resolved to an existing saved workspace, so a separate layout named **Codex inspection 2026-10-16** was created before chart mutations. The original tab was not used for those mutations. This also demonstrates that a generic chart URL and requested symbol do not alone specify the authenticated initial workspace. [A01–A03]

The update retains **35 controlled scenarios, 290 steps, and 27 selected screenshots**: 244 steps completed, 10 failed, and 36 were cancelled. These counts include scenario-start navigation and measure inspection activity, not application coverage. Failed locators, intercepted clicks, and later recoveries are retained. The [authenticated index](evidence/authenticated-index.json) maps A01–A35 to full REA Evidence IDs, declared actions, artifacts, outcomes, and limitations. E01–E18 remain the separate 15 October anonymous baseline.

The browser was an externally owned CDP target, not an isolated profile. REA reported Chromium version `8.2.4133.87`; CDP's product string was `Chrome/8.2.4133.87`. These are reported identities, not an independently verified engine build. A supplementary DOM read measured **1879 × 916, DPR 1**, despite the earlier scenarios requesting 1440 × 1000. Do not use the requested viewport as measured geometry. Early scenarios requested Asia/Bangkok emulation; later scenarios used the provider's UTC default. The chart displayed UTC+7. Browser emulation, chart display timezone, and instrument exchange timezone are separate settings.

The packaged [review derivative](evidence/authenticated-review.json) masks account names, existing layout identifiers, private script IDs, and account summary figures in text. Original Evidence IDs identify source records; each modified text artifact has a derivative digest and its original digest. Selected screenshots retain original pixels and ordinary signed-in UI. Screenshots of private account balances and EURUSD ticket margin values are excluded. The complete authenticated export remains outside the distributable package. No cookies, storage values, request/response bodies, header values, or authenticated WebSocket payloads were collected.

## What changed in the replication specification

| Capability | Authenticated observation | Local behavior to reproduce | Remaining boundary |
| --- | --- | --- | --- |
| Layouts | Create a named layout; save and reload RSI, drawings, and a two-chart arrangement | Durable layout identity, versioned chart state, loading/saving/saved/error feedback | Cross-device conflicts, deletion, sharing, autosave failure |
| Indicators | Built-in RSI added, configured tabs inspected, numeric outputs visible | Separate pane, versioned inputs, styling, timeframe visibility, readable data window | Independent formula/warm-up equivalence |
| Drawings | Place line, undo, redo, edit price to 7100, save, reload | Financial coordinates, command history, selection and edit dialog | All other drawing types, drag/snap/lock edge cases |
| Multi-chart | Two charts change from daily to hourly through interval sync | Per-chart state plus explicit shared sync policies | Crosshair/time/range sync and larger layouts |
| Replay | Select historical start, step forward, change menu state, leave replay | Historical clock, study recomputation, independent live quote state | Playback timing accuracy, replay trading/fills, saved replay restore |
| Alerts | Price/drawing conditions, frequency, message and notification forms | Typed condition model, context-sensitive trigger choices, scheduling | Creation, delivery, retries, restart persistence |
| Pine | Authored indicator and strategy compile; diagnostic and report states observed | Editor, compile states, executable study layer, strategy/report contracts | General Pine language compatibility and private scripts |
| Trading | Paper connection, nontradable SPX warning, EURUSD tickets and DOM | Capability checks, order draft state, instrument precision, account panels | Submit/cancel/amend/fill/reject lifecycle |

## RSI, indicator panes, and persistence

The indicator directory contains duplicate DOM identities for the favorite and technical-result entries of `STD;RSI`. Choosing the first matched built-in entry successfully added RSI. A pointer click on its settings control was intercepted by the canvas; keyboard activation of the same control opened the dialog. These failures reflect locator/interaction paths, not evidence that settings are unavailable. [A04–A07]

For the captured SPX daily state, the data window displayed close **7744.06**, RSI **51.94**, and RSI-based MA **55.09**. These are observation fixtures, not a proof of formula equivalence. A replacement must match the same provider history, corporate/session rules, initialization, warm-up, bar finality, and rounding before comparing outputs. [A05, A07–A08]

The inspected RSI settings were:

| Tab | Captured settings |
| --- | --- |
| Inputs | Length 14; source Close; Calculate Divergence unchecked; smoothing SMA, length 14; BB StdDev 2 disabled; calculation timeframe Chart; Wait for timeframe closes checked |
| Style | RSI and RSI-based MA plots; upper/middle/lower bands 70/50/30; background and overbought/oversold fills; precision Default; price-scale/status-line display options |
| Visibility | Ticks; seconds 1–59; minutes 1–59; hours 1–24; days 1–366; weeks 1–52; months 1–12; ranges |

The dialog was cancelled without changing these settings. Saving with Control+S and reloading restored the RSI pane, establishing persistence across a real page reload rather than merely keeping an in-memory component alive. Separate data, presentation, visibility, and timeframe policies are therefore useful in the local indicator schema. [A07–A08]

[RSI Inputs screenshot](screenshots/authenticated/A07-inputs-state.png) · [Style](screenshots/authenticated/A07-style-state.png) · [Visibility](screenshots/authenticated/A07-visibility-state.png)

## Drawings and command history

Selecting Horizontal line and clicking the plot created a line near 7099.39. Control+Z removed it, Control+Y restored it, and the Object tree listed the line beside the chart and indicators. A later reload retained the drawing. Double-clicking it opened settings; the Coordinates input was edited to **7100.00**, applied, and saved. Style included a price-label option. [A08–A09]

The local drawing record needs a price anchor with instrument identity and display precision. Screen coordinates are an input/rendering concern. Commands should record creation and coordinate edits, allowing undo/redo without duplicating objects. Serialization must preserve the drawing across reload independently of renderer object identity. These observations cover one horizontal line, not the full tool catalog.

[Drawing coordinates screenshot](screenshots/authenticated/A09-coordinate-state.png) · [Object tree](screenshots/authenticated/A08-objects-state.png)

## Multi-chart layouts and synchronization

A two-column layout successfully instantiated two SPX chart regions with studies. The underlying interval-sync switch reported `aria-disabled=true` and refused direct pointer activation, including through its label. Keyboard Enter on its containing row toggled selection; selecting one hour then changed **both** headers from 1D to 1h. A save and reload restored two charts. The layout was subsequently returned to one daily chart and saved. [A17–A20]

The original E04 one-chart disabled-switch observation must not be generalized into an account restriction. In the authenticated state, the row was usable through a different interaction path. A local implementation should provide consistent pointer and keyboard behavior and store interval synchronization as explicit layout state. Synchronizing symbols, crosshairs, clicked times, or visible ranges remains unverified.

[Synchronized chart screenshot](screenshots/authenticated/A19-synced-state.png) · [Restored two-chart layout](screenshots/authenticated/A20-restored-state.png)

## Historical replay

Bar replay exposed a historical start selector, play/forward controls, speed, and Replay Trading. Selecting a historical point changed the chart and indicator values; stepping forward changed OHLC and RSI again. In the captured step, RSI changed from **66.57 to 61.45** and its moving average from **71.73 to 71.37**. The data-window date remained a hover date, so it cannot establish the next replay timestamp. Last-day change continued to show live information. [A13–A14]

The speed menu listed 10x, 7x, 5x, 3x, 1x, 0.5x, 0.3x, 0.2x, and 0.1x, with labels from ten updates per second down to one every ten seconds. These labels were inspected; actual cadence was not benchmarked. Exiting opened **Leave current replay?**, an unchecked Save this replay option, and Leave/Stay choices. Leaving without saving returned the chart to current data. [A14–A16]

A local replay clock must bound bars and studies independently of the live quote stream. Crosshair date, replay cursor, last visible bar, and latest live quote must remain distinct. Otherwise a UI can look correct while simulations read future observations. Saved replay and replay order execution need further reference tests.

[Historical replay screenshot](screenshots/authenticated/A14-historical-state.png) · [Forward step](screenshots/authenticated/A14-forward-state.png) · [Speed options](screenshots/authenticated/A14-speed-options.png)

## Alert creation forms

Creating an alert while the horizontal line was selected preselected **Price / Crossing / Horizontal line** and showed a once-per-bar trigger. Opening an ordinary price alert showed **SPX / Price / Crossing / numeric value**, an additional-condition action, expiration, Message, and Notifications. The condition list exposed Crossing, Crossing Up, Crossing Down, and Show more. The ordinary price trigger menu distinguished Once only from Every time; its description says Every time triggers once per minute while the condition remains met. These semantics are specific to this captured condition context. [A09–A11]

Message opens an alert-name field, message editor, placeholder insertion, and Apply/Cancel. Notifications offered app, toast, email, webhook URL, sound and repetition, alternate plain-text email, and a notification schedule with muting outside that schedule. In the captured state app/toast were checked, email/webhook were unchecked, the URL input was disabled while webhook was off, and sound was 3 Notes Reverb once. No address or webhook was entered. [A11–A12]

No alert was created. The local design needs condition-dependent evaluation and frequency, expiration, templated messages, channel preferences, and a persistent scheduler if alerts run with the browser closed. Form presence supplies no evidence of delivery reliability, webhook protocol, server retry behavior, or quota semantics.

[Price alert screenshot](screenshots/authenticated/A10-alert-form.png) · [Trigger menu](screenshots/authenticated/A11-trigger-options.png) · [Notifications](screenshots/authenticated/A12-notification-state.png)

## Pine compilation and strategy reports

Only newly authored probe scripts were used. The untouched starter editor was replaced with this Pine v6 indicator:

```pine
//@version=6
indicator("Codex inspection SMA", overlay=true)
plot(ta.sma(close, 20), title="SMA20")
```

Add to chart compiled it and displayed SMA20 on the price chart and in the data window, with **7738.79** for the captured SPX state. This verifies an executing script path. It does not establish a local equivalent SMA result without a matching dataset. [A20–A21]

An initial crossover-strategy typing probe hit `CE10188` because the editor's autoindent placed the entered `plot` in local scope. This was an input construction issue; the UI correctly exposed a diagnostic and a no-trades state. A global-only mechanics probe then compiled successfully:

```pine
//@version=6
strategy("Codex inspection strategy", overlay=true, initial_capital=100000)
strategy.entry("L", strategy.long, qty=1)
strategy.close("L")
plot(ta.sma(close, 20), title="SMA20")
```

This deliberately simple script exercises report generation, not a meaningful trading strategy. The captured report showed total PnL, drawdown, trade count, profitable-trade fraction, profit factor, equity visualization, and performance-analysis areas. The displayed SPX report currency was **NONE**, so its numerical results must not be relabeled USD. Its displayed historical range was not independently validated. List of trades exposed entry/exit timestamps, prices, size, net PnL, return, Show on chart, column setup, and Download .csv. Download was not clicked. [A22–A24]

Strategy Properties exposed initial capital 100000, currency Same as chart, default size 100% equity, pyramiding 1, Default bar detalization (4 ticks/bar), On bar close execution, commission 0 Percent, 1x long/short leverage, slippage 0 ticks, limit orders at Requested price, and One tick order delay. The probe's explicit `qty=1` overrides its default order-size setting. The dialog was cancelled without changes. These settings are part of a reproducible backtest contract; an equity plot alone is insufficient. [A24]

[Strategy report screenshot](screenshots/authenticated/A24-report-state.png) · [Trades](screenshots/authenticated/A24-trades-state.png) · [Execution properties](screenshots/authenticated/A24-properties-state.png)

The [Pine network summary](evidence/authenticated-network-summary.json) records remote `pine-facade.tradingview.com` calls during these probes, including POST `/pine-facade/save/new_draft`, POST `/pine-facade/translate_light`, and permission/translation requests for private USER script identities, which are masked. No bodies or credential/header values were captured. The timing associates remote compilation and draft persistence with Add to chart; it does not recover compiler internals or establish where every study calculation executes. Compilation created remote draft state even without an explicit named Save or Publish. A local editor therefore needs its own supported interpreter/compiler or an explicit bounded script model.

## Paper simulation and order-entry surfaces

The broker chooser allowed connection to **Paper Trading**. No real broker connection or order submission was performed. An SPX order ticket stated **Indices can't be traded directly**, directing users toward derivatives. This confirms the capability warning anticipated from E01 metadata; visible Buy/Sell boxes do not establish tradability. [A25–A28]

Changing only the inspection chart to `OANDA:EURUSD` exposed a usable ticket: Buy/Sell quotes, Market/Limit/Stop modes, Units quantity, margin/leverage and pip-value information, take-profit/stop-loss exits, and order review/submit controls. Limit and Stop added price and time-in-force, with Week visible in this state. None of the submit actions were used. Market and Order mode were restored after inspection. [A29–A32]

DOM mode showed a price ladder with bid/ask levels and Flatten, CXL All, Reverse, Buy Mkt, and Sell Mkt actions. These were inventoried without activation. The account manager exposed Positions, Orders, Order history, Balance history, Activity log, Trade history, and Analytics, plus a position grid with prices, quantities, exits, PnL, leverage, margin, and expiration columns. Positions was empty. Other account tabs were not traversed. Existing simulator account figures were excluded from the review text and screenshots. [A31–A32]

The local implementation should separate a disposable order draft from a submitted order and keep replay simulation distinct from live paper trading. Contract size, tick size, quantity units, quote currency, margin, and supported order types belong to instrument/broker capabilities. Fill rules, partial fills, rejection, cancellation, amendments, accounting parity, and recovery remain open.

## Cleanup and outstanding verification

The inspection created a separate saved layout and remote Pine draft state. Alerts were cancelled rather than created; no orders or publications were submitted. The original chart tab was not selected for chart mutations. Multi-chart testing ended by saving the inspection layout as one daily chart; later Pine and symbol probes may have been autosaved by the application. Treat this inspection layout as disposable.

REA releases its CDP connection as `disconnected-external` and does not own the browser process. Several simulator-disconnection attempts failed because of transient menu state and selectors. Supplementary native browser interaction opened the Paper Trading context menu and invoked its broker **Log out** item; a later snapshot no longer showed the account manager. This was broker logout, not TradingView account logout. The browser endpoint temporarily became unavailable during tab cleanup. After reconnecting, the original EURUSD tab was verified still present and restored to the foreground, and the inspection tab was closed successfully. Final broker status was not independently confirmed by reopening its connection UI. The scratch layout/draft were not deleted. [A32–A35; supplementary cleanup notes]

The largest remaining parity obligations are full Pine compatibility, formula/history equivalence, all drawing tools, alert delivery and persistence, actual order lifecycle/accounting, saved replay, layout conflicts, watchlist editing, advanced chart types, and intermediate responsive/touch behavior. The original startup network capture remains bounded to E01. No original server/source implementation was recovered.

Regenerate the packaged authenticated extracts offline with:

```bash
python analysis/tradingview/extract_authenticated_evidence.py
python analysis/tradingview/build_viewer.py
```

The extractor validates derivative text and selected-image SHA-256 digests. It never executes captured page content. See [README.txt](README.txt) for package structure and [LOCAL-IMPLEMENTATION.md](LOCAL-IMPLEMENTATION.md) for the architecture and expanded acceptance criteria.
