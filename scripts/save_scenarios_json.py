import os
import json

WORKSPACE = r"C:\Users\Surface\.gemini\antigravity\scratch\pipefish-labs"

# 24 Enriched Scenarios with crystal-clear toddler/beginner explanations and real-world stories
SCENARIOS_DATA = {
    "receptionist": {
        "category": "beginner",
        "icon": "📞",
        "badge": "⭐ Beginner Friendly",
        "friendlyName": "Emergency Support Call & Live Booking",
        "techName": "Receptionist Agent (Voice & Text)",
        "friendlyProblem": "A customer calls in panic at 2:00 AM because an API is returning errors on their production account.",
        "friendlyGoal": "Understand caller, verify account, locate on-call engineer, file a P1 ticket, book an emergency triage meeting, and send an SMS confirmation—all in under 3 seconds.",
        "friendlyTakeaway": "Instead of putting the caller on hold for 30 minutes or waiting for business hours, 8 specialized AI agents pass the baton in seconds to resolve the emergency with zero human data entry.",
        "nodes": [
            {"name": "Voice Ingestion", "friendlyTitle": "👂 1. Listen & Transcribe Voice Call", "friendlyDesc": "Listens to the caller's voice message, transcribes every word with 100% accuracy, and extracts their contact details.", "tools": "📞 Phone System · Speech AI"},
            {"name": "Intent Classifier", "friendlyTitle": "🎯 2. Understand Urgency & Severity", "friendlyDesc": "Analyzes the problem and flags it as a high-priority 'P0 Outage' because the customer is an enterprise VIP.", "tools": "🧠 Intent Engine · SLA Rules"},
            {"name": "Account Verifier", "friendlyTitle": "🔐 3. Verify Customer Account", "friendlyDesc": "Checks the database securely to make sure the caller is an active customer and matches their phone number.", "tools": "🗄️ Database Bridge · Zero-Trust Auth"},
            {"name": "Engineer Router", "friendlyTitle": "👥 4. Find Active On-Call Engineer", "friendlyDesc": "Scans the team's schedule to find the exact on-call engineer awake and available right now.", "tools": "💬 Slack · PagerDuty Schedule"},
            {"name": "Ticket Generator", "friendlyTitle": "🎫 5. Open Official Support Ticket", "friendlyDesc": "Automatically files a complete support ticket with error logs attached so the engineer doesn't have to ask questions.", "tools": "📋 Jira · Helpdesk Bridge"},
            {"name": "Calendar Sync", "friendlyTitle": "📅 6. Schedule Meeting & Video Link", "friendlyDesc": "Books an emergency triage bridge on Google Calendar and sends a Zoom link to both the engineer and the customer.", "tools": "📆 Google Calendar · Zoom Bridge"},
            {"name": "SMS Responder", "friendlyTitle": "💬 7. Text Customer Back Instantly", "friendlyDesc": "Texts the customer a clear confirmation with their ticket number, ETA, and calendar invite within 2 seconds.", "tools": "📱 SMS Carrier · Voice Synthesizer"},
            {"name": "Audit Logger", "friendlyTitle": "🛡️ 8. Seal Tamper-Proof Audit Log", "friendlyDesc": "Permanently logs every single step and handoff into an encrypted audit record for 100% compliance and accountability.", "tools": "🔒 Encrypted Audit Log · Webhook"}
        ]
    },
    "sales": {
        "category": "beginner",
        "icon": "💼",
        "badge": "⭐ Beginner Friendly",
        "friendlyName": "Instant Inbound Sales Lead Closing",
        "techName": "Sales Enablement Agent",
        "friendlyProblem": "A $25k/month enterprise lead submits a contact form requesting custom automation.",
        "friendlyGoal": "Research the company, score the deal, match the best Solutions Architect, draft a custom proposal, and book a meeting.",
        "friendlyTakeaway": "Leads contacted in under 5 minutes are 21x more likely to convert. AI agent chains eliminate the 24-hour waiting gap entirely.",
        "nodes": [
            {"name": "Lead Ingestion", "friendlyTitle": "📥 1. Capture Inbound Lead", "friendlyDesc": "Reads the website contact form, extracts the visitor's email, company name, and budget requirements.", "tools": "🌐 Website Webhook · Form Parser"},
            {"name": "Company Research", "friendlyTitle": "🔍 2. Research Company Background", "friendlyDesc": "Instantly looks up company revenue, headcount, tech stack, and recent funding rounds without manual Googling.", "tools": "📊 Company Intel Database · API"},
            {"name": "ICP Qualification", "friendlyTitle": "⭐ 3. Calculate Fit Score", "friendlyDesc": "Scores the lead as 96/100 (Tier A+ VIP) based on budget ($25k/mo) and enterprise company size.", "tools": "🎯 Scoring AI · Qualification Rules"},
            {"name": "AE Matching", "friendlyTitle": "🤝 4. Match Senior Sales Architect", "friendlyDesc": "Finds the best-matched senior sales engineer specializing in enterprise CRM integrations.", "tools": "📅 Google Calendar · AE Skill Matrix"},
            {"name": "Proposal Drafter", "friendlyTitle": "📑 5. Draft Tailored Proposal", "friendlyDesc": "Automatically drafts a custom scope proposal PDF with tailored ROI calculations and deliverables.", "tools": "📄 Document Engine · PDF Builder"},
            {"name": "CRM Sync", "friendlyTitle": "💼 6. Update Salesforce & HubSpot", "friendlyDesc": "Creates a new deal stage in CRM and attaches full company research so the sales rep is prepared.", "tools": "☁️ Salesforce · HubSpot CRM Bridge"},
            {"name": "Slack Alert", "friendlyTitle": "🔔 7. Alert Sales Team on Slack", "friendlyDesc": "Sends a message into the team's Slack channel with a 1-click button to approve the meeting and proposal.", "tools": "💬 Slack Bot · Interactive Buttons"},
            {"name": "Email Outbound", "friendlyTitle": "✉️ 8. Send Personalized Invitation", "friendlyDesc": "Sends the prospect a personalized welcome email with calendar invite and next steps within 3 seconds.", "tools": "📧 Email Engine · Calendar Invite"}
        ]
    },
    "logistics": {
        "category": "beginner",
        "icon": "🚚",
        "badge": "⭐ Beginner Friendly",
        "friendlyName": "Cargo Port Congestion Rerouting",
        "techName": "Logistics / Supply Chain Agent",
        "friendlyProblem": "A massive shipping port is delayed, risking spoiling 1,400 refrigerated freight containers.",
        "friendlyGoal": "Detect port congestion, find alternate rail & truck routes, rebook freight carriers, and alert customers automatically.",
        "friendlyTakeaway": "Autonomous supply chain chains prevent millions of dollars in spoiled cargo by solving delays in seconds instead of days.",
        "nodes": [
            {"name": "EDI Telemetry", "friendlyTitle": "📡 1. Receive Port Delay Alert", "friendlyDesc": "Picks up live satellite and port radar feeds showing a 48-hour backlog at the destination terminal.", "tools": "🛰️ GPS Telematics · EDI Stream"},
            {"name": "Risk Classifier", "friendlyTitle": "⚠️ 2. Assess Cold-Chain Risk", "friendlyDesc": "Calculates that the cargo will spoil if delayed more than 12 hours and flags emergency reroute.", "tools": "🌡️ Temperature Sensors · SLA Rules"},
            {"name": "Carrier Query", "friendlyTitle": "🔎 3. Find Available Trains & Trucks", "friendlyDesc": "Searches regional rail yards and refrigerated trucking fleets to find backup transport capacity.", "tools": "🚛 Carrier Network · Cross-Dock API"},
            {"name": "Route Optimizer", "friendlyTitle": "🗺️ 4. Calculate Fastest Bypass Route", "friendlyDesc": "Finds a rail route bypassing the congested port that gets the cargo delivered 8 hours ahead of schedule.", "tools": "🧭 Route Optimization Engine"},
            {"name": "Carrier Dispatch", "friendlyTitle": "📦 5. Book Alternate Carriers", "friendlyDesc": "Instantly books and transmits electronic shipping orders to the new rail and trucking partners.", "tools": "⚡ Automated Booking API · EDI 204"},
            {"name": "ERP Ledger Sync", "friendlyTitle": "📑 6. Update Warehouse ERP Records", "friendlyDesc": "Updates inventory schedules in SAP ERP so the receiving warehouse knows the new dock arrival time.", "tools": "🏢 SAP ERP · Oracle Cloud Bridge"},
            {"name": "Customer Alert", "friendlyTitle": "📱 7. Notify Receiving Customers", "friendlyDesc": "Sends proactive updates to retail buyers with live GPS tracking before they even noticed the port delay.", "tools": "📲 Tracking Portal · SMS/Email"},
            {"name": "Reliability AI", "friendlyTitle": "📈 8. Learn & Save Record", "friendlyDesc": "Records performance metrics so future supply chain decisions get even smarter and faster.", "tools": "🔒 Immutable Log · Reliability AI"}
        ]
    },
    "docs": {
        "category": "beginner",
        "icon": "📝",
        "badge": "⭐ Beginner Friendly",
        "friendlyName": "Instant Software Manual & API Documentation",
        "techName": "Documentation Agent",
        "friendlyProblem": "Engineering team pushed new code, but nobody wrote the instruction manual or updated API docs.",
        "friendlyGoal": "Scan code changes, generate user manuals, create interactive diagrams, and publish them online.",
        "friendlyTakeaway": "Documentation is normally the most neglected part of software. AI agent chains keep user guides 100% updated automatically.",
        "nodes": [
            {"name": "Code Scanner", "friendlyTitle": "🔍 1. Read Code Changes", "friendlyDesc": "Extracts all new functions, parameters, and features added in the latest software update.", "tools": "💻 Code Parser · Git Commit Hook"},
            {"name": "OpenAPI Generator", "friendlyTitle": "📜 2. Build API Specifications", "friendlyDesc": "Generates official OpenAPI 3.1 technical specifications for developers.", "tools": "📋 OpenAPI Generator · Schema Bridge"},
            {"name": "Code Examples", "friendlyTitle": "💡 3. Write Working Code Examples", "friendlyDesc": "Writes step-by-step example code in Python, JavaScript, and Go showing how to use the feature.", "tools": "✨ Code Synthesizer · Multi-Language"},
            {"name": "Diagram Builder", "friendlyTitle": "📊 4. Draw System Flowcharts", "friendlyDesc": "Creates clean interactive Mermaid diagrams showing how data flows through the system.", "tools": "🎨 Mermaid.js Diagram Engine"},
            {"name": "Tutorial Writer", "friendlyTitle": "📖 5. Write Beginner Guides", "friendlyDesc": "Drafts plain-English tutorials and quickstart guides with clear explanations.", "tools": "✍️ Technical Writer AI"},
            {"name": "QC Validator", "friendlyTitle": "🔗 6. Verify Links & Quality", "friendlyDesc": "Checks that all hyperlinks work and ensures no outdated terminology is present.", "tools": "🔎 Link Checker · QC Validator"},
            {"name": "Portal Publisher", "friendlyTitle": "🚀 7. Publish to Developer Portal", "friendlyDesc": "Deploys the polished documentation directly to the live website.", "tools": "🌐 Cloudflare / Static Publisher"},
            {"name": "Release Notes", "friendlyTitle": "🏷️ 8. Generate Release Notes", "friendlyDesc": "Creates a human-readable changelog announcing what is new in version 2.4.", "tools": "📢 Changelog Generator"}
        ]
    },
    "codescan": {
        "category": "security",
        "icon": "🛡️",
        "badge": "Security & Privacy",
        "friendlyName": "Instant Code Vulnerability & Secret Patching",
        "techName": "Code-Scanning Agent",
        "friendlyProblem": "A developer accidentally committed a database password and a security bug into the main codebase.",
        "friendlyGoal": "Scan 1.4 million lines of code, detect the leaked password, block dangerous deployments, and create a verified fix.",
        "friendlyTakeaway": "Security breaches happen in seconds when humans miss small details. AI code-scanning chains protect apps automatically before bad code goes live.",
        "nodes": [
            {"name": "AST Parser", "friendlyTitle": "🔍 1. Scan Codebase Structure", "friendlyDesc": "Parses every file in the code commit to analyze logic patterns and data pathways.", "tools": "💻 Code Parser · AST Analyzer"},
            {"name": "Secret Scanner", "friendlyTitle": "🔑 2. Find Leaked Passwords & Keys", "friendlyDesc": "Spots an exposed cloud password left in line 42 of a configuration file.", "tools": "🕵️ Secret Detector · Entropy Filter"},
            {"name": "Vulnerability Engine", "friendlyTitle": "🛡️ 3. Detect Security Vulnerabilities", "friendlyDesc": "Identifies an unescaped database query that could let malicious hackers steal data.", "tools": "🔒 OWASP Security Engine"},
            {"name": "Dependency Tracker", "friendlyTitle": "📦 4. Check External Libraries", "friendlyDesc": "Cross-references all installed packages against national cybersecurity vulnerability lists.", "tools": "📚 National Vulnerability Database"},
            {"name": "Auto Patch AI", "friendlyTitle": "✨ 5. Write Safe Code Fix", "friendlyDesc": "Automatically writes the exact code fix to replace the exposed password with secure vault storage.", "tools": "🤖 Safe Code Refactor AI"},
            {"name": "CI/CD Gate", "friendlyTitle": "🚫 6. Block Unsafe Release", "friendlyDesc": "Temporarily pauses deployment and leaves a helpful comment on GitHub with the fix ready to merge.", "tools": "🐙 GitHub CI/CD Gate · Code Review"},
            {"name": "Compliance Vault", "friendlyTitle": "📋 7. Save Security Proof", "friendlyDesc": "Stores a signed audit log proving the issue was caught and patched for upcoming SOC 2 audits.", "tools": "🔐 SOC 2 Compliance Vault"},
            {"name": "Security Dashboard", "friendlyTitle": "📊 8. Update Security Scorecard", "friendlyDesc": "Recalculates company security health score to 99.8% and notifies the security team.", "tools": "📈 Security Dashboard · Metrics"}
        ]
    },
    "crypto": {
        "category": "security",
        "icon": "🔐",
        "badge": "Security & Privacy",
        "friendlyName": "Post-Quantum Encryption & Key Protection",
        "techName": "Encryption / Cryptography Agent",
        "friendlyProblem": "Legacy RSA encryption is vulnerable to future quantum computer decryption attacks.",
        "friendlyGoal": "Audit encryption keys, generate post-quantum ML-KEM keys, rotate hardware security modules, and certify quantum safety.",
        "friendlyTakeaway": "Upgrading encryption across thousands of servers normally takes 6 months of IT meetings. Agent chains execute the transition safely in seconds.",
        "nodes": [
            {"name": "Crypto Scanner", "friendlyTitle": "🔍 1. Audit Current Keys", "friendlyDesc": "Scans all servers to identify old encryption algorithms that need quantum-safe upgrades.", "tools": "🔎 Crypto Inventory Scanner"},
            {"name": "Risk Evaluator", "friendlyTitle": "⚠️ 2. Rank Risk Priorities", "friendlyDesc": "Prioritizes which databases need immediate quantum-proof protection.", "tools": "📊 Quantum Risk Evaluator"},
            {"name": "NIST Key Gen", "friendlyTitle": "🔑 3. Generate ML-KEM-768 Keys", "friendlyDesc": "Generates NIST-standard post-quantum mathematical encryption keys.", "tools": "🔐 NIST PQC Engine"},
            {"name": "DSA Signer", "friendlyTitle": "✍️ 4. Sign Data Payloads", "friendlyDesc": "Signs outgoing messages with post-quantum digital signatures to prevent tampering.", "tools": "🛡️ ML-DSA Digital Signer"},
            {"name": "HSM Key Rotation", "friendlyTitle": "🔄 5. Rotate Hardware Keys", "friendlyDesc": "Securely rotates master keys inside hardware security modules without downtime.", "tools": "🔒 AWS KMS / Vault HSM"},
            {"name": "Hybrid TLS", "friendlyTitle": "📜 6. Issue Hybrid Certificates", "friendlyDesc": "Deploys dual-layer security certificates that work with both old and new web browsers.", "tools": "🌐 Hybrid TLS PKI"},
            {"name": "ZDR Enclave", "friendlyTitle": "🛡️ 7. Spin Up Secure Enclaves", "friendlyDesc": "Creates private memory spaces where secret data exists only for milliseconds before vanishing.", "tools": "⚡ Zero-Data-Retention Enclave"},
            {"name": "Audit Certificate", "friendlyTitle": "✅ 8. Issue Quantum-Safe Proof", "friendlyDesc": "Issues a cryptographically signed compliance token confirming 100% post-quantum readiness.", "tools": "📋 PQC Audit Certificate"}
        ]
    },
    "integration": {
        "category": "it",
        "icon": "🔗",
        "badge": "IT & Systems",
        "friendlyName": "Multi-App Real-Time Data Sync",
        "techName": "Integration Agent",
        "friendlyProblem": "Salesforce, Workday, and SAP have conflicting customer data and mismatching formats.",
        "friendlyGoal": "Ingest data across all 3 platforms, translate formats, resolve conflicting edits, and sync them bi-directionally.",
        "friendlyTakeaway": "Instead of brittle Zapier zaps or manual CSV uploads, agent chains reconcile complex enterprise databases with zero data loss.",
        "nodes": [
            {"name": "Multi-Protocol Ingest", "friendlyTitle": "📥 1. Receive App Signals", "friendlyDesc": "Listens to real-time events across SAP, Workday, and Salesforce at once.", "tools": "🌐 Multi-Protocol Ingest"},
            {"name": "Schema Transformer", "friendlyTitle": "🔄 2. Translate Formats", "friendlyDesc": "Converts messy legacy XML schemas into clean, standardized JSON data contracts.", "tools": "📑 Schema Transformer"},
            {"name": "State Sync Resolver", "friendlyTitle": "⚖️ 3. Resolve Edit Conflicts", "friendlyDesc": "Detects when two users edit the same account and smartly merges the most recent updates.", "tools": "🤝 Bi-Directional State Sync"},
            {"name": "OAuth Manager", "friendlyTitle": "🔑 4. Manage Login Tokens", "friendlyDesc": "Handles secure API keys and rate limits so no connections get blocked.", "tools": "🔒 OAuth Token Manager"},
            {"name": "Circuit Breaker", "friendlyTitle": "⚡ 5. Prevent System Crashes", "friendlyDesc": "Uses automatic retries and backoff timers so high traffic never breaks the connection.", "tools": "🛡️ Circuit Breaker & Retry"},
            {"name": "API Dispatcher", "friendlyTitle": "📤 6. Update All Systems", "friendlyDesc": "Sends synchronized updates simultaneously to SAP, Workday, and Salesforce.", "tools": "🏢 Enterprise API Dispatcher"},
            {"name": "HMAC Seal", "friendlyTitle": "🔐 7. Sign Security Seal", "friendlyDesc": "Signs every transaction with cryptographic verification for compliance proof.", "tools": "✍️ HMAC SHA-256 Seal"},
            {"name": "Telemetry Health", "friendlyTitle": "📊 8. Confirm 99.999% Sync", "friendlyDesc": "Publishes real-time delivery confirmation metrics to the central system dashboard.", "tools": "📈 Telemetry Health Monitor"}
        ]
    },
    "finops": {
        "category": "finance",
        "icon": "💳",
        "badge": "Finance & Legal",
        "friendlyName": "Cloud & AI Token Spend Optimizer",
        "techName": "FinTech Ops Agent",
        "friendlyProblem": "Cloud computing and AI token costs are surging unpredictably across multiple teams.",
        "friendlyGoal": "Monitor per-second GPU and token spend, detect budget surges, enforce spend limits, and cut wasted compute.",
        "friendlyTakeaway": "Companies waste up to 30% of their cloud budget on oversized servers. FinOps agent chains keep AI spending tightly controlled automatically.",
        "nodes": [
            {"name": "Token Cost Tracker", "friendlyTitle": "📊 1. Track Live Token Usage", "friendlyDesc": "Monitors exact AI token consumption and cloud compute costs down to the penny.", "tools": "📈 Real-Time Cost Tracker"},
            {"name": "Cloud Allocator", "friendlyTitle": "☁️ 2. Allocate Cloud Spend", "friendlyDesc": "Attributes AWS, GCP, and Azure server costs to specific teams and projects.", "tools": "🏢 Multi-Cloud Cost Allocator"},
            {"name": "Unit Economics", "friendlyTitle": "💡 3. Calculate ROI per Task", "friendlyDesc": "Calculates the exact return on investment for each AI model and task.", "tools": "🧠 Unit Economics Engine"},
            {"name": "Server Rightsizer", "friendlyTitle": "📉 4. Rightsize Servers", "friendlyDesc": "Recommends switching idle large servers to smaller, faster, cheaper alternatives.", "tools": "⚙️ Compute Rightsizer"},
            {"name": "Spend Cap Enforcer", "friendlyTitle": "🛑 5. Enforce Budget Caps", "friendlyDesc": "Applies automated spending limits to prevent runaway cloud bills before they happen.", "tools": "🛡️ Spend Cap Enforcer"},
            {"name": "Anomaly Detector", "friendlyTitle": "🚨 6. Detect Cost Surges", "friendlyDesc": "Flags unusual spending spikes instantly using kernel metrics.", "tools": "⚠️ Anomaly Detector"},
            {"name": "ERP Ledger Bridge", "friendlyTitle": "📑 7. Sync Financial Ledger", "friendlyDesc": "Posts organized cost breakdowns directly into company accounting software.", "tools": "🏢 ERP / Ledger Bridge"},
            {"name": "FinOps Attestation", "friendlyTitle": "✅ 8. Verify Cost Reductions", "friendlyDesc": "Certifies that 28% in cloud costs was saved and logs the audit trail.", "tools": "📋 FinOps Attestation"}
        ]
    },
    "contractintel": {
        "category": "finance",
        "icon": "⚖️",
        "badge": "Finance & Legal",
        "friendlyName": "Instant Legal Contract Review & Risk Scoring",
        "techName": "Contract Intelligence Agent",
        "friendlyProblem": "A 45-page enterprise contract needs urgent review for hidden liability risks and compliance traps.",
        "friendlyGoal": "Parse contract clauses, flag high-risk terms, check GDPR/HIPAA compliance, track renewal dates, and draft redlines.",
        "friendlyTakeaway": "Legal reviews that take lawyers 3 days can be analyzed, risk-scored, and redlined in 3 seconds by specialized agent chains.",
        "nodes": [
            {"name": "Legal OCR Parser", "friendlyTitle": "📄 1. Read Legal Document", "friendlyDesc": "Extracts all text, clauses, and tables from PDFs, scanned documents, and Word files.", "tools": "👁️ Multimodal OCR Parser"},
            {"name": "Clause Classifier", "friendlyTitle": "🏷️ 2. Classify Every Clause", "friendlyDesc": "Categorizes confidentiality, indemnification, payment terms, and termination rights.", "tools": "📚 Legal Clause Taxonomy"},
            {"name": "Regulatory Auditor", "friendlyTitle": "🛡️ 3. Check Privacy Laws", "friendlyDesc": "Verifies compliance against GDPR, HIPAA, and SOC 2 data protection standards.", "tools": "⚖️ Regulatory Auditor"},
            {"name": "Risk Matrix", "friendlyTitle": "⚠️ 4. Score Liability Risks", "friendlyDesc": "Flags unlimited liability clauses and high-risk penalty terms with a warning score.", "tools": "🎯 Risk Scoring Matrix"},
            {"name": "Deadline Extractor", "friendlyTitle": "📅 5. Extract Key Deadlines", "friendlyDesc": "Pulls out auto-renewal dates, cancellation windows, and milestone deadlines.", "tools": "📆 Deadline Extractor"},
            {"name": "Redline AI", "friendlyTitle": "✍️ 6. Draft Redline Revisions", "friendlyDesc": "Generates protective clause amendments ready for executive approval.", "tools": "✨ Redline Clause AI"},
            {"name": "PQC Seal", "friendlyTitle": "🔐 7. Seal Document Proof", "friendlyDesc": "Applies post-quantum cryptographic hashing to protect document authenticity.", "tools": "🔒 ML-KEM Cryptographic Seal"},
            {"name": "Executive Registry", "friendlyTitle": "📋 8. Deliver Executive Summary", "friendlyDesc": "Publishes a 1-page executive summary with key recommendations and risk findings.", "tools": "📊 Structured Registry"}
        ]
    },
    "observability": {
        "category": "it",
        "icon": "📡",
        "badge": "IT & Systems",
        "friendlyName": "Self-Healing Server Health & Anomaly Fixer",
        "techName": "Monitoring / Observability Agent",
        "friendlyProblem": "Server latency spikes to 5 seconds on checkout API, causing customer cart drop-offs.",
        "friendlyGoal": "Ingest 140,000 logs/sec, locate the faulty microservice, restart failed containers, and restore 99.99% speed.",
        "friendlyTakeaway": "Instead of waiting for on-call engineers to wake up and read logs, observability agents detect and heal server slowdowns autonomously.",
        "nodes": [
            {"name": "OTel Collector", "friendlyTitle": "📡 1. Collect Live Telemetry", "friendlyDesc": "Monitors 140,000 server logs per second across Kubernetes clusters in real time.", "tools": "📊 OpenTelemetry Collector"},
            {"name": "Distributed Tracing", "friendlyTitle": "🔗 2. Trace Broken Pathways", "friendlyDesc": "Traces the exact path of slowed checkout requests across distributed web servers.", "tools": "🔍 Jaeger Distributed Tracing"},
            {"name": "Anomaly Engine", "friendlyTitle": "⚠️ 3. Detect Latency Spike", "friendlyDesc": "Identifies that the /checkout payment gateway is timing out.", "tools": "📈 Anomaly Engine"},
            {"name": "Root Cause AI", "friendlyTitle": "🔎 4. Pinpoint Root Cause", "friendlyDesc": "Isolates a database lock on server #4 as the exact root cause of the slowdown.", "tools": "🧠 Root Cause Analyzer"},
            {"name": "Grafana Dashboard", "friendlyTitle": "📊 5. Render Incident View", "friendlyDesc": "Draws a live Grafana dashboard highlighting the bottleneck for the engineering team.", "tools": "🖥️ Grafana Visualization"},
            {"name": "Alert Filter", "friendlyTitle": "🔕 6. Silence Noise Alerts", "friendlyDesc": "Suppresses 500 duplicate alerts so engineers don't get flooded with alarm fatigue.", "tools": "🛡️ Alert Filter & Suppressor"},
            {"name": "Self-Healing Action", "friendlyTitle": "🔄 7. Trigger Auto-Restart", "friendlyDesc": "Safely restarts the frozen database container and reroutes traffic automatically.", "tools": "⚡ Self-Healing Playbook"},
            {"name": "SLA Logger", "friendlyTitle": "✅ 8. Confirm 99.99% Uptime", "friendlyDesc": "Verifies checkout response times return to 45ms and records 100% uptime SLA proof.", "tools": "📋 SLA Compliance Logger"}
        ]
    },
    "trend": {
        "category": "sales",
        "icon": "📈",
        "badge": "Sales & Growth",
        "friendlyName": "Real-Time Market Trend Spotting Engine",
        "techName": "Trend Spotting Agent",
        "friendlyProblem": "Executive team wants to discover explosive new industry shifts before competitors notice.",
        "friendlyGoal": "Scrape discussion forums, patent filings, and arXiv preprints to spot +410% spikes in emerging technology adoption.",
        "friendlyTakeaway": "Spotting market trends early gives businesses months of head start. Agent chains turn noisy web data into actionable market intelligence.",
        "nodes": [
            {"name": "Signal Scraper", "friendlyTitle": "🌐 1. Scrape Global Discussions", "friendlyDesc": "Scans forums, news, patent filings, and scientific papers for new conversation topics.", "tools": "🕷️ Multi-Source Signal Scraper"},
            {"name": "Vector Cluster", "friendlyTitle": "🧩 2. Group Related Topics", "friendlyDesc": "Uses AI embeddings to cluster thousands of messy posts into clean topic categories.", "tools": "🧠 Semantic Vector Clustering"},
            {"name": "Velocity Engine", "friendlyTitle": "📈 3. Measure Growth Velocity", "friendlyDesc": "Calculates that interest in post-quantum cryptography has surged +410% this quarter.", "tools": "📊 Velocity Acceleration Engine"},
            {"name": "Patent Correlator", "friendlyTitle": "📜 4. Check Patent Filings", "friendlyDesc": "Cross-references trends with actual US Patent Office filings to verify real commercial interest.", "tools": "🏛️ USPTO Patent Correlator"},
            {"name": "Opportunity Scorer", "friendlyTitle": "💰 5. Score Market Opportunity", "friendlyDesc": "Ranks the business revenue potential and market readiness of the trend.", "tools": "🎯 Opportunity Scoring Engine"},
            {"name": "Competitor Mapper", "friendlyTitle": "🗺️ 6. Map Competitor Activity", "friendlyDesc": "Checks what competitors are building or hiring for in this space.", "tools": "🔎 Competitor Horizon Mapper"},
            {"name": "Strategy Briefing", "friendlyTitle": "📑 7. Build Executive Dossier", "friendlyDesc": "Compiles a clean 1-page summary with clear strategic timing advice.", "tools": "📄 Strategy Briefing Builder"},
            {"name": "Slack Dispatcher", "friendlyTitle": "🔔 8. Push Strategic Alert", "friendlyDesc": "Sends a notification into executive Slack channels with key findings.", "tools": "💬 Slack Strategy Dispatcher"}
        ]
    },
    "quantum": {
        "category": "it",
        "icon": "⚡",
        "badge": "IT & Systems",
        "friendlyName": "Quantum Simulation Task Dispatch",
        "techName": "Execution Agent",
        "friendlyProblem": "A complex 56-qubit molecular simulation job requires quantum error mitigation and hardware execution.",
        "friendlyGoal": "Transpile quantum circuits, map physical qubits, execute across IBM Quantum QPU, and optimize results in seconds.",
        "friendlyTakeaway": "Bridging quantum hardware with enterprise AI takes seconds with native DAG handoffs.",
        "nodes": [
            {"name": "Circuit Ingestion", "friendlyTitle": "📥 1. Parse Quantum Circuit", "friendlyDesc": "Ingests serialized Qiskit circuit representation and decomposes gates.", "tools": "⚡ Qiskit Ingestion Bridge"},
            {"name": "Error Mitigation", "friendlyTitle": "🛡️ 2. Apply Zero-Noise Extrapolation", "friendlyDesc": "Calculates mitigation curves to eliminate quantum noise.", "tools": "🧮 QEM Mitigation Solver"},
            {"name": "QPU Transpiler", "friendlyTitle": "🔄 3. Transpile Physical Topology", "friendlyDesc": "Maps virtual qubits onto physical superconducting hardware.", "tools": "⚙️ Hardware Transpiler"},
            {"name": "Confidential Enclave", "friendlyTitle": "🔒 4. Spin Up RAM Enclave", "friendlyDesc": "Encrypts payload in AWS Nitro memory enclave.", "tools": "🛡️ AWS Nitro ZDR"},
            {"name": "QPU Dispatch", "friendlyTitle": "⚡ 5. Submit to Quantum Processor", "friendlyDesc": "Executes 8,192 measurement shots on IBM Quantum Eagle QPU.", "tools": "☁️ IBM Quantum REST API"},
            {"name": "State Tomography", "friendlyTitle": "📊 6. Compute Density Matrix", "friendlyDesc": "Reconstructs quantum state from shot measurements.", "tools": "📈 Tomography Engine"},
            {"name": "Result Optimizer", "friendlyTitle": "✨ 7. Synthesize Eigenstate Value", "friendlyDesc": "Extracts ground state energy eigenvalue to 6 decimals.", "tools": "🧠 VQE Optimizer"},
            {"name": "Audit Handoff", "friendlyTitle": "✅ 8. Seal Quantum Execution Proof", "friendlyDesc": "Records cryptographically signed execution proof.", "tools": "🔒 HMAC Execution Seal"}
        ]
    },
    "reverse": {
        "category": "security",
        "icon": "🔬",
        "badge": "Security & Privacy",
        "friendlyName": "Binary Malware Reverse Engineering",
        "techName": "Reverse Engineering Agent",
        "friendlyProblem": "An unknown obfuscated binary file was detected on a corporate server.",
        "friendlyGoal": "Disassemble machine code, decompile control flow graphs, extract hidden C2 IP addresses, and generate YARA detection rules.",
        "friendlyTakeaway": "Automating binary reverse engineering protects corporate infrastructure before malware can propagate.",
        "nodes": [
            {"name": "Binary Ingestion", "friendlyTitle": "📥 1. Ingest PE/ELF Binary", "friendlyDesc": "Extracts headers, sections, and import tables from the suspicious file.", "tools": "🔬 Binary Ingestion"},
            {"name": "CFG Reconstruction", "friendlyTitle": "🗺️ 2. Reconstruct Control Flow", "friendlyDesc": "Builds complete graph of all execution branching paths.", "tools": "🧩 Ghidra Headless API"},
            {"name": "Unpacker AI", "friendlyTitle": "🔓 3. Neutralize Packing & Anti-Debug", "friendlyDesc": "Detects evasion routines and strips packers.", "tools": "🛡️ Dynamic Unpacker"},
            {"name": "String Decrypter", "friendlyTitle": "🔑 4. Decrypt Hidden Strings", "friendlyDesc": "Uncovers hidden command-and-control server URLs.", "tools": "🕵️ Entropy Solver"},
            {"name": "Protocol Analyzer", "friendlyTitle": "📡 5. Decode Network Framing", "friendlyDesc": "Identifies encrypted beaconing protocol mechanics.", "tools": "🌐 C2 Protocol Parser"},
            {"name": "YARA Rule Gen", "friendlyTitle": "📝 6. Generate YARA Rule", "friendlyDesc": "Synthesizes production YARA rule for threat hunting.", "tools": "✨ YARA Compiler"},
            {"name": "Intel Dossier", "friendlyTitle": "📑 7. Build Threat Dossier", "friendlyDesc": "Compiles technical reverse engineering dossier.", "tools": "📄 Threat Intel Builder"},
            {"name": "EDR Dispatch", "friendlyTitle": "🛡️ 8. Deploy Endpoint Defense", "friendlyDesc": "Pushes detection signatures to corporate EDR.", "tools": "🔒 EDR Webhook API"}
        ]
    },
    "errorcorr": {
        "category": "it",
        "icon": "🛠️",
        "badge": "IT & Systems",
        "friendlyName": "Self-Healing Data Corruption Repair",
        "techName": "Self-Healing Agent",
        "friendlyProblem": "4.2% byte corruption detected across distributed vector database shards.",
        "friendlyGoal": "Calculate syndrome matrices, locate corrupt byte offsets with Berlekamp-Massey, and restore data shards with zero loss.",
        "friendlyTakeaway": "Self-healing database meshes keep vector search 100% available without human intervention.",
        "nodes": [
            {"name": "Shard Monitor", "friendlyTitle": "📡 1. Detect Corrupt Bytes", "friendlyDesc": "Scans distributed vector shards and flags byte errors.", "tools": "📊 Storage Telemetry"},
            {"name": "Syndrome Solver", "friendlyTitle": "🧮 2. Compute Syndrome Matrix", "friendlyDesc": "Calculates algebraic parity syndromes.", "tools": "📐 Galois Field Matrix"},
            {"name": "Polynomial Locator", "friendlyTitle": "🔍 3. Locate Error Offsets", "friendlyDesc": "Identifies exact faulty memory coordinates.", "tools": "🧠 Berlekamp-Massey"},
            {"name": "Chien Search", "friendlyTitle": "🎯 4. Evaluate Error Values", "friendlyDesc": "Solves for precise original byte values.", "tools": "⚡ Chien Evaluator"},
            {"name": "Byte Reconstruction", "friendlyTitle": "🛠️ 5. Reconstruct Damaged Shard", "friendlyDesc": "Applies Reed-Solomon algebraic byte repair.", "tools": "🔧 C++ RS Engine"},
            {"name": "Integrity Check", "friendlyTitle": "✅ 6. Verify Checksum", "friendlyDesc": "Validates cryptographic SHA-256 hash match.", "tools": "🔒 SHA-256 Validator"},
            {"name": "Shard Hot-Swap", "friendlyTitle": "🔄 7. Hot-Swap Vector Memory", "friendlyDesc": "Deploys repaired shard into vector index with zero downtime.", "tools": "🗄️ Qdrant / Pinecone"},
            {"name": "Audit Logging", "friendlyTitle": "📋 8. Log Parity Health Proof", "friendlyDesc": "Records data repair metrics into compliance ledger.", "tools": "📜 Parity Audit Store"}
        ]
    },
    "market": {
        "category": "sales",
        "icon": "📊",
        "badge": "Sales & Growth",
        "friendlyName": "Enterprise Market & Competitor Research",
        "techName": "Market Research Agent",
        "friendlyProblem": "Executive team needs complete competitive intelligence and TAM/SAM sizing for European AI compliance software.",
        "friendlyGoal": "Analyze SEC 10-K filings, map competitor pricing parity, synthesize customer reviews, and publish a SWOT dossier.",
        "friendlyTakeaway": "Autonomous market analysis condenses weeks of consultant research into 3 seconds of verifiable data.",
        "nodes": [
            {"name": "SEC Edgar Ingest", "friendlyTitle": "📑 1. Ingest SEC 10-K Filings", "friendlyDesc": "Parses public filings, balance sheets, and risk factors.", "tools": "🏛️ SEC EDGAR RAG"},
            {"name": "Competitor Scraper", "friendlyTitle": "🌐 2. Audit Competitor Offerings", "friendlyDesc": "Extracts pricing tiers, features, and partner programs.", "tools": "🕷️ Live Web Scraper"},
            {"name": "TAM/SAM Calculator", "friendlyTitle": "💡 3. Compute Market Sizing", "friendlyDesc": "Calculates addressable market size across European sectors.", "tools": "🧠 Market Math Engine"},
            {"name": "Pricing Matrix", "friendlyTitle": "💰 4. Map Pricing Parity", "friendlyDesc": "Ranks feature pricing against industry competitors.", "tools": "📊 Pricing Benchmark"},
            {"name": "Customer Sentiment", "friendlyTitle": "🗣️ 5. Analyze User Reviews", "friendlyDesc": "Extracts top user complaints and feature wishlists.", "tools": "🧠 Sentiment NLP"},
            {"name": "SWOT Synthesis", "friendlyTitle": "🎯 6. Assemble SWOT Matrix", "friendlyDesc": "Compiles strengths, weaknesses, and opportunities.", "tools": "📋 SWOT Builder"},
            {"name": "Executive PDF", "friendlyTitle": "📄 7. Generate Briefing PDF", "friendlyDesc": "Assembles high-res executive market briefing.", "tools": "📑 Document Synthesizer"},
            {"name": "CRM Enrichment", "friendlyTitle": "💼 8. Sync Market Data to CRM", "friendlyDesc": "Attaches competitive battlecards directly to active deals.", "tools": "☁️ HubSpot / Salesforce"}
        ]
    },
    "revops": {
        "category": "sales",
        "icon": "🚀",
        "badge": "Sales & Growth",
        "friendlyName": "Growth Funnel & Enterprise Personalization",
        "techName": "Growth Strategy Agent",
        "friendlyProblem": "A 3.4x spike in sign-ups from fintech companies ($50M+ ARR) was detected.",
        "friendlyGoal": "Enrich account firmographics, calculate PLG lead score, generate custom personalized landing pages, and route directly to VP Sales.",
        "friendlyTakeaway": "Converting enterprise traffic on first visit requires hyper-personalized sales execution at machine speed.",
        "nodes": [
            {"name": "Event Stream", "friendlyTitle": "📡 1. Capture Sign-Up Surge", "friendlyDesc": "Detects real-time surge in enterprise visitor traffic.", "tools": "📊 PostHog Event Stream"},
            {"name": "Firmographic Intel", "friendlyTitle": "🔍 2. Enrich Company Details", "friendlyDesc": "Fetches ARR, technology stack, and decision maker names.", "tools": "🏢 Clearbit Reveal API"},
            {"name": "PLG Scorer", "friendlyTitle": "⭐ 3. Calculate PLG Lead Score", "friendlyDesc": "Scores account as Tier-1 enterprise growth prospect.", "tools": "🎯 PLG Scoring Model"},
            {"name": "Dynamic Landing Page", "friendlyTitle": "🎨 4. Generate Custom Page", "friendlyDesc": "Renders personalized landing page tailored to fintech security.", "tools": "✨ Dynamic UI Engine"},
            {"name": "LTV Predictor", "friendlyTitle": "💵 5. Forecast Contract LTV", "friendlyDesc": "Projects $180k annual expansion revenue.", "tools": "📈 Stripe LTV Predictor"},
            {"name": "Sales Route", "friendlyTitle": "🤝 6. Route to VP of Sales", "friendlyDesc": "Assigns lead directly to top Enterprise Account Executive.", "tools": "📅 Cal / AE Matrix"},
            {"name": "Slack War Room", "friendlyTitle": "🔔 7. Launch Slack Deal Room", "friendlyDesc": "Creates dedicated private channel with deal battlecard.", "tools": "💬 Slack API Bot"},
            {"name": "Outbound Sequence", "friendlyTitle": "✉️ 8. Dispatch VIP Outreach", "friendlyDesc": "Sends executive invitation with custom demo video link.", "tools": "📧 Personalized Outreach"}
        ]
    },
    "analytics": {
        "category": "sales",
        "icon": "🧠",
        "badge": "Sales & Growth",
        "friendlyName": "Big Data Clickstream & Retention Cohorts",
        "techName": "Research Agent",
        "friendlyProblem": "250 million user event streams across Snowflake and ClickHouse need retention analysis.",
        "friendlyGoal": "Ingest high-throughput streams, deduplicate user sessions, compute N-day retention curves, and dispatch anomaly alerts.",
        "friendlyTakeaway": "Eliminating SQL data bottlenecks empowers executive teams to make real-time product decisions.",
        "nodes": [
            {"name": "Stream Ingest", "friendlyTitle": "📥 1. Ingest 250M Event Stream", "friendlyDesc": "Pulls real-time analytics events across distributed databases.", "tools": "⚡ ClickHouse HTTP API"},
            {"name": "Session Dedupe", "friendlyTitle": "🔄 2. Deduplicate User Sessions", "friendlyDesc": "Cleans bot traffic and isolates authentic user journeys.", "tools": "🧹 Stream Deduplicator"},
            {"name": "Cohort Calculator", "friendlyTitle": "📊 3. Calculate 30-Day Retention", "friendlyDesc": "Computes behavioral cohort curves across customer segments.", "tools": "🧮 Python Code Interpreter"},
            {"name": "Feature Attribution", "friendlyTitle": "🔍 4. Attribute Key Conversion Drivers", "friendlyDesc": "Discovers features that drive 4.2x higher renewal rates.", "tools": "🧠 Attribution Model"},
            {"name": "Anomaly Check", "friendlyTitle": "⚠️ 5. Detect Drop-Off Bottleneck", "friendlyDesc": "Flags sudden 14% drop in step 3 of onboarding flow.", "tools": "📈 Anomaly Detector"},
            {"name": "Executive Dashboard", "friendlyTitle": "🖥️ 6. Render BI Visualizations", "friendlyDesc": "Builds interactive metric dashboard for product leaders.", "tools": "📊 BI Dashboard Engine"},
            {"name": "Actionable Alert", "friendlyTitle": "🔔 7. Dispatch Product Alert", "friendlyDesc": "Notifies UX team with exact screen coordinates to fix.", "tools": "💬 Slack Alert Hook"},
            {"name": "Audit Trail", "friendlyTitle": "📋 8. Log Analytics Dataset Hash", "friendlyDesc": "Records dataset checksum in data governance registry.", "tools": "🔒 Governance Hash Log"}
        ]
    },
    "auditing": {
        "category": "security",
        "icon": "📋",
        "badge": "Security & Privacy",
        "friendlyName": "SOC 2 / ISO 27001 Cloud Compliance Proof",
        "techName": "Analysis Agent",
        "friendlyProblem": "Annual compliance audit requires verification of IAM key rotation and backup encryption across 45 cloud accounts.",
        "friendlyGoal": "Aggregate CloudTrail logs, verify Least Privilege access, validate immutable backups, and compile signed auditor evidence packages.",
        "friendlyTakeaway": "Turning 300 hours of painful spreadsheet compliance audits into 3 seconds of verifiable cryptographic proof.",
        "nodes": [
            {"name": "CloudTrail Ingest", "friendlyTitle": "📥 1. Ingest 45 Cloud Audit Logs", "friendlyDesc": "Streams AWS, GCP, and Azure management logs.", "tools": "📊 CloudTrail API"},
            {"name": "IAM Policy Check", "friendlyTitle": "🔐 2. Verify Least Privilege IAM", "friendlyDesc": "Checks that zero service accounts have wildcards (*).", "tools": "🛡️ IAM Verifier Engine"},
            {"name": "Key Rotation Audit", "friendlyTitle": "🔄 3. Audit Key Rotation Dates", "friendlyDesc": "Validates that all encryption keys rotate every 90 days.", "tools": "🔒 Vault Transit Sys"},
            {"name": "Backup Verification", "friendlyTitle": "💾 4. Verify Immutable Backups", "friendlyDesc": "Checks that daily database snapshots are air-gapped.", "tools": "🗄️ S3 Object Lock Check"},
            {"name": "SOC 2 Matrix", "friendlyTitle": "📋 5. Map Controls to SOC 2 Trust", "friendlyDesc": "Maps verified checks against SOC 2 Type II criteria.", "tools": "📚 Compliance Taxonomy"},
            {"name": "Annex IV Packager", "friendlyTitle": "🇪🇺 6. Build EU AI Act Dossier", "friendlyDesc": "Generates Annex IV technical documentation package.", "tools": "⚖️ Regulatory Packager"},
            {"name": "Cryptographic Signer", "friendlyTitle": "✍️ 7. Sign Audit Evidence Token", "friendlyDesc": "Applies digital signature to prevent auditor evidence tampering.", "tools": "🔒 ML-DSA Digital Seal"},
            {"name": "Auditor Delivery", "friendlyTitle": "📦 8. Deliver Compliance Portal", "friendlyDesc": "Publishes 1-click evidence zip file for auditor download.", "tools": "🌐 Auditor Portal API"}
        ]
    },
    "logtriage": {
        "category": "it",
        "icon": "🚨",
        "badge": "IT & Systems",
        "friendlyName": "High-Volume Error Log Triage & Dispatch",
        "techName": "Log Triage Agent",
        "friendlyProblem": "85,000 log events per second are flooding the logging pipeline with cascading timeouts.",
        "friendlyGoal": "Parse logs, extract stack traces, group recurring error signatures, correlate with git commits, and dispatch P1 PagerDuty alerts.",
        "friendlyTakeaway": "Preventing alert fatigue allows engineering teams to fix outages before users notice.",
        "nodes": [
            {"name": "Log Tokenizer", "friendlyTitle": "📥 1. Parse 85k Logs/Second", "friendlyDesc": "Ingests raw telemetry stream at high throughput.", "tools": "⚡ Vector Log Tokenizer"},
            {"name": "Stack Extractor", "friendlyTitle": "🔍 2. Extract Stack Traces", "friendlyDesc": "Isolates Python and Node.js crash exception traces.", "tools": "🧠 Regex Stack Extractor"},
            {"name": "Error Clustering", "friendlyTitle": "🧩 3. Deduplicate 4,200 Errors", "friendlyDesc": "Groups 4,200 repeated crashes into 1 root bug.", "tools": "📊 Vector Clustering"},
            {"name": "Git Blame Correlator", "friendlyTitle": "💻 4. Correlate with Git Commit", "friendlyDesc": "Matches stack trace to commit #84a2f merged 12m ago.", "tools": "🐙 GitHub Blame API"},
            {"name": "Severity Scorer", "friendlyTitle": "⚠️ 5. Classify Severity as P1", "friendlyDesc": "Ranks issue as high severity due to revenue impact.", "tools": "🎯 SLA Classifier"},
            {"name": "Sentry Bridge", "friendlyTitle": "🎫 6. Open Tracking Issue", "friendlyDesc": "Creates linked incident in Sentry with diagnostic data.", "tools": "🐛 Sentry API Bridge"},
            {"name": "PagerDuty Trigger", "friendlyTitle": "🚨 7. Alert On-Call Engineer", "friendlyDesc": "Dispatches phone and push notification to lead engineer.", "tools": "📱 PagerDuty Events v2"},
            {"name": "Triage Telemetry", "friendlyTitle": "✅ 8. Log Triage Attestation", "friendlyDesc": "Records response latency in engineering reliability SLA.", "tools": "📜 Immutable Triage Store"}
        ]
    },
    "erp": {
        "category": "finance",
        "icon": "📑",
        "badge": "Finance & Legal",
        "friendlyName": "Enterprise ERP Ledger & 3-Way Matching",
        "techName": "Audit Agent",
        "friendlyProblem": "Q3 inventory rebalancing, PO reconciliation, and vendor ledger postings across 14 distribution nodes.",
        "friendlyGoal": "Synchronize ERP master data, execute 3-way matching on invoices, calculate regional VAT/GST taxes, and post double-entry ledgers.",
        "friendlyTakeaway": "Eliminating invoice errors saves millions in vendor overcharges and accounting delays.",
        "nodes": [
            {"name": "ERP Master Sync", "friendlyTitle": "📥 1. Sync SAP & Oracle Master Data", "friendlyDesc": "Pulls vendor registries, chart of accounts, and POs.", "tools": "🏢 SAP S/4HANA OData"},
            {"name": "Invoice OCR Parser", "friendlyTitle": "📄 2. Parse Vendor Invoice PDF", "friendlyDesc": "Extracts line items, taxes, quantities, and terms.", "tools": "👁️ OCR Document AI"},
            {"name": "3-Way Matcher", "friendlyTitle": "⚖️ 3. Execute 3-Way Reconciliation", "friendlyDesc": "Compares PO, warehouse receipt, and invoice amounts.", "tools": "🧠 PO 3-Way Matcher"},
            {"name": "Tax Calculator", "friendlyTitle": "💵 4. Compute Regional VAT/GST", "friendlyDesc": "Validates regional sales tax across 14 states.", "tools": "🏛️ Avalara AvaTax API"},
            {"name": "Discrepancy Resolver", "friendlyTitle": "🔍 5. Flag $140 Pricing Variance", "friendlyDesc": "Catches pricing discrepancy and requests vendor credit.", "tools": "⚠️ Exception Handler"},
            {"name": "Double Entry Poster", "friendlyTitle": "📑 6. Post Double-Entry Ledger", "friendlyDesc": "Generates verified debit and credit journal entries.", "tools": "🏢 Oracle Fusion ERP"},
            {"name": "EDI Dispatcher", "friendlyTitle": "📤 7. Transmit EDI Remittance", "friendlyDesc": "Sends EDI 820 payment advice to vendor bank.", "tools": "⚡ EDI 820 Gateway"},
            {"name": "Audit Cryptoseal", "friendlyTitle": "🔒 8. Seal Financial Ledger Hash", "friendlyDesc": "Applies cryptographic balance seal to journal log.", "tools": "🛡️ Cryptographic Ledger"}
        ]
    },
    "trafficrouter": {
        "category": "it",
        "icon": "🌐",
        "badge": "IT & Systems",
        "friendlyName": "Global Edge Traffic & DNS Failover",
        "techName": "Traffic Router Agent",
        "friendlyProblem": "A major ISP cable cut caused latency spikes on US-East routes.",
        "friendlyGoal": "Monitor edge health, calculate lowest-latency DNS paths, transfer active HTTP/2 sessions without dropped requests, and shield from DDoS.",
        "friendlyTakeaway": "Multi-cloud traffic routing guarantees 100% uptime even when underlying cloud providers fail.",
        "nodes": [
            {"name": "BGP Health Monitor", "friendlyTitle": "📡 1. Ingest BGP Latency Feed", "friendlyDesc": "Detects 340ms latency surge on US-East data center routes.", "tools": "📊 Edge Telemetry Feed"},
            {"name": "Anycast Resolver", "friendlyTitle": "🗺️ 2. Calculate Optimal Failover", "friendlyDesc": "Identifies Frankfurt and US-West nodes as lowest latency.", "tools": "🧭 Anycast Route Solver"},
            {"name": "WAF Shield", "friendlyTitle": "🛡️ 3. Verify Clean Traffic Flow", "friendlyDesc": "Filters malicious DDoS bot floods before rerouting.", "tools": "🔒 Cloudflare WAF API"},
            {"name": "Session Shift", "friendlyTitle": "🔄 4. Migrate Active HTTP/2 Sessions", "friendlyDesc": "Transfers 12,000 active sessions with zero dropped packets.", "tools": "⚡ Envoy Control Plane"},
            {"name": "DNS Update", "friendlyTitle": "🌐 5. Update Geo-DNS Records", "friendlyDesc": "Updates Route 53 latency routing records in 500ms.", "tools": "☁️ AWS Route 53 API"},
            {"name": "Canary Verification", "friendlyTitle": "🧪 6. Run Canary Health Checks", "friendlyDesc": "Tests synthetic transactions across failover routes.", "tools": "🔬 Synthetic Checker"},
            {"name": "Edge Cache Warm", "friendlyTitle": "⚡ 7. Pre-Warm Edge Caches", "friendlyDesc": "Syncs top cached assets to new regional data centers.", "tools": "🗄️ Redis Edge Cache"},
            {"name": "Routing Attestation", "friendlyTitle": "📋 8. Log Failover Attestation", "friendlyDesc": "Records failover duration (1.2s total) in SLA audit.", "tools": "📜 SLA Compliance Log"}
        ]
    },
    "networkdispatch": {
        "category": "it",
        "icon": "🛰️",
        "badge": "IT & Systems",
        "friendlyName": "Enterprise SD-WAN Mesh & Bandwidth QoS",
        "techName": "Network Dispatch Agent",
        "friendlyProblem": "350 remote branch offices require network routing optimization for VoIP and video.",
        "friendlyGoal": "Analyze SD-WAN mesh topology, prioritize video traffic with QoS, provision encrypted WireGuard tunnels, and verify SLA uptime.",
        "friendlyTakeaway": "Autonomous network dispatch maintains crisp video calls and zero packet loss across global offices.",
        "nodes": [
            {"name": "Topology Ingest", "friendlyTitle": "📥 1. Read 350-Branch SD-WAN Mesh", "friendlyDesc": "Monitors network load across 350 global office routers.", "tools": "🏢 Cisco vManage REST"},
            {"name": "Jitter Analyzer", "friendlyTitle": "📊 2. Detect VoIP Packet Jitter", "friendlyDesc": "Identifies 4.8% packet loss impacting video calls in Sydney.", "tools": "📈 Jitter Analyzer"},
            {"name": "QoS Prioritizer", "friendlyTitle": "🎯 3. Set Dynamic QoS Rules", "friendlyDesc": "Gives top priority to video calls over background file downloads.", "tools": "⚡ DiffServ QoS Policy"},
            {"name": "Tunnel Provisioner", "friendlyTitle": "🔐 4. Provision WireGuard Tunnel", "friendlyDesc": "Spins up encrypted peer-to-peer backup tunnel in 400ms.", "tools": "🔒 WireGuard Kernel API"},
            {"name": "Juniper Config", "friendlyTitle": "⚙️ 5. Push Juniper RPC Config", "friendlyDesc": "Updates routing tables across branch gateway hardware.", "tools": "🔧 Juniper PyEZ RPC"},
            {"name": "Zero-Touch Sync", "friendlyTitle": "🔄 6. Zero-Touch Synchronize", "friendlyDesc": "Applies synchronized policies with zero branch downtime.", "tools": "🌐 Zero-Touch Mesh"},
            {"name": "Bandwidth Test", "friendlyTitle": "🧪 7. Test Synthetic Video Stream", "friendlyDesc": "Verifies packet loss drops to 0.00% and latency is < 28ms.", "tools": "🔬 Synthetic Stream Test"},
            {"name": "Network Audit", "friendlyTitle": "📋 8. Commit Network Audit State", "friendlyDesc": "Stores cryptographically signed network configuration state.", "tools": "📜 PQC Network Ledger"}
        ]
    },
    "selfimproving": {
        "category": "it",
        "icon": "🔄",
        "badge": "IT & Systems",
        "friendlyName": "Self-Improving AI Reflection & Prompt Autotune",
        "techName": "Self-Improving Agent",
        "friendlyProblem": "AI agent pipeline throughput dropped by 8% due to complex prompt variations.",
        "friendlyGoal": "Collect execution traces, classify error patterns, generate step-by-step LLM critiques, and autotune system instructions using DSPy.",
        "friendlyTakeaway": "Autonomous systems optimize their own instructions over time, getting faster, cheaper, and smarter with every execution.",
        "nodes": [
            {"name": "Trace Collector", "friendlyTitle": "📥 1. Ingest Execution Traces", "friendlyDesc": "Pulls 10,000 multi-agent decision steps from vector memory.", "tools": "📊 OpenTelemetry Traces"},
            {"name": "Failure Taxonomy", "friendlyTitle": "🔍 2. Classify Weak Decision Points", "friendlyDesc": "Finds where agent reasoning loops hesitated or took sub-optimal steps.", "tools": "🧠 Failure Taxonomy AI"},
            {"name": "Self-Critique AI", "friendlyTitle": "💡 3. Generate LLM Self-Critiques", "friendlyDesc": "Runs recursive reflection prompts explaining how to do better.", "tools": "✨ Reflection Critique"},
            {"name": "DSPy Optimizer", "friendlyTitle": "⚙️ 4. Autotune Instructions via DSPy", "friendlyDesc": "Mutates agent prompt tokens using Bayesian optimization.", "tools": "🔧 DSPy Optimization"},
            {"name": "Eval Sandbox", "friendlyTitle": "🧪 5. Run Evaluation Benchmark", "friendlyDesc": "Tests 500 synthetic test cases to verify 0 regressions.", "tools": "🔬 Eval Harness Suite"},
            {"name": "Memory Commit", "friendlyTitle": "🧠 6. Store Golden Examples in Vector DB", "friendlyDesc": "Saves top high-performing reasoning paths into Pinecone.", "tools": "🗄️ Pinecone Vector DB"},
            {"name": "Canary Rollout", "friendlyTitle": "🚀 7. Canary Deploy New System Prompt", "friendlyDesc": "Rolls out optimized prompt to 10% of production traffic.", "tools": "⚡ Prompt Canary Deploy"},
            {"name": "Evolution Attestation", "friendlyTitle": "✅ 8. Certify +14% Speed Improvement", "friendlyDesc": "Records verified +14% latency improvement in audit logs.", "tools": "📜 Evolution Audit Hash"}
        ]
    },
    "systemoptimizing": {
        "category": "it",
        "icon": "⚙️",
        "badge": "IT & Systems",
        "friendlyName": "Continuous Server & Memory Kernel Tuning",
        "techName": "System-Optimizing Agent",
        "friendlyProblem": "Server CPU and memory bottlenecks detected across 12 microservices.",
        "friendlyGoal": "Profile low-level kernel cycles with eBPF, tune slow database query execution plans, optimize Redis cache TTLs, and scale Kubernetes pods.",
        "friendlyTakeaway": "Autonomous kernel profiling fixes infrastructure slowdowns before they can trigger user-facing outages.",
        "nodes": [
            {"name": "eBPF Profiler", "friendlyTitle": "📡 1. Profile Linux Kernel Cycles", "friendlyDesc": "Attaches eBPF probes to profile CPU cycles and memory locks.", "tools": "⚡ eBPF Kernel Probe"},
            {"name": "Query Plan Optimizer", "friendlyTitle": "🗄️ 2. Analyze Slow SQL Queries", "friendlyDesc": "Runs EXPLAIN ANALYZE on slow database queries and adds missing index.", "tools": "🧠 Postgres EXPLAIN API"},
            {"name": "Redis Cache Tuner", "friendlyTitle": "⚡ 3. Optimize Cache Hit Ratio", "friendlyDesc": "Tunes Redis TTLs, boosting cache hit rates from 71% to 96%.", "tools": "🗄️ Redis Cluster API"},
            {"name": "Protobuf Compressor", "friendlyTitle": "📦 4. Compress gRPC RPC Payloads", "friendlyDesc": "Applies snappy compression to cut inter-service network bandwidth by 54%.", "tools": "🔧 gRPC Compressor"},
            {"name": "K8s HPA Autoscaler", "friendlyTitle": "📈 5. Autoscale Kubernetes Pods", "friendlyDesc": "Adjusts HPA target metrics to spin up 4 new pods in 1.4s.", "tools": "☁️ K8s Metrics Server"},
            {"name": "GC Defragmenter", "friendlyTitle": "🧹 6. Defragment Runtime Memory", "friendlyDesc": "Triggers concurrent garbage collection to free 6.2 GB RAM.", "tools": "⚙️ JVM / Go GC Tuner"},
            {"name": "Envoy Pool Tuner", "friendlyTitle": "🌐 7. Optimize Connection Pools", "friendlyDesc": "Expands connection pools on edge proxies to eliminate TCP handshakes.", "tools": "🔧 Envoy Proxy API"},
            {"name": "Tuning Certificate", "friendlyTitle": "✅ 8. Issue System Performance Seal", "friendlyDesc": "Certifies that average server latency dropped to 18ms.", "tools": "📜 Performance Seal"}
        ]
    },
    "finops": {
        "category": "finance",
        "icon": "💰",
        "badge": "Finance & Legal",
        "friendlyName": "Multi-Cloud FinOps & Token Spend Optimization",
        "techName": "FinTech Ops Agent",
        "friendlyProblem": "Runaway LLM token spend across multi-cloud infrastructure threatens monthly margins.",
        "friendlyGoal": "Ingest real-time token telemetry across AWS, GCP, and Azure, right-size frontier models, enforce hard spend quotas, and reconcile departmental chargebacks.",
        "friendlyTakeaway": "Automated FinOps agents eliminate cloud overages before they occur, slashing token costs by up to 40% with zero downtime.",
        "nodes": [
            {"name": "Billing Ingestion", "friendlyTitle": "📊 1. Ingest Multi-Cloud Billing Streams", "friendlyDesc": "Aggregates real-time cost telemetry from AWS, GCP, and Azure simultaneously.", "tools": "☁️ Cloud Billing API"},
            {"name": "Cost Normalizer", "friendlyTitle": "🔄 2. Normalize Currency & Usage", "friendlyDesc": "Normalizes disparate usage formats into unified JSON cost metrics.", "tools": "⚙️ OpenCost Prometheus"},
            {"name": "Model Rightsizer", "friendlyTitle": "🎯 3. Calculate Model Rightsizing", "friendlyDesc": "Evaluates task complexity and recommends smaller, cost-effective frontier models.", "tools": "🧠 Unit Economics AI"},
            {"name": "Spend Quota Enforcer", "friendlyTitle": "🛑 4. Enforce Departmental Budgets", "friendlyDesc": "Applies automated circuit breakers before monthly spend caps are breached.", "tools": "🔒 Vault Quota Leases"},
            {"name": "Anomaly Detector", "friendlyTitle": "⚠️ 5. Detect Sudden Spending Surges", "friendlyDesc": "Identifies abnormal query volume spikes and flags potential runaway loops.", "tools": "📈 Statistical Profiler"},
            {"name": "ERP Chargeback", "friendlyTitle": "💼 6. Allocate Departmental Costs", "friendlyDesc": "Generates immutable chargeback logs directly mapped to cost center IDs.", "tools": "🗄️ ERP Reconciliation"},
            {"name": "Financial Ledger", "friendlyTitle": "📋 7. Post Double-Entry Journal Records", "friendlyDesc": "Posts verified balance records to corporate accounting systems.", "tools": "📜 Financial Ledger Bridge"},
            {"name": "FinOps Certificate", "friendlyTitle": "🛡️ 8. Seal Audit-Ready Efficiency Proof", "friendlyDesc": "Generates cryptographic proof of compliance with FinOps governance mandates.", "tools": "🔒 PQC Signed Receipt"}
        ]
    },
    "contractintel": {
        "category": "finance",
        "icon": "📜",
        "badge": "Finance & Legal",
        "friendlyName": "Autonomous Contract Intelligence & Compliance Redlining",
        "techName": "Contract Intelligence Agent",
        "friendlyProblem": "Vendor Master Services Agreements and DPAs take weeks for legal teams to manually review and redline.",
        "friendlyGoal": "Parse legal contracts into structured clause registries, classify regulatory risk, flag uncapped liabilities, extract milestone deadlines, and generate protective redlines.",
        "friendlyTakeaway": "Automated contract intelligence accelerates turnaround from weeks to seconds while eliminating hidden liability exposures.",
        "nodes": [
            {"name": "Document Ingestion", "friendlyTitle": "📄 1. Parse Legal PDF & DOCX Files", "friendlyDesc": "Converts unstructured legal agreements into standardized JSON ASTs.", "tools": "📑 Multimodal OCR"},
            {"name": "Clause Extractor", "friendlyTitle": "🔍 2. Extract Key Contract Clauses", "friendlyDesc": "Identifies indemnification, limitation of liability, and governing law sections.", "tools": "🧠 Legal Clause Classifier"},
            {"name": "Regulatory Auditor", "friendlyTitle": "⚖️ 3. Audit Regulatory Frameworks", "friendlyDesc": "Verifies compliance against GDPR, HIPAA, SOC 2, and CCPA standards.", "tools": "🛡️ Compliance Engine"},
            {"name": "Risk Scorer", "friendlyTitle": "⚠️ 4. Score Liability Exposures", "friendlyDesc": "Flags uncapped indemnification and high-risk terms with P0-P3 severity tags.", "tools": "📊 Risk Matrix Engine"},
            {"name": "Deadline Tracker", "friendlyTitle": "📅 5. Map Milestones & Renewal Dates", "friendlyDesc": "Extracts auto-renewal dates and syncs them to executive calendars.", "tools": "📆 Calendar & CLM Bridge"},
            {"name": "Redline Generator", "friendlyTitle": "✏️ 6. Generate Protective Redlines", "friendlyDesc": "Drafts customized compromise language protecting enterprise interests.", "tools": "📝 Redline Synthesizer"},
            {"name": "CLM Synchronization", "friendlyTitle": "💼 7. Sync with DocuSign & CLM", "friendlyDesc": "Publishes redlines and approval packages to enterprise contract repositories.", "tools": "☁️ DocuSign CLM API"},
            {"name": "Cryptographic Seal", "friendlyTitle": "🔒 8. Apply PQC Cryptographic Seal", "friendlyDesc": "Seals verified document state using NIST ML-KEM-768 quantum-safe signatures.", "tools": "🛡️ NIST FIPS 203 Seal"}
        ]
    },
    "missedcalltextback": {
        "category": "beginner",
        "icon": "📱",
        "badge": "⭐ Beginner Friendly",
        "friendlyName": "Autonomous Missed Call Recovery & Sub-3s Text-Back",
        "techName": "Missed Call / Text Back Agent",
        "friendlyProblem": "67% of inbound callers hang up when directed to voicemail and immediately contact competitors.",
        "friendlyGoal": "Intercept dropped or unanswered calls, transcribe voicemail audio, identify the prospect via CRM, compose a personalized text-back, and dispatch it via SMS in under 3 seconds.",
        "friendlyTakeaway": "Instant sub-3s text responses boost inbound lead recovery by over 300% with 0 bytes of persistent disk storage.",
        "nodes": [
            {"name": "Telephony Ingestion", "friendlyTitle": "📞 1. Detect Missed Inbound Ring", "friendlyDesc": "Picks up unanswered telephony webhook within 120ms of carrier disconnect.", "tools": "📱 Twilio / Telnyx Webhook"},
            {"name": "Caller Resolver", "friendlyTitle": "🔍 2. Resolve Contact Identity", "friendlyDesc": "Matches caller number against HubSpot CRM to personalize the outreach.", "tools": "🗄️ HubSpot CRM Bridge"},
            {"name": "Audio Transcriber", "friendlyTitle": "🎙️ 3. Transcribe Voicemail Audio", "friendlyDesc": "Transcribes caller audio message and flags intent and urgency.", "tools": "⚡ Speech-to-Text AI"},
            {"name": "SMS Composer", "friendlyTitle": "💬 4. Compose Personalized SMS", "friendlyDesc": "Drafts context-specific greeting offering callback or appointment booking.", "tools": "🧠 Dynamic Context Engine"},
            {"name": "Carrier Dispatcher", "friendlyTitle": "🚀 5. Dispatch SMS Sub-3s", "friendlyDesc": "Sends text response through cellular carrier within 2.4s total SLA.", "tools": "📱 Carrier Messaging API"},
            {"name": "Calendar Scheduler", "friendlyTitle": "📅 6. Coordinate Callback Slot", "friendlyDesc": "Provides 1-click scheduling link matching representative availability.", "tools": "📆 Google Calendar Sync"},
            {"name": "CRM Logger", "friendlyTitle": "💼 7. Log Activity Record", "friendlyDesc": "Records full transcript, SMS status, and callback slot in CRM history.", "tools": "☁️ CRM Activity API"},
            {"name": "SLA Verifier", "friendlyTitle": "🛡️ 8. Seal Recovery Attestation", "friendlyDesc": "Verifies sub-3s SLA delivery in RAM-only enclave with zero disk retention.", "tools": "🔒 Cryptographic Proof"}
        ]
    },
    "llmops": {
        "category": "it",
        "icon": "🧪",
        "badge": "AI Reliability",
        "friendlyName": "Continuous Prompt Evaluation & Canary Benchmark Router",
        "techName": "LLMOps & Prompt Evaluation Agent",
        "friendlyProblem": "Frontier model updates silently break system prompts, introduce hallucinations, and degrade response quality in production.",
        "friendlyGoal": "Run continuous prompt evaluations across golden benchmarks, detect semantic drift, evaluate hallucination rate, and dynamically route traffic to the highest-performing frontier model.",
        "friendlyTakeaway": "Automated prompt ops ensures enterprise AI workflows never silently break, cutting token costs by 42% while guaranteeing zero hallucination drift.",
        "nodes": [
            {"name": "Prompt Ingestion", "friendlyTitle": "📥 1. Ingest Prompt Template", "friendlyDesc": "Loads system prompt and test dataset from version-controlled repository.", "tools": "📂 Git Repository Hook"},
            {"name": "Drift Engine", "friendlyTitle": "📐 2. Calculate Semantic Drift", "friendlyDesc": "Computes cosine distance embeddings against baseline response distributions.", "tools": "🧠 Vector Distance AI"},
            {"name": "Hallucination Verifier", "friendlyTitle": "🛡️ 3. Verify Groundedness Index", "friendlyDesc": "Evaluates RAG context faithfulness and ensures zero hallucination leakage.", "tools": "🔬 RAG Triad Evaluator"},
            {"name": "Canary Benchmarker", "friendlyTitle": "⚡ 4. Benchmark Frontier Models", "friendlyDesc": "Tests Gemini 2.5 Flash, Mistral Large, and Claude 3.7 Sonnet on latency and quality.", "tools": "🚀 Frontier Model API"},
            {"name": "Pareto Router", "friendlyTitle": "⚖️ 5. Optimize Cost-Latency Frontier", "friendlyDesc": "Dynamically selects optimal model, achieving 42% cost reduction within SLA.", "tools": "📊 Pareto Frontier Router"},
            {"name": "Prompt Mutator", "friendlyTitle": "🔧 6. Autotune Prompt via DSPy", "friendlyDesc": "Employs reflection loops to patch weak instructions and eliminate edge-case failures.", "tools": "⚙️ DSPy Teleprompter"},
            {"name": "CI/CD Gatekeeper", "friendlyTitle": "🚦 7. Block Regression in CI/CD", "friendlyDesc": "Fails GitHub Actions check if quality drops below 99.0% threshold.", "tools": "☁️ GitHub Actions Gate"},
            {"name": "Attestation Verifier", "friendlyTitle": "📜 8. Seal Benchmark Attestation", "friendlyDesc": "Generates verifiable cryptographic receipt of model evaluation compliance.", "tools": "🔒 Enclave Attestation Seal"}
        ]
    }
}

# Save json file for easy reusability
with open(os.path.join(WORKSPACE, "scripts", "scenarios_data.json"), "w", encoding="utf-8") as f:
    json.dump(SCENARIOS_DATA, f, indent=2)

print("Saved scenarios_data.json with", len(SCENARIOS_DATA), "entries.")
