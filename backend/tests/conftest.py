from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from strat_scope.app import create_app
from strat_scope.config import ORIGIN, Config


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    assets = tmp_path / "assets"
    assets.mkdir()
    (assets / "index.html").write_text("<p>Technical fixture</p>")
    certificate = tmp_path / "certificate"
    certificate.touch()
    config = Config(tmp_path / "store", certificate, certificate, assets)
    with TestClient(create_app(config), base_url=ORIGIN) as instance:
        yield instance
