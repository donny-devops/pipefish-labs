import unittest
from security.automated_compliance_checker import AutomatedComplianceChecker

class TestAutomatedComplianceChecker(unittest.TestCase):
    def setUp(self):
        self.checker = AutomatedComplianceChecker(".")

    def test_check_non_root_dockerfile(self):
        res = self.checker.check_non_root_dockerfile()
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["control"], "NON_ROOT_CONTAINER")

    def test_run_all_checks(self):
        report = self.checker.run_all_checks()
        self.assertEqual(report["audit_status"], "COMPLIANT")
        self.assertGreaterEqual(report["total_controls"], 2)
        self.assertEqual(report["passed_controls"], report["total_controls"])

if __name__ == "__main__":
    unittest.main()
