"""Direct Uvicorn TLS; one worker and no access log containing caller data."""

import uvicorn

from strat_scope.app import create_app
from strat_scope.config import Config


def main() -> None:
    config = Config.from_environment()
    config.validate()
    uvicorn.run(
        create_app(config),
        host="127.0.0.1",
        port=4111,
        workers=1,
        ssl_certfile=str(config.certificate),
        ssl_keyfile=str(config.private_key),
        access_log=False,
        ws_max_size=1024,
        server_header=False,
    )


if __name__ == "__main__":
    main()
