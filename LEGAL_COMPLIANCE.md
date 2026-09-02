# 🏛️ PipeFish Labs — Enterprise Legal & Regulatory Compliance Framework
**Version:** 2.4.0  
**Effective Date:** 2026-09-02  
**Canonical Reference:** [pipefishlabs.io/legal-privacy-policy/](https://pipefishlabs.io/legal-privacy-policy/)

---

## 1. EU AI Act Annex IV Conformity Assessment
PipeFish Labs multi-agent systems are engineered to satisfy **High-Risk AI System** conformity obligations set forth under Annex IV of Regulation (EU) 2024/1689:
- **Technical Documentation (§ 1)**: Automated generation of system architecture dossiers, MCP connector scopes, and training/evaluation datasets.
- **Risk Management System (Article 9)**: Continuous eBPF Falco runtime monitoring detecting adversarial inputs, unexpected privilege escalations, or data exfiltration.
- **Data Governance (Article 10)**: Automated PII redaction and mathematical Zero-Data Retention (ZDR) RAM-only processing.
- **Human Oversight (Article 14)**: Deterministic human-in-the-loop override endpoints allowing instantaneous emergency circuit breaking and agent termination.

---

## 2. SOC 2 Type II Security & Audit Controls
- **CC6.1 (Logical Access Controls)**: All agent operations authenticate via mTLS and temporary HashiCorp Vault tokens (TTL <= 300s).
- **CC6.3 (Least Privilege Tool Scoping)**: Model Context Protocol (MCP) servers restrict agent capabilities exclusively to authorized subroutines.
- **CC7.2 (Intrusion Detection)**: Real-time Falco rules and Zeek protocol analysis inspecting 100% of inter-node network traffic.

---

## 3. HIPAA Business Associate Agreement (BAA) Alignment
- **Zero-Data Retention (ZDR)**: Protected Health Information (PHI) processed by the Receptionist or Analysis agents resides strictly in RAM within encrypted enclaves.
- **Encryption in Transit**: NIST FIPS 203 (ML-KEM-768) post-quantum encapsulation and TLS 1.3 enforced across all API and webhook surfaces.
- **Audit Trails**: Immutable append-only audit ledgers recorded in PostgreSQL with SHA-256 integrity hashes.

---

## 4. Standard Contractual Clauses (SCC) & Data Processing Addendum (DPA)
PipeFish Labs offers pre-signed enterprise DPAs incorporating European Commission Standard Contractual Clauses for international data transfers. Inquiries can be addressed to `legal@pipefishlabs.io`.
