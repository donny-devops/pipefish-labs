import os
import re
import unittest
from pathlib import Path

class TestAdmissionAndMcpPolicy(unittest.TestCase):
    def setUp(self):
        self.security_dir = Path(__file__).resolve().parent.parent / "security"
        self.admission_file = self.security_dir / "agent_admission_policy.rego"
        self.mcp_file = self.security_dir / "mcp_tool_boundary_policy.rego"

    def test_rego_files_exist(self):
        self.assertTrue(self.admission_file.is_file(), "agent_admission_policy.rego must exist")
        self.assertTrue(self.mcp_file.is_file(), "mcp_tool_boundary_policy.rego must exist")

    def test_admission_policy_rules(self):
        content = self.admission_file.read_text(encoding="utf-8")
        self.assertIn("package pipefish.admission", content)
        self.assertIn("import rego.v1", content)
        self.assertIn("runAsNonRoot", content)
        self.assertIn("readOnlyRootFilesystem", content)
        self.assertIn("hostPath", content)
        self.assertIn("privileged", content)
        self.assertIn("allowPrivilegeEscalation", content)
        self.assertIn("limits.cpu", content)
        self.assertIn("limits.memory", content)
        self.assertIn("hostNetwork", content)
        self.assertIn("hostPID", content)
        self.assertIn("hostIPC", content)

    def test_mcp_policy_rules(self):
        content = self.mcp_file.read_text(encoding="utf-8")
        self.assertIn("package pipefish.mcp", content)
        self.assertIn("import rego.v1", content)
        self.assertIn("VoiceReceptionistBot", content)
        self.assertIn("SalesGrowthOrchestrator", content)
        self.assertIn("ReverseEngineerBot", content)
        self.assertIn("CryptoArchitectBot", content)
        self.assertIn("has_boundary_violation", content)

    def test_simulated_mcp_boundary_validation(self):
        # Python mirror of the Rego boundary violation rules
        def has_boundary_violation(args: dict) -> bool:
            pattern = re.compile(r"[;&|`]")
            for k, val in args.items():
                if isinstance(val, str):
                    if "../" in val or "..\\" in val:
                        return True
                    if pattern.search(val):
                        return True
            return False

        # Compliant payload
        safe_args = {"action": "status", "query": "latency_report", "limit": "100"}
        self.assertFalse(has_boundary_violation(safe_args))

        # Path traversal attack
        traversal_args = {"file": "../../etc/shadow"}
        self.assertTrue(has_boundary_violation(traversal_args))

        # Windows path traversal attack
        win_traversal_args = {"path": "..\\..\\windows\\system32"}
        self.assertTrue(has_boundary_violation(win_traversal_args))

        # Shell command injection
        cmd_injection_args = {"param": "status; rm -rf /"}
        self.assertTrue(has_boundary_violation(cmd_injection_args))

        # Subshell execution
        subshell_args = {"param": "file`whoami`"}
        self.assertTrue(has_boundary_violation(subshell_args))

if __name__ == "__main__":
    unittest.main()
