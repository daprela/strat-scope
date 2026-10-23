.PHONY: bootstrap run stop ready browser browser-vivaldi contracts contracts-check check test lint test-e2e test-db
export UV_CACHE_DIR := /tmp/strat-scope-uv-cache
export npm_config_cache := /tmp/strat-scope-npm-cache

bootstrap:
	python scripts/foundation.py bootstrap

run:
	python scripts/foundation.py run

stop:
	python scripts/service.py stop

ready:
	python scripts/service.py ready

browser:
	python scripts/open_browser.py

browser-vivaldi:
	STRAT_SCOPE_BROWSER=/usr/bin/vivaldi STRAT_SCOPE_BROWSER_ID=vivaldi python scripts/open_browser.py

contracts:
	python scripts/foundation.py contracts

contracts-check:
	python scripts/foundation.py contracts-check

lint:
	cd backend && uv run ruff check .
	cd backend && uv run ruff format --check .
	cd backend && uv run basedpyright
	npm --prefix frontend run typecheck
	npm --prefix frontend run lint
	npm --prefix frontend run format:check

test:
	cd backend && uv run pytest
	npm --prefix frontend run test -- --run

check: contracts-check lint test

test-e2e:
	python scripts/verify_lifecycle.py

test-db:
	python scripts/verify_store.py
