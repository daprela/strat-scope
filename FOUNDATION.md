# Local foundation

This installation serves **https://127.0.0.1:4111**. It exposes infrastructure
readiness only. Market data, chart workspace tasks, provider connections, replay,
trading and saving product work are not implemented.

From the repository root:

```bash
make bootstrap       # frozen Python/npm installation and local frontend build
make run             # foreground TLS service; one worker, exact loopback port
make ready           # chain/hostname validation using the installed public CA
make browser         # graphical Chromium profile verified for this installation
make browser-vivaldi # separately verified Vivaldi profile
make stop            # identity-checked shutdown; verifies that the listener closes
```

`make run` stays in its terminal. Run the other commands from another terminal.
Ctrl+C also stops the foreground service. An occupied port is an error; the host
does not select an alternative address, port or insecure protocol.

`make browser-vivaldi` opens `/usr/bin/vivaldi` with the dedicated
`~/.local/share/strat-scope/vivaldi-profile`; it never reuses the user's
ordinary Vivaldi profile. Vivaldi's direct DevTools automation is currently
unstable on this host, so its browser-specific certification remains pending.

The persistent store and TLS files live under `~/.local/share/strat-scope/`, outside
the synced checkout. `STRAT_SCOPE_STORE`, `STRAT_SCOPE_CERT` and `STRAT_SCOPE_KEY`
are service-only overrides. Reject unsafe roots and escaping symlinks before use.
Keep an active store on a tested local filesystem. Never put private keys, live
state or browser-profile contents in the source tree or evidence distribution.

The installed certificate covers IP SAN `127.0.0.1`. Its local CA is installed in
the user's legacy and XDG NSS databases. Graphical Chromium's persistent profile
at `~/.local/share/strat-scope/browser-profile` was verified with normal certificate
validation; `make browser` opens that profile. Other browser profiles are not
certified by these checks. Vivaldi verification attempts failed at browser
startup/DevTools integration and are not counted as passes.

System-wide CA installation required an unavailable sudo password and was not
performed. `make ready` uses the installed public CA explicitly; this is validated
TLS, not disabled validation. The separate graphical-browser check proves user
trust independently. OS clients that rely solely on the system CA bundle will
need administrator installation of the public root:

```bash
sudo install -m 0644 ~/.local/share/strat-scope/tls/root.crt /etc/pki/ca-trust/source/anchors/strat-scope-local.crt
sudo update-ca-trust extract
```

`python scripts/install_host.py --trust-user` provisions the user installation
idempotently. Add `--renew` before the leaf's one-year expiry; stop/relaunch the
service afterward. The existing CA is preserved. `--trust-system` invokes the
Fedora administrator commands above. Public fingerprints, SAN and validity are
safe to inspect; never copy or publish either private key.

The approved application toolchains are CPython 3.14.8 with the conventional GIL,
Node 24.18.0, React 19, TypeScript 6, Vite 8 and Lightweight Charts 5.2.1. Exact
dependency versions are in `backend/uv.lock` and `frontend/package-lock.json`.
The OpenAPI generator lives in an isolated npm tooling workspace because its
released peer dependency is TypeScript 5. Application compilation stays on
TypeScript 6; there is one root npm lockfile and installation. No peer-dependency
bypass is used. Library license/attribution files are locally distributed under
`frontend/public/licenses/`; full installed package license identities are in
`foundation-evidence/installation.json`.

The service validates Host/Origin and issues a purpose-bound, in-memory capability
to the first tab. It expires after 300 seconds. Disconnect, expiry, revocation and
a second tab do not grant a replacement writer. Restart the service to obtain a
fresh owner epoch. WebSocket authentication travels in a bounded first message,
never a URL. This status-only bootstrap does not supply business mutation APIs.

SQLite uses FULL synchronization, DELETE journaling and tracked SQL migrations.
An OS-held lock excludes competing processes. Immutable content is flushed and
verified before a scoped metadata transaction; operation identities reconcile a
lost acknowledgement. Publication updates preserve unrelated scopes and prior
retained content. No cleanup/reclamation or business schema is implemented yet.
Physical tests cover process interruption and injected failures on the installed
store's filesystem; they do not certify hardware power loss or malicious OS changes.

Verification commands:

```bash
make check           # contracts, strict types/lint/format, backend and frontend tests
make test-db         # temporary fixtures on the installed store's actual filesystem
make test-e2e        # service must be stopped; graphical TLS, restart and browser probes
```

Browser checks use installed Chromium. Set `STRAT_SCOPE_BROWSER` to another exact
compatible executable and rerun verification when changing it. Playwright's
configured release browser can be installed separately if needed. `make browser`
must use the same executable that was verified.

Renderer probes are isolated at `frontend/tests/browser/probe.html`, served only by
the test server. They retain 100k synthetic buckets per chart while paging vendor
buffers, with four study-like panes and 100 drawing primitives. They preserve
exact original strings and real UTC buckets while testing paired Bid/Ask geometry,
absence, native hover, resize/disposal and native image export. Performance starts
before fixture construction; interaction timing is fenced by actual canvas draw
counters; receipt timing requires the new bucket to appear in drawn geometry.
These fixtures certify neither provider integration nor product UI/financial truth.
Future product exports still need their approved source labels and UI evidence.

Sanitized results, failed earlier renderer measurements, screenshots, native image
exports, TLS profile/chain facts and physical-store observations are retained in
`foundation-evidence/`. `backend/.venv/bin/python scripts/collect_evidence.py`
refreshes public installation/source identities and evidence checksums. This work
does not modify dossier authorities or generated dossier artifacts, so their
viewer/checksums/ZIP are unchanged.
