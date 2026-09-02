"""
PipeFish Labs — Autonomous Incident Triage & ChatOps Bot
Version: 2.4.0
Connects Slack, Discord, and Opsgenie/PagerDuty alerts to the 8-Node Autonomous Mesh
"""

import json
from typing import Dict, Any
from sdk.pipefish_sdk import PipeFishAgentMesh
from sdk.productivity_connectors import SlackAlertConnector, LinearConnector

class IncidentTriageBot:
    """
    Ingests infrastructure and application alerts, assesses priority, triggers
    the Log Triage or System Optimizing agent graph, and dispatches remediation plans.
    """

    def __init__(self, api_key: str = "bot_live_mesh_key"):
        self.client = PipeFishAgentMesh(api_key=api_key)
        self.slack = SlackAlertConnector()
        self.linear = LinearConnector()

    def handle_incident_alert(self, raw_alert: Dict[str, Any]) -> Dict[str, Any]:
        alert_name = raw_alert.get("alert_name", "Unknown Alert")
        severity = raw_alert.get("severity", "P3").upper()
        service = raw_alert.get("service", "core-ingress")

        # 1. Trigger the appropriate 8-node agent graph
        scenario = "systemoptimizing" if "latency" in alert_name.lower() or "cpu" in alert_name.lower() else "logtriage"
        execution_result = self.client.trigger_graph_execution(
            scenario_key=scenario,
            payload=raw_alert
        )

        # 2. If high severity (P1/P2), auto-create a Linear issue
        linear_issue = None
        if severity in ["P1", "P2"]:
            linear_issue = self.linear.create_issue(
                title=f"{severity} Incident: {alert_name} on {service}",
                description=f"Auto-escalated by PipeFish Incident Bot.\nMesh Result: {json.dumps(execution_result)}",
                priority=1 if severity == "P1" else 2
            )

        # 3. Format Slack Notification Block
        slack_blocks = self.slack.build_alert_blocks(
            scenario=scenario,
            status=execution_result["status"],
            details=f"Alert: {alert_name} | Target Service: {service}\nRemediation Graph: {scenario} (Nodes Executed: 8)",
            severity=severity
        )

        return {
            "alert_processed": alert_name,
            "severity": severity,
            "agent_scenario": scenario,
            "mesh_status": execution_result["status"],
            "linear_issue": linear_issue,
            "slack_payload": slack_blocks
        }

if __name__ == "__main__":
    bot = IncidentTriageBot()
    res = bot.handle_incident_alert({
        "alert_name": "Ingress CPU Latency Spike",
        "severity": "P1",
        "service": "k8s-ingress-controller"
    })
    print("Incident Bot Response:")
    print(json.dumps(res, indent=2))
