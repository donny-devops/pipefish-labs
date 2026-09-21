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
import errno
import http.server
import os
import socket
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


class QuietRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Serve files without writing request paths to stderr."""

    def log_message(self, format: str, *args: object) -> None:
        return


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


def port_bound(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        try:
            sock.connect((host, port))
        except OSError:
            return False
    return True


def probe_host(bind: str) -> str:
    if bind == "0.0.0.0":
        return "127.0.0.1"
    return bind


def serve_forever(bind: str, port: int, directory: Path) -> None:
    handler = partial(QuietRequestHandler, directory=str(directory))
    try:
        httpd = http.server.ThreadingHTTPServer((bind, port), handler)
    except OSError as exc:
        if exc.errno != errno.EADDRINUSE:
            raise
        wait_ready(port, probe_host(bind))
        print(f"preview already running on :{port}")
        return
    httpd.serve_forever()


def spawn_detached(bind: str, port: int) -> None:
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
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
    )


def wait_ready(port: int, host: str = "127.0.0.1", attempts: int = 50) -> None:
    for _ in range(attempts):
        if is_ready(port, host):
            print(f"preview ready on :{port}")
            return
        time.sleep(0.1)
    raise SystemExit(f"preview failed to start on :{port}")


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
    host = probe_host(args.bind)

    os.chdir(ROOT)
    ensure_dist()

    if is_ready(args.port, host):
        print(f"preview already running on :{args.port}")
        return 0

    if port_bound(args.port, host):
        wait_ready(args.port, host)
        return 0

    if args.foreground:
        serve_forever(args.bind, args.port, dist_dir())
        return 0

    spawn_detached(args.bind, args.port)
    wait_ready(args.port, host)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
