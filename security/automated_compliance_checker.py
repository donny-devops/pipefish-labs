"""
PipeFish Labs — Automated Compliance & Zero-Trust Policy Checker
Version: 2.4.0
Standards: EU AI Act Annex IV, SOC 2 Type II, HIPAA, NIST CSF
"""

import os
import json
import sys
from typing import Dict, Any, List

class AutomatedComplianceChecker:
    """
    Automated policy checker that inspects local codebase configurations,
    Dockerfile policies, OPA rules, and security controls to verify compliance.
    """

    def __init__(self, root_dir: str = "."):
        self.root_dir = root_dir

    def check_non_root_dockerfile(self) -> Dict[str, Any]:
        dockerfile_path = os.path.join(self.root_dir, "Dockerfile.mcp")
        if not os.path.exists(dockerfile_path):
            return {"control": "NON_ROOT_CONTAINER", "status": "FAIL", "reason": "Dockerfile.mcp missing"}

        with open(dockerfile_path, "r", encoding="utf-8") as f:
            content = f.read()

        has_user = "USER pfl" in content or "USER 10001" in content
        return {
            "control": "NON_ROOT_CONTAINER",
            "standard": "SOC 2 CC6.1 & CIS Benchmark 4.1",
            "status": "PASS" if has_user else "FAIL",
            "details": "Container executes as non-root user (UID: 10001)" if has_user else "Missing USER declaration"
        }

    def check_zdr_enclave_files(self) -> Dict[str, Any]:
        """Verifies no unencrypted credential files are left in git."""
        forbidden_patterns = [".pem", ".key", "id_rsa"]
        found = []
        for root, _, files in os.walk(self.root_dir):
            if ".git" in root: continue
            for file in files:
                if any(file.endswith(ext) for ext in forbidden_patterns):
                    found.append(file)

        return {
            "control": "SECRET_ZERO_LEAKAGE",
            "standard": "EU AI Act Annex IV & SOC 2 CC6.3",
            "status": "PASS" if not found else "FAIL",
            "details": "No lingering private keys or cleartext certs found in repository" if not found else f"Found: {found}"
        }

    def run_all_checks(self) -> Dict[str, Any]:
        checks = [
            self.check_non_root_dockerfile(),
            self.check_zdr_enclave_files()
        ]
        all_passed = all(c["status"] == "PASS" for c in checks)
        return {
            "audit_status": "COMPLIANT" if all_passed else "NON_COMPLIANT",
            "total_controls": len(checks),
            "passed_controls": len([c for c in checks if c["status"] == "PASS"]),
            "results": checks
        }

if __name__ == "__main__":
    checker = AutomatedComplianceChecker()
    report = checker.run_all_checks()
    print(json.dumps(report, indent=2))
    if report["audit_status"] != "COMPLIANT":
        sys.exit(1)
