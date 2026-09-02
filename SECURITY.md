# Security Policy

## Supported Versions

Security updates are currently provided for the following versions and branches of the `pipefish-labs` project:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Scope

This repository involves experimental AI agent architectures, asynchronous API integrations, and containerized deployments. We are particularly interested in reports concerning:

*   **Infrastructure:** Container escapes, exposed daemon vulnerabilities, or misconfigurations within our Docker and Kubernetes orchestration layers.
*   **Agentic Systems:** Prompt injection, context-window exploits, or unauthorized state-machine transitions in our AI workflows (e.g., Mistral AI integrations).
*   **Web Frameworks:** Authentication bypasses, connection pooling exploits, or injection flaws in our FastAPI and SQLAlchemy middleware.
*   **Cryptography:** Memory safety violations or non-constant-time execution in cryptographic modules.

## Reporting a Vulnerability

Please do not report security vulnerabilities through public GitHub issues. 

To report a vulnerability, please open a **Private Vulnerability Report** through the GitHub Security Advisory tab in this repository. 

You can expect an initial acknowledgment within 48 hours. If the vulnerability is accepted, we will keep you updated on the patching process, mitigate the issue in a private fork, and coordinate a timeline for a public disclosure and fix release.
