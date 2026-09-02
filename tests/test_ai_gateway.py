import unittest
from sdk.ai_gateway import UniversalAIGateway, ModelProvider

class TestUniversalAIGateway(unittest.TestCase):
    def setUp(self):
        self.gateway = UniversalAIGateway()

    def test_route_reasoning_task(self):
        res = self.gateway.route_task("reasoning", "Evaluate zero-trust DAG graph.")
        self.assertEqual(res["task_type"], "reasoning")
        self.assertEqual(res["provider"], ModelProvider.MISTRAL)
        self.assertIn("mistral-large-latest", res["model_identifier"])
        self.assertIn(ModelProvider.ANTHROPIC, res["fallback_providers"])
        self.assertEqual(res["status"], "DISPATCHED")

    def test_route_deep_search_task(self):
        res = self.gateway.route_task("deep_search", "Analyze SEC 10-K filings.")
        self.assertEqual(res["provider"], ModelProvider.PERPLEXITY)
        self.assertEqual(res["model_identifier"], "sonar-pro")

    def test_unknown_task_defaults(self):
        res = self.gateway.route_task("custom_undefined_task", "Test prompt.")
        self.assertEqual(res["provider"], ModelProvider.MISTRAL)

if __name__ == "__main__":
    unittest.main()
