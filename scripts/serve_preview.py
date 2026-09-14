#!/usr/bin/env python3
"""Idempotent static preview of ./dist on port 8787.

Cloud Agent `start` runs this without flags: if nothing is listening, spawn a
detached server, wait until GET / succeeds, then return. `make serve` uses
`--foreground` so the process stays attached for local development.

This does not call Wrangler or Cloudflare. Use `make preview` when you need
edge routing, `_headers`, and `_redirects`.
"""

from __future__ import annotations

import argparse
import http.server
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from functools import partial
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PORT = 8787
DEFAULT_BIND = "0.0.0.0"
LOG_PATH = Path("/tmp/pfl-preview.log")


def dist_dir() -> Path:
    return ROOT / "dist"


def ensure_dist() -> None:
    if (dist_dir() / "index.html").is_file():
        return
    script = ROOT / "scripts" / "build_site.py"
    subprocess.check_call([sys.executable, str(script)], cwd=ROOT)


def is_ready(port: int, host: str = "127.0.0.1") -> bool:
    url = f"http://{host}:{port}/"
    try:
        with urllib.request.urlopen(url, timeout=1) as response:
            return 200 <= response.status < 500
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def serve_forever(bind: str, port: int, directory: Path) -> None:
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
    httpd = http.server.ThreadingHTTPServer((bind, port), handler)
    httpd.serve_forever()


def spawn_detached(bind: str, port: int) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log = open(LOG_PATH, "ab", buffering=0)
    subprocess.Popen(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "--foreground",
            "--bind",
            bind,
            "--port",
            str(port),
        ],
        cwd=str(ROOT),
        stdout=log,
        stderr=log,
        start_new_session=True,
        close_fds=True,
    )


def wait_ready(port: int, attempts: int = 50) -> None:
    for _ in range(attempts):
        if is_ready(port):
            print(f"preview ready on :{port}")
            return
        time.sleep(0.1)
    raise SystemExit(f"preview failed to start on :{port}; see {LOG_PATH}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--foreground",
        action="store_true",
        help="Stay attached (for make serve). Default detaches after ready.",
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--bind", default=DEFAULT_BIND)
    args = parser.parse_args()

    os.chdir(ROOT)
    ensure_dist()

    if is_ready(args.port):
        print(f"preview already running on :{args.port}")
        return 0

    if args.foreground:
        serve_forever(args.bind, args.port, dist_dir())
        return 0

    spawn_detached(args.bind, args.port)
    wait_ready(args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
