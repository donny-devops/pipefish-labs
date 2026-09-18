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

if __name__ == "__main__":
    unittest.main()
