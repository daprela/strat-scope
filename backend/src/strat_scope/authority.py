"""Process-lifetime capability. Expiry/disconnect never confers takeover."""

import hmac
import secrets
import time
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Lease:
    token: str
    epoch: str
    purpose: str
    expires_at: float


class Authority:
    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self.clock = clock
        self.epoch = secrets.token_hex(16)
        self.lease: Lease | None = None
        self.claimed = False
        self.active = True

    def claim(self) -> Lease:
        if self.claimed or not self.active:
            raise PermissionError("writer already claimed; restart required")
        self.claimed = True
        self.lease = Lease(
            secrets.token_urlsafe(32),
            self.epoch,
            "foundation-status",
            self.clock() + 300,
        )
        return self.lease

    def check(self, token: str, epoch: str, purpose: str) -> None:
        lease = self.lease
        if (
            not self.active
            or lease is None
            or not hmac.compare_digest(token, lease.token)
            or epoch != self.epoch
            or purpose != lease.purpose
            or self.clock() >= lease.expires_at
        ):
            raise PermissionError("capability denied")

    def revoke(self) -> None:
        self.active = False
        self.lease = None
        self.epoch = secrets.token_hex(16)
