---
name: web-lcp-optimizer
description: >-
  Audits, diagnoses, and optimizes Largest Contentful Paint (LCP) and Core Web Vitals for static and edge-served web applications. Automates image conversion to modern WebP format, configures high-priority preloads, eliminates render-blocking CSS delays, manages edge caching headers, and enforces DOM integrity verification.
---

# Web LCP Optimizer

## Overview
The `web-lcp-optimizer` skill distills end-to-end performance engineering workflows for web applications into an automated, reproducible toolkit. It diagnoses LCP bottlenecks, converts oversized hero images to high-compression WebP assets, injects high-priority preloads, removes artificial animation render delays, and verifies edge caching headers and DOM integrity.

## Dependencies
- **`debug-optimize-lcp`**: Used for Chrome DevTools Core Web Vitals diagnostic traces, element timing breakdowns, and DevTools waterfall inspections.
- **`modern-web-guidance`**: Reference guidelines for modern layout, aspect-ratio rules, and responsive image syntax.

## Quick Start

Run an initial LCP audit on the entrypoint HTML:
```pwsh
uv run .agents/skills/web-lcp-optimizer/scripts/lcp_tool.py audit --html index.html --output scratch/lcp_audit.json
```

Verify LCP compliance and edge cache headers:
```pwsh
uv run .agents/skills/web-lcp-optimizer/scripts/lcp_tool.py verify --html index.html --headers-file _headers --output scratch/lcp_verify.json
```

## Utility Scripts

The skill includes a dedicated multi-command Python CLI script located at `.agents/skills/web-lcp-optimizer/scripts/lcp_tool.py`.

### 1. `audit`
Scans HTML and CSS for high-impact LCP bottlenecks, including video preloads in `<head>`, missing high-priority image preloads, legacy image formats, and CSS `opacity: 0` initial states.

```pwsh
uv run .agents/skills/web-lcp-optimizer/scripts/lcp_tool.py audit \
  --html index.html \
  --css assets/pfl.css \
  --output scratch/audit_results.json
```

### 2. `convert-images`
Converts high-resolution hero PNG or JPEG images into lightweight WebP format using Pillow with optimal compression settings.

```pwsh
uv run --with pillow .agents/skills/web-lcp-optimizer/scripts/lcp_tool.py convert-images \
  --input hero-logo.png \
  --output hero-logo.webp \
  --quality 85
```

### 3. `inject-preload`
Injects `<link rel="preload" as="image" href="..." type="image/webp" fetchpriority="high">` into `<head>`.

```pwsh
uv run .agents/skills/web-lcp-optimizer/scripts/lcp_tool.py inject-preload \
  --html index.html \
  --image-url /hero-logo.webp
```

### 4. `verify`
Verifies that all LCP criteria are met:
- `<picture>` tag referencing WebP source exists in HTML.
- `fetchpriority="high"` preload is active.
- Edge `_headers` contains long-lived public cache directives for `*.webp`.

```pwsh
uv run .agents/skills/web-lcp-optimizer/scripts/lcp_tool.py verify \
  --html index.html \
  --headers-file _headers \
  --output scratch/lcp_verify.json
```

## Workflow

1. **Diagnose**: Run `lcp_tool.py audit` against the target HTML and stylesheet. Inspect the generated JSON output for high-severity bottlenecks.
2. **Convert Assets**: For any hero images in PNG/JPEG format exceeding 100 KB, run `lcp_tool.py convert-images` to produce WebP counterparts.
3. **Configure Preloads**: Inject high-priority preloads with `fetchpriority="high"` and eliminate bandwidth-hogging media preloads (e.g., MP4 videos) from `<head>`.
4. **Remove CSS Render Delays**: Ensure above-the-fold hero elements render immediately on first paint (`opacity: 1 !important; transform: none !important;`).
5. **Configure Headers**: Ensure `_headers` grants a 30-day cache (`max-age=2592000`) for `/*.webp`.
6. **Verify & Test**: Run `lcp_tool.py verify` and repository regression checks (`scripts/verify_dom_integrity.py`).

## Rate Limiting
Not applicable. All file manipulations, image compression, and DOM checks operate locally on the workspace filesystem.

## Common Mistakes

1. **Preloading non-critical media**: Preloading videos or below-the-fold images starves the network connection of critical CSS and the LCP image. Only preload the single primary hero image.
2. **Missing dimensions on `<picture>`/`<img>`**: Omitting `width` and `height` attributes causes Cumulative Layout Shift (CLS) when the WebP loads.
3. **Leaving CSS opacity at 0**: Animating above-the-fold hero content with JavaScript or keyframes delays the LCP paint timestamp even if the image is cached. Always ensure immediate hero visibility.
