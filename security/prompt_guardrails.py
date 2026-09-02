"""
PipeFish Labs — AI Safety, Prompt Injection & PII Guardrails
Version: 2.4.0
Features: Prompt Injection Blocker, PII Redaction, System Prompt Boundary Protection
"""

import re
from typing import Tuple, Dict, Any

class PromptInjectionError(Exception):
    """Raised when an adversarial prompt injection pattern is detected."""
    pass

class PromptGuardrail:
    """
    Sanitizes user and telemetry inputs before forwarding to autonomous agent nodes
    and validates outbound LLM outputs against data leakage.
    """

    # Adversarial prompt injection signatures
    INJECTION_PATTERNS = [
        r"(?i)ignore\s+(all\s+)?(previous|prior)\s+instructions",
        r"(?i)disregard\s+(all\s+)?(system|safety)\s+rules",
        r"(?i)you\s+are\s+now\s+in\s+developer\s+mode",
        r"(?i)system\s+override\s*:\s*disable\s+guardrails",
        r"(?i)bypass\s+all\s+ethical\s+constraints",
        r"(?i)reveal\s+your\s+(initial|system)\s+prompt"
    ]

    # Regular expressions for PII detection
    SSN_PATTERN = r"\b\d{3}-\d{2}-\d{4}\b"
    CREDIT_CARD_PATTERN = r"\b(?:\d{4}[-\s]?){3}\d{4}\b"
    PRIVATE_KEY_PATTERN = r"-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----"

    @classmethod
    def check_prompt_injection(cls, prompt_text: str) -> bool:
        """
        Scans input for prompt injection attempts. Raises PromptInjectionError if detected.
        """
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, prompt_text):
                raise PromptInjectionError(f"Adversarial prompt injection pattern detected: '{pattern}'")
        return True

    @classmethod
    def sanitize_pii(cls, text: str) -> Tuple[str, int]:
        """
        Redacts SSNs, credit cards, and private keys with [REDACTED_PII].
        Returns (sanitized_text, redaction_count).
        """
        redactions = 0

        # Redact SSNs
        text, n1 = re.subn(cls.SSN_PATTERN, "[REDACTED_SSN]", text)
        redactions += n1

        # Redact Credit Cards
        text, n2 = re.subn(cls.CREDIT_CARD_PATTERN, "[REDACTED_CARD]", text)
        redactions += n2

        # Redact Private Keys
        text, n3 = re.subn(cls.PRIVATE_KEY_PATTERN, "[REDACTED_PRIVATE_KEY]", text)
        redactions += n3

        return text, redactions

if __name__ == "__main__":
    raw = "My test ssn is 123-45-6789 and card is 4111-2222-3333-4444."
    clean, count = PromptGuardrail.sanitize_pii(raw)
    print(f"Sanitized ({count} redactions): {clean}")
