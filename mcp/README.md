# PipeFish Labs — Model Context Protocol (MCP) Server

Official Model Context Protocol (MCP) server for the **PipeFish Labs** autonomous multi-agent mesh.

Connects AI coding assistants (**Claude Desktop**, **Cursor**, **Mistral Le Chat**, or custom agents) directly to enterprise agent execution graphs, least-privilege Vault enclaves, eBPF profiling, and post-quantum cryptographic verifiers.

---

## 🚀 Quickstart

### Option A: Python / Virtual Environment (Recommended)

1. Clone or install:
```bash
git clone https://github.com/donny-devops/pipefish-labs.git
cd pipefish-labs
pip install -e .
```

2. Add to **Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "pipefish-agent-mesh": {
      "command": "python",
      "args": ["-m", "sdk.mcp_server"],
      "cwd": "/path/to/pipefish-labs"
    }
  }
}
```

3. Add to **Cursor IDE** (`.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "pipefish-agent-mesh": {
      "command": "python",
      "args": ["sdk/mcp_server.py"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

---

### Option B: Docker Container

Run directly with zero local Python dependencies:

```bash
docker run -i --rm ghcr.io/donny-devops/pipefish-labs/mcp-server:latest
```

Claude Desktop configuration:
```json
{
  "mcpServers": {
    "pipefish-agent-mesh": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "ghcr.io/donny-devops/pipefish-labs/mcp-server:latest"]
    }
  }
}
```

---

## 🛠️ Available MCP Tools

| Tool Name | Parameters | Purpose |
|---|---|---|
| `trigger_agent_graph` | `scenario_key`, `payload` | Triggers 8-node execution graph with Native Mistral Handoffs |
| `get_agent_spec` | `agent_key` | Retrieves zero-trust secrets, RBAC perms, and PQC handoff spec |
| `verify_enclave_status` | *(none)* | Validates Zero-Data Retention (ZDR) and NIST ML-KEM-768 readiness |
| `k8s_autoscale_check` | `deployment_name`, `current_cpu_pct` | Checks pod CPU and returns HPA scaling recommendation |
| `vault_lease_issue` | `role_name`, `ttl_seconds` | Issues ephemeral dynamic secret lease with auto-revocation |
| `ebpf_kernel_profile` | `target_service`, `duration_seconds` | Profiles eBPF tracepoints for RPC latency anomalies |
| `db_zdr_query` | `query` | Runs zero-retention SQL query with automated PII masking |

---

## 📝 Community Registry Pull Request Template

When submitting to [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers):

```markdown
### Server Name
`pipefish-labs-mcp-server`

### Repository
https://github.com/donny-devops/pipefish-labs

### Description
Enterprise MCP server for the PipeFish Labs autonomous multi-agent mesh. Supports 22 scenario graphs, Native Mistral Handoffs, zero-trust Vault leases, eBPF kernel telemetry, and NIST FIPS 203 ML-KEM-768 post-quantum cryptographic verification.

### Tools Provided
- `trigger_agent_graph`
- `get_agent_spec`
- `verify_enclave_status`
- `k8s_autoscale_check`
- `vault_lease_issue`
- `ebpf_kernel_profile`
- `db_zdr_query`

### License
MIT
```
