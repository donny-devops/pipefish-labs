"""
PipeFish Labs — Lemon Squeezy Monetization & Checkout Integration
Version: 2.4.0
Features: Checkout URL Generation, Subscription Lifecycle Management, Webhook HMAC Verification
"""

import hmac
import hashlib
import json
from typing import Dict, Any, Optional

class LemonSqueezyError(Exception):
    """Base exception for Lemon Squeezy operations."""
    pass

class LemonSqueezyWebhookError(LemonSqueezyError):
    """Raised when webhook signature verification fails."""
    pass

class LemonSqueezyClient:
    """
    Client for automating enterprise customer checkout sessions,
    agent tier subscriptions, and webhook event processing via Lemon Squeezy.
    """

    BASE_URL = "https://api.lemonsqueezy.com/v1"

    # Pre-configured Tier Variant IDs (can be overridden via environment variables)
    TIERS = {
        "starter": {"name": "PipeFish Agent Starter", "variant_id": "ls_var_starter_100"},
        "growth": {"name": "PipeFish Multi-Agent Growth", "variant_id": "ls_var_growth_500"},
        "enterprise": {"name": "PipeFish Zero-Trust Enterprise Enclave", "variant_id": "ls_var_enterprise_2500"}
    }

    def __init__(self, api_key: str = None, webhook_secret: str = None):
        self.api_key = api_key or "demo_lemonsqueezy_key"
        self.webhook_secret = webhook_secret or "demo_webhook_signing_secret"

    def create_checkout_session(
        self,
        tier: str,
        customer_email: str,
        tenant_name: str,
        success_url: str = "https://pipefishlabs.io/demo/?checkout=success"
    ) -> Dict[str, Any]:
        """
        Builds a checkout session payload and returns the hosted checkout URL.
        """
        tier_info = self.TIERS.get(tier.lower())
        if not tier_info:
            raise LemonSqueezyError(f"Unknown tier '{tier}'. Must be one of {list(self.TIERS.keys())}")

        checkout_data = {
            "checkout_url": f"https://pipefishlabs.lemonsqueezy.com/buy/{tier_info['variant_id']}?checkout[email]={customer_email}&checkout[custom][tenant]={tenant_name}",
            "tier": tier,
            "variant_id": tier_info["variant_id"],
            "customer_email": customer_email,
            "tenant_name": tenant_name,
            "success_url": success_url,
            "status": "READY"
        }
        return checkout_data

    def verify_webhook(self, raw_payload: bytes, signature_header: str) -> bool:
        """
        Validates HMAC-SHA256 signature on inbound Lemon Squeezy webhooks.
        """
        if not signature_header:
            raise LemonSqueezyWebhookError("Missing X-Signature header.")

        expected_sig = hmac.new(
            self.webhook_secret.encode("utf-8"),
            raw_payload,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_sig, signature_header):
            raise LemonSqueezyWebhookError("Lemon Squeezy signature mismatch.")

        return True

    def process_webhook_event(self, raw_payload: bytes, signature_header: str) -> Dict[str, Any]:
        """
        Verifies signature and extracts structured event data (e.g. order_created, subscription_created).
        """
        self.verify_webhook(raw_payload, signature_header)
        event = json.loads(raw_payload.decode("utf-8"))
        event_name = event.get("meta", {}).get("event_name", "unknown")
        custom_data = event.get("meta", {}).get("custom_data", {})

        return {
            "event_name": event_name,
            "tenant_name": custom_data.get("tenant", "default_tenant"),
            "customer_email": event.get("data", {}).get("attributes", {}).get("user_email"),
            "order_id": event.get("data", {}).get("id"),
            "status": "PROCESSED"
        }

if __name__ == "__main__":
    client = LemonSqueezyClient(webhook_secret="secret_9941")
    checkout = client.create_checkout_session(
        tier="growth",
        customer_email="cto@enterprise.com",
        tenant_name="Acme-Global"
    )
    print("Checkout payload:")
    print(json.dumps(checkout, indent=2))
