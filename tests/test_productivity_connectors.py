import unittest
from sdk.productivity_connectors import (
    LinearConnector,
    SlackAlertConnector,
    NotionSyncConnector
)

class TestProductivityConnectors(unittest.TestCase):
    def test_linear_create_issue(self):
        connector = LinearConnector(team_id="SEC")
        issue = connector.create_issue("Unsigned Webhook Attempt", "Webhook rejected by verifier", priority=1)
        self.assertEqual(issue["platform"], "linear")
        self.assertEqual(issue["team_id"], "SEC")
        self.assertIn("[SEC] Unsigned Webhook Attempt", issue["title"])
        self.assertEqual(issue["status"], "CREATED")

    def test_slack_build_alert_blocks(self):
        connector = SlackAlertConnector()
        blocks = connector.build_alert_blocks("systemoptimizing", "COMPLETED", "All nodes healthy", severity="INFO")
        self.assertIn("attachments", blocks)
        self.assertEqual(len(blocks["attachments"]), 1)
        self.assertEqual(blocks["attachments"][0]["color"], "#00D4FF")

    def test_notion_build_page_payload(self):
        connector = NotionSyncConnector("db_123")
        payload = connector.build_page_payload("Q3 Market TAM Report", "Analysis details...", ["Research", "TAM"])
        self.assertEqual(payload["parent"]["database_id"], "db_123")
        self.assertIn("properties", payload)

if __name__ == "__main__":
    unittest.main()
