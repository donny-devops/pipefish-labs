import os
import json

spec_data = {
  "receptionist": {
    "title": "Receptionist Agent (Voice & Text)",
    "skills": "voice-receptionist, text-intent-classifier, calendar-sync, crm-emr-bridge",
    "mcp": "mcp-server-telephony (Twilio/Telnyx), mcp-server-google-calendar, mcp-server-hubspot",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/voice-intake | mailhook://support-inbound@pipefishlabs.io",
    "secrets": "Twilio Account SID/Auth Token (HashiCorp Vault KV v2), OAuth2 Refresh Tokens",
    "apis": "Twilio Voice API, Google Calendar API v3, HubSpot CRM API, Stripe Billing API",
    "a2a": "mTLS gRPC DAG Handoff with HMAC-SHA256 state signature verification",
    "rbac": "Role: VoiceReceptionistBot | Perms: calendar.read_write, crm.contact.create (ZDR Enclave)"
  },
  "sales": {
    "title": "Sales Enablement Agent",
    "skills": "lead-scoring-icp, salesforce-hubspot-sync, proposal-gen, clearbit-enrichment",
    "mcp": "mcp-server-salesforce, mcp-server-apollo, mcp-server-doc-generator",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/lead-form | mailhook://sales-inbound@pipefishlabs.io",
    "secrets": "Salesforce Connected App Client Secret (AWS KMS), Clearbit API Key (Vault)",
    "apis": "Salesforce REST API v58, Apollo.io Enrichment API, Pandadoc API, Slack Webhooks",
    "a2a": "JSON-RPC over NATS JetStream with RSA-4096 Signed Payload Tokens",
    "rbac": "Role: SalesEnablementBot | Perms: crm.opportunity.edit, email.send, doc.generate"
  },
  "logistics": {
    "title": "Logistics / Supply Chain Agent",
    "skills": "edi-manifest-parser, telematics-gps-monitor, port-rerouting, customs-clearing",
    "mcp": "mcp-server-edi-214, mcp-server-port-rotterdam-api, mcp-server-freight-crm",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/edi-ingest | mailhook://dispatch@pipefishlabs.io",
    "secrets": "EDI Trading Partner Certificates (Vault PKI), GPS Telematics API Token",
    "apis": "EDI 204/214/856 Standards, Samsara Telematics API, Project44 Visibility API",
    "a2a": "Kafka Event Mesh with Avro Schema Validation & PQC Dilithium Signatures",
    "rbac": "Role: SupplyChainDispatcher | Perms: manifest.read, reroute.execute, edi.transmit"
  },
  "integration": {
    "title": "Integration Agent",
    "skills": "multi-protocol-ingest, schema-transformer-xml-json, state-sync, Vault-oauth-lifecycle",
    "mcp": "mcp-server-kafka, mcp-server-sap-rfc, mcp-server-graphql-gateway",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/integration-mesh | mailhook://sync@pipefishlabs.io",
    "secrets": "SAP RFC Service Account Keys (Vault), OAuth2 Client Secret Store",
    "apis": "Kafka REST Proxy, SAP S/4HANA OData API, GraphQL Mesh, Workday REST API",
    "a2a": "gRPC Streaming with Circuit Breaker & Automatic Retry Fallback",
    "rbac": "Role: MiddlewareIntegrator | Perms: stream.read_write, token.rotate, schema.transform"
  },
  "quantum": {
    "title": "Execution Agent",
    "skills": "vqe-eigensolver, circuit-transpiler, quantum-error-mitigation, hpc-execution",
    "mcp": "mcp-server-qiskit, mcp-server-ibm-quantum, mcp-server-aws-braket",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/quantum-job-results",
    "secrets": "IBM Quantum Platform API Key (Vault KV v2), AWS Braket Access Keys",
    "apis": "Qiskit Runtime API, IBM Q Cloud REST API, AWS Braket SDK, Cirq Engine",
    "a2a": "Asynchronous Parallel Worker Threads with Zero-Noise Extrapolation Verification",
    "rbac": "Role: QuantumExecutionEngine | Perms: qpu.submit, transpiler.compile, hpc.allocate"
  },
  "reverse": {
    "title": "Reverse Engineering Agent",
    "skills": "binary-disassembly, control-flow-graph, ghidra-ast, yara-generator",
    "mcp": "mcp-server-ghidra-headless, mcp-server-yara-compiler, mcp-server-cape-sandbox",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/binary-analysis-intel",
    "secrets": "Ghidra Server Auth Credentials, VirusTotal API Enterprise Key",
    "apis": "Ghidra Headless API, CAPEv2 Sandbox REST API, YARA C Engine, Binary Ninja API",
    "a2a": "Isolated Container IPC Enclave with Cryptographic Hash Integrity Verification",
    "rbac": "Role: ReverseEngineerBot | Perms: binary.disassemble, cfg.generate, yara.compile"
  },
  "crypto": {
    "title": "Encryption / Cryptography Agent",
    "skills": "nist-ml-kem-768, nist-ml-dsa-signatures, hsm-vault-rotation, mtls-hybrid-pki",
    "mcp": "mcp-server-openssl-pqc, mcp-server-hashicorp-vault, mcp-server-aws-kms",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/pqc-key-rotation-alert",
    "secrets": "Vault Root CA Master Token, AWS KMS Hardware Security Module Master Key",
    "apis": "OpenSSL 3.2 PQC Module, HashiCorp Vault Transit API, AWS KMS Sign/Verify",
    "a2a": "NIST FIPS 203 (ML-KEM-768) Encapsulated Key Exchange over mTLS 1.3",
    "rbac": "Role: CryptoArchitectBot | Perms: kms.rotate, cert.issue, enclave.encrypt"
  },
  "errorcorr": {
    "title": "Error-Correcting Agent",
    "skills": "reed-solomon-repair, ldpc-parity-checker, berlekamp-massey-locator, vector-shard-rebuilder",
    "mcp": "mcp-server-reed-solomon, mcp-server-vector-shard-manager, mcp-server-parity",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/parity-corruption-repair",
    "secrets": "Vector Database Storage Encryption Keys (Vault KV v2)",
    "apis": "Reed-Solomon C++ Native Library, Pinecone Shard Management API, Qdrant API",
    "a2a": "High-Speed Memory Bus RPC with Parity Check Bit Verification",
    "rbac": "Role: ErrorCorrectionEngine | Perms: shard.repair, parity.compute, storage.write"
  },
  "trend": {
    "title": "Trend Spotting Agent",
    "skills": "multi-source-signal-scraper, semantic-embedding-cluster, patent-correlator, strategy-alert",
    "mcp": "mcp-server-patent-uspto, mcp-server-twitter-v2, mcp-server-rss-aggregator",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/macro-trend-alert",
    "secrets": "X/Twitter API v2 Bearer Token, USPTO Patent Search Key (Vault)",
    "apis": "USPTO Open Data API, arXiv API, NewsAPI, Pinecone Vector Index",
    "a2a": "Pub/Sub Stream with Isolation Forest Velocity Anomaly Triggering",
    "rbac": "Role: TrendSpottingBot | Perms: signal.scrape, embedding.compute, alert.dispatch"
  },
  "market": {
    "title": "Market Research Agent",
    "skills": "sec-10k-extractor, competitive-matrix, tam-sam-calculator, swot-synthesizer",
    "mcp": "mcp-server-sec-edgar, mcp-server-gartner-search, mcp-server-rag-vector-db",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/market-research-digest",
    "secrets": "SEC EDGAR User-Agent Auth Headers, Financial Data API Key (Vault)",
    "apis": "SEC EDGAR REST API, Financial Modeling Prep API, OpenAI Embeddings API",
    "a2a": "RAG Vector Context Retrieval with Cross-Encoder Reranking",
    "rbac": "Role: MarketAnalystBot | Perms: edgar.fetch, rag.query, dossier.build"
  },
  "codescan": {
    "title": "Code-Scanning Agent",
    "skills": "ast-semgrep-parser, entropy-secret-scanner, owasp-cve-matcher, pr-inline-blocking",
    "mcp": "mcp-server-semgrep, mcp-server-github-actions, mcp-server-dependency-track",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/sast-dast-audit-event",
    "secrets": "GitHub App Private Key (Vault), SonarQube Auth Token",
    "apis": "GitHub GraphQL API v4, Semgrep CLI API, Dependency-Track REST API",
    "a2a": "Git Commit Hook Trigger with Automated PR Inline Blocking",
    "rbac": "Role: SecurityScannerBot | Perms: code.scan, pr.comment, build.block"
  },
  "docs": {
    "title": "Documentation Agent",
    "skills": "ast-code-extractor, openapi-31-gen, mermaid-diagram-gen, portal-publisher",
    "mcp": "mcp-server-typedoc, mcp-server-mermaid, mcp-server-openapi-generator",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/autodoc-build-complete",
    "secrets": "Developer Portal Deployment Token (Vault v2)",
    "apis": "TypeDoc CLI API, Sphinx Builder, OpenAPI v3.1 Spec Generator",
    "a2a": "CI/CD Pipeline Hook with Automated Markdown & Diagram Generation",
    "rbac": "Role: DocGeneratorBot | Perms: ast.parse, doc.publish, site.build"
  },
  "observability": {
    "title": "Monitoring / Observability Agent",
    "skills": "opentelemetry-collector, trace-correlator-jaeger, prometheus-anomaly, self-healing-remediation",
    "mcp": "mcp-server-prometheus, mcp-server-jaeger, mcp-server-grafana-api",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/opentelemetry-alert",
    "secrets": "Grafana Admin API Token, Datadog Application Key (Vault)",
    "apis": "OpenTelemetry Collector Protocol (OTLP), Prometheus Query API (PromQL), Jaeger Tracing",
    "a2a": "OTLP gRPC Trace Mesh with SLA Violation Triggering",
    "rbac": "Role: ObservabilityEngine | Perms: telemetry.read, alert.fire, pod.restart"
  },
  "revops": {
    "title": "Growth Strategy Agent",
    "skills": "posthog-signup-monitor, plg-lead-scorer, dynamic-personalization, stripe-ltv-predictor",
    "mcp": "mcp-server-posthog, mcp-server-clearbit, mcp-server-stripe-billing",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/growth-intent-trigger",
    "secrets": "PostHog Project Key, Stripe Secret Key (Vault v2)",
    "apis": "PostHog Insights API, Segment Stream, Clearbit Reveal API, Stripe API",
    "a2a": "Real-Time Event Stream with Dynamic Landing Page Personalization",
    "rbac": "Role: RevOpsGrowthBot | Perms: analytics.read, crm.enrich, variant.deploy"
  },
  "analytics": {
    "title": "Research Agent",
    "skills": "clickhouse-stream-ingest, cohort-funnel-calc, churn-predictor, bi-dashboard-synth",
    "mcp": "mcp-server-snowflake, mcp-server-clickhouse, mcp-server-mixpanel",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/analytics-digest",
    "secrets": "Snowflake Key-Pair Auth Credentials (Vault), ClickHouse SSL Key",
    "apis": "ClickHouse HTTP Query API, Snowflake SQL REST API, Mixpanel Export API",
    "a2a": "High-Throughput Vector Embedding Query Loop over Distributed Shards",
    "rbac": "Role: ResearchAnalystBot | Perms: db.query, cohort.compute, bi.export"
  },
  "auditing": {
    "title": "Analysis Agent",
    "skills": "cloudtrail-audit-collector, iam-policy-verifier, kms-vault-auditor, nonconformity-detector",
    "mcp": "mcp-server-aws-cloudtrail, mcp-server-gcp-audit, mcp-server-vault-sys",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/soc2-audit-proof",
    "secrets": "AWS ReadOnlyAudit Access Key (Vault), GCP Audit Service Account",
    "apis": "AWS CloudTrail API, GCP Cloud Audit Logs API, HashiCorp Vault Sys API",
    "a2a": "Immutable Merkle Tree Ledger Verification Protocol",
    "rbac": "Role: AuditAnalysisBot | Perms: audit.read, policy.verify, report.sign"
  },
  "logtriage": {
    "title": "Log Triage Agent",
    "skills": "vector-log-tokenizer, stack-trace-extractor, severity-classifier, pagerduty-dispatcher",
    "mcp": "mcp-server-elasticsearch, mcp-server-sentry, mcp-server-pagerduty",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/log-exception-ingest",
    "secrets": "Elasticsearch API Key (Vault), PagerDuty Events v2 API Key",
    "apis": "Vector Log Engine API, Elasticsearch Search API, PagerDuty Events v2 API",
    "a2a": "Zero-Loss Vector Stream Tokenizer with P1 Escalation Triggers",
    "rbac": "Role: LogTriageBot | Perms: logs.ingest, issue.link, incident.trigger"
  },
  "erp": {
    "title": "Audit Agent",
    "skills": "sap-oracle-master-sync, po-3way-matcher, general-ledger-double-entry, edi-dispatcher",
    "mcp": "mcp-server-sap-s4hana, mcp-server-oracle-fusion, mcp-server-avalara",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/erp-financial-event",
    "secrets": "SAP Client Certificates (Vault PKI), Avalara Tax API Password",
    "apis": "SAP S/4HANA Financials OData API, Oracle ERP Cloud REST API, Avalara AvaTax",
    "a2a": "Double-Entry Cryptographic Balance Audit Handoff",
    "rbac": "Role: FinancialAuditBot | Perms: ledger.post, po.match, edi.dispatch"
  },
  "trafficrouter": {
    "title": "Traffic Router Agent",
    "skills": "bgp-edge-health-monitor, route53-geo-balancer, cloudflare-waf-shield, canary-shifter",
    "mcp": "mcp-server-cloudflare-workers, mcp-server-aws-route53, mcp-server-envoy-proxy",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/edge-latency-alert",
    "secrets": "Cloudflare Global API Key (Vault v2), AWS Route 53 IAM Token",
    "apis": "Cloudflare v4 REST API, AWS Route 53 API, Envoy Control Plane gRPC",
    "a2a": "BGP Anycast Dynamic Routing Control Plane Protocol",
    "rbac": "Role: EdgeTrafficRouter | Perms: dns.update, WAF.block, proxy.configure"
  },
  "networkdispatch": {
    "title": "Network Dispatch Agent",
    "skills": "sdwan-topology-analyzer, qos-dssc-prioritizer, wireguard-provisioner, zero-touch-provisioner",
    "mcp": "mcp-server-cisco-sdwan, mcp-server-juniper-pyez, mcp-server-wireguard",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/sdwan-mesh-alert",
    "secrets": "Cisco vManage Authentication Token (Vault), WireGuard Private Key Store",
    "apis": "Cisco SD-WAN REST API, Juniper PyEZ RPC API, WireGuard Kernel API",
    "a2a": "gNMI / YANG Network Telemetry Stream over Encrypted WireGuard Tunnel",
    "rbac": "Role: NetworkDispatchEngine | Perms: sdwan.configure, tunnel.create, qos.set"
  },
  "selfimproving": {
    "title": "Self-Improving Agent",
    "skills": "opentelemetry-trace-collector, failure-taxonomy-categorizer, dspy-prompt-autotuner, vector-memory",
    "mcp": "mcp-server-dspy-optimizer, mcp-server-pinecone-memory, mcp-server-eval-harness",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/reflection-loop-complete",
    "secrets": "Pinecone Vector DB Master Key (Vault v2), DSPy Optimization Secret",
    "apis": "DSPy Optimization Engine, Pinecone Vector API, OpenTelemetry Trace API",
    "a2a": "LLM Self-Critique & Automated Instruction Mutation Reflection Loop",
    "rbac": "Role: SelfImprovingEngine | Perms: prompt.mutate, memory.write, eval.run"
  },
  "systemoptimizing": {
    "title": "System-Optimizing Agent",
    "skills": "ebpf-cpu-memory-profiler, explain-analyze-planner, redis-cache-tuner, k8s-hpa-autoscaler",
    "mcp": "mcp-server-ebpf-profiler, mcp-server-postgres-planner, mcp-server-k8s-metrics",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/runtime-tuning-event",
    "secrets": "Kubernetes Service Account Token (Vault), Redis Cluster Auth Pass",
    "apis": "eBPF Kernel Profiler, PostgreSQL EXPLAIN API, Kubernetes Metrics Server API",
    "a2a": "Low-Overhead Kernel Telemetry Stream with Automated HPA Scaling Triggers",
    "rbac": "Role: SystemOptimizerBot | Perms: k8s.autoscale, query.optimize, cache.flush"
  }
}

