import unittest
from security.secret_scanner_manager import SecretScannerManager, shannon_entropy, is_allowlisted

class TestSecretScannerManager(unittest.TestCase):
    def setUp(self):
        self.manager = SecretScannerManager()

    def test_shannon_entropy_calculation(self):
        self.assertEqual(shannon_entropy(""), 0.0)
        # Uniform random distribution has higher entropy than single char repeat
        single_char = "AAAAAAAAAAAAAAAAAAAAAAAA"
        random_hex = "4f3a8b2c1d9e0f7a6b5c4d3e"
        self.assertLess(shannon_entropy(single_char), shannon_entropy(random_hex))

    def test_is_allowlisted(self):
        self.assertTrue(is_allowlisted("mock_api_key_12345"))
        self.assertTrue(is_allowlisted("test_token_secret_value"))
        self.assertTrue(is_allowlisted("placeholder_secret"))
        self.assertFalse(is_allowlisted("AKIAIOSFODNN7RANDOMKEY"))

    def test_repo_scan_is_clean(self):
        findings = self.manager.scan()
        critical_findings = [f for f in findings if f.severity == "CRITICAL"]
        self.assertEqual(len(critical_findings), 0, f"Found unexpected critical secrets: {critical_findings}")

    def test_report_generation(self):
        findings = self.manager.scan()
        report = self.manager.generate_report(findings)
        self.assertIn("status", report)
        self.assertIn("findings_by_severity", report)
        self.assertEqual(report["status"], "CLEAN")

if __name__ == "__main__":
    unittest.main()