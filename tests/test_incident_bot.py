import unittest
from bots.incident_bot import IncidentTriageBot

class TestIncidentTriageBot(unittest.TestCase):
    def setUp(self):
        self.bot = IncidentTriageBot()

    def test_handle_p1_incident(self):
        res = self.bot.handle_incident_alert({
            "alert_name": "High CPU Latency Anomaly",
            "severity": "P1",
            "service": "k8s-ingress"
        })
        self.assertEqual(res["severity"], "P1")
        self.assertEqual(res["agent_scenario"], "systemoptimizing")
        self.assertEqual(res["mesh_status"], "COMPLETED")
        self.assertIsNotNone(res["linear_issue"])
        self.assertEqual(res["linear_issue"]["priority"], 1)

    def test_handle_p3_incident(self):
        res = self.bot.handle_incident_alert({
            "alert_name": "Unusual Log Pattern",
            "severity": "P3",
            "service": "api-gateway"
        })
        self.assertEqual(res["severity"], "P3")
        self.assertEqual(res["agent_scenario"], "logtriage")
        self.assertIsNone(res["linear_issue"])  # P3 does not auto-create urgent Linear issue

if __name__ == "__main__":
    unittest.main()
