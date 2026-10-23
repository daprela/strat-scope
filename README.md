# Strat Scope

Strat Scope is an offline replication and implementation dossier for a TradingView-style chart workspace, with a target Dukascopy historical-trading experience. It records observed interface behavior, masked evidence, product
requirements, domain and architecture decisions, approved UI artifacts, and a local implementation blueprint.

The full trading application is not implemented yet. A runnable local TLS
foundation is available at `https://127.0.0.1:4111`, but it currently exposes
infrastructure status only. The generated viewer is a separate, static offline
reference site: it does not connect to TradingView, Dukascopy, or any other
network service, and it does not execute captured target HTML.

The goal of the project is to build a platform to validate  automated strategies through backtest and quantitative analysis.

The existing platforms that allow to do a similar analysis are expensive and their functionality limited for what I want to achieve.

The platform relies on historical data downloaded from Dukascopy and saved in parquet format. For license reasons I cannot add these data to this repository but they can be easily downloaded. Historical data from Dukascopy can go back over ten years and are available in 1m candles, 1H and even tick data. This allow an in-depth analysis over a period that is not normally available on other commercial platforms.

This repo started from a reverse engineer of Tradingview made through [REA](https://github.com/morluto/rea#how-rea-works) .

## Contents

The primary dossier lives in `analysis/tradingview/`:

- `REPLICATION-ANALYSIS.md` and `AUTHENTICATED-FINDINGS.md` document observed behavior and masked signed-in findings.
- `requirements-dossier.md`, `domain-model.md`, and `architecture-dossier.md` describe the proposed local product and its technical boundaries.
- `ui-dossier.md`, `visual-system.md`, and `ui-artifacts/` contain the UI design, wireframes, mockups, and review evidence.
- `LOCAL-IMPLEMENTATION.md` explains the proposed implementation approach.
- `evidence/` and `screenshots/` hold captured source material; treat it as untrusted data.
- `index.html` is the generated, searchable offline viewer.

`backend/` and `frontend/` currently contain project governance and initial
foundation work; they are not a complete application release.

## Prerequisites

- Python 3.14 is the validation environment; existing dossier scripts retain compatibility where possible.
- The `markdown` Python package is required only to generate the offline viewer. The evidence extractors use the standard library.
- The local foundation uses GNU Make, `uv`, Node.js 24, npm, and OpenSSL. Its
  exact dependency versions are locked in `backend/uv.lock` and
  `frontend/package-lock.json`.

An isolated environment is optional but recommended:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install markdown
```

## Prepare and run the local foundation

The local foundation serves the built frontend and infrastructure endpoints
over TLS at `https://127.0.0.1:4111`. It deliberately does not provide market
data, charting, replay, trading, or persistence product workflows yet.

Provision the local TLS identity once if it is not already installed. This
creates the store and private keys outside the checkout, under
`~/.local/share/strat-scope/`:

```bash
python scripts/install_host.py --trust-user
```

Install the locked dependencies and build the frontend:

```bash
make bootstrap
```

Start the service in one terminal:

```bash
make run
```

Then, from another terminal, validate it and open the verified browser profile:

```bash
make ready
make browser
```

`make ready` validates the TLS chain and hostname using the local public CA.
`make browser` opens the Chromium profile verified for this installation; other
browser profiles are not certified. Stop the service when finished:

```bash
make stop
```

`Ctrl+C` also stops the foreground `make run` process. The service uses only
the exact loopback HTTPS origin above; it does not fall back to another port or
an insecure HTTP listener.

### Make targets

| Command                | Purpose                                                                              |
| ---------------------- | ------------------------------------------------------------------------------------ |
| `make bootstrap`       | Install frozen backend and frontend dependencies, then build the frontend.           |
| `make run`             | Run the one-worker local TLS service in the foreground.                              |
| `make stop`            | Perform identity-checked shutdown and verify the listener closes.                    |
| `make ready`           | Check the local HTTPS readiness endpoint with TLS validation.                        |
| `make browser`         | Open the verified Chromium profile at the local HTTPS origin.                        |
| `make browser-vivaldi` | Open the separately verified Vivaldi profile at the local HTTPS origin.             |
| `make contracts`       | Regenerate the OpenAPI schema and frontend API declarations.                         |
| `make contracts-check` | Confirm generated schema and API declarations have no drift.                         |
| `make lint`            | Run backend lint, formatting/type checks, and frontend type/lint/format checks.      |
| `make test`            | Run backend and frontend unit tests.                                                 |
| `make check`           | Run contract verification, linting, and unit tests.                                  |
| `make test-db`         | Exercise durable-store behavior with temporary fixtures on the installed filesystem. |
| `make test-e2e`        | Run TLS lifecycle and browser probes; the service must be stopped first.             |

## Build the offline viewer

From the repository root, regenerate the dossier-derived indexes and viewer:

```bash
python analysis/tradingview/extract_evidence.py
python analysis/tradingview/extract_authenticated_evidence.py
python analysis/tradingview/build_viewer.py
python -m py_compile analysis/tradingview/*.py
```

For a full regeneration that also rebuilds the design artifacts and checks the mockups, run:

```bash
python analysis/tradingview/build_wireframes.py
python analysis/tradingview/build_mockups.py --all
python analysis/tradingview/check_mockups.py
```

Do not edit generated evidence indexes, HTML, SVGs, or screenshots in place when a maintained generator owns them. Rebuild `SHA256SUMS` and `analysis/tradingview/tradingview-replication-dossier.zip` after changing dossier contents or artifacts.

## Open a local session

Open [analysis/tradingview/index.html](analysis/tradingview/index.html) directly in a modern browser. No web server and no network connection are required.

The viewer links to local reports, evidence, screenshots, wireframes, and mockups. If browser file-access policies interfere with viewing an asset, serve the repository locally instead:

```bash
python -m http.server 8000
```

Then browse to `http://localhost:8000/analysis/tradingview/index.html` and stop the server with `Ctrl+C` when finished.

## Safety and provenance

Captured DOM, text, and JSON are evidence—not executable input. Keep source documents, captured evidence, and generated output separate; do not embed or run captured TradingView HTML. The archive is a dossier distribution rather than a standalone product-source release.

## Helpers

This project uses [trail-code](https://github.com/trailhq/Trail-Code) to save tokens and make the development work more efficient.
