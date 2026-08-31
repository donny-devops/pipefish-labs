import sys
import os

REQUIRED_ELEMENTS = [
    ('id="briefing-canvas"', "Executive Briefing Video Canvas (#briefing-canvas)"),
    ('id="hcanvas"', "Hero Node Network Canvas (#hcanvas)"),
    ('id="sec-subnav"', "Page Index Sticky Sub-nav (#sec-subnav)"),
    ('id="demo-status-bar-text"', "Agent Simulator Status Bar (#demo-status-bar-text)"),
    ('id="demo-rows-container"', "Agent Simulator Rows Container (#demo-rows-container)"),
    ('id="run-demo-btn"', "Agent Simulator Run Button (#run-demo-btn)"),
    ('id="about-team"', "Executive Leadership & Engineering Section (#about-team)"),
    ('id="capabilities"', "Capabilities Section (#capabilities)"),
    ('id="architecture"', "Workflow Architecture Section (#architecture)"),
    ('id="agents"', "Autonomous Multi-Agent Section (#agents)"),
    ('class="logo"', "Header Logo (.logo)"),
    ('class="ft-brand"', "Footer Brand Section (.ft-brand)")
]

def verify_dom(filepath='index.html'):
    if not os.path.exists(filepath):
        print(f"[ERROR] {filepath} not found!")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    missing = []
    for snippet, label in REQUIRED_ELEMENTS:
        if snippet not in content:
            missing.append(label)

    if missing:
        print("[FAIL] DOM INTEGRITY VIOLATION DETECTED!")
        print("The following critical elements are missing from index.html:")
        for item in missing:
            print(f"  - {item}")
        sys.exit(1)
    else:
        print("[PASS] DOM INTEGRITY VERIFIED: All critical elements exist in index.html.")

if __name__ == '__main__':
    verify_dom()
