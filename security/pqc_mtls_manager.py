"""
PipeFish Labs — Post-Quantum mTLS & Key Rotation Manager
Version: 2.4.0
Features: Ephemeral Key Rotation, Handshake Token Verification, NIST FIPS 203 ML-KEM-768 Simulation
"""

import time
import hmac
import hashlib
import secrets
from typing import Dict, Any, Optional

class PQCKeyManager:
    """
    Manages automated rotation of inter-agent mTLS keys and cryptographic tokens.
    Enforces short TTLs (default: 300s) to limit exposure windows.
    """

    def __init__(self, node_id: str, rotation_interval_seconds: int = 300):
        self.node_id = node_id
        self.rotation_interval = rotation_interval_seconds
        self.current_key_id = None
        self.current_secret = None
        self.key_created_at = 0.0
        self.rotate_keys()

    def rotate_keys(self) -> str:
        """
        Rotates the active cryptographic key and invalidates prior ephemeral sessions.
        """
        self.current_key_id = f"pqc_kem_{self.node_id}_{int(time.time())}_{secrets.token_hex(4)}"
        self.current_secret = secrets.token_bytes(32)
        self.key_created_at = time.time()
        return self.current_key_id

    def is_expired(self) -> bool:
        return (time.time() - self.key_created_at) > self.rotation_interval

    def sign_a2a_ticket(self, target_node: str, payload_digest: str) -> Dict[str, Any]:
        """
        Issues an ephemeral cryptographic handshake ticket authorizing inter-agent execution.
        """
        if self.is_expired():
            self.rotate_keys()

        timestamp = int(time.time())
        token_body = f"{self.node_id}:{target_node}:{payload_digest}:{timestamp}".encode("utf-8")
        signature = hmac.new(self.current_secret, token_body, hashlib.sha256).hexdigest()

        return {
            "key_id": self.current_key_id,
            "source_node": self.node_id,
            "target_node": target_node,
            "payload_digest": payload_digest,
            "timestamp": timestamp,
            "signature": signature,
            "cipher_suite": "NIST-FIPS-203-ML-KEM-768"
        }

    def verify_ticket(self, ticket: Dict[str, Any], max_drift_seconds: int = 60) -> bool:
        """
        Verifies that an incoming A2A ticket was signed by the current secret and is within time window.
        """
        now = int(time.time())
        if abs(now - ticket["timestamp"]) > max_drift_seconds:
            return False

        token_body = f"{ticket['source_node']}:{ticket['target_node']}:{ticket['payload_digest']}:{ticket['timestamp']}".encode("utf-8")
        expected_sig = hmac.new(self.current_secret, token_body, hashlib.sha256).hexdigest()

        return hmac.compare_digest(expected_sig, ticket["signature"])

if __name__ == "__main__":
    mgr = PQCKeyManager("node-01-receptionist")
    print(f"Active Key ID: {mgr.current_key_id}")
    ticket = mgr.sign_a2a_ticket("node-02-sales", "sha256_mock_digest")
    print(f"Ticket Verified: {mgr.verify_ticket(ticket)}")
