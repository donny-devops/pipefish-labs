"""
PipeFish Labs — Local Zero-Retention / Offline SQLite Adapter
Version: 2.4.0
Enforces RAM-only (:memory:) execution by default for Zero-Data Retention (ZDR) compliance.
"""

import json
import sqlite3
import threading
import uuid
from typing import Any, Dict, Optional


class SQLiteStore:
    """
    In-memory or embedded zero-retention SQLite storage engine
    for recording multi-agent execution telemetry and DAG state transitions.
    """

    def __init__(self, db_path: str = ":memory:"):
        if not isinstance(db_path, str) or not db_path.strip():
            raise ValueError("db_path must be a non-empty string.")
        self.db_path = db_path
        self._lock = threading.Lock()
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS executions (
                    id TEXT PRIMARY KEY,
                    scenario TEXT NOT NULL,
                    status TEXT NOT NULL,
                    nodes_executed INTEGER NOT NULL,
                    handoff_mode TEXT NOT NULL,
                    payload_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS dag_handoffs (
                    id TEXT PRIMARY KEY,
                    execution_id TEXT NOT NULL,
                    step_index INTEGER NOT NULL,
                    node_title TEXT NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY(execution_id) REFERENCES executions(id)
                );
            """)

    def save_execution(self, scenario: str, status: str, nodes: int, handoff_mode: str, payload: Dict[str, Any]) -> str:
        if not isinstance(scenario, str) or not scenario.strip() or len(scenario) > 128:
            raise ValueError("scenario must be a non-empty string up to 128 characters.")
        if not isinstance(status, str) or not status.strip() or len(status) > 32:
            raise ValueError("status must be a non-empty string up to 32 characters.")
        if isinstance(nodes, bool) or not isinstance(nodes, int) or nodes < 0 or nodes > 10_000:
            raise ValueError("nodes must be an integer from 0 to 10000.")
        if not isinstance(handoff_mode, str) or not handoff_mode.strip() or len(handoff_mode) > 64:
            raise ValueError("handoff_mode must be a non-empty string up to 64 characters.")
        if not isinstance(payload, dict):
            raise ValueError("payload must be an object.")
        encoded = json.dumps(payload, separators=(",", ":"))
        if len(encoded) > 262_144:
            raise ValueError("payload exceeds 256KiB.")
        exec_id = str(uuid.uuid4())
        with self._lock:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO executions (id, scenario, status, nodes_executed, handoff_mode, payload_json) VALUES (?, ?, ?, ?, ?, ?)",
                    (exec_id, scenario, status, nodes, handoff_mode, encoded)
                )
        return exec_id

    def log_step(self, execution_id: str, step_index: int, node_title: str, status: str = "COMPLETED"):
        if not isinstance(execution_id, str) or not execution_id.strip():
            raise ValueError("execution_id must be a non-empty string.")
        if isinstance(step_index, bool) or not isinstance(step_index, int) or step_index < 0 or step_index > 10_000:
            raise ValueError("step_index must be an integer from 0 to 10000.")
        if not isinstance(node_title, str) or not node_title.strip() or len(node_title) > 160:
            raise ValueError("node_title must be a non-empty string up to 160 characters.")
        if not isinstance(status, str) or not status.strip() or len(status) > 32:
            raise ValueError("status must be a non-empty string up to 32 characters.")
        step_id = str(uuid.uuid4())
        with self._lock:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO dag_handoffs (id, execution_id, step_index, node_title, status) VALUES (?, ?, ?, ?, ?)",
                    (step_id, execution_id, step_index, node_title, status)
                )

    def get_execution(self, execution_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM executions WHERE id = ?", (execution_id,))
            row = cursor.fetchone()
        if not row:
            return None
        return dict(row)

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    store = SQLiteStore()
    eid = store.save_execution(
        scenario="systemoptimizing",
        status="COMPLETED",
        nodes=8,
        handoff_mode="mistral_native",
        payload={"alert": "Memory spike on pod-01"}
    )
    store.log_step(eid, 0, "Telemetry Ingestion")
    print(f"Recorded in RAM-only SQLite: {store.get_execution(eid)}")
