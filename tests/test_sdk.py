import unittest
import json
from sdk.pipefish_sdk import PipeFishAgentMesh

class TestPipeFishAgentMesh(unittest.TestCase):
    def setUp(self):
        self.client = PipeFishAgentMesh(api_key="test_live_key_9941", endpoint="https://api.pipefishlabs.io/v1")

    def test_initialization_success(self):
        self.assertEqual(self.client.api_key, "test_live_key_9941")
        self.assertEqual(self.client.endpoint, "https://api.pipefishlabs.io/v1")

    def test_initialization_missing_key(self):
        with self.assertRaises(ValueError):
            PipeFishAgentMesh(api_key="")

    def test_trigger_graph_execution_systemoptimizing(self):
        payload = {"alert": "High BGP latency at edge gateway #4"}
        result = self.client.trigger_graph_execution(
            scenario_key="systemoptimizing",
            payload=payload
        )
        self.assertEqual(result["scenario"], "systemoptimizing")
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["nodes_executed"], 8)
        self.assertTrue(result["mcp_connectors_verified"])
        self.assertEqual(result["zdr_enclave_retention_bytes"], 0)
        self.assertIn("Mistral Native Handoff", result["handoff_mode"])
        self.assertEqual(result["execution_summary"]["inbound_telemetry"], payload)

    def test_trigger_graph_execution_receptionist(self):
        payload = {"caller_id": "+15550192834", "channel": "voice", "intent": "Tier 2 Support"}
        result = self.client.trigger_graph_execution(
            scenario_key="receptionist",
            payload=payload
        )
        self.assertEqual(result["scenario"], "receptionist")
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["nodes_executed"], 8)

    def test_trigger_graph_execution_missedcalltextback(self):
        """Agent 25 — missed call / text-back; COMMS domain."""
        payload = {
            "caller_id": "+15559876543",
            "channel": "voice",
            "event": "missed_call",
            "priority": "P1"
        }
        result = self.client.trigger_graph_execution(
            scenario_key="missedcalltextback",
            payload=payload
        )
        self.assertEqual(result["scenario"], "missedcalltextback")
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["nodes_executed"], 8)
        self.assertTrue(result["mcp_connectors_verified"])
        self.assertEqual(result["zdr_enclave_retention_bytes"], 0)
        self.assertIn("Mistral Native Handoff", result["handoff_mode"])
        self.assertEqual(result["execution_summary"]["inbound_telemetry"], payload)

    def test_trigger_graph_execution_finops(self):
        """Agent 23 — FinTech Ops; FINTECH · PAYMENTS domain."""
        payload = {
            "transaction_id": "txn_9Kq1fR2w",
            "amount_cents": 500000,
            "currency": "usd",
            "reconciliation_required": True
        }
        result = self.client.trigger_graph_execution(
            scenario_key="finops",
            payload=payload
        )
        self.assertEqual(result["scenario"], "finops")
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["nodes_executed"], 8)
        self.assertTrue(result["mcp_connectors_verified"])
        self.assertEqual(result["zdr_enclave_retention_bytes"], 0)
        self.assertEqual(result["execution_summary"]["inbound_telemetry"], payload)

    def test_trigger_graph_execution_contractintel(self):
        """Agent 24 — Contract Intelligence; SECURITY · COMPLIANCE domain."""
        payload = {
            "document_id": "doc_NDA_2026_001",
            "document_type": "NDA",
            "parties": ["PipeFish Labs", "Acme Corp"],
            "flag_pii": True
        }
        result = self.client.trigger_graph_execution(
            scenario_key="contractintel",
            payload=payload
        )
        self.assertEqual(result["scenario"], "contractintel")
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["nodes_executed"], 8)
        self.assertTrue(result["mcp_connectors_verified"])
        self.assertEqual(result["zdr_enclave_retention_bytes"], 0)
        self.assertEqual(result["execution_summary"]["inbound_telemetry"], payload)

    def test_trigger_graph_execution_llmops(self):
        """Agent 26 — LLMOps & Prompt Evaluation; AI-INFRA · SRE domain."""
        payload = {
            "prompt_template": "enterprise_system_prompt_v2",
            "eval_suite": "golden_benchmark_v1",
            "max_drift_threshold": 0.05
        }
        result = self.client.trigger_graph_execution(
            scenario_key="llmops",
            payload=payload
        )
        self.assertEqual(result["scenario"], "llmops")
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["nodes_executed"], 8)
        self.assertTrue(result["mcp_connectors_verified"])
        self.assertEqual(result["zdr_enclave_retention_bytes"], 0)
        self.assertEqual(result["execution_summary"]["inbound_telemetry"], payload)

    def test_trigger_all_26_scenario_graphs(self):
        """Verifies that all 26 canonical scenario keys execute an 8-node graph with 0-byte retention."""
        canonical_keys = [
            "receptionist", "sales", "logistics", "integration", "quantum",
            "reverse", "crypto", "errorcorr", "trend", "market", "codescan",
            "docs", "observability", "revops", "analytics", "auditing",
            "logtriage", "erp", "trafficrouter", "networkdispatch",
            "selfimproving", "systemoptimizing", "finops", "contractintel",
            "missedcalltextback", "llmops"
        ]
        for key in canonical_keys:
            res = self.client.trigger_graph_execution(key, {"test_probe": True})
            self.assertEqual(res["scenario"], key)
            self.assertEqual(res["status"], "COMPLETED")
            self.assertEqual(res["nodes_executed"], 8)
            self.assertTrue(res["mcp_connectors_verified"])
            self.assertEqual(res["zdr_enclave_retention_bytes"], 0)

    def test_opentelemetry_span_instrumentation(self):
        """Verifies OpenTelemetry W3C tracecontext and 8-node DAG span generation."""
        res = self.client.trigger_graph_execution("receptionist", {"call_type": "inbound_voice"})
        self.assertIn("trace_context", res)
        trace_ctx = res["trace_context"]
        self.assertEqual(len(trace_ctx["trace_id"]), 32)
        self.assertTrue(trace_ctx["traceparent"].startswith("00-"))
        self.assertEqual(trace_ctx["spans_count"], 9)  # 1 root + 8 node child spans
        self.assertEqual(len(res["spans"]), 9)
        
        # Verify root span
        root_span = res["spans"][0]
        self.assertEqual(root_span["name"], "pipefish.mesh.receptionist")
        self.assertIsNone(root_span["parent_span_id"])
        
        # Verify 8 node spans
        for i in range(1, 9):
            node_span = res["spans"][i]
            node_span_name = f"pipefish.node.{i}"
            self.assertEqual(node_span["name"], node_span_name)
            self.assertEqual(node_span["attributes"]["pipefish.node_index"], i)
            self.assertTrue(node_span["attributes"]["pipefish.zdr_enclave"])
            self.assertEqual(node_span["status"], "OK")

    def test_list_supported_scenarios(self):
        scenarios = self.client.list_supported_scenarios()
        self.assertEqual(len(scenarios), 26)
        self.assertIn("receptionist", scenarios)
        self.assertIn("llmops", scenarios)
        self.assertIn("systemoptimizing", scenarios)

    def test_get_scenario_spec(self):
        spec = self.client.get_scenario_spec("llmops")
        self.assertEqual(spec["id"], "26")
        self.assertEqual(spec["domain"], "AI-INFRA · SRE")

        with self.assertRaises(KeyError):
            self.client.get_scenario_spec("non_existent_scenario")

    def test_trigger_invalid_scenario_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.client.trigger_graph_execution("invalid_scenario", {"test": True})

    def test_trigger_invalid_payload_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.client.trigger_graph_execution("receptionist", "not-a-dict") # type: ignore

if __name__ == "__main__":
    unittest.main()