# Update demo/index.html as well
with open('demo/index.html', 'r', encoding='utf-8') as fp:
    demo_content = fp.read()

js_code = f"window.agentSpecsData = {json.dumps(spec_data)};\n"
if 'window.agentSpecsData' not in demo_content:
    demo_content = demo_content.replace('const scenarios = {', js_code + 'const scenarios = {')

drawer_html = '''
      <!-- Dynamic Agent Architecture Spec Drawer -->
      <div id="demo-spec-drawer" style="margin-top:24px;background:rgba(6,7,12,0.92);border:1px solid var(--border-strong);border-radius:var(--r-md);padding:24px;box-shadow:0 0 30px rgba(0,212,255,0.08)">
        <!-- Rendered dynamically -->
      </div>
'''
if 'id="demo-spec-drawer"' not in demo_content:
    demo_content = demo_content.replace('<div class="demo-status-bar">', drawer_html + '\n      <div class="demo-status-bar">')

# Update renderDemoRows in demo/index.html
old_render = '''function renderDemoRows() {
  const container = document.getElementById('demo-rows-container');
  const sc = scenarios[currentScenarioKey];
  container.innerHTML = '';
  sc.nodes.forEach((node, index) => {
    const row = document.createElement('div');
    row.className = 'demo-row';
    row.id = `demo-node-${index}`;
    row.innerHTML = `
      <div class="demo-node-num">${node.num}</div>
      <div class="demo-node-title">${node.title}</div>
      <div class="demo-node-desc">${node.desc}</div>
      <div class="demo-node-status" id="demo-status-${index}">Standby</div>
    `;
    container.appendChild(row);
  });
}'''

