#!/usr/bin/env python3
"""
PipeFish Labs - Static Site Build

Assembles the publicly servable website into ./dist so that it can be uploaded
as Cloudflare Workers static assets.

This uses a strict allowlist. Only file types that belong on a public web server
are copied, so repository source (Python, Terraform, Rego, SQL, Helm charts,
Postman collections, tests, CI config) can never be published by accident.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# File extensions that are safe to publish.
ALLOWED_SUFFIXES = frozenset(
    {
        ".html",
        ".css",
        ".js",
        ".mjs",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".svg",
        ".webp",
        ".avif",
        ".ico",
        ".mp4",
        ".webm",
        ".woff",
        ".woff2",
        ".txt",
        ".xml",
        ".webmanifest",
        ".pdf",
    }
)

# Directories never walked, regardless of extension.
EXCLUDED_DIRS = frozenset(
    {
        ".git",
        ".github",
        ".githooks",
        ".wrangler",
        "__pycache__",
        "node_modules",
        "dist",
        "ansible",
        "bots",
        "charts",
        "db",
        "docs",
        "examples",
        "infra",
        "linkedin",
        "mcp",
        "postman",
        "sales",
        "scripts",
        "security",
        "src",
        "terraform",
        "tests",
    }
)

# Extensionless or otherwise non-allowlisted files that must still be published,
# as paths relative to the repository root.
EXTRA_FILES = (
    "CNAME",
    "_headers",
    "_redirects",
    "admin/config.yml",
    "sdk/openapi.yaml",
    "sdk/asyncapi.yaml",
)

# Cloudflare rejects any single static asset larger than this.
MAX_ASSET_BYTES = 25 * 1024 * 1024


def is_publishable(path: Path) -> bool:
    return path.suffix.lower() in ALLOWED_SUFFIXES


def iter_site_files(root: Path, out_dir: Path):
    """Yield repo-relative paths of every allowlisted file under root."""
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        # Never pick up a previous build, which would nest output inside itself.
        if out_dir == path or out_dir in path.parents:
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in relative.parts[:-1]):
            continue
        if not is_publishable(path):
            continue
        yield relative


def collect(root: Path, out_dir: Path) -> tuple[list[Path], list[str]]:
    files = list(iter_site_files(root, out_dir))
    seen = set(files)
    missing: list[str] = []
    for name in EXTRA_FILES:
        relative = Path(name)
        if not (root / relative).is_file():
            missing.append(name)
            continue
        if relative not in seen:
            files.append(relative)
            seen.add(relative)
    return sorted(files), missing


def build(root: Path, out_dir: Path) -> int:
    # rmtree below is destructive, so refuse anything that could be a real tree.
    if out_dir == root or out_dir in root.parents:
        print(
            f"error: refusing to use {out_dir} as the output directory",
            file=sys.stderr,
        )
        return 1

    files, missing = collect(root, out_dir)

    # _headers carries the site's Content-Security-Policy and HSTS. Shipping
    # without it would silently publish a site with no security headers, so a
    # missing entry fails the build instead of warning.
    if missing:
        for name in missing:
            print(f"error: required file is missing: {name}", file=sys.stderr)
        return 1

    if not files:
        print("error: no publishable files found", file=sys.stderr)
        return 1

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    total_bytes = 0
    oversized: list[tuple[Path, int]] = []

    for relative in files:
        source = root / relative
        size = source.stat().st_size
        total_bytes += size
        if size > MAX_ASSET_BYTES:
            oversized.append((relative, size))
        destination = out_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    if oversized:
        for relative, size in oversized:
            print(
                f"error: {relative} is {size / 1048576:.1f} MiB, over the "
                f"{MAX_ASSET_BYTES / 1048576:.0f} MiB Cloudflare asset limit",
                file=sys.stderr,
            )
        return 1

    # index.html and 404.html anchor the routing configured in wrangler.jsonc.
    for required in ("index.html", "404.html"):
        if not (out_dir / required).is_file():
            print(f"error: {required} missing from build output", file=sys.stderr)
            return 1

    print(f"Built {len(files)} files ({total_bytes / 1048576:.1f} MiB) into {out_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the static site into ./dist")
    parser.add_argument(
        "--out",
        default=str(ROOT / "dist"),
        help="output directory (default: ./dist)",
    )
    args = parser.parse_args()
    return build(ROOT, Path(args.out).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
