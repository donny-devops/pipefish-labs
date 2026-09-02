import unittest
from sdk.compliance_report import ComplianceAuditGenerator

class TestComplianceAuditGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ComplianceAuditGenerator(tenant_id="test-tenant")

    def test_generate_report_eu_ai_act(self):
        report = self.generator.generate_report(standard="EU_AI_ACT_ANNEX_IV")
        self.assertEqual(report["tenant_id"], "test-tenant")
        self.assertEqual(report["overall_status"], "CONFORMITY_VERIFIED")
        self.assertEqual(report["controls_evaluated"], 4)
        self.assertEqual(report["controls_passed"], 4)
        self.assertTrue(len(report["integrity_sha256"]) == 64)

    def test_generate_report_soc2(self):
        report = self.generator.generate_report(standard="SOC2_TYPE_II")
        self.assertEqual(report["compliance_standard"], "SOC2_TYPE_II")
        self.assertEqual(report["overall_status"], "CONFORMITY_VERIFIED")

if __name__ == "__main__":
    unittest.main()
