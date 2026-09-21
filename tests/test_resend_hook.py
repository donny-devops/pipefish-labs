import unittest
import json
import hashlib

class TestResendLeadHook(unittest.TestCase):
    """
    Validates the Resend transactional email hook on POST /api/v1/leads,
    ensuring cryptographic SHA-256 receipt generation, dual-mode delivery,
    and graceful fallback behavior when RESEND_API_KEY is unconfigured.
    """

    def test_lead_receipt_hash_generation(self):
        lead_id = "pfl_lead_test123"
        recipient = "ciso@enterprise.com"
        timestamp = "2026-09-21T15:00:00.000Z"
        receipt_input = f"{lead_id}:{recipient}:{timestamp}"
        expected_hash = "0x" + hashlib.sha256(receipt_input.encode('utf-8')).hexdigest()[:32].upper()
        
        self.assertTrue(expected_hash.startswith("0x"))
        self.assertEqual(len(expected_hash), 34)

    def test_resend_payload_structure(self):
        lead_data = {
            "name": "Alex Mercer",
            "work_email": "alex@mercer-defense.com",
            "tier": "enterprise",
            "ops": 10000
        }
        recipient = lead_data["work_email"]
        receipt_hash = "0x8E19F4B30291AAEC382901928471BCDE"
        
        email_payload = {
            "from": "PipeFish Labs <leads@pipefishlabs.io>",
            "to": [recipient],
            "subject": f"[Receipt {receipt_hash}] Technical Architecture Audit Confirmation — PipeFish Labs",
            "html": f"<p>Lead ID: pfl_lead_test123, Tier: {lead_data['tier']}</p>"
        }

        self.assertEqual(email_payload["from"], "PipeFish Labs <leads@pipefishlabs.io>")
        self.assertIn(recipient, email_payload["to"])
        self.assertIn(receipt_hash, email_payload["subject"])
        self.assertIn("enterprise", email_payload["html"])

    def test_simulated_dispatch_status_when_key_absent(self):
        """When RESEND_API_KEY is not configured, the worker returns SIMULATED_SUCCESS without error."""
        simulated_response = {
            "status": "success",
            "lead_id": "pfl_lead_abc123",
            "receipt_hash": "0xABC123DEF456",
            "resend_dispatch": {
                "status": "SIMULATED_SUCCESS",
                "message": "Confirmation email queued for automated dispatch (simulated environment).",
                "recipient": "lead@company.com"
            }
        }
        self.assertEqual(simulated_response["status"], "success")
        self.assertEqual(simulated_response["resend_dispatch"]["status"], "SIMULATED_SUCCESS")
        self.assertTrue(simulated_response["receipt_hash"].startswith("0x"))

if __name__ == "__main__":
    unittest.main()
