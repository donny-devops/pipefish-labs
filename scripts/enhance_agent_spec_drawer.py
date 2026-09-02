import os
import json

spec_data = {
  "receptionist": {
    "title": "Receptionist Agent (Voice & Text)",
    "duties": "The Receptionist Agent combines voice and text handling into a unified intake pipeline for voice calls, SMS, web chats, and email channels:<br><br>• Multichannel Inbound Handling: Answers 100% of after-hours calls and incoming texts/emails with a low average voice latency of 3.2 seconds.<br>• Intent Classification &amp; Verification: Automatically classifies buyer intent, checks account eligibility, and verifies team capacity.<br>• Scheduling &amp; Sales Conversion: Books consultation calls directly into calendars, generates proposals, and handles follow-up contract and retainer signatures.<br>• Integrated Node Execution: Coordinates seamlessly downstream via Native Mistral Handoffs with availability checks, intake verification, CRM/EMR synchronization, automated payment requests, and escalation alerts.",
    "skills": "voice-receptionist, text-intent-classifier, calendar-sync, crm-emr-bridge",
    "mcp": "mcp-server-telephony (Twilio/Telnyx), mcp-server-google-calendar, mcp-server-hubspot",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/voice-intake | mailhook://support-inbound@pipefishlabs.io",
    "secrets": "Twilio Account SID/Auth Token (HashiCorp Vault KV v2), OAuth2 Refresh Tokens",
    "apis": "Twilio Voice API, Google Calendar API v3, HubSpot CRM API, Stripe Billing API",
    "a2a": "Mistral Native Handoff (Tool Call State Persistence across 8-Node Graph without Middleware)",
    "rbac": "Role: VoiceReceptionistBot | Perms: calendar.read_write, crm.contact.create (ZDR Enclave)"
  },
  "sales": {
    "title": "Sales Enablement Agent",
    "duties": "• Sales Operations Agent: Orchestrates backend pipeline mechanics, manages data workflows, and coordinates cross-functional task handoffs across enterprise systems.<br>• Sales Follow-Up Agent: Manages automated, context-aware touchpoints to keep prospects engaged after initial meetings without human intervention.<br>• Sales Outreach Agent: Crafts and executes hyper-personalized inbound and outbound messaging sequences tailored to buyer intent signals.<br>• Email Agent: Handles high-volume email composition, delivery tracking, and intelligent response parsing across communication threads.<br>• Lead Qualification Agent: Evaluates incoming leads against predefined account criteria, verifying budget, authority, need, and timeline instantly.<br>• CRM Hygiene Agent: Automatically cleans, enriches, and updates CRM records to ensure continuous data accuracy and eliminate manual data-entry lag.<br>• Proposal Generator Agent: Instantly synthesizes scoping data, pricing matrices, and terms to dynamically produce customized sales proposals.<br>• Deal Recovery Agent: Detects stalled pipelines or dormant opportunities, executing automated re-engagement triggers to resurrect dead deals.",
    "skills": "lead-scoring-icp, salesforce-hubspot-sync, proposal-gen, clearbit-enrichment",
    "mcp": "mcp-server-salesforce, mcp-server-apollo, mcp-server-doc-generator",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/lead-form | mailhook://sales-inbound@pipefishlabs.io",
    "secrets": "Salesforce Connected App Client Secret (AWS KMS), Clearbit API Key (Vault)",
    "apis": "Salesforce REST API v58, Apollo.io Enrichment API, Pandadoc API, Slack Webhooks",
    "a2a": "Mistral Native Handoff with Seamless Tool Call State Persistence",
    "rbac": "Role: SalesEnablementBot | Perms: crm.opportunity.edit, email.send, doc.generate"
  },
  "logistics": {
    "title": "Logistics / Supply Chain Agent",
    "duties": "Logistics and supply chain capabilities are engineered around an automated 8-node asynchronous agent chain that handles high-throughput freight orchestration, tracking, and exception management.<br><br>• EDI &amp; Manifest Parsing: Automatically extracts load details, transport specs, and status updates using standards like EDI 214.<br>• Cold-Chain &amp; Telematics Monitoring: Continuously monitors GPS and IoT telemetry signals to track temperature-sensitive cargo and transit milestones.<br>• Dynamic Re-Routing: Evaluates port and rail APIs in real-time (such as reacting to congestion at terminals like Rotterdam) to optimize shipment routes.<br>• Customs &amp; Tariff Clearing: Streamlines customs documentation and tariff processing to prevent border bottlenecks.<br>• Carrier Dispatch &amp; Tender: Coordinates tender offers and dispatches carriers based on availability, capacity, and historical performance.<br>• ETA Recalculation: Dynamically updates arrival projections based on live traffic, weather, and transit anomalies.<br>• Warehouse Intake Booking: Automatically schedules dock doors and books warehouse intake upon freight arrival.<br>• Consignee Alerts &amp; Exceptions: Resolves operational exceptions and alerts consignees proactively before delays impact delivery.",
    "skills": "edi-manifest-parser, telematics-gps-monitor, port-rerouting, customs-clearing",
    "mcp": "mcp-server-edi-214, mcp-server-port-rotterdam-api, mcp-server-freight-crm",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/edi-ingest | mailhook://dispatch@pipefishlabs.io",
    "secrets": "EDI Trading Partner Certificates (Vault PKI), GPS Telematics API Token",
    "apis": "EDI 204/214/856 Standards, Samsara Telematics API, Project44 Visibility API",
    "a2a": "Mistral Native Handoff (8-Node Asynchronous State Flow)",
    "rbac": "Role: SupplyChainDispatcher | Perms: manifest.read, reroute.execute, edi.transmit"
  },
  "integration": {
    "title": "Integration Agent",
    "duties": "<b>Integration Agent Capabilities</b><br><br>• Multi-Protocol Ingestion: Ingests events and signals across REST APIs, gRPC, GraphQL, webhooks, Kafka event meshes, and SAP RFC endpoints.<br>• Payload Transformation: Automatically reconciles schema field mismatches, transforming disparate formats such as converting XML payloads to JSON.<br>• Bi-Directional State Sync: Enforces real-time, synchronized state updates across enterprise systems, CRMs, and legacy architectures.<br>• Token Lifecycle Management: Manages OAuth 2.0 flows and API token lifecycles with secure vault integrations.<br>• Transactional Reliability: Implements transactional circuit breakers and automated retry loops to maintain fault-tolerant pipeline execution.<br>• Cryptographic Verification: Secures state handoffs and data pipelines using HMAC-SHA256 payload signing and NIST post-quantum encryption protocols.",
    "skills": "multi-protocol-ingest, schema-transformer-xml-json, state-sync, Vault-oauth-lifecycle",
    "mcp": "mcp-server-kafka, mcp-server-sap-rfc, mcp-server-graphql-gateway",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/integration-mesh | mailhook://sync@pipefishlabs.io",
    "secrets": "SAP RFC Service Account Keys (Vault), OAuth2 Client Secret Store",
    "apis": "Kafka REST Proxy, SAP S/4HANA OData API, GraphQL Mesh, Workday REST API",
    "a2a": "Mistral Native Handoff with Zero-Middleware State Handoff",
    "rbac": "Role: MiddlewareIntegrator | Perms: stream.read_write, token.rotate, schema.transform"
  },
  "quantum": {
    "title": "Execution Agent",
    "duties": "• Independent Step Execution: Runs standalone tasks within the multi-agent DAG pipeline, processing serialized data payloads without blocking downstream nodes.<br>• Cryptographic State Verification: Validates incoming payloads signed with HMAC-SHA256 and NIST post-quantum encryption standards before executing core business logic.<br>• Ephemeral ZDR Processing: Operates inside Zero-Data Retention confidential enclaves (such as AWS Nitro and SGX) to ensure 0-byte persistent storage of sensitive data during runtime.<br>• Cross-System Interoperability: Bridges custom Model Context Protocol (MCP) servers, enterprise APIs, and legacy software systems to carry out automated actions.<br>• Autonomous Error Escalation: Detects execution anomalies and routes exceptions back through error-correcting or triage agents when criteria fall outside preset parameters.",
    "skills": "vqe-eigensolver, circuit-transpiler, quantum-error-mitigation, hpc-execution",
    "mcp": "Managed Mistral MCP Connectors: mcp-server-qiskit, mcp-server-ibm-quantum, mcp-server-hashicorp-vault",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/quantum-job-results",
    "secrets": "IBM Quantum Platform API Key (Vault KV v2), AWS Braket Access Keys",
    "apis": "Qiskit Runtime API, IBM Q Cloud REST API, AWS Braket SDK, Cirq Engine",
    "a2a": "Mistral Native Handoff (Ephemeral ZDR Enclave Tool Handoff)",
    "rbac": "Role: QuantumExecutionEngine | Perms: qpu.submit, enclave.access (HashiCorp Vault Enclave Connector)"
  },
  "reverse": {
    "title": "Reverse Engineering Agent",
    "duties": "• Binary Disassembly &amp; PE/ELF Agent: Ingests obfuscated binaries or payload samples to map out initial file structures, headers, and export/import tables.<br>• Control Flow Graph (CFG) Agent: Decompiles and reconstructs control flow structures to visualize execution blocks, branching logic, and subroutine paths.<br>• Decompilation &amp; AST Agent (Ghidra Bridge): Interfaces with decompilation frameworks (such as Ghidra Headless API, IDA Pro, or Binary Ninja) to transform low-level assembly into clean Abstract Syntax Trees.<br>• Anti-Analysis &amp; Unpacker Agent: Detects, isolates, and neutralizes packing routines, anti-debugging checks, and environment evasion traps.<br>• API Hashing &amp; String Decrypter Agent: Resolves dynamic API hashing routines and automatically decrypts obfuscated string tables to reveal hidden configurations or indicators of compromise.<br>• C2 Network Protocol Agent: Analyzes network communication routines, protocol framing, and command-and-control beaconing mechanics embedded in the binary.<br>• YARA Signature Generator Agent: Automatically distills behavioral and structural traits into production-ready YARA rules for threat hunting and detection engineering.<br>• Threat Intel Dossier Agent: Synthesizes outputs across the entire analysis chain into a structured, comprehensive technical dossier and report.",
    "skills": "binary-disassembly, control-flow-graph, ghidra-ast, yara-generator",
    "mcp": "mcp-server-ghidra-headless, mcp-server-yara-compiler, mcp-server-cape-sandbox",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/binary-analysis-intel",
    "secrets": "Ghidra Server Auth Credentials, VirusTotal API Enterprise Key",
    "apis": "Ghidra Headless API, CAPEv2 Sandbox REST API, YARA C Engine, Binary Ninja API",
    "a2a": "Mistral Native Handoff (Isolated AST Enclave Tool Call)",
    "rbac": "Role: ReverseEngineerBot | Perms: binary.disassemble, cfg.generate, yara.compile"
  },
  "crypto": {
    "title": "Encryption / Cryptography Agent",
    "duties": "<b>Encryption / Cryptography Agent Capabilities</b><br><br>• Post-Quantum Cryptography (PQC) Integration: Provisions and enforces NIST FIPS 203 ML-KEM-768 key encapsulation mechanisms and FIPS 204 ML-DSA signatures across internal mTLS microservices.<br>• Hardware Security Module (HSM) Operations: Manages automated master key rotation and secure cryptographic operations integrated with HashiCorp Vault, AWS KMS, and PKI Certificate Authorities.<br>• Hybrid Certificate Enforcement: Oversees mTLS hybrid certificate management to secure modern multi-agent communication streams.<br>• Cryptographic Inventory &amp; Auditing: Automatically tracks, audits, and verifies cryptographic assets, algorithms, and key lifecycles across distributed systems.<br>• Zero-Data-Retention (ZDR) Handoffs: Coordinates with enclaves to ensure that sensitive payloads processed during multi-agent state transitions are kept secure in RAM-only environments with strict zero-byte retention policies.",
    "skills": "nist-ml-kem-768, nist-ml-dsa-signatures, hsm-vault-rotation, mtls-hybrid-pki",
    "mcp": "Managed Mistral MCP Connectors: mcp-server-openssl-pqc, mcp-server-hashicorp-vault, mcp-server-aws-kms",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/pqc-key-rotation-alert",
    "secrets": "Vault Root CA Master Token, AWS KMS Hardware Security Module Master Key",
    "apis": "OpenSSL 3.2 PQC Module, HashiCorp Vault Transit API, AWS KMS Sign/Verify",
    "a2a": "Mistral Native Handoff (NIST FIPS 203 ML-KEM-768 Tool Exchange)",
    "rbac": "Role: CryptoArchitectBot | Perms: kms.rotate, cert.issue, enclave.encrypt"
  },
  "errorcorr": {
    "title": "Error-Correcting Agent",
    "duties": "• Error Detection and Monitoring: Continuously scans distributed vector database shards and inbound telemetry streams to detect byte corruption rates and anomalous payloads.<br>• Reed-Solomon and LDPC Decoding: Utilizes error-correcting codes such as Reed-Solomon byte repair, LDPC parity checkers, and syndrome calculations to reconstruct damaged data payloads.<br>• Polynomial Evaluation: Employs specialized components like the Error Locator Polynomial Agent (Berlekamp-Massey) and Chien Search &amp; Evaluator Agent to isolate and correct transmission faults.<br>• Automated Data Integrity Verification: Validates restored data chunks through sequential pipeline handoffs before downstream synchronization or storage ingestion.",
    "skills": "reed-solomon-repair, ldpc-parity-checker, berlekamp-massey-locator, vector-shard-rebuilder",
    "mcp": "mcp-server-reed-solomon, mcp-server-vector-shard-manager, mcp-server-parity",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/parity-corruption-repair",
    "secrets": "Vector Database Storage Encryption Keys (Vault KV v2)",
    "apis": "Reed-Solomon C++ Native Library, Pinecone Shard Management API, Qdrant API",
    "a2a": "Mistral Native Handoff (Zero-Loss Memory Bus Tool Call)",
    "rbac": "Role: ErrorCorrectionEngine | Perms: shard.repair, parity.compute, storage.write"
  },
  "trend": {
    "title": "Trend Spotting Agent",
    "duties": "• Market Signal Monitoring: Continuously scans social APIs, forum discussions, patent registries, and RSS feeds to detect macro trends and consumer intent shifts.<br>• Velocity &amp; Anomaly Detection: Tracks metric surges (such as rapid spikes in post-quantum cryptography procurement discussions across CISO forums) to flag emerging industry movements early.<br>• Correlative Analysis: Works in tandem with patent and academic paper correlators to validate organic social trends against technical and scientific research.<br>• Upstream Telemetry Handoffs: Generates and passes structured JSON payloads downstream into semantic clustering, sentiment analysis, and executive trend dossier engines within the <a href=\"https://pipefishlabs.io/\" target=\"_blank\" style=\"color:var(--cyan);text-decoration:underline\">PipeFish Labs</a> agent mesh.",
    "skills": "multi-source-signal-scraper, semantic-embedding-cluster, patent-correlator, strategy-alert",
    "mcp": "Mistral Websearch Connector, mcp-server-patent-uspto, mcp-server-twitter-v2, mcp-server-rss-aggregator",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/macro-trend-alert",
    "secrets": "X/Twitter API v2 Bearer Token, USPTO Patent Search Key (Vault)",
    "apis": "USPTO Open Data API, arXiv API, NewsAPI, Pinecone Vector Index",
    "a2a": "Mistral Native Handoff (Isolation Forest Pub/Sub Tool Handoff)",
    "rbac": "Role: TrendSpottingBot | Perms: signal.scrape, embedding.compute, alert.dispatch"
  },
  "market": {
    "title": "Market Research Agent",
    "duties": "Market Research Agent functions as an autonomous data collection and intelligence node designed to monitor external market landscapes, aggregate competitive data, and synthesize macro trends without manual oversight.<br><br><b>Core Capabilities</b><br>• Automated Signal Scrapping &amp; Ingestion: Continuously pulling data from external industry sources, social forums, patent registries, academic papers, and RSS feeds.<br>• Trend &amp; Sentiment Analysis: Processing velocity surges in market demand, consumer sentiment, and emerging technology or procurement shifts (such as post-quantum cryptography adoption or competitor product releases).<br>• Competitor Horizon Mapping: Tracking market shifts, parsing competitive adjustments, and updating internal commercial opportunity scoring metrics.<br>• Executive Dossier Generation: Synthesizing disparate qualitative and quantitative data points into structured operational briefings, strategic alerts, and handoff payloads for upstream/downstream nodes like strategy or sales enablement agents.",
    "skills": "sec-filing-rag, websearch-connector, sec-10k-extractor, competitive-matrix, swot-synthesizer",
    "mcp": "Mistral Document Library RAG Tool, Mistral Websearch Connector, mcp-server-sec-edgar",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/market-research-digest",
    "secrets": "SEC EDGAR User-Agent Auth Headers, Financial Data API Key (Vault)",
    "apis": "SEC EDGAR REST API, Financial Modeling Prep API, OpenAI Embeddings API",
    "a2a": "Mistral Native Handoff (RAG & Websearch Context Persistence)",
    "rbac": "Role: MarketAnalystBot | Perms: edgar.fetch, rag.query, dossier.build"
  },
  "codescan": {
    "title": "Code-Scanning Agent",
    "duties": "Code-Scanning Agent functions as part of a SAST/DAST audit pipeline designed to scan repositories and commits for security flaws, code vulnerabilities, and exposed secrets.<br><br><b>Core Capabilities</b><br>• AST Syntax Tree Parsing: Utilizes engines like Semgrep to parse source code structures across large repositories (e.g., millions of lines of code) to identify logic flaws and code anti-patterns.<br>• Vulnerability Detection: Scans for critical security issues such as SQL injection vectors (e.g., in OAuth callback handlers) and other common application vulnerabilities.<br>• Secret &amp; API Key Scanning: Performs entropy checks and pattern matching to discover hardcoded API tokens, private keys, and cloud credentials (such as AWS secrets).<br>• Dependency Analysis: Matches somatic dependencies against known CVE databases to flag vulnerable software components.<br>• Automated Remediation &amp; Enforcement: Works alongside automated refatch/patch agents, generates inline pull request (PR) comments, and blocks unsafe code merges through deep integration with CI/CD systems, SonarQube, and Git hooks.",
    "skills": "ast-semgrep-parser, entropy-secret-scanner, owasp-cve-matcher, pr-inline-blocking",
    "mcp": "mcp-server-semgrep, mcp-server-github-actions, mcp-server-dependency-track",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/sast-dast-audit-event",
    "secrets": "GitHub App Private Key (Vault), SonarQube Auth Token",
    "apis": "GitHub GraphQL API v4, Semgrep CLI API, Dependency-Track REST API",
    "a2a": "Mistral Native Handoff (Git Commit Hook PR Tool Handoff)",
    "rbac": "Role: SecurityScannerBot | Perms: code.scan, pr.comment, build.block"
  },
  "docs": {
    "title": "Documentation Agent",
    "duties": "A documentation-focused AI agent combines automated tools, context-retrieval loops, and structured instructions to manage, write, and maintain documentation.<br><br><b>Core Capabilities</b><br>• Automated Content Generation: Drafts initial documentation, user guides, README files, or release notes directly from codebases, commit histories, or technical specifications.<br>• API Reference Synchronization: Monitors code or endpoint updates, detects parameter changes, and updates reference documentation automatically to prevent drift between code and docs.<br>• Style &amp; Quality Enforcement: Applies team-specific style guides, checks for clarity, flags terminology violations, and performs structural quality control (QC) checks.<br>• Interactive Q&amp;A and Support: Acts as an intelligent assistant capable of answering user or developer questions in natural language by parsing internal knowledge bases or product manuals.<br>• Workflow &amp; Task Execution: Operates within an agentic loop—reading files, running linters or formatters, executing scripts, and opening pull requests or change requests without manual step-by-step human intervention.",
    "skills": "ast-code-extractor, openapi-31-gen, mermaid-diagram-gen, portal-publisher",
    "mcp": "mcp-server-typedoc, mcp-server-mermaid, mcp-server-openapi-generator",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/autodoc-build-complete",
    "secrets": "Developer Portal Deployment Token (Vault v2)",
    "apis": "TypeDoc CLI API, Sphinx Builder, OpenAPI v3.1 Spec Generator",
    "a2a": "Mistral Native Handoff (CI/CD Markdown & Diagram Tool Handoff)",
    "rbac": "Role: DocGeneratorBot | Perms: ast.parse, doc.publish, site.build"
  },
  "observability": {
    "title": "Monitoring / Observability Agent",
    "duties": "Autonomous agents engineered for infrastructure monitoring and observability perform tasks spanning metric collection, log aggregation, automated anomaly detection, root cause analysis (RCA), and incident remediation. Unlike traditional static dashboards or rigid alerting rules (like Prometheus thresholds or PagerDuty triggers), observability agents utilize LLMs and deterministic tools to query telemetry pipelines, correlate cross-stack events, and execute safe triage workflows.<br><br><b>Core Capabilities</b><br>• Natural Language Telemetry Querying: Translates plain-text queries into structured metric or log expressions, querying Prometheus (PromQL), Loki (LogQL), OpenTelemetry, or Datadog APIs without requiring engineers to manually construct complex queries.<br>• Automated Root Cause Analysis: Cross-correlates alerts, recent deployments, infrastructure logs, and trace spans during an incident to isolate anomalies and pinpoint faulty code commits, misconfigured environment variables, or exhausted resource limits.<br>• Log Pattern Recognition &amp; Summarization: Aggregates noisy stack traces, error bursts, and warning logs into concise summaries, categorizing recurring exceptions and flagging novel error signatures.<br>• Proactive Anomaly Detection: Continuously evaluates baseline performance metrics (latency, CPU, memory, error rates) to flag subtle behavioral shifts or capacity exhaustion trends before they trigger hard alert thresholds.<br>• Self-Healing &amp; Remediation Orchestration: Triggers predefined, safety-checked remediation runbooks—such as restarting unhealthy microservices, scaling Kubernetes pods, flushing bloated caches, or rolling back faulty container deployments via CI/CD webhooks.<br>• Context-Aware Alert Enrichment: Automatically enriches alert notifications dispatched to Slack, PagerDuty, or Jira with relevant diagnostic context, including recent deployment diffs, affected pod IPs, and correlated dashboard links.<br><br><b>Underlying Architecture</b><br>• Data Ingestion &amp; APM Integration: Connects with observability backends via OpenTelemetry Collector, Prometheus, Grafana, Datadog, New Relic, or cloud-native providers (AWS CloudWatch, GCP Operations Suite).<br>• Execution Sandbox: Implements strict permission boundaries and human-in-the-loop (HITL) approval gates before executing destructive or high-impact remediation scripts (e.g., database failovers or traffic rerouting).<br>• Vector Memory &amp; Knowledge Retrieval: Utilizes vector databases to index past incident post-mortems, runbook documentation, and historical error logs, enabling the agent to retrieve relevant historical resolution steps for ongoing alerts.",
    "skills": "opentelemetry-collector, trace-correlator-jaeger, prometheus-anomaly, self-healing-remediation",
    "mcp": "mcp-server-prometheus, mcp-server-jaeger, mcp-server-grafana-api",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/opentelemetry-alert",
    "secrets": "Grafana Admin API Token, Datadog Application Key (Vault)",
    "apis": "OpenTelemetry Collector Protocol (OTLP), Prometheus Query API (PromQL), Jaeger Tracing",
    "a2a": "Mistral Native Handoff (OTLP Trace Mesh SLA Tool Handoff)",
    "rbac": "Role: ObservabilityEngine | Perms: telemetry.read, alert.fire, pod.restart"
  },
  "revops": {
    "title": "Growth Strategy Agent",
    "duties": "• Market Opportunity Analysis: Scans industry trends, competitor positioning, and customer feedback data to identify high-potential revenue channels and untapped audience segments.<br>• Funnel Optimization: Audits user acquisition, activation, retention, referral, and revenue (AARRR) metrics to pinpoint friction points and recommend conversion rate optimization (CRO) tactics.<br>• Automated Lead Generation: Executes multi-channel prospecting workflows, leveraging scrapers, API integrations, and enrichment tools to build targeted target-account lists.<br>• Content &amp; SEO Scaling: Analyzes search intent, keyword gaps, and traffic performance data to generate data-driven content outlines and programmatic SEO strategies.<br>• Experimentation &amp; A/B Testing: Designs, monitors, and evaluates rapid-fire growth experiments, calculating statistical significance and iteration roadmaps.<br>• Customer Retention Modelling: Analyzes churn triggers, engagement drops, and usage patterns to deploy automated re-engagement triggers and lifecycle marketing flows.",
    "skills": "posthog-signup-monitor, plg-lead-scorer, dynamic-personalization, stripe-ltv-predictor",
    "mcp": "mcp-server-posthog, mcp-server-clearbit, mcp-server-stripe-billing",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/growth-intent-trigger",
    "secrets": "PostHog Project Key, Stripe Secret Key (Vault v2)",
    "apis": "PostHog Insights API, Segment Stream, Clearbit Reveal API, Stripe API",
    "a2a": "Mistral Native Handoff (Real-Time Event Stream Personalization)",
    "rbac": "Role: RevOpsGrowthBot | Perms: analytics.read, crm.enrich, variant.deploy"
  },
  "analytics": {
    "title": "Research Agent",
    "duties": "<b>Research Agent Core Capabilities</b><br><br>• Autonomous Signal &amp; Telemetry Ingestion: Processes high-throughput data streams, ingests disparate enterprise signals, and prepares unstructured inputs for upstream processing.<br>• Built-In SEC Filing Synthesis &amp; RAG: Utilizes Mistral's out-of-the-box Document Library RAG tool and Websearch connector to parse SEC 10-K/10-Q filings, financial reports, and live market intelligence.<br>• Contextual Information Retrieval: Searches, aggregates, and synthesizes multi-source data across databases, APIs, and document stores to build coherent research dossiers.<br>• Directed Acyclic Graph (DAG) State Handoffs: Packages verified JSON payloads and passes structured context securely via Native Mistral Handoffs to downstream analysis and execution agents with persistent state.<br>• Zero-Data Retention (ZDR) Security Enforcement: Operates inside ephemeral confidential enclaves (AWS Nitro/SGX) to guarantee that sensitive research parameters leave zero retention footprints.<br>• Continuous Multi-Agent Coordination: Collaborates asynchronously with specialized nodes—such as the <a href=\"https://pipefishlabs.io/\" target=\"_blank\" style=\"color:var(--cyan);text-decoration:underline\">Analysis Agent</a>, <a href=\"https://pipefishlabs.io/\" target=\"_blank\" style=\"color:var(--cyan);text-decoration:underline\">Audit Agent</a>, and <a href=\"https://pipefishlabs.io/\" target=\"_blank\" style=\"color:var(--cyan);text-decoration:underline\">Execution Agent</a>—to maintain continuous operational momentum without human intervention.",
    "skills": "sec-filing-rag, websearch-connector, clickhouse-stream-ingest, cohort-funnel-calc, bi-dashboard-synth",
    "mcp": "Mistral Document Library RAG Tool, Mistral Websearch Connector, mcp-server-snowflake, mcp-server-clickhouse",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/analytics-digest",
    "secrets": "Snowflake Key-Pair Auth Credentials (Vault), ClickHouse SSL Key",
    "apis": "ClickHouse HTTP Query API, Snowflake SQL REST API, Mixpanel Export API",
    "a2a": "Mistral Native Handoff (Document Library RAG & Websearch Context Persistence)",
    "rbac": "Role: ResearchAnalystBot | Perms: db.query, cohort.compute, bi.export, rag.query"
  },
  "auditing": {
    "title": "Analysis Agent",
    "duties": "• Contextual Synthesis: Processes and analyzes structured signals, telemetry data, and multi-source inputs to extract actionable insights and operational requirements.<br>• Native Code Interpreter Execution: Attaches Mistral's native Code Interpreter to execute Python scripts directly within the context window for retention cohort calculations and stream telemetry analysis.<br>• State Verification: Evaluates data integrity and operational parameters before handing off verified payloads through Native Mistral Handoff state transitions.<br>• Decision Support: Powers automated decision-making engines by classifying intent, checking enterprise capacity, and flagging non-conformities or exceptions in real time.",
    "skills": "code-interpreter-python, cloudtrail-audit-collector, iam-policy-verifier, retention-cohort-calc, telemetry-stream-eval",
    "mcp": "Mistral Code Interpreter (Python Execution Sandbox), mcp-server-aws-cloudtrail, mcp-server-vault-sys",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/soc2-audit-proof",
    "secrets": "AWS ReadOnlyAudit Access Key (Vault), GCP Audit Service Account",
    "apis": "AWS CloudTrail API, GCP Cloud Audit Logs API, HashiCorp Vault Sys API, Python Execution Sandbox",
    "a2a": "Mistral Native Handoff (Code Interpreter Python Context Window Execution)",
    "rbac": "Role: AuditAnalysisBot | Perms: audit.read, policy.verify, python.execute, report.sign"
  },
  "logtriage": {
    "title": "Log Triage Agent",
    "duties": "• Inbound Log Ingestion: Parses high-volume telemetry streams (handling up to 85,000 log events per second) to classify critical exceptions, stack trace cascades, and API gateway timeouts.<br>• Vector Parsing &amp; Tokenization: Utilizes the <a href=\"https://pipefishlabs.io/\" target=\"_blank\" style=\"color:var(--cyan);text-decoration:underline\">High-Volume Log Parser &amp; Tokenizer Agent</a> engine to process incoming signals concurrently.<br>• Extraction &amp; Clustering: Automatically extracts stack traces and exception payloads, clustering and deduplicating noisy log events.<br>• Severity Classification &amp; SLA Matching: Matches incidents against P1, P2, and P3 severity tiers and SLAs.<br>• Root Cause Correlation: Correlates exceptions with source code files via Git Blame synchronization and links issues directly to tracking tools like <a href=\"https://pipefishlabs.io/\" target=\"_blank\" style=\"color:var(--cyan);text-decoration:underline\">Sentry</a> or Rollbar.<br>• Noise Suppression &amp; Automated Dispatch: Filters out alert fatigue and dispatches verified incidents to on-call engineers through platforms like PagerDuty or Opsgenie.",
    "skills": "vector-log-tokenizer, stack-trace-extractor, severity-classifier, pagerduty-dispatcher",
    "mcp": "mcp-server-elasticsearch, mcp-server-sentry, mcp-server-pagerduty",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/log-exception-ingest",
    "secrets": "Elasticsearch API Key (Vault), PagerDuty Events v2 API Key",
    "apis": "Vector Log Engine API, Elasticsearch Search API, PagerDuty Events v2 API",
    "a2a": "Mistral Native Handoff (Zero-Loss Vector Stream Tool Handoff)",
    "rbac": "Role: LogTriageBot | Perms: logs.ingest, issue.link, incident.trigger"
  },
  "erp": {
    "title": "Audit Agent",
    "duties": "• Append-Only Logging: Records immutable, verifiable logs of prompt hashes, model versions, temperature parameters, and decision outputs to maintain a tamper-proof audit trail.<br>• Compliance Verification: Continuously cross-references agent operations and state transitions against regulatory mandates like EU AI Act Annex IV, SOC 2 Type II, and HIPAA.<br>• Traceability Tracking: Monitors multi-agent directed acyclic graph (DAG) state handoffs and cryptographic token scoping to verify that every node executes within its authorized boundaries.<br>• Real-Time Telemetry: Captures and reports execution metrics, exception handling logs, and anomaly detection events to ensure enterprise readiness and operational transparency.",
    "skills": "sap-oracle-master-sync, po-3way-matcher, general-ledger-double-entry, edi-dispatcher",
    "mcp": "mcp-server-sap-s4hana, mcp-server-oracle-fusion, mcp-server-avalara",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/erp-financial-event",
    "secrets": "SAP Client Certificates (Vault PKI), Avalara Tax API Password",
    "apis": "SAP S/4HANA Financials OData API, Oracle ERP Cloud REST API, Avalara AvaTax",
    "a2a": "Mistral Native Handoff (Double-Entry Cryptographic Balance Handoff)",
    "rbac": "Role: FinancialAuditBot | Perms: ledger.post, po.match, edi.dispatch"
  },
  "trafficrouter": {
    "title": "Traffic Router Agent",
    "duties": "• Inbound Telemetry Ingestion: Captures and evaluates real-time network and routing signals, such as BGP route latency spikes or edge gateway congestion alerts.<br>• Intelligent Traffic Re-Routing: Automatically reroutes active sessions (such as thousands of concurrent HTTP/2 connections) across distributed global edge gateways, cloud providers (e.g., AWS Route 53, Cloudflare), and proxy layers (Envoy, NGINX, HAProxy).<br>• Asynchronous DAG State Handoff: Passes cryptographically signed operational payloads and routing metrics downstream to failover, shield, and health-monitoring nodes without blocking or latency bottlenecks.<br>• Autonomous Edge Optimization: Coordinates with telemetry and balancer agents to dynamically balance geographic traffic loads and maintain high availability under fluctuating traffic spikes.",
    "skills": "bgp-edge-health-monitor, route53-geo-balancer, cloudflare-waf-shield, canary-shifter",
    "mcp": "mcp-server-cloudflare-workers, mcp-server-aws-route53, mcp-server-envoy-proxy",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/edge-latency-alert",
    "secrets": "Cloudflare Global API Key (Vault v2), AWS Route 53 IAM Token",
    "apis": "Cloudflare v4 REST API, AWS Route 53 API, Envoy Control Plane gRPC",
    "a2a": "Mistral Native Handoff (BGP Anycast Dynamic Routing Handoff)",
    "rbac": "Role: EdgeTrafficRouter | Perms: dns.update, WAF.block, proxy.configure"
  },
  "networkdispatch": {
    "title": "Network Dispatch Agent",
    "duties": "• Cross-system network routing: Dispatches operational traffic, data payloads, and service events securely across hybrid infrastructure, custom MCP servers, and integrated carrier systems.<br>• Asynchronous DAG state coordination: Manages cryptographically signed payloads (using HMAC-SHA256 and NIST ML-KEM-768 post-quantum encryption) to route transactional state transitions seamlessly between specialized multi-agent nodes via Native Mistral Handoffs.<br>• Multi-channel endpoint dispatch: Coordinates external signal handoffs across voice, email, SMS, UCC/VTC, and API surfaces as part of the <a href=\"https://pipefishlabs.io/\" target=\"_blank\" style=\"color:var(--cyan);text-decoration:underline\">PipeFish Labs</a> orchestration platform.",
    "skills": "sdwan-topology-analyzer, qos-dssc-prioritizer, wireguard-provisioner, zero-touch-provisioner",
    "mcp": "mcp-server-cisco-sdwan, mcp-server-juniper-pyez, mcp-server-wireguard",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/sdwan-mesh-alert",
    "secrets": "Cisco vManage Authentication Token (Vault), WireGuard Private Key Store",
    "apis": "Cisco SD-WAN REST API, Juniper PyEZ RPC API, WireGuard Kernel API",
    "a2a": "Mistral Native Handoff (gNMI / YANG Network Telemetry Stream Handoff)",
    "rbac": "Role: NetworkDispatchEngine | Perms: sdwan.configure, tunnel.create, qos.set"
  },
  "selfimproving": {
    "title": "Self-Improving Agent",
    "skills": "opentelemetry-trace-collector, failure-taxonomy-categorizer, dspy-prompt-autotuner, vector-memory",
    "mcp": "mcp-server-dspy-optimizer, mcp-server-pinecone-memory, mcp-server-eval-harness",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/reflection-loop-complete",
    "secrets": "Pinecone Vector DB Master Key (Vault v2), DSPy Optimization Secret",
    "apis": "DSPy Optimization Engine, Pinecone Vector API, OpenTelemetry Trace API",
    "a2a": "Mistral Native Handoff (LLM Self-Critique Instruction Mutation Handoff)",
    "rbac": "Role: SelfImprovingEngine | Perms: prompt.mutate, memory.write, eval.run"
  },
  "systemoptimizing": {
    "title": "System-Optimizing Agent",
    "duties": "The System-Optimizing Agent acts as an automated infrastructure tuning engine designed to diagnose and resolve performance bottlenecks across distributed microservice architectures.<br><br>• Target Signal Processing: Ingests live inbound telemetry signals such as CPU/memory bottlenecks, database indexing latency, and unoptimized RPC query plans across distributed systems.<br>• Continuous Runtime Tuning: Automatically coordinates execution across specialized subagents to resolve performance constraints in real-time.<br>• Associated Subagent Chain: Works alongside foundational modules in the live agent mesh, including the eBPF CPU &amp; Memory Profiler Agent (Kernel Profiler), Database Index &amp; Query Plan Optimizer Agent (EXPLAIN ANALYZE), Cache Invalidation &amp; Hit Ratio Tuning Agent (Redis/Memcached), RPC Payload &amp; Serialization Compressor Agent (gRPC/Protobuf), Kubernetes Autoscaling &amp; HPA Tuner Agent (K8s Metrics API), Garbage Collection &amp; Memory Defragmenter Agent (JVM/Go Runtime), and Load Balancer &amp; Connection Pool Optimizer Agent (Envoy/HAProxy).",
    "skills": "ebpf-cpu-memory-profiler, explain-analyze-planner, redis-cache-tuner, k8s-hpa-autoscaler",
    "mcp": "Managed Mistral MCP Connectors: mcp-server-ebpf-profiler, mcp-server-postgres-planner, mcp-server-k8s-metrics",
    "webhooks": "https://api.pipefishlabs.io/v1/webhooks/runtime-tuning-event",
    "secrets": "Kubernetes Service Account Token (Vault), Redis Cluster Auth Pass",
    "apis": "eBPF Kernel Profiler, PostgreSQL EXPLAIN API, Kubernetes Metrics Server API",
    "a2a": "Mistral Native Handoff (Kernel Telemetry Stream with K8s HPA Scaling Connector)",
    "rbac": "Role: SystemOptimizerBot | Perms: k8s.autoscale (K8s HPA Connector), query.optimize, cache.flush (Zero-Trust Scoped)"
  }
}

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as fp:
    index_content = fp.read()

old_json_str = index_content.split('window.agentSpecsData = ')[1].split(';\nconst demoScenarios =')[0]
new_json_str = json.dumps(spec_data)
index_content = index_content.replace(old_json_str, new_json_str)

with open('index.html', 'w', encoding='utf-8') as fp:
    fp.write(index_content)
print("Successfully injected updated Mistral Native Handoffs & Managed MCP Connectors spec_data into index.html")

# 2. Update demo/index.html
with open('demo/index.html', 'r', encoding='utf-8') as fp:
    demo_content = fp.read()

old_demo_json_str = demo_content.split('window.agentSpecsData = ')[1].split(';\nconst scenarios =')[0]
demo_content = demo_content.replace(old_demo_json_str, new_json_str)

with open('demo/index.html', 'w', encoding='utf-8') as fp:
    fp.write(demo_content)
print("Successfully injected updated Mistral Native Handoffs & Managed MCP Connectors spec_data into demo/index.html")
