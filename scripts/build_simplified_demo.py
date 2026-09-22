"""
Comprehensive generator to apply the beginner-friendly educational interactive
Agent Chain simulator to demo/index.html and index.html.
"""

import os
import sys
import json

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE not in sys.path:
    sys.path.insert(0, WORKSPACE)

# Load enriched scenario metadata from scenarios_data.json
scenarios_json_path = os.path.join(WORKSPACE, "scripts", "scenarios_data.json")
if os.path.exists(scenarios_json_path):
    with open(scenarios_json_path, "r", encoding="utf-8") as f:
        SCENARIOS_DATA = json.load(f)
else:
    SCENARIOS_DATA = {}

print(f"Loaded {len(SCENARIOS_DATA)} scenario profiles from scenarios_data.json.")

def build_simulator_pages():
    """Builds and applies the updated simulator components to index.html and demo/index.html."""
    from scripts.apply_simplified_simulator import update_index, update_demo
    update_index()
    update_demo()
    print("[SUCCESS] All simulator pages built and updated.")

if __name__ == "__main__":
    build_simulator_pages()
