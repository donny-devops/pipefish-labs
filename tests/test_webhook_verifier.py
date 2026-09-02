import time
import unittest
from sdk.webhook_verifier import (
    WebhookVerifier,
    WebhookVerificationError,
    WebhookTimestampExpiredError,
    WebhookSignatureMismatchError
)

class TestWebhookVerifier(unittest.TestCase):
    def setUp(self):
        self.secret = "whsec_test_secret_key_123"
        self.verifier = WebhookVerifier(self.secret, default_tolerance_seconds=300)
        self.payload = b'{"event":"agent.state_handoff","node":"01"}'

    def test_valid_signature_verification(self):
        ts = int(time.time())
        sig = self.verifier.compute_signature(self.payload, ts)
        self.assertTrue(self.verifier.verify(self.payload, sig))

    def test_expired_timestamp_rejected(self):
        old_ts = int(time.time()) - 400
        sig = self.verifier.compute_signature(self.payload, old_ts)
        with self.assertRaises(WebhookTimestampExpiredError):
            self.verifier.verify(self.payload, sig, tolerance_seconds=300)

    def test_tampered_payload_rejected(self):
        ts = int(time.time())
        sig = self.verifier.compute_signature(self.payload, ts)
        tampered = b'{"event":"agent.state_handoff","node":"02"}'
        with self.assertRaises(WebhookSignatureMismatchError):
            self.verifier.verify(tampered, sig)

    def test_malformed_header_rejected(self):
        with self.assertRaises(WebhookVerificationError):
            self.verifier.verify(self.payload, "invalid_header")

if __name__ == "__main__":
    unittest.main()
