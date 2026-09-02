import unittest
from sdk.enterprise_connectors import EnterpriseConnectors

class TestEnterpriseConnectors(unittest.TestCase):
    def test_salesforce_sync(self):
        res = EnterpriseConnectors.salesforce_sync({"Email": "lead@enterprise.com", "Company": "GlobalLogistics"})
        self.assertEqual(res["platform"], "salesforce")
        self.assertEqual(res["status"], "SYNCED")
        self.assertTrue(res["record_id"].startswith("00Q"))

    def test_asana_create_task(self):
        res = EnterpriseConnectors.asana_create_task("proj_101", "Audit Agent Node", "Review SOC 2")
        self.assertEqual(res["platform"], "asana")
        self.assertEqual(res["status"], "TASK_CREATED")

    def test_stripe_create_checkout(self):
        res = EnterpriseConnectors.stripe_create_checkout("cus_99", 250000, "usd")
        self.assertEqual(res["platform"], "stripe")
        self.assertEqual(res["amount_cents"], 250000)
        self.assertTrue(res["checkout_id"].startswith("cs_live_"))

    def test_obsidian_export(self):
        note = EnterpriseConnectors.obsidian_export_markdown("Agent Memory Architecture", "Vector search details", ["ai", "memory"])
        self.assertIn("title: Agent Memory Architecture", note)
        self.assertIn("#ai", note)
        self.assertIn("#memory", note)

    def test_posthog_capture(self):
        res = EnterpriseConnectors.posthog_capture("user_123", "simulator_executed", {"scenario": "receptionist"})
        self.assertEqual(res["platform"], "posthog")
        self.assertEqual(res["status"], "EVENT_CAPTURED")

if __name__ == "__main__":
    unittest.main()
