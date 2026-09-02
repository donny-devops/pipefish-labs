import time
import unittest
from security.pqc_mtls_manager import PQCKeyManager

class TestPQCKeyManager(unittest.TestCase):
    def setUp(self):
        self.mgr = PQCKeyManager("node-test-01", rotation_interval_seconds=2)

    def test_key_initialization(self):
        self.assertIsNotNone(self.mgr.current_key_id)
        self.assertIn("pqc_kem_node-test-01", self.mgr.current_key_id)

    def test_sign_and_verify_ticket_success(self):
        ticket = self.mgr.sign_a2a_ticket("node-test-02", "digest_abc123")
        self.assertEqual(ticket["source_node"], "node-test-01")
        self.assertEqual(ticket["target_node"], "node-test-02")
        self.assertTrue(self.mgr.verify_ticket(ticket))

    def test_verify_tampered_ticket_rejected(self):
        ticket = self.mgr.sign_a2a_ticket("node-test-02", "digest_abc123")
        ticket["payload_digest"] = "digest_tampered"
        self.assertFalse(self.mgr.verify_ticket(ticket))

    def test_automated_key_rotation_on_expiry(self):
        old_key = self.mgr.current_key_id
        time.sleep(2.1)
        self.assertTrue(self.mgr.is_expired())
        new_key = self.mgr.rotate_keys()
        self.assertNotEqual(old_key, new_key)
        self.assertFalse(self.mgr.is_expired())

if __name__ == "__main__":
    unittest.main()
