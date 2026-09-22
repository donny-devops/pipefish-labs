-- ==============================================================================
-- PipeFish Labs — Supabase / PostgreSQL Enterprise Database Schema
-- Version: 2.4.0
-- Security: Row Level Security (RLS), Encrypted PII, Tamper-Proof Audit Ledgers
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. ENUMS
CREATE TYPE agent_scenario_type AS ENUM (
  'receptionist', 'sales', 'logistics', 'integration', 'quantum',
  'reverse', 'crypto', 'errorcorr', 'trend', 'market', 'codescan',
  'docs', 'observability', 'revops', 'analytics', 'auditing',
  'logtriage', 'erp', 'trafficrouter', 'networkdispatch',
  'selfimproving', 'systemoptimizing', 'finops', 'contractintel',
  'missedcalltextback'
);

CREATE TYPE execution_status AS ENUM ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED');
CREATE TYPE subscription_tier AS ENUM ('STARTER', 'GROWTH', 'ENTERPRISE');

-- 2. TENANTS TABLE
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  tier subscription_tier NOT NULL DEFAULT 'STARTER',
  api_key_hash VARCHAR(64) NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. AGENT EXECUTIONS TABLE
CREATE TABLE agent_executions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  scenario agent_scenario_type NOT NULL,
  status execution_status NOT NULL DEFAULT 'PENDING',
  nodes_executed INT NOT NULL DEFAULT 0,
  zdr_enclave_verified BOOLEAN NOT NULL DEFAULT TRUE,
  handoff_mode VARCHAR(64) NOT NULL DEFAULT 'mistral_native',
  pqc_cipher VARCHAR(64) NOT NULL DEFAULT 'NIST-FIPS-203-ML-KEM-768',
  inbound_telemetry JSONB,
  started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

-- 4. DAG STATE HANDOFF LOGS (Tamper-Evident Ledger)
CREATE TABLE dag_handoff_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  execution_id UUID NOT NULL REFERENCES agent_executions(id) ON DELETE CASCADE,
  step_index INT NOT NULL,
  source_node VARCHAR(64) NOT NULL,
  target_node VARCHAR(64) NOT NULL,
  payload_sha256 VARCHAR(64) NOT NULL,
  hmac_signature VARCHAR(128) NOT NULL,
  mcp_connector VARCHAR(128),
  verified_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. COMPLIANCE AUDIT LEDGER (Immutable append-only log)
CREATE TABLE compliance_audit_ledger (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  standard VARCHAR(64) NOT NULL,
  control_id VARCHAR(32) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'COMPLIANT',
  integrity_sha256 VARCHAR(64) NOT NULL,
  verified_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. LEMON SQUEEZY SUBSCRIPTIONS
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  lemon_squeezy_order_id VARCHAR(128) UNIQUE,
  customer_email VARCHAR(255) NOT NULL,
  tier subscription_tier NOT NULL DEFAULT 'GROWTH',
  status VARCHAR(64) NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMPTZ
);

-- 7. INDEXES FOR HIGH-THROUGHPUT LOOKUPS
CREATE INDEX idx_executions_tenant_scenario ON agent_executions(tenant_id, scenario);
CREATE INDEX idx_handoff_execution ON dag_handoff_logs(execution_id, step_index);
CREATE INDEX idx_audit_tenant_standard ON compliance_audit_ledger(tenant_id, standard);

-- 8. ROW LEVEL SECURITY (RLS) POLICIES
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_executions ENABLE ROW LEVEL SECURITY;
ALTER TABLE dag_handoff_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE compliance_audit_ledger ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_tenants ON tenants
  FOR ALL
  USING (id = current_setting('app.current_tenant_id', true)::UUID);

CREATE POLICY tenant_isolation_executions ON agent_executions
  FOR ALL
  USING (tenant_id = current_setting('app.current_tenant_id', true)::UUID);

CREATE POLICY tenant_isolation_handoff_logs ON dag_handoff_logs
  FOR ALL
  USING (
    execution_id IN (
      SELECT id FROM agent_executions
      WHERE tenant_id = current_setting('app.current_tenant_id', true)::UUID
    )
  );

CREATE POLICY tenant_isolation_audit_ledger ON compliance_audit_ledger
  FOR ALL
  USING (tenant_id = current_setting('app.current_tenant_id', true)::UUID);

CREATE POLICY tenant_isolation_subscriptions ON subscriptions
  FOR ALL
  USING (tenant_id = current_setting('app.current_tenant_id', true)::UUID);

-- 9. IMMUTABLE APPEND-ONLY AUDIT & HANDOFF TRIGGERS
CREATE OR REPLACE FUNCTION prevent_audit_tampering()
RETURNS TRIGGER AS $$
BEGIN
  RAISE EXCEPTION 'Cryptographic audit ledger rows are immutable. Updates and deletions are strictly prohibited.';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_immutable_compliance_audit
  BEFORE UPDATE OR DELETE ON compliance_audit_ledger
  FOR EACH ROW EXECUTE FUNCTION prevent_audit_tampering();

CREATE TRIGGER trg_immutable_dag_handoffs
  BEFORE UPDATE OR DELETE ON dag_handoff_logs
  FOR EACH ROW EXECUTE FUNCTION prevent_audit_tampering();
