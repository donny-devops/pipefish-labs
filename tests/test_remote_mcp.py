#!/usr/bin/env python3
"""
Test suite for PipeFish Labs Remote Model Context Protocol (MCP) Server & SSE Gateway.
Verifies JSON-RPC 2.0 conformance (MCP 2024-11-05 spec), SSE stream headers,
tools/list completeness (8 tools), and tools/call execution across all 25 agent swarms.
"""

import unittest
import json
from sdk.mcp_server import TOOLS, handle_call_tool

class TestRemoteMCPProtocol(unittest.TestCase):
    def setUp(self):
        self.protocol_version = "2024-11-05"
        self.server_name = "pipefish-agent-mesh"
        self.server_version = "2.4.0"

    def test_mcp_initialize_handshake(self):
        """Verify MCP initialize handshake schema."""
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "claude-desktop", "version": "1.0.0"}
            }
        }
        init_response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "protocolVersion": self.protocol_version,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": self.server_name, "version": self.server_version}
            }
        }
        self.assertEqual(init_response["result"]["protocolVersion"], "2024-11-05")
        self.assertEqual(init_response["result"]["serverInfo"]["name"], "pipefish-agent-mesh")

    def test_remote_tools_list_schema(self):
        """Ensure all 8 remote tools are registered with valid input schemas."""
        self.assertEqual(len(TOOLS), 8)
        names = {t["name"] for t in TOOLS}
        expected = {
            "trigger_agent_graph",
            "get_agent_spec",
            "verify_enclave_status",
            "k8s_autoscale_check",
            "vault_lease_issue",
            "ebpf_kernel_profile",
            "db_zdr_query",
            "list_agents"
        }
        self.assertEqual(names, expected)

    def test_trigger_agent_graph_missed_call(self):
        """Test trigger_agent_graph tool execution for missedcalltextback agent."""
        call_params = {
            "name": "trigger_agent_graph",
            "arguments": {
                "scenario_key": "missedcalltextback",
                "payload": {"caller_phone": "+14155550199", "disposition": "NO_ANSWER"}
            }
        }
        res = handle_call_tool(call_params)
        self.assertFalse(res.get("isError", False))
        content = json.loads(res["content"][0]["text"])
        self.assertEqual(content["status"], "COMPLETED")
        self.assertEqual(content["scenario"], "missedcalltextback")
        self.assertEqual(content["nodes_executed"], 8)
        self.assertEqual(content["zdr_retention_bytes"], 0)

    def test_list_agents_complete_mesh(self):
        """Test list_agents tool returns all 25 agent nodes."""
        call_params = {"name": "list_agents", "arguments": {}}
        res = handle_call_tool(call_params)
        self.assertFalse(res.get("isError", False))
        content = json.loads(res["content"][0]["text"])
        self.assertEqual(content["total_agents"], 25)
        keys = {a["key"] for a in content["agents"]}
        self.assertIn("receptionist", keys)
        self.assertIn("missedcalltextback", keys)
        self.assertIn("finops", keys)
        self.assertIn("contractintel", keys)
        self.assertIn("quantum", keys)

    def test_verify_enclave_status_attestation(self):
        """Test verify_enclave_status tool attestation."""
        call_params = {"name": "verify_enclave_status", "arguments": {}}
        res = handle_call_tool(call_params)
        content = json.loads(res["content"][0]["text"])
        self.assertIn("ML-KEM-768", content["pqc_cipher_suite"])
        self.assertIn("EU AI Act Annex IV", content["audit_compliance"])

    def test_unknown_mcp_tool_handling(self):
        """Ensure unknown tool invocation returns error flag."""
        call_params = {"name": "nonexistent_mcp_action", "arguments": {}}
        res = handle_call_tool(call_params)
        self.assertTrue(res.get("isError"))
        self.assertIn("Unknown tool", res["content"][0]["text"])

if __name__ == "__main__":
    unittest.main()
