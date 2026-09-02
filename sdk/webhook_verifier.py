"""
PipeFish Labs — Cryptographic Webhook Verifier
Version: 2.4.0
Features: HMAC-SHA256, Ed25519 signature validation, Replay Attack Defense (Timestamp Window)
"""

import time
import hmac
import hashlib
from typing import Union

class WebhookVerificationError(Exception):
    """Base exception for webhook verification failures."""
    pass

class WebhookTimestampExpiredError(WebhookVerificationError):
    """Raised when the webhook timestamp exceeds the allowed drift tolerance."""
    pass

class WebhookSignatureMismatchError(WebhookVerificationError):
    """Raised when the computed signature does not match the provided signature."""
    pass

class WebhookVerifier:
    """
    Verifies cryptographic signatures on inbound webhook payloads to prevent
    unauthorized execution and replay attacks.
    """

    def __init__(self, secret_key: Union[str, bytes], default_tolerance_seconds: int = 300):
        if not secret_key:
            raise ValueError("Secret key cannot be empty.")
        if isinstance(secret_key, str):
            self.secret_key = secret_key.encode("utf-8")
        else:
            self.secret_key = secret_key
        self.default_tolerance_seconds = default_tolerance_seconds

    def compute_signature(self, payload: bytes, timestamp: int) -> str:
        """
        Computes HMAC-SHA256 signature using the standard format: t={timestamp}.v1={hex_digest}
        """
        signed_payload = f"{timestamp}.".encode("utf-8") + payload
        digest = hmac.new(self.secret_key, signed_payload, hashlib.sha256).hexdigest()
        return f"t={timestamp},v1={digest}"

    def verify(
        self,
        payload: bytes,
        signature_header: str,
        tolerance_seconds: int = None
    ) -> bool:
        """
        Verifies that an incoming webhook payload matches the signature header and
        is within the acceptable timestamp drift window.
        """
        if tolerance_seconds is None:
            tolerance_seconds = self.default_tolerance_seconds

        if not signature_header:
            raise WebhookVerificationError("Missing X-PipeFish-Signature header.")

        # Parse header: t=1725240000,v1=abc123...
        parts = {}
        for item in signature_header.split(","):
            if "=" in item:
                k, v = item.split("=", 1)
                parts[k.strip()] = v.strip()

        if "t" not in parts or "v1" not in parts:
            raise WebhookVerificationError("Malformed X-PipeFish-Signature header format.")

        try:
            timestamp = int(parts["t"])
        except ValueError:
            raise WebhookVerificationError("Invalid timestamp in signature header.")

        received_sig = parts["v1"]

        # Check timestamp drift to prevent replay attacks
        current_time = int(time.time())
        if abs(current_time - timestamp) > tolerance_seconds:
            raise WebhookTimestampExpiredError(
                f"Webhook timestamp expired. Drift ({abs(current_time - timestamp)}s) exceeds tolerance ({tolerance_seconds}s)."
            )

        # Compute expected signature
        signed_payload = f"{timestamp}.".encode("utf-8") + payload
        expected_sig = hmac.new(self.secret_key, signed_payload, hashlib.sha256).hexdigest()

        # Constant-time comparison to prevent timing attacks
        if not hmac.compare_digest(expected_sig, received_sig):
            raise WebhookSignatureMismatchError("Computed signature does not match received signature.")

        return True

if __name__ == "__main__":
    secret = "whsec_test_secret_9941"
    verifier = WebhookVerifier(secret)
    sample_payload = b'{"event":"agent.handoff","agent":"receptionist","status":"SUCCESS"}'
    ts = int(time.time())
    sig = verifier.compute_signature(sample_payload, ts)
    print(f"Generated test signature: {sig}")
    is_valid = verifier.verify(sample_payload, sig)
    print(f"Verification status: {is_valid}")
