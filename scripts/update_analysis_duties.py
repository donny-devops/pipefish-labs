import os
import json

# Update duties for Analysis Agent (key: auditing)
with open('index.html', 'r', encoding='utf-8') as fp:
    content = fp.read()

# Extract spec data JSON
parts = content.split('window.agentSpecsData = ')
json_str = parts[1].split(';\nconst demoScenarios =')[0]
specs = json.loads(json_str)

specs['auditing']['duties'] = "• Contextual Synthesis: Processes and analyzes structured signals, telemetry data, and multi-source inputs to extract actionable insights and operational requirements.<br>• State Verification: Evaluates data integrity and operational parameters before handing off verified payloads through cryptographic Directed Acyclic Graph (DAG) state transitions.<br>• Decision Support: Powers automated decision-making engines by classifying intent, checking enterprise capacity, and flagging non-conformities or exceptions in real time."

new_json_str = json.dumps(specs)

# Replace in index.html
content = content.replace(json_str, new_json_str)

# Ensure duties rendering block exists in index.html
duties_block = '''if (drawerEl && window.agentSpecsData && window.agentSpecsData[currentDemoScenario]) {
    const spec = window.agentSpecsData[currentDemoScenario];
    const dutiesHtml = spec.duties ? `
      <div style="background:rgba(0,212,255,0.06);padding:14px;border:1px solid var(--cyan-dim);border-radius:6px;margin-bottom:14px">
        <strong style="color:var(--cyan);display:block;margin-bottom:6px;font-family:var(--font-mono);font-size:13px">📋 CORE AGENT DUTIES &amp; RESPONSIBILITIES:</strong>
        <div style="color:var(--text-strong);font-size:13px;line-height:1.75">${spec.duties}</div>
      </div>
    ` : '';
    drawerEl.innerHTML = `
      <div style="font-family:var(--font-display);font-size:14px;font-weight:800;color:var(--cyan);letter-spacing:0.12em;margin-bottom:14px;text-transform:uppercase;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">
        <span>⚡ AGENT ARCHITECTURE &amp; SECRETS DRAWER: ${spec.title}</span>
        <span style="font-size:11px;color:var(--text-dim);font-family:var(--font-mono)">ZERO-TRUST ENCLAVE VERIFIED</span>
      </div>
      ${dutiesHtml}
      <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:16px;font-size:12.5px;line-height:1.6">'''

if 'const dutiesHtml = spec.duties' not in content:
    old_block = '''if (drawerEl && window.agentSpecsData && window.agentSpecsData[currentDemoScenario]) {
    const spec = window.agentSpecsData[currentDemoScenario];
    drawerEl.innerHTML = `
      <div style="font-family:var(--font-display);font-size:14px;font-weight:800;color:var(--cyan);letter-spacing:0.12em;margin-bottom:14px;text-transform:uppercase;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">
        <span>⚡ AGENT ARCHITECTURE &amp; SECRETS DRAWER: ${spec.title}</span>
        <span style="font-size:11px;color:var(--text-dim);font-family:var(--font-mono)">ZERO-TRUST ENCLAVE VERIFIED</span>
      </div>
      <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:16px;font-size:12.5px;line-height:1.6">'''
    content = content.replace(old_block, duties_block)

with open('index.html', 'w', encoding='utf-8') as fp:
    fp.write(content)
print("Updated index.html with Analysis Agent duties.")

# Replace in demo/index.html
with open('demo/index.html', 'r', encoding='utf-8') as fp:
    demo_content = fp.read()

demo_parts = demo_content.split('window.agentSpecsData = ')
demo_json_str = demo_parts[1].split(';\nconst scenarios =')[0]

demo_content = demo_content.replace(demo_json_str, new_json_str)

demo_duties_block = '''if (drawerEl && window.agentSpecsData && window.agentSpecsData[currentScenarioKey]) {
    const spec = window.agentSpecsData[currentScenarioKey];
    const dutiesHtml = spec.duties ? `
      <div style="background:rgba(0,212,255,0.06);padding:14px;border:1px solid var(--cyan-dim);border-radius:6px;margin-bottom:14px">
        <strong style="color:var(--cyan);display:block;margin-bottom:6px;font-family:var(--font-mono);font-size:13px">📋 CORE AGENT DUTIES &amp; RESPONSIBILITIES:</strong>
        <div style="color:var(--text-strong);font-size:13px;line-height:1.75">${spec.duties}</div>
      </div>
    ` : '';
    drawerEl.innerHTML = `
      <div style="font-family:var(--font-display);font-size:14px;font-weight:800;color:var(--cyan);letter-spacing:0.12em;margin-bottom:14px;text-transform:uppercase;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">
        <span>⚡ AGENT ARCHITECTURE &amp; SECRETS DRAWER: ${spec.title}</span>
        <span style="font-size:11px;color:var(--text-dim);font-family:var(--font-mono)">ZERO-TRUST ENCLAVE VERIFIED</span>
      </div>
      ${dutiesHtml}
      <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:16px;font-size:12.5px;line-height:1.6">'''

if 'const dutiesHtml = spec.duties' not in demo_content:
    old_demo_block = '''if (drawerEl && window.agentSpecsData && window.agentSpecsData[currentScenarioKey]) {
    const spec = window.agentSpecsData[currentScenarioKey];
    drawerEl.innerHTML = `
      <div style="font-family:var(--font-display);font-size:14px;font-weight:800;color:var(--cyan);letter-spacing:0.12em;margin-bottom:14px;text-transform:uppercase;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">
        <span>⚡ AGENT ARCHITECTURE &amp; SECRETS DRAWER: ${spec.title}</span>
        <span style="font-size:11px;color:var(--text-dim);font-family:var(--font-mono)">ZERO-TRUST ENCLAVE VERIFIED</span>
      </div>
      <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:16px;font-size:12.5px;line-height:1.6">'''
    demo_content = demo_content.replace(old_demo_block, demo_duties_block)

with open('demo/index.html', 'w', encoding='utf-8') as fp:
    fp.write(demo_content)

print("Updated demo/index.html with Analysis Agent duties.")
