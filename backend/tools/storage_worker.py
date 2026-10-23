"""Real-process interruption/barrier fixture; never used by the service."""

import os
import sys
from pathlib import Path

from strat_scope.retention import Store

store = Store(Path(sys.argv[1]))
if sys.argv[2] == "hold":
    print("owned", flush=True)
    _ = sys.stdin.readline()
else:

    def frontier(name: str) -> None:
        if name == sys.argv[2]:
            print(name, flush=True)
            _ = sys.stdin.readline()
            os._exit(77)

    _ = store.publish("alpha", 1, "next", b"new", store.epoch, frontier)
store.close()
