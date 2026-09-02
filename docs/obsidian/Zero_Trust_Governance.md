---
title: Agentic Zero-Trust Governance
tags: [zero-trust, security, vault, ebpf, pqc]
---

# Agentic Zero-Trust Governance

Every agent node in the PipeFish mesh operates under least-privilege Model Context Protocol (MCP) tool scoping.

## Security Pillars:
1. **RAM-Only Enclaves**: Zero persistent disk writes.
2. **eBPF Falco Detection**: Kernel monitoring preventing memory scraping and unauthorized egress.
3. **PQC ML-KEM-768**: Post-quantum key encapsulation.
4. **Short-Lived Leases**: 300s TTL HashiCorp Vault tokens.

Related: [[Agent_Mesh_Architecture]]
