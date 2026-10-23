"""Service-only configuration and owned-root confinement."""

import os
from dataclasses import dataclass
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[3]
ORIGIN = "https://127.0.0.1:4111"


def owned_root(path: Path) -> Path:
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("owned root must be an absolute canonical local path")
    resolved = path.resolve()
    if resolved != path or resolved == Path("/") or resolved in REPOSITORY.parents:
        raise ValueError("unsafe owned root")
    if resolved.is_relative_to(REPOSITORY):
        raise ValueError("runtime state must be outside the synced checkout")
    return resolved


def confined(root: Path, relative: str) -> Path:
    target = root / relative
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("invalid relative path")
    if target.resolve() != target or not target.is_relative_to(root):
        raise ValueError("symlink or path escape")
    return target


@dataclass(frozen=True)
class Config:
    store: Path
    certificate: Path
    private_key: Path
    assets: Path = REPOSITORY / "frontend" / "dist"

    def validate(self) -> None:
        owned_root(self.store)
        for path in (self.certificate, self.private_key):
            if not path.is_absolute() or path.resolve().is_relative_to(REPOSITORY):
                raise ValueError("TLS files must be absolute and outside source")
            if not path.is_file():
                raise ValueError("TLS files unavailable")
        if not (self.assets / "index.html").is_file():
            raise ValueError("build the local client before starting")

    @classmethod
    def from_environment(cls) -> Config:
        base = Path.home() / ".local" / "share" / "strat-scope"
        return cls(
            Path(os.environ.get("STRAT_SCOPE_STORE", str(base / "store"))),
            Path(os.environ.get("STRAT_SCOPE_CERT", str(base / "tls/server.crt"))),
            Path(os.environ.get("STRAT_SCOPE_KEY", str(base / "tls/server.key"))),
        )
