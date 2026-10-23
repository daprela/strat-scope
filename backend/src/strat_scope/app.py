"""One local TLS host; its endpoints expose infrastructure status only."""

import asyncio
import json
import os
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Header, HTTPException, Request, WebSocket
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send

from strat_scope.authority import Authority
from strat_scope.config import ORIGIN, Config
from strat_scope.diagnostics import Diagnostics
from strat_scope.retention import Store
from strat_scope.wire import (
    Authentication,
    Capability,
    ExactObservation,
    UpdateEnvelope,
)


class OriginBoundary:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return
        headers = dict(scope.get("headers", []))
        host = headers.get(b"host", b"")
        origin = headers.get(b"origin")
        valid = host == b"127.0.0.1:4111" and (
            origin is None or origin == ORIGIN.encode()
        )
        if scope["type"] == "websocket":
            valid = valid and origin == ORIGIN.encode()
        if not valid:
            if scope["type"] == "websocket":
                await send({"type": "websocket.close", "code": 1008})
            else:
                await JSONResponse({"detail": "origin denied"}, status_code=403)(
                    scope, receive, send
                )
            return
        await self.app(scope, receive, send)


def create_app(config: Config) -> FastAPI:
    authority = Authority()
    diagnostics: Diagnostics | None = None

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
        nonlocal diagnostics
        started = time.monotonic()
        config.validate()
        store = Store(config.store)
        diagnostics = Diagnostics(config.store)
        identity = config.store / "service.json"
        identity.write_text(
            json.dumps(
                {
                    "pid": os.getpid(),
                    "birth": Path("/proc/self/stat").read_text().split()[21],
                }
            )
        )
        diagnostics.emit("startup", "ready", (time.monotonic() - started) * 1000)
        try:
            yield
        finally:
            authority.revoke()
            identity.unlink(missing_ok=True)
            store.close()
            diagnostics.emit("shutdown", "stopped")
            diagnostics.close()

    app = FastAPI(
        title="Strat Scope Foundation",
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    app.add_middleware(OriginBoundary)

    @app.middleware("http")
    async def security_headers(
        request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
            "connect-src 'self'; img-src 'self' data: blob:; frame-ancestors 'none'; "
            "base-uri 'none'; form-action 'none'"
        )
        return response

    @app.get("/api/ready")
    def ready() -> dict[str, str | int]:
        return {
            "status": "infrastructure-ready",
            "business_features": "not-implemented",
            "diagnostic_dropped_events": diagnostics.dropped if diagnostics else 0,
            "diagnostic_rotations": diagnostics.rotations if diagnostics else 0,
        }

    @app.post("/api/bootstrap", response_model=Capability)
    def bootstrap(
        request: Request, x_foundation_bootstrap: Annotated[str, Header()] = ""
    ) -> Capability:
        if request.headers.get("origin") != ORIGIN or x_foundation_bootstrap != "1":
            raise HTTPException(403, "bootstrap denied")
        try:
            lease = authority.claim()
        except PermissionError:
            raise HTTPException(
                409, "writer already claimed; restart required"
            ) from None
        return Capability(token=lease.token, epoch=lease.epoch)

    def authenticate(token: str, epoch: str, purpose: str) -> None:
        try:
            authority.check(token, epoch, purpose)
        except PermissionError:
            raise HTTPException(403, "capability denied") from None

    @app.get("/api/status", response_model=UpdateEnvelope)
    def status(
        authorization: Annotated[str, Header()] = "",
        x_owner_epoch: Annotated[str, Header()] = "",
        x_capability_purpose: Annotated[str, Header()] = "",
    ) -> UpdateEnvelope:
        authenticate(
            authorization.removeprefix("Bearer "), x_owner_epoch, x_capability_purpose
        )
        return UpdateEnvelope(epoch=authority.epoch)

    @app.post("/api/revoke", status_code=204)
    def revoke(authentication: Authentication) -> None:
        authenticate(authentication.token, authentication.epoch, authentication.purpose)
        authority.revoke()

    @app.websocket("/api/updates")
    async def updates(websocket: WebSocket) -> None:
        await websocket.accept()
        try:
            raw = await asyncio.wait_for(websocket.receive_text(), timeout=5)
            if len(raw) > 1024:
                raise ValueError("oversized authentication")
            authentication = Authentication.model_validate_json(raw)
            authority.check(
                authentication.token, authentication.epoch, authentication.purpose
            )
            await websocket.send_text(
                UpdateEnvelope(epoch=authority.epoch).model_dump_json()
            )
            # Status delivery is bounded; reconnect always authenticates afresh.
            await websocket.close(code=1000)
        except ValueError, PermissionError, TimeoutError:
            await websocket.close(code=1008)

    # Publish envelope/value definitions without introducing a business endpoint.
    original_openapi = app.openapi

    def openapi() -> dict[str, object]:
        schema = original_openapi()
        components = schema.setdefault("components", {}).setdefault("schemas", {})
        exact = ExactObservation.model_json_schema(
            ref_template="#/components/schemas/{model}"
        )
        components.update(exact.pop("$defs", {}))
        components["ExactObservation"] = exact
        return schema

    app.openapi = openapi
    app.mount("/", StaticFiles(directory=config.assets, html=True, check_dir=False))
    return app
