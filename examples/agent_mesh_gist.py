#!/usr/bin/env python3
"""
PipeFish Labs — Quickstart Gist: Multi-Agent Execution with Zero-Trust Resilience
Usage: python examples/agent_mesh_gist.py
"""

import os
import sys

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sdk.pipefish_sdk import PipeFishAgentMesh
from sdk.middleware import CircuitBreaker, TokenBucketRateLimiter
from security.pqc_mtls_manager import PQCKeyManager
from sdk.sqlite_store import SQLiteStore

def main():
    print("[INIT] [PipeFish Labs] Initializing Resilient Multi-Agent Mesh...")

    # 1. Initialize Components
    client = PipeFishAgentMesh(api_key="demo_quickstart_key")
    circuit_breaker = CircuitBreaker(failure_threshold=3, cooldown_seconds=5.0)
    rate_limiter = TokenBucketRateLimiter(rate=5.0, capacity=10.0)
    key_manager = PQCKeyManager(node_id="gateway-node-01")
    store = SQLiteStore(":memory:")

    # 2. Rate Limiter Guard
    if not rate_limiter.acquire(1.0):
        print("Rate limit reached. Request throttled.")
        return

    # 3. Issue Ephemeral PQC A2A Ticket
    ticket = key_manager.sign_a2a_ticket(
        target_node="systemoptimizing",
        payload_digest="sha256_k8s_cpu_anomaly"
    )
    print(f"Issued PQC Handshake Ticket: {ticket['key_id']}")

    # 4. Trigger 8-Node Execution Graph inside Circuit Breaker
    result = circuit_breaker.call(
        client.trigger_graph_execution,
        scenario_key="systemoptimizing",
        payload={"alert": "CPU latency spike on K8s ingress", "pqc_ticket": ticket}
    )

    # 5. Record to In-Memory Zero-Retention Store
    exec_id = store.save_execution(
        scenario=result["scenario"],
        status=result["status"],
        nodes=result["nodes_executed"],
        handoff_mode=result["handoff_mode"],
        payload=result["execution_summary"]
    )
    print(f"Execution Recorded in RAM-Only SQLite (ID: {exec_id})")
    print(f"Status: {result['status']} | Nodes: {result['nodes_executed']} | Mode: {result['handoff_mode']}")

if __name__ == "__main__":
    main()