new_render = '''function renderDemoRows() {
  const container = document.getElementById('demo-rows-container');
  const drawerEl = document.getElementById('demo-spec-drawer');
  const sc = scenarios[currentScenarioKey];
  container.innerHTML = '';
  sc.nodes.forEach((node, index) => {
    const row = document.createElement('div');
    row.className = 'demo-row';
    row.id = `demo-node-${index}`;
    row.innerHTML = `
      <div class="demo-node-num">${node.num}</div>
      <div class="demo-node-title">${node.title}</div>
      <div class="demo-node-desc">${node.desc}</div>
      <div class="demo-node-status" id="demo-status-${index}">Standby</div>
    `;
    container.appendChild(row);
  });

  if (drawerEl && window.agentSpecsData && window.agentSpecsData[currentScenarioKey]) {
    const spec = window.agentSpecsData[currentScenarioKey];
    drawerEl.innerHTML = `
      <div style="font-family:var(--font-display);font-size:14px;font-weight:800;color:var(--cyan);letter-spacing:0.12em;margin-bottom:14px;text-transform:uppercase;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">
        <span>⚡ AGENT ARCHITECTURE &amp; SECRETS DRAWER: ${spec.title}</span>
        <span style="font-size:11px;color:var(--text-dim);font-family:var(--font-mono)">ZERO-TRUST ENCLAVE VERIFIED</span>
      </div>
      <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:16px;font-size:12.5px;line-height:1.6">
        <div style="background:rgba(12,14,24,0.8);padding:12px;border:1px solid var(--border-strong);border-radius:6px">
          <strong style="color:var(--cyan);display:block;margin-bottom:4px;font-family:var(--font-mono)">🛠️ SKILL Files &amp; MCP Servers:</strong>
          <div style="color:var(--text-strong)">SKILLS: <span style="color:var(--magenta)">${spec.skills}</span></div>
          <div style="color:var(--text-body);margin-top:2px">MCP: ${spec.mcp}</div>
        </div>
        <div style="background:rgba(12,14,24,0.8);padding:12px;border:1px solid var(--border-strong);border-radius:6px">
          <strong style="color:var(--cyan);display:block;margin-bottom:4px;font-family:var(--font-mono)">🌐 Webhooks &amp; Mailhooks:</strong>
          <div style="color:var(--text-strong);font-family:var(--font-mono);font-size:11.5px">${spec.webhooks}</div>
        </div>
        <div style="background:rgba(12,14,24,0.8);padding:12px;border:1px solid var(--border-strong);border-radius:6px">
          <strong style="color:var(--cyan);display:block;margin-bottom:4px;font-family:var(--font-mono)">🔐 Secrets &amp; Management Platform:</strong>
          <div style="color:var(--text-strong)">${spec.secrets}</div>
        </div>
        <div style="background:rgba(12,14,24,0.8);padding:12px;border:1px solid var(--border-strong);border-radius:6px">
          <strong style="color:var(--cyan);display:block;margin-bottom:4px;font-family:var(--font-mono)">🔌 Target APIs &amp; Dependencies:</strong>
          <div style="color:var(--text-strong)">${spec.apis}</div>
        </div>
        <div style="background:rgba(12,14,24,0.8);padding:12px;border:1px solid var(--border-strong);border-radius:6px">
          <strong style="color:var(--cyan);display:block;margin-bottom:4px;font-family:var(--font-mono)">🛰️ A2A Communication Protocols:</strong>
          <div style="color:var(--text-strong)">${spec.a2a}</div>
        </div>
        <div style="background:rgba(12,14,24,0.8);padding:12px;border:1px solid var(--border-strong);border-radius:6px">
          <strong style="color:var(--cyan);display:block;margin-bottom:4px;font-family:var(--font-mono)">🛡️ Access Control, Roles &amp; Permissions:</strong>
          <div style="color:var(--text-strong);font-family:var(--font-mono);font-size:11.5px">${spec.rbac}</div>
        </div>
      </div>
    `;
  }
}'''

if old_render in demo_content:
    demo_content = demo_content.replace(old_render, new_render)

with open('demo/index.html', 'w', encoding='utf-8') as fp:
    fp.write(demo_content)

print("Successfully updated demo/index.html with Spec Drawer data.")
