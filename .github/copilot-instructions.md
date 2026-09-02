# GitHub Copilot Custom Repository Instructions — PipeFish Labs

## Project Overview
PipeFish Labs is an enterprise autonomous multi-agent orchestration and zero-trust security platform. The repository contains Python and TypeScript SDKs, reference MCP servers, an interactive 8-node simulator, Helm charts, and infrastructure definitions.

## Key Architectural Directives for Copilot

1. **Native Mistral Handoffs**:
   - Always use tool-call handoffs (`handoff_mode: "mistral_native"`) rather than custom message bus middleware when connecting adjacent agent nodes.
   - Preserve execution context and pass cryptographically signed state envelopes (`HMAC-SHA256` or `NIST FIPS 203 ML-KEM-768`).

2. **Zero-Trust Tool Scoping (Model Context Protocol)**:
   - When generating or modifying tools for the `mcp_server.py`, ensure all inputs are validated with JSON Schema.
   - Never expose raw database write credentials or root container privileges. Use short-lived Vault token leases (TTL <= 300s).

3. **Zero-Data Retention (ZDR) Compliance**:
   - Never write sensitive payload data or customer PII to persistent disk.
   - Use RAM-backed storage (`/tmp` tmpfs or SQLite `:memory:`) and apply `ZDRFilesystemScrubber.secure_scrub_file` before process exit.

4. **Code Quality & Testing**:
   - Python: Strictly adhere to Python 3.10+, PEP 8, and include Google-style docstrings and explicit type hints.
   - When adding new functionality, always create corresponding unit tests under `tests/test_*.py` using standard `unittest`.
   - Never delete or bypass existing DOM integrity checks in `scripts/verify_dom_integrity.py`.
