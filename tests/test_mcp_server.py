import unittest
import json
from sdk.mcp_server import TOOLS, handle_call_tool

class TestMCPServer(unittest.TestCase):
    def test_tools_list(self):
        self.assertEqual(len(TOOLS), 8)
        tool_names = [t["name"] for t in TOOLS]
        self.assertIn("trigger_agent_graph", tool_names)
        self.assertIn("get_agent_spec", tool_names)
        self.assertIn("verify_enclave_status", tool_names)
        self.assertIn("k8s_autoscale_check", tool_names)
        self.assertIn("vault_lease_issue", tool_names)
        self.assertIn("ebpf_kernel_profile", tool_names)
        self.assertIn("db_zdr_query", tool_names)
        self.assertIn("list_agents", tool_names)

    def test_call_k8s_autoscale_check(self):
        params = {
            "name": "k8s_autoscale_check",
            "arguments": {
                "deployment_name": "pipefish-mcp-server",
                "current_cpu_pct": 82.5
            }
        }
        res = handle_call_tool(params)
        data = json.loads(res["content"][0]["text"])
        self.assertEqual(data["deployment"], "pipefish-mcp-server")
        self.assertTrue(data["scale_recommended"])
        self.assertEqual(data["target_replicas"], 5)

    def test_call_vault_lease_issue(self):
        params = {
            "name": "vault_lease_issue",
            "arguments": {
                "role_name": "system-optimizer",
                "ttl_seconds": 180
            }
        }
        res = handle_call_tool(params)
        data = json.loads(res["content"][0]["text"])
        self.assertEqual(data["role"], "system-optimizer")
        self.assertEqual(data["lease_duration_seconds"], 180)
        self.assertEqual(data["status"], "ISSUED")

    def test_call_db_zdr_query(self):
        params = {
            "name": "db_zdr_query",
            "arguments": {
                "query": "SELECT count(*) FROM tenants;"
            }
        }
        res = handle_call_tool(params)
        data = json.loads(res["content"][0]["text"])
        self.assertTrue(data["pii_masked"])
        self.assertEqual(data["disk_writes_bytes"], 0)
        self.assertEqual(data["enclave_isolation"], "RAM_ONLY")

    def test_call_list_agents(self):
        params = {"name": "list_agents", "arguments": {}}
        res = handle_call_tool(params)
        data = json.loads(res["content"][0]["text"])
        self.assertEqual(data["total_agents"], 25)
        keys = [a["key"] for a in data["agents"]]
        self.assertIn("missedcalltextback", keys)
        self.assertIn("finops", keys)
        self.assertIn("contractintel", keys)
        self.assertIn("receptionist", keys)
        self.assertIn("systemoptimizing", keys)

    def test_call_unknown_tool_returns_error(self):
        params = {"name": "nonexistent_tool", "arguments": {}}
        res = handle_call_tool(params)
        self.assertTrue(res.get("isError"))
        self.assertIn("Unknown tool", res["content"][0]["text"])

if __name__ == "__main__":
    unittest.main()
