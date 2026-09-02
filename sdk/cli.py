#!/usr/bin/env python3
"""
PipeFish Labs — Command Line Interface (CLI)
Version: 2.4.0
Usage: pipefish [COMMAND] [OPTIONS]
"""

import sys
import os
import json
import argparse

# Ensure project root is in path when executed directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sdk.pipefish_sdk import PipeFishAgentMesh
from sdk.compliance_report import ComplianceAuditGenerator
from sdk.webhook_verifier import WebhookVerifier, WebhookVerificationError

def cmd_simulate(args):
    """Simulates an 8-node agent execution graph."""
    client = PipeFishAgentMesh(api_key=args.api_key or "demo_cli_key")
    payload = json.loads(args.payload) if args.payload else {"source": "cli_invocation", "priority": "high"}
    print(f"\n[EXEC] [PipeFish Labs] Executing 8-node graph for scenario: {args.scenario}...")
    result = client.trigger_graph_execution(args.scenario, payload)
    print(json.dumps(result, indent=2))

def cmd_mcp(args):
    """Launches the reference MCP server on stdio."""
    from sdk.mcp_server import main as mcp_main
    print("[PipeFish Labs] Starting Model Context Protocol (MCP) server on stdio...", file=sys.stderr)
    mcp_main()

def cmd_compliance(args):
    """Generates an automated compliance audit report."""
    generator = ComplianceAuditGenerator(tenant_id=args.tenant or "pipefish-core")
    report = generator.generate_report(standard=args.standard)
    print(json.dumps(report, indent=2))

def cmd_verify_webhook(args):
    """Verifies a webhook signature header."""
    try:
        verifier = WebhookVerifier(secret_key=args.secret)
        payload_bytes = args.payload.encode("utf-8")
        is_valid = verifier.verify(payload_bytes, args.signature)
        print(f"[SUCCESS] Webhook Signature Verified: {is_valid}")
    except WebhookVerificationError as exc:
        print(f"[ERROR] Webhook Verification Failed: {exc}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        prog="pipefish",
        description="PipeFish Labs — Enterprise AI Automation & Multi-Agent Mesh CLI"
    )
    parser.add_argument("--version", action="version", version="pipefish 2.4.0 (NIST FIPS 203 ML-KEM-768)")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # simulate
    sub_sim = subparsers.add_parser("simulate", help="Trigger an 8-node agent execution graph")
    sub_sim.add_argument("scenario", choices=[
        "receptionist", "sales", "logistics", "integration", "quantum",
        "reverse", "crypto", "errorcorr", "trend", "market", "codescan",
        "docs", "observability", "revops", "analytics", "auditing",
        "logtriage", "erp", "trafficrouter", "networkdispatch",
        "selfimproving", "systemoptimizing"
    ], help="Scenario key")
    sub_sim.add_argument("--payload", default=None, help="JSON telemetry payload string")
    sub_sim.add_argument("--api-key", default=None, help="PipeFish API key")

    # mcp
    subparsers.add_parser("mcp", help="Run the reference Model Context Protocol (MCP) server on stdio")

    # compliance
    sub_comp = subparsers.add_parser("compliance", help="Generate automated regulatory audit report")
    sub_comp.add_argument("--standard", default="EU_AI_ACT_ANNEX_IV", choices=["EU_AI_ACT_ANNEX_IV", "SOC2_TYPE_II", "HIPAA"])
    sub_comp.add_argument("--tenant", default="pipefish-core", help="Tenant ID")

    # verify-webhook
    sub_wh = subparsers.add_parser("verify-webhook", help="Validate cryptographic webhook signature")
    sub_wh.add_argument("--secret", required=True, help="Webhook signing secret")
    sub_wh.add_argument("--payload", required=True, help="Payload string")
    sub_wh.add_argument("--signature", required=True, help="X-PipeFish-Signature header value")

    args = parser.parse_args()

    if args.command == "simulate":
        cmd_simulate(args)
    elif args.command == "mcp":
        cmd_mcp(args)
    elif args.command == "compliance":
        cmd_compliance(args)
    elif args.command == "verify-webhook":
        cmd_verify_webhook(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
