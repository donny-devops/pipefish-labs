# Security Policy & Vulnerability Disclosure — PipeFish Labs

PipeFish Labs is committed to maintaining the highest security standards across our autonomous multi-agent orchestration platform, Model Context Protocol (MCP) connectors, and Zero-Trust confidential enclave architectures.

## Supported Versions

| Version | Supported          | Security Fix SLA |
| ------- | ------------------ | ---------------- |
| 2.x.x   | :white_check_mark: | < 24 hours (P1)  |
| 1.x.x   | :x:                | Best Effort      |

## Reporting a Vulnerability

If you discover a potential security vulnerability within `pipefishlabs.io` or the `donny-devops/pipefish-labs` repository:

1. **Email Confidential Reports**: Send details to `security@pipefishlabs.io` or `adonis@pipefishlabs.io`.
2. **Encrypt Sensitive Payloads**: Use our PQC ML-KEM-768 / GPG master key when transmitting proof-of-concept exploits.
3. **Include Response Details**: Please include affected component versions, steps to reproduce, and potential impact assessment.

## Vulnerability Remediation SLAs

- **P1 Critical (Enclave Breach / Secret Exposure / Remote Code Execution)**: Immediate patch & release within 24 hours.
- **P2 High (DAG Handoff Spoofing / RBAC Bypass)**: Resolution within 72 hours.
- **P3 Medium/Low (Telemetry Drift / Minor Anomaly)**: Addressed in next scheduled release cycle.

## Automated Security Protections

Our CI/CD pipeline enforces:
- **CodeQL SAST & Security Analysis** (`.github/workflows/codeql.yml`)
- **Gitleaks Pre-Commit Secret Scanning** (`.github/workflows/secret-scanning.yml`)
- **DOM & Media Integrity Verification** (`scripts/verify_dom_integrity.py`)
