import json
from typing import cast

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from strat_scope.authority import Authority
from strat_scope.config import ORIGIN
from strat_scope.wire import Capability


def claim(client: TestClient) -> Capability:
    response = client.post(
        "/api/bootstrap", headers={"Origin": ORIGIN, "X-Foundation-Bootstrap": "1"}
    )
    assert response.status_code == 200
    return Capability.model_validate_json(response.content)


def test_foreign_bootstrap_and_second_tab_cannot_acquire(client: TestClient) -> None:
    for headers in (
        {},
        {"Origin": "https://foreign.invalid"},
        {"Origin": "null"},
        {"Origin": ORIGIN, "Host": "evil.invalid"},
    ):
        assert client.post("/api/bootstrap", headers=headers).status_code == 403
    capability = claim(client)
    assert (
        client.post(
            "/api/bootstrap", headers={"Origin": ORIGIN, "X-Foundation-Bootstrap": "1"}
        ).status_code
        == 409
    )
    assert capability.token not in client.get("/api/ready").text
    assert client.get("/api/ready").headers["cache-control"] == "no-store"


def test_http_and_ws_require_exact_capability_context(client: TestClient) -> None:
    capability = claim(client)
    headers = {
        "Authorization": "Bearer " + capability.token,
        "X-Owner-Epoch": capability.epoch,
        "X-Capability-Purpose": capability.purpose,
    }
    assert client.get("/api/status", headers=headers).status_code == 200
    for changed in (
        {"Authorization": "wrong"},
        {"X-Owner-Epoch": "old"},
        {"X-Capability-Purpose": "trading"},
        {"Origin": "https://foreign.invalid"},
    ):
        assert client.get("/api/status", headers=headers | changed).status_code == 403
    with client.websocket_connect(
        "wss://127.0.0.1:4111/api/updates", headers={"Origin": ORIGIN}
    ) as ws:
        ws.send_json(
            {
                "token": capability.token,
                "epoch": capability.epoch,
                "purpose": capability.purpose,
            }
        )
        message = cast(dict[str, str], ws.receive_json())
        assert message["status"] == "infrastructure-ready"
    for origin in ("https://foreign.invalid", "null"):
        with (
            pytest.raises(WebSocketDisconnect),
            client.websocket_connect(
                "wss://127.0.0.1:4111/api/updates", headers={"Origin": origin}
            ),
        ):
            pass
    with client.websocket_connect(
        "wss://127.0.0.1:4111/api/updates", headers={"Origin": ORIGIN}
    ) as ws:
        ws.send_text(
            json.dumps(
                {
                    "token": "wrong",
                    "epoch": capability.epoch,
                    "purpose": capability.purpose,
                }
            )
        )
        with pytest.raises(WebSocketDisconnect):
            ws.receive_text()
    auth = {
        "token": capability.token,
        "epoch": capability.epoch,
        "purpose": capability.purpose,
    }
    assert client.post("/api/revoke", json=auth).status_code == 204
    assert client.get("/api/status", headers=headers).status_code == 403


def test_expiry_and_disconnect_never_grant_takeover() -> None:
    now = [0.0]
    authority = Authority(lambda: now[0])
    lease = authority.claim()
    now[0] = 300.0
    with pytest.raises(PermissionError):
        authority.check(lease.token, lease.epoch, lease.purpose)
    with pytest.raises(PermissionError):
        authority.claim()
    authority.revoke()
    with pytest.raises(PermissionError):
        authority.check(lease.token, lease.epoch, lease.purpose)
