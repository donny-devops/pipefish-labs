import unittest
import hmac
import hashlib
import json
from sdk.lemon_squeezy import (
    LemonSqueezyClient,
    LemonSqueezyError,
    LemonSqueezyWebhookError
)

class TestLemonSqueezyClient(unittest.TestCase):
    def setUp(self):
        self.secret = "whsec_ls_test_123"
        self.client = LemonSqueezyClient(api_key="api_key_123", webhook_secret=self.secret)

    def test_create_checkout_session_success(self):
        session = self.client.create_checkout_session(
            tier="growth",
            customer_email="ciso@fintech.com",
            tenant_name="FintechCore"
        )
        self.assertEqual(session["tier"], "growth")
        self.assertEqual(session["status"], "READY")
        self.assertIn("pipefishlabs.lemonsqueezy.com", session["checkout_url"])
        self.assertIn("ciso@fintech.com", session["checkout_url"])

    def test_create_checkout_invalid_tier(self):
        with self.assertRaises(LemonSqueezyError):
            self.client.create_checkout_session(
                tier="invalid_tier_xyz",
                customer_email="ciso@fintech.com",
                tenant_name="FintechCore"
            )

    def test_verify_webhook_valid(self):
        payload = b'{"meta":{"event_name":"order_created","custom_data":{"tenant":"FintechCore"}},"data":{"id":"order_99","attributes":{"user_email":"ciso@fintech.com"}}}'
        sig = hmac.new(self.secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
        result = self.client.process_webhook_event(payload, sig)
        self.assertEqual(result["event_name"], "order_created")
        self.assertEqual(result["tenant_name"], "FintechCore")
        self.assertEqual(result["status"], "PROCESSED")

    def test_verify_webhook_invalid_signature(self):
        payload = b'{"meta":{"event_name":"order_created"}}'
        with self.assertRaises(LemonSqueezyWebhookError):
            self.client.process_webhook_event(payload, "invalid_sig_abc")

if __name__ == "__main__":
    unittest.main()
