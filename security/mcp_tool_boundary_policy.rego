package pipefish.mcp

import rego.v1

# Default deny
default allow = false

# Allow if caller role is authorized for the tool and all parameters pass boundary checks
allow if {
    is_authorized_role(input.caller_role, input.tool_name)
    not has_boundary_violation(input.arguments)
}

# Role-to-tool whitelist matrix
is_authorized_role("VoiceReceptionistBot", tool) if {
    valid_tools := {"mcp-server-telephony", "mcp-server-google-calendar", "mcp-server-hubspot", "mcp-server-sms-gateway"}
    valid_tools[tool]
}

is_authorized_role("SalesGrowthOrchestrator", tool) if {
    valid_tools := {"mcp-server-salesforce", "mcp-server-hubspot", "mcp-server-posthog", "mcp-server-clearbit", "mcp-server-doc-generator"}
    valid_tools[tool]
}

is_authorized_role("ReverseEngineerBot", tool) if {
    valid_tools := {"mcp-server-ghidra-headless", "mcp-server-yara-compiler", "mcp-server-cape-sandbox"}
    valid_tools[tool]
}

is_authorized_role("CryptoArchitectBot", tool) if {
    valid_tools := {"mcp-server-openssl-pqc", "mcp-server-hashicorp-vault", "mcp-server-aws-kms"}
    valid_tools[tool]
}

is_authorized_role("SystemOptimizerBot", tool) if {
    valid_tools := {"mcp-server-ebpf-profiler", "mcp-server-postgres-planner", "mcp-server-k8s-metrics"}
    valid_tools[tool]
}

is_authorized_role("ObservabilityTriageOrchestrator", tool) if {
    valid_tools := {"mcp-server-prometheus", "mcp-server-jaeger", "mcp-server-grafana-api", "mcp-server-elasticsearch", "mcp-server-sentry", "mcp-server-pagerduty"}
    valid_tools[tool]
}

# General super-admin role for kernel services
is_authorized_role("KernelServiceOrchestrator", _)

# Boundary violation detection
has_boundary_violation(args) if {
    some key, val in args
    is_string(val)
    contains(val, "../")
}

has_boundary_violation(args) if {
    some key, val in args
    is_string(val)
    contains(val, "..\\")
}

has_boundary_violation(args) if {
    some key, val in args
    is_string(val)
    regex.match("[;&|`]", val)
}

# Explicit denial messages for policy audit feedback
deny contains msg if {
    not is_authorized_role(input.caller_role, input.tool_name)
    msg := sprintf("Role '%v' is unauthorized to invoke MCP tool '%v'", [input.caller_role, input.tool_name])
}

deny contains msg if {
    has_boundary_violation(input.arguments)
    msg := "MCP tool arguments contain boundary violations (path traversal or shell metacharacters)"
}
