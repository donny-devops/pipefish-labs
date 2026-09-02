# Changelog — PipeFish Labs

All notable changes to the PipeFish Labs autonomous multi-agent platform and SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.4.0] — 2026-09-02

### Added
- **Native Mistral Handoffs**: Standardized 8-node asynchronous DAG state transitions to Mistral's native tool-call handoffs with persistent state and zero middleware routing overhead.
- **Managed MCP Connectors**: Deployed Model Context Protocol (MCP) servers for least-privilege scoping across Kubernetes (HPA autoscaling) and HashiCorp Vault enclaves.
- **Built-in Research & Audit Tools**: Added Mistral Document Library RAG tool & Websearch connector to the Research Agent and Code Interpreter Python sandbox to the Analysis Agent.
- **Reference MCP Server (`sdk/mcp_server.py`)**: Standard stdio JSON-RPC 2.0 server supporting `trigger_agent_graph`, `get_agent_spec`, `verify_enclave_status`, `k8s_autoscale_check`, `vault_lease_issue`, `ebpf_kernel_profile`, and `db_zdr_query`.
- **TypeScript / Node.js SDK (`sdk/pipefish_sdk.ts`)**: Type-safe client package `@pipefish-labs/sdk` with union typings for all 22 agent scenario graphs.
- **Unified CLI (`sdk/cli.py`)**: `pipefish` command line interface for graph simulation, MCP serving, webhook signature validation, and compliance audit reporting.
- **Cryptographic Webhook Verifier (`sdk/webhook_verifier.py`)**: HMAC-SHA256 signature verification with 300s timestamp drift replay protection.
- **Enterprise Helm Chart (`charts/pipefish-agent-mesh/`)**: Production Kubernetes deployment chart with non-root security context, read-only rootfs, and Cilium NetworkPolicy.
- **eBPF Falco Rules (`security/falco_rules.yaml`)**: Cloud-native runtime threat detection for Zero-Data Retention enclaves and PQC key protection.
- **Coraza WAF Configuration (`security/coraza_waf_rules.conf`)**: OWASP CRS inspection rules for agent webhook signatures and payload sizes.
- **AsyncAPI 3.0 Contract (`sdk/asyncapi.yaml`)**: Real-time streaming API specifications for NATS JetStream, Kafka, and WebSockets.
- **Terraform Infrastructure (`terraform/`)**: IaC templates for AWS Nitro Enclaves, VPC isolation, and automated KMS key rotation.
- **Interactive API Documentation Portal (`sdk/index.html`)**: Developer documentation hub matching PipeFish Labs design system.
- **Automated CI/CD Pipeline (9 Workflows)**:
  - CodeQL SAST Analysis
  - Gitleaks & Mistral API Key Secret Scanner
  - Trivy Container Security Scanner
  - Spectral OpenAPI 3.1 Linter
  - Lychee Site & Docs Link Checker
  - Python SDK Unit Test Suite
  - DOM & Media Integrity Verification
  - Google Lighthouse CWV & SEO Audit
  - SLSA Level 3 Build Provenance
