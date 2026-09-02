# 🌐 PipeFish Labs — Enterprise AI Automation & Autonomous Multi-Agent Systems

[![CI - Verify DOM](https://github.com/donny-devops/pipefish-labs/actions/workflows/verify-dom.yml/badge.svg)](https://github.com/donny-devops/pipefish-labs/actions/workflows/verify-dom.yml)
[![CodeQL](https://github.com/donny-devops/pipefish-labs/actions/workflows/codeql.yml/badge.svg)](https://github.com/donny-devops/pipefish-labs/actions/workflows/codeql.yml)
[![Secret Scanning](https://github.com/donny-devops/pipefish-labs/actions/workflows/secret-scanning.yml/badge.svg)](https://github.com/donny-devops/pipefish-labs/actions/workflows/secret-scanning.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/donny-devops/pipefish-labs/blob/main/LICENSE)
[![Website](https://img.shields.io/badge/Website-pipefishlabs.io-blue)](https://pipefishlabs.io)

PipeFish Labs is the only firm delivering AI automation, zero-trust security, autonomous multi-agent systems, and strategic management consulting as a single integrated platform — powered by **Native Mistral Handoffs** and **Managed MCP Connectors**.

---

## ⚡ Key Platform Capabilities

- **Autonomous Multi-Agent Orchestration**: Asynchronous DAG state handoffs, 8-node live execution graphs, zero wait states, and payload validation.
- **Native Mistral Handoffs**: Tool-call state persistence across agent chains with cryptographically signed JSON payloads for seamless inter-agent communication.
- **Managed MCP Connectors**: Pre-built, security-audited Model Context Protocol connectors for CRM, EMR, ERP, Phone, Email, and custom enterprise systems.
- **Code Interpreter & Document Library RAG**: On-demand code execution sandbox and retrieval-augmented generation over enterprise document libraries.
- **Agentic Zero-Trust Governance & Identity**: mTLS identity rotation, HashiCorp Vault enclaves, least-privilege tool scoping, and SOC 2 Type II audit logging.
- **Automated Regulatory Compliance**: Embedded conformity controls aligned with EU AI Act Annex IV, CSRD sustainability reporting, and HIPAA rules.
- **High-Throughput Data & Automation**: Real-time stream telemetry, custom API middleware, and cross-stack integration across 20+ core technical disciplines.

---

## 🚀 Live Interactive Simulator

The platform includes an interactive 8-node multi-agent execution simulator supporting 20+ enterprise scenario graphs:

- **Receptionist Agent**: Multi-channel voice & text intake, call routing, and CRM sync.
- **Sales Enablement Agent**: Automated lead enrichment, contract generation, and deal recovery.
- **Growth Strategy Agent**: Product analytics monitoring, dynamic A/B page variant generation, and PLG scoring.
- **Execution Agent**: High-throughput distributed API execution and parallel subagent coordination.
- **Audit Agent**: Continuous cloud log collection, access policy verification, and SOC 2 evidence packaging.
- **Analysis Agent**: Stream telemetry ingestion, retention cohort calculation, and anomaly detection.
- **Research Agent**: SEC filing synthesis, market TAM/SAM analysis, and competitive moat evaluation.
- **Self-Improving Agent**: Reflection loops, DSPy algorithmic prompt tuning, and regression eval matrices.
- **System-Optimizing Agent**: eBPF kernel profiling, EXPLAIN plan tuning, and K8s HPA autoscaling.

---

## 🐍 Python SDK

The PipeFish Labs Python SDK (`sdk/pipefish_sdk.py`) provides programmatic access to the autonomous multi-agent orchestration platform with Native Mistral Handoffs.

```python
from sdk.pipefish_sdk import PipeFishAgentMesh

# Initialize the agent mesh client
mesh = PipeFishAgentMesh(api_key="your_api_key_here")

# Trigger an 8-node execution graph with Native Mistral Handoff state persistence
result = mesh.trigger_graph_execution(
    scenario_key="systemoptimizing",
    payload={"alert": "CPU latency spike on K8s ingress pod-491"}
)

print(result)
# {
#   "scenario": "systemoptimizing",
#   "status": "COMPLETED",
#   "nodes_executed": 8,
#   "handoff_mode": "Mistral Native Handoff (Tool Call State Persistence)",
#   "mcp_connectors_verified": true,
#   ...
# }
```

---

## 🛠️ Repository Architecture

| Path | Description |
|------|-------------|
| `index.html` | Main platform landing page & 8-node live interactive execution simulator |
| `demo/index.html` | Standalone multi-agent execution simulator interface |
| `sdk/pipefish_sdk.py` | Python SDK for programmatic agent mesh orchestration |
| `services-solutions/` | Service catalog, 20+ specialized solutions, and investment tiers |
| `case-studies-results/` | Documented case studies (HonuEco, Omnium International, Lubrexx) |
| `benefits-testimonials/` | Client testimonials and competitive differentiation matrix |
| `affiliates-corporate-partnerships/` | Co-build, referral, and technology ecosystem tracks |
| `blog/` | Engineering deep-dive articles |
| `assets/pfl.css` | Shared site-wide design system stylesheet |
| `.github/workflows/` | CI/CD pipeline definitions |

---

## 🔒 Security

PipeFish Labs takes security seriously. Our security posture includes:

- **Vulnerability Reporting**: See [SECURITY.md](SECURITY.md) for our responsible disclosure policy. Report vulnerabilities via GitHub Private Security Advisories.
- **CodeQL Static Analysis**: Automated semantic code scanning on every push and pull request to detect vulnerabilities before they reach production.
- **Gitleaks Secret Scanning**: Continuous scanning for hardcoded secrets, API keys, and credentials across all commits and pull requests.
- **SLSA Provenance**: Supply-chain integrity verification via [SLSA Level 3](https://slsa.dev) build provenance generated by the OpenSSF SLSA Generic Generator.
- **Zero-Trust Architecture**: mTLS identity, automated secret rotation via HashiCorp Vault, eBPF Falco threat IDS, and zero-data-retention AI enclaves.
- **Post-Quantum Cryptography**: Production-ready NIST FIPS 203 (ML-KEM-768) and FIPS 204 (ML-DSA) key encapsulation and digital signatures.

---

## ⚙️ CI/CD Pipeline

This repository is protected by four GitHub Actions workflows:

| Workflow | File | Purpose |
|----------|------|---------|
| **Verify DOM** | `verify-dom.yml` | DOM integrity validation for the platform landing page and simulator |
| **CodeQL** | `codeql.yml` | Semantic static analysis and vulnerability scanning |
| **Secret Scanning** | `secret-scanning.yml` | Gitleaks-based detection of hardcoded secrets and credentials |
| **SLSA Provenance** | `generator-generic-ossf-slsa3-publish.yml` | OpenSSF SLSA Level 3 supply-chain provenance generation |

---

## 📝 Engineering Blog

Deep-dive technical articles on enterprise AI architecture, security, and compliance:

- [Architecting Autonomous Multi-Agent Systems](https://pipefishlabs.io/blog/architecting-autonomous-multi-agent-systems/)
- [eBPF Falco Runtime Threat Detection for AI Workloads](https://pipefishlabs.io/blog/ebpf-falco-runtime-threat-detection-ai-workloads/)
- [EU AI Act Annex IV Conformity Guide](https://pipefishlabs.io/blog/eu-ai-act-annex-iv-conformity-guide/)
- [Model Context Protocol (MCP) Server Security](https://pipefishlabs.io/blog/model-context-protocol-mcp-server-security/)
- [Post-Quantum Cryptography Production Guide](https://pipefishlabs.io/blog/post-quantum-cryptography-production-guide/)
- [Zero-Data-Retention AI Enclaves for Enterprise Privacy](https://pipefishlabs.io/blog/zero-data-retention-ai-enclaves-enterprise-privacy/)
- [DAG State Handoff in Multi-Agent Execution](https://pipefishlabs.io/blog/dag-state-handoff-multi-agent-execution/)
- [Zero-Downtime SOC 2 Compliance Modernization](https://pipefishlabs.io/blog/zero-downtime-soc2-compliance-modernization/)

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. **Fork** the repository and create a feature branch from `main`.
2. **Follow** the existing code style and project conventions.
3. **Write** clear commit messages describing your changes.
4. **Test** your changes locally before submitting a pull request.
5. **Submit** a pull request with a description of what your change does and why.

Please review our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing. For security-related issues, follow the process outlined in [SECURITY.md](SECURITY.md) — do not open public issues for vulnerabilities.

---

## 📬 Connect & Inquiries

- **Website**: [pipefishlabs.io](https://pipefishlabs.io)
- **Book a Strategy Session**: [pipefishlabs.io/book-a-demo-contact/](https://pipefishlabs.io/book-a-demo-contact/)
- **Case Studies**: [pipefishlabs.io/case-studies-results/](https://pipefishlabs.io/case-studies-results/)
- **Email**: pipefish.labs@gmail.com
