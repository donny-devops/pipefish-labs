import os
import unittest
import re

class TestDatabaseSchema(unittest.TestCase):
    def setUp(self):
        schema_path = os.path.join(os.path.dirname(__file__), "..", "db", "schema.sql")
        with open(schema_path, "r", encoding="utf-8") as f:
            self.schema_sql = f.read()

    def test_enum_contains_all_25_scenarios(self):
        expected_scenarios = [
            "receptionist", "sales", "logistics", "integration", "quantum",
            "reverse", "crypto", "errorcorr", "trend", "market", "codescan",
            "docs", "observability", "revops", "analytics", "auditing",
            "logtriage", "erp", "trafficrouter", "networkdispatch",
            "selfimproving", "systemoptimizing", "finops", "contractintel",
            "missedcalltextback"
        ]
        enum_match = re.search(
            r"CREATE TYPE agent_scenario_type AS ENUM \((.*?)\);",
            self.schema_sql,
            re.DOTALL
        )
        self.assertIsNotNone(enum_match, "agent_scenario_type ENUM not found in schema.sql")
        enum_body = enum_match.group(1)
        for scenario in expected_scenarios:
            self.assertIn(f"'{scenario}'", enum_body, f"Scenario '{scenario}' missing from agent_scenario_type ENUM")

    def test_rls_enabled_on_all_tables(self):
        tables = [
            "tenants",
            "agent_executions",
            "dag_handoff_logs",
            "compliance_audit_ledger",
            "subscriptions"
        ]
        for table in tables:
            pattern = rf"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;"
            self.assertRegex(
                self.schema_sql,
                pattern,
                f"Table '{table}' does not have Row Level Security enabled."
            )

    def test_tenant_isolation_policies(self):
        policies = [
            "tenant_isolation_tenants",
            "tenant_isolation_executions",
            "tenant_isolation_handoff_logs",
            "tenant_isolation_audit_ledger",
            "tenant_isolation_subscriptions"
        ]
        for policy in policies:
            pattern = rf"CREATE POLICY {policy} ON"
            self.assertRegex(
                self.schema_sql,
                pattern,
                f"Policy '{policy}' missing from schema.sql"
            )

    def test_immutable_audit_triggers(self):
        self.assertIn("prevent_audit_tampering", self.schema_sql)
        self.assertIn("trg_immutable_compliance_audit", self.schema_sql)
        self.assertIn("trg_immutable_dag_handoffs", self.schema_sql)

if __name__ == "__main__":
    unittest.main()
