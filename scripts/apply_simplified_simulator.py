import os
import re
import json

WORKSPACE = r"C:\Users\Surface\.gemini\antigravity\scratch\pipefish-labs"

# Load SCENARIOS_DATA from json file
with open(os.path.join(WORKSPACE, "scripts", "scenarios_data.json"), "r", encoding="utf-8") as f:
    SCENARIOS_DATA = json.load(f)

print(f"Loaded {len(SCENARIOS_DATA)} scenario profiles from scenarios_data.json.")

# CSS to inject into <style>
CSS_BLOCK = """
  /* ─── SIMPLIFIED AGENT CHAIN STYLING & EDUCATIONAL UX ─── */
  .primer-box { background: linear-gradient(135deg, rgba(8,14,28,0.96) 0%, rgba(13,20,38,0.96) 100%); border: 1px solid rgba(0,212,255,0.35); border-radius: var(--r-lg); padding: clamp(20px, 3vw, 30px); margin-bottom: 24px; box-shadow: 0 12px 36px rgba(0,0,0,0.45); border-left: 5px solid var(--cyan); }
  .category-filter-chips { display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
  .cat-chip { font-family: var(--font-fm); font-size: 11.5px; font-weight: 700; padding: 7px 16px; border-radius: 100px; background: rgba(11,14,23,0.85); border: 1px solid var(--border-strong); color: var(--text-body); cursor: pointer; transition: all 0.2s ease; }
  .cat-chip:hover, .cat-chip.active { background: rgba(0,212,255,0.15); border-color: var(--cyan); color: var(--cyan); box-shadow: 0 0 14px rgba(0,212,255,0.25); }
  .active-story-card { background: linear-gradient(135deg, rgba(11,14,23,0.96) 0%, rgba(17,22,37,0.96) 100%); border: 1px solid rgba(0,212,255,0.3); border-radius: var(--r-md); padding: 22px 26px; margin-bottom: 22px; box-shadow: 0 8px 28px rgba(0,0,0,0.35); }
  .speed-btn { font-family: var(--font-fm); font-size: 11px; font-weight: 700; padding: 5px 10px; border-radius: 6px; background: var(--surface); border: 1px solid var(--border); color: var(--text-dim); cursor: pointer; transition: all 0.2s; }
  .speed-btn.active { background: var(--elevated); border-color: var(--cyan); color: var(--cyan); }
  .live-progress-box { margin-bottom: 20px; background: rgba(4,7,16,0.92); border: 1px solid rgba(0,212,255,0.3); border-radius: var(--r-md); padding: 16px 20px; display: none; }
  .completion-celebration-card { display: none; margin-top: 24px; background: linear-gradient(135deg, rgba(3,15,20,0.96) 0%, rgba(10,25,30,0.96) 100%); border: 2px solid #00FF66; border-radius: var(--r-md); padding: 28px 32px; box-shadow: 0 0 40px rgba(0,255,102,0.2); margin-bottom: 24px; }
"""

PRIMER_HTML = """
    <!-- 10-Second Concept Primer for Beginners -->
    <div class="primer-box ai">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:14px;">
        <div style="display:flex;align-items:center;gap:10px;">
          <span style="font-size:24px;">💡</span>
          <span style="font-family:var(--font-fm);font-size:13px;font-weight:800;color:var(--cyan);letter-spacing:0.12em;text-transform:uppercase;">How Autonomous Agent Chains Work (In 10 Seconds)</span>
        </div>
        <span style="font-family:var(--font-fm);font-size:11px;color:var(--cyan);background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.25);padding:3px 10px;border-radius:100px;">Beginner's Guide</span>
      </div>
      <p style="font-size:14px;line-height:1.65;color:var(--text-body);margin-bottom:18px;">
        Think of an <strong style="color:var(--text-strong)">Autonomous Agent Chain</strong> like an Olympic relay team. Instead of asking one slow AI bot to do everything, eight specialized AI agents work together—each doing one specific job with verified precision, then passing the baton in milliseconds.
      </p>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;">
        <div style="background:rgba(6,7,12,0.7);border:1px solid var(--border);border-radius:var(--r-md);padding:14px 16px;">
          <div style="font-size:16px;font-weight:800;color:var(--text-strong);margin-bottom:6px;">🎯 1. The Trigger</div>
          <p style="font-size:12.5px;line-height:1.55;color:var(--text-dim);margin:0;">A customer phone call, web lead, freight exception, or cybersecurity event arrives in real time.</p>
        </div>
        <div style="background:rgba(6,7,12,0.7);border:1px solid var(--border);border-radius:var(--r-md);padding:14px 16px;">
          <div style="font-size:16px;font-weight:800;color:var(--text-strong);margin-bottom:6px;">🏃‍♂️ 2. The AI Relay Race</div>
          <p style="font-size:12.5px;line-height:1.55;color:var(--text-dim);margin:0;">Specialist AI agents verify, research, route, and execute without waiting on humans.</p>
        </div>
        <div style="background:rgba(6,7,12,0.7);border:1px solid var(--border);border-radius:var(--r-md);padding:14px 16px;">
          <div style="font-size:16px;font-weight:800;color:var(--text-strong);margin-bottom:6px;">🏆 3. Instant Outcome</div>
          <p style="font-size:12.5px;line-height:1.55;color:var(--text-dim);margin:0;">Work is finished in ~2.4 seconds with zero errors, zero dropped tasks, and verified compliance.</p>
        </div>
      </div>
    </div>

    <!-- Category Filter Chips -->
    <div class="category-filter-chips ai">
      <button class="cat-chip active" onclick="filterCategory('all', this)">🌐 All Scenarios (24)</button>
      <button class="cat-chip" onclick="filterCategory('beginner', this)">⭐ Beginner Favorites</button>
      <button class="cat-chip" onclick="filterCategory('sales', this)">💼 Sales &amp; Growth</button>
      <button class="cat-chip" onclick="filterCategory('security', this)">🛡️ Security &amp; Privacy</button>
      <button class="cat-chip" onclick="filterCategory('it', this)">⚙️ IT &amp; Systems</button>
      <button class="cat-chip" onclick="filterCategory('finance', this)">💰 Finance &amp; Legal</button>
    </div>
"""

STORY_CARD_HTML = """
    <!-- Active Mission & Story Card -->
    <div id="active-story-card" class="active-story-card ai"></div>
"""

def update_index():
    with open(os.path.join(WORKSPACE, "index.html"), "r", encoding="utf-8") as f:
        idx_content = f.read()

    if "/* ─── SIMPLIFIED AGENT CHAIN STYLING" not in idx_content:
        idx_content = idx_content.replace("</style>", CSS_BLOCK + "\n</style>", 1)

    if '<div class="primer-box' not in idx_content:
        idx_content = idx_content.replace('<div class="demo-tabs ai">', PRIMER_HTML + '\n    <div class="demo-tabs ai">')

    if '<div id="active-story-card"' not in idx_content:
        idx_content = idx_content.replace('    <div class="demo-container ai">', STORY_CARD_HTML + '\n    <div class="demo-container ai">')

    controls_pattern = re.compile(r'<div class="demo-controls">.*?</div>', re.DOTALL)
    new_controls = """
      <!-- Action Controls -->
      <div class="demo-controls" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:22px;">
        <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
          <button id="run-demo-btn" onclick="runDemoGraph()" class="btn btn-p" style="font-size:14px;padding:12px 24px;font-weight:800;box-shadow:0 0 20px var(--cyan-glow);">▶️ Start Live Chain Simulation</button>
          <button id="step-demo-btn" onclick="stepDemoGraph()" class="btn btn-o" style="font-size:13px;padding:10px 18px;font-weight:700;">⏭️ Step-by-Step Mode (Learn)</button>
          <button id="reset-demo-btn" onclick="resetDemoGraph()" class="btn btn-o" style="font-size:13px;padding:10px 16px;">🔄 Reset</button>
        </div>
        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
          <div style="display:flex;align-items:center;gap:4px;background:rgba(6,7,12,0.8);border:1px solid var(--border);border-radius:8px;padding:4px 8px;">
            <span style="font-family:var(--font-fm);font-size:10.5px;color:var(--text-dim);margin-right:4px;">SPEED:</span>
            <button class="speed-btn" onclick="setSpeed(0.5, this)" title="Slow speed for learning">🐢 0.5x</button>
            <button class="speed-btn active" onclick="setSpeed(1, this)" title="Normal speed">⚡ 1x</button>
            <button class="speed-btn" onclick="setSpeed(2, this)" title="Fast speed">🚀 2x</button>
          </div>
          <button id="view-mode-toggle-btn" onclick="toggleViewMode()" class="btn btn-o" style="font-size:12px;padding:8px 14px;font-family:var(--font-fm);">💡 Plain English View</button>
          <button id="copy-demo-payload-btn" onclick="copyDemoPayload()" class="btn btn-o" style="font-size:12px;padding:8px 14px;">📋 Copy Telemetry</button>
        </div>
      </div>

      <!-- Live Dynamic Storyteller & Progress Bar -->
      <div id="live-progress-box" class="live-progress-box">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
          <span id="live-storyteller-title" style="font-family:var(--font-fm);font-size:12px;font-weight:800;color:var(--cyan);letter-spacing:0.08em;text-transform:uppercase;">⚡ AGENTS COLLABORATING LIVE IN REAL TIME</span>
          <span id="live-progress-pct" style="font-family:var(--font-fm);font-size:12px;font-weight:800;color:var(--magenta);">0%</span>
        </div>
        <div style="width:100%;height:6px;background:rgba(255,255,255,0.08);border-radius:100px;overflow:hidden;margin-bottom:10px;">
          <div id="live-progress-bar-fill" style="width:0%;height:100%;background:linear-gradient(90deg,var(--cyan),var(--magenta));transition:width 0.25s ease;border-radius:100px;"></div>
        </div>
        <div id="live-storyteller-caption" style="font-size:13.5px;color:var(--text-strong);line-height:1.5;font-weight:600;">
          Initializing multi-agent graph...
        </div>
      </div>
"""
    if controls_pattern.search(idx_content):
        idx_content = controls_pattern.sub(new_controls, idx_content, count=1)

    if '<div id="completion-celebration-card"' not in idx_content:
        idx_content = idx_content.replace('<div class="demo-status-bar">', '<!-- Completion Celebration Card -->\n      <div id="completion-celebration-card" class="completion-celebration-card"></div>\n      <div class="demo-status-bar">')

    # Replace JavaScript engine in index.html
    js_start = idx_content.find("const demoScenarios = {")
    js_end = idx_content.find("/* ── EXECUTIVE BRIEFING VIDEO CANVAS SCRIPT ── */")
    if js_start != -1 and js_end != -1:
        js_replacement = f"""
window.SCENARIOS_DATA = {json.dumps(SCENARIOS_DATA, indent=2)};
let currentDemoScenario = 'receptionist';
let currentDemoKey = 'receptionist';
let isRunning = false;
let isStepMode = false;
let currentStepIdx = 0;
let simulationSpeed = 1.0;
let isDevView = false;
let currentCategory = 'all';
let simTimer = null;

function filterCategory(cat, btn) {{
  currentCategory = cat;
  document.querySelectorAll('.cat-chip').forEach(c => c.classList.remove('active'));
  if (btn) btn.classList.add('active');

  const tabs = document.querySelectorAll('.demo-tab');
  let firstVisible = null;
  tabs.forEach(tab => {{
    const key = tab.getAttribute('data-key') || tab.getAttribute('onclick')?.match(/['"]([^'"]+)['"]/)?.[1];
    if (!key) return;
    tab.setAttribute('data-key', key);
    const meta = window.SCENARIOS_DATA[key];
    const match = (cat === 'all') || (meta && meta.category === cat);
    if (match) {{
      tab.style.display = 'inline-block';
      if (!firstVisible) firstVisible = tab;
    }} else {{
      tab.style.display = 'none';
    }}
  }});

  const activeTab = document.querySelector('.demo-tab.active');
  if (activeTab && activeTab.style.display === 'none' && firstVisible) {{
    firstVisible.click();
  }}
}}

function switchDemo(key, btn) {{
  if (isRunning) resetDemoGraph();
  currentDemoKey = key;
  currentDemoScenario = key;

  document.querySelectorAll('.demo-tab').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  else {{
    const target = document.querySelector(`.demo-tab[data-key="${{key}}"]`);
    if (target) target.classList.add('active');
  }}

  renderActiveStoryCard();
  renderDemoRows();
  updatePayloadHeader();

  const statusBar = document.getElementById('demo-status-bar-text');
  if (statusBar) statusBar.textContent = 'Idle - press Start Live Chain Simulation to trigger the agents.';

  const celebCard = document.getElementById('completion-celebration-card');
  if (celebCard) celebCard.style.display = 'none';

  const progressBox = document.getElementById('live-progress-box');
  if (progressBox) progressBox.style.display = 'none';
}}

function updatePayloadHeader() {{
  const meta = window.SCENARIOS_DATA[currentDemoKey] || {{}};
  const pType = document.getElementById('demo-payload-type');
  const pText = document.getElementById('demo-payload-text');
  if (pType) pType.textContent = `LIVE INBOUND SIGNAL — ${{meta.techName || currentDemoKey.toUpperCase()}}`;
  if (pText) pText.textContent = `INBOUND EVENT: "${{meta.friendlyProblem || 'Inbound trigger received.'}}"`;
}}

function renderActiveStoryCard() {{
  const card = document.getElementById('active-story-card');
  if (!card) return;
  const data = window.SCENARIOS_DATA[currentDemoKey];
  if (!data) return;

  card.innerHTML = `
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:14px;">
      <div style="display:flex;align-items:center;gap:12px;">
        <span style="font-size:32px;background:rgba(0,212,255,0.1);padding:8px 12px;border-radius:12px;border:1px solid rgba(0,212,255,0.3);">${{data.icon}}</span>
        <div>
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
            <span style="font-family:var(--font-fm);font-size:15px;font-weight:800;color:var(--text-strong);">${{data.friendlyName}}</span>
            <span style="font-family:var(--font-fm);font-size:10px;color:var(--cyan);background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.3);padding:2px 8px;border-radius:100px;">${{data.badge}}</span>
          </div>
          <div style="font-family:var(--font-fm);font-size:11.5px;color:var(--text-dim);">${{data.techName}} · 8 Autonomous Specialist Nodes</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:12px;font-family:var(--font-fm);font-size:11px;">
        <span style="color:var(--cyan);background:rgba(0,212,255,0.06);padding:6px 12px;border-radius:6px;border:1px solid rgba(0,212,255,0.2);">⏱️ Duration: ~2.4s</span>
        <span style="color:#00FF66;background:rgba(0,255,102,0.06);padding:6px 12px;border-radius:6px;border:1px solid rgba(0,255,102,0.2);">🛡️ RAM Enclave ZDR</span>
      </div>
    </div>

    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-bottom:16px;">
      <div style="background:rgba(255,50,75,0.06);border:1px solid rgba(255,50,75,0.25);border-radius:var(--r-md);padding:14px 18px;">
        <div style="font-family:var(--font-fm);font-size:11px;font-weight:800;color:#FF5252;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:6px;">🚨 The Real-World Problem</div>
        <p style="font-size:13.5px;line-height:1.55;color:var(--text-strong);margin:0;">${{data.friendlyProblem}}</p>
      </div>

      <div style="background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.25);border-radius:var(--r-md);padding:14px 18px;">
        <div style="font-family:var(--font-fm);font-size:11px;font-weight:800;color:var(--cyan);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:6px;">🤖 The Autonomous AI Mission</div>
        <p style="font-size:13.5px;line-height:1.55;color:var(--text-strong);margin:0;">${{data.friendlyGoal}}</p>
      </div>
    </div>

    <div style="background:rgba(0,0,0,0.35);border:1px solid var(--border);border-radius:var(--r-md);padding:12px 16px;display:flex;align-items:center;gap:10px;">
      <span style="font-size:18px;">💡</span>
      <div style="font-size:12.5px;line-height:1.5;color:var(--text-body);">
        <strong style="color:var(--cyan)">Why This Is Revolutionary:</strong> ${{data.friendlyTakeaway}}
      </div>
    </div>
  `;
}}

function renderDemoRows() {{
  const container = document.getElementById('demo-rows-container');
  if (!container) return;
  const data = window.SCENARIOS_DATA[currentDemoKey];
  if (!data || !data.nodes) return;

  container.innerHTML = '';
  data.nodes.forEach((node, i) => {{
    const row = document.createElement('div');
    row.className = 'demo-row';
    row.id = `demo-node-${{i}}`;
    row.style.cssText = 'background:var(--elevated);border:1px solid var(--border);border-radius:var(--r-md);padding:14px 18px;margin-bottom:10px;display:grid;grid-template-columns:clamp(60px,8vw,80px) 1fr auto;gap:14px;align-items:center;transition:all .3s ease;';

    if (isDevView) {{
      row.innerHTML = `
        <div style="font-family:var(--font-fm);font-size:12px;font-weight:800;color:var(--cyan)">NODE 0${{i+1}}</div>
        <div>
          <div style="font-family:var(--font-fm);font-size:13px;font-weight:700;color:var(--text-strong);margin-bottom:4px">${{node.name}} [LIV: node_0${{i+1}}]</div>
          <div style="font-family:var(--font-fm);font-size:11.5px;color:var(--text-dim);line-height:1.4">${{node.friendlyDesc}}</div>
          <div style="margin-top:6px;font-family:var(--font-fm);font-size:10px;color:var(--magenta)">HMAC: 0x${{(Math.sin(i+1)*10000000).toString(16).slice(0,8).toUpperCase()}} · Tool: ${{node.tools}}</div>
        </div>
        <div id="demo-status-${{i}}" class="node-status-badge" style="font-family:var(--font-fm);font-size:11px;font-weight:800;color:var(--text-dim);text-align:right">⚪ Ready</div>
      `;
    }} else {{
      row.innerHTML = `
        <div style="font-family:var(--font-fm);font-size:12px;font-weight:800;color:var(--cyan);background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.25);padding:6px 10px;border-radius:6px;text-align:center">Step 0${{i+1}}</div>
        <div>
          <div style="font-size:14px;font-weight:800;color:var(--text-strong);margin-bottom:3px">${{node.friendlyTitle}}</div>
          <div style="font-size:12.5px;color:var(--text-body);line-height:1.5">${{node.friendlyDesc}}</div>
          <div style="margin-top:6px;display:flex;align-items:center;gap:6px">
            <span style="font-family:var(--font-fm);font-size:10.5px;color:var(--text-dim);background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:2px 8px;border-radius:4px">🛠️ Tools: ${{node.tools}}</span>
          </div>
        </div>
        <div id="demo-status-${{i}}" class="node-status-badge" style="font-family:var(--font-fm);font-size:11.5px;font-weight:800;color:var(--text-dim);text-align:right">⚪ Ready in Queue</div>
      `;
    }}

    container.appendChild(row);
  }});
}}

function setSpeed(speed, btn) {{
  simulationSpeed = speed;
  document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
}}

function toggleViewMode() {{
  isDevView = !isDevView;
  const btn = document.getElementById('view-mode-toggle-btn');
  if (btn) {{
    btn.textContent = isDevView ? '🧑‍💻 Developer View' : '💡 Plain English View';
  }}
  renderDemoRows();
}}

function runDemoGraph() {{
  if (isRunning) return;
  isRunning = true;
  isStepMode = false;
  currentStepIdx = 0;

  const runBtn = document.getElementById('run-demo-btn');
  const stepBtn = document.getElementById('step-demo-btn');
  if (runBtn) runBtn.disabled = true;
  if (stepBtn) stepBtn.disabled = true;

  const progressBox = document.getElementById('live-progress-box');
  if (progressBox) progressBox.style.display = 'block';

  const celebCard = document.getElementById('completion-celebration-card');
  if (celebCard) celebCard.style.display = 'none';

  executeSimulationStep();
}}

function stepDemoGraph() {{
  if (!isRunning) {{
    isRunning = true;
    isStepMode = true;
    currentStepIdx = 0;
    const progressBox = document.getElementById('live-progress-box');
    if (progressBox) progressBox.style.display = 'block';
    const celebCard = document.getElementById('completion-celebration-card');
    if (celebCard) celebCard.style.display = 'none';
  }}

  const stepBtn = document.getElementById('step-demo-btn');
  if (stepBtn) stepBtn.textContent = '⏭️ Next Agent Step →';

  executeSimulationStep(true);
}}

function executeSimulationStep(isManualStep = false) {{
  const data = window.SCENARIOS_DATA[currentDemoKey];
  if (!data || !data.nodes) return;

  const total = data.nodes.length;

  if (currentStepIdx > 0) {{
    const prevIdx = currentStepIdx - 1;
    const prevRow = document.getElementById(`demo-node-${{prevIdx}}`);
    const prevStatus = document.getElementById(`demo-status-${{prevIdx}}`);
    if (prevRow) {{
      prevRow.style.borderColor = 'rgba(0,255,102,0.4)';
      prevRow.style.background = 'rgba(0,255,102,0.04)';
      prevRow.style.boxShadow = 'none';
    }}
    if (prevStatus) {{
      prevStatus.style.color = '#00FF66';
      prevStatus.textContent = isDevView ? 'PASSED ✓' : '🟢 Done & Handed Off ✓';
    }}
  }}

  if (currentStepIdx < total) {{
    const curIdx = currentStepIdx;
    const node = data.nodes[curIdx];
    const curRow = document.getElementById(`demo-node-${{curIdx}}`);
    const curStatus = document.getElementById(`demo-status-${{curIdx}}`);

    if (curRow) {{
      curRow.style.borderColor = 'var(--cyan)';
      curRow.style.background = 'rgba(0,212,255,0.09)';
      curRow.style.boxShadow = '0 0 24px rgba(0,212,255,0.25)';
      curRow.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
    }}
    if (curStatus) {{
      curStatus.style.color = 'var(--cyan)';
      curStatus.textContent = isDevView ? 'EXECUTING (140ms)...' : '🟡 Working on it...';
    }}

    const pct = Math.round(((curIdx + 1) / total) * 100);
    const fill = document.getElementById('live-progress-bar-fill');
    const pctText = document.getElementById('live-progress-pct');
    const caption = document.getElementById('live-storyteller-caption');

    if (fill) fill.style.width = `${{pct}}%`;
    if (pctText) pctText.textContent = `${{pct}}%`;
    if (caption) {{
      caption.innerHTML = `
        <span style="color:var(--cyan);font-weight:800;">Step ${{curIdx+1}} of ${{total}}:</span>
        ${{node.friendlyDesc}} <span style="color:var(--text-dim);font-size:12px;">(Tools: ${{node.tools}})</span>
      `;
    }}

    const statusBar = document.getElementById('demo-status-bar-text');
    if (statusBar) {{
      statusBar.textContent = `Node 0${{curIdx+1}} Active: ${{node.friendlyTitle}} (Native Mistral Handoff)`;
    }}

    currentStepIdx++;

    if (!isManualStep) {{
      const baseDelay = 420;
      const delay = baseDelay / simulationSpeed;
      simTimer = setTimeout(() => executeSimulationStep(false), delay);
    }}
  }} else {{
    isRunning = false;
    isStepMode = false;
    const runBtn = document.getElementById('run-demo-btn');
    const stepBtn = document.getElementById('step-demo-btn');
    if (runBtn) runBtn.disabled = false;
    if (stepBtn) {{
      stepBtn.disabled = false;
      stepBtn.textContent = '⏭️ Step-by-Step Mode (Learn)';
    }}

    const statusBar = document.getElementById('demo-status-bar-text');
    if (statusBar) {{
      statusBar.textContent = 'Pipeline Complete - All 8 Nodes Executed & Synchronized Cleanly (0 Errors).';
    }}

    const caption = document.getElementById('live-storyteller-caption');
    if (caption) {{
      caption.innerHTML = `
        <span style="color:#00FF66;font-weight:800;">🎉 Mission Accomplished!</span> All 8 specialist agents finished the workflow in ~2.1s with 100% verified accuracy.
      `;
    }}

    showCelebrationCard();
  }}
}}

function showCelebrationCard() {{
  const card = document.getElementById('completion-celebration-card');
  if (!card) return;
  const data = window.SCENARIOS_DATA[currentDemoKey];
  if (!data) return;

  card.style.display = 'block';
  card.innerHTML = `
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:16px;">
      <span style="font-size:36px;">🎉</span>
      <div>
        <div style="font-family:var(--font-fm);font-size:18px;font-weight:900;color:#00FF66;letter-spacing:0.04em;">
          Mission Complete: ${{data.friendlyName}} Finished!
        </div>
        <div style="font-size:13px;color:var(--text-body);">
          All 8 autonomous specialist agents executed in <strong>2.1 seconds</strong> with zero errors and zero manual human delay.
        </div>
      </div>
    </div>

    <div style="background:rgba(6,7,12,0.8);border:1px solid rgba(0,255,102,0.3);border-radius:var(--r-md);padding:18px 22px;margin-bottom:20px;">
      <div style="font-family:var(--font-fm);font-size:12px;font-weight:800;color:var(--cyan);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;">
        🧠 What You Just Learned:
      </div>
      <ul style="margin:0;padding-left:20px;font-size:13.5px;line-height:1.7;color:var(--text-strong);">
        <li><strong style="color:var(--cyan)">1. Zero Human Lag:</strong> Traditional business operations require humans to manually copy-paste between CRM, email, Jira, and calendars. Agent chains solve the whole problem in seconds.</li>
        <li><strong style="color:var(--cyan)">2. The Relay Race Baton:</strong> Each specialist agent does one job perfectly, then passes cryptographically verified state directly to the next agent without buggy middleware.</li>
        <li><strong style="color:var(--cyan)">3. 100% Tamper-Proof Audit:</strong> Every action is sealed with post-quantum cryptography and zero data retention for complete security.</li>
      </ul>
    </div>

    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
      <button onclick="randomDemoScenario()" class="btn btn-p" style="font-size:13.5px;padding:10px 20px;font-weight:800;">
        🎲 Try Another Scenario Next →
      </button>
      <a href="/book-a-demo-contact/" class="btn btn-o" style="font-size:13px;padding:10px 18px;border-color:var(--cyan);color:var(--cyan);">
        📅 Book a 90-Min Architecture Audit ↗
      </a>
    </div>
  `;
  card.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
}}

function randomDemoScenario() {{
  const keys = Object.keys(window.SCENARIOS_DATA);
  const next = keys[Math.floor(Math.random() * keys.length)];
  switchDemo(next);
  const storyCard = document.getElementById('active-story-card');
  if (storyCard) storyCard.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
}}

function resetDemoGraph() {{
  if (simTimer) clearTimeout(simTimer);
  isRunning = false;
  isStepMode = false;
  currentStepIdx = 0;

  const runBtn = document.getElementById('run-demo-btn');
  const stepBtn = document.getElementById('step-demo-btn');
  if (runBtn) runBtn.disabled = false;
  if (stepBtn) {{
    stepBtn.disabled = false;
    stepBtn.textContent = '⏭️ Step-by-Step Mode (Learn)';
  }}

  const progressBox = document.getElementById('live-progress-box');
  if (progressBox) progressBox.style.display = 'none';

  const celebCard = document.getElementById('completion-celebration-card');
  if (celebCard) celebCard.style.display = 'none';

  renderDemoRows();

  const statusBar = document.getElementById('demo-status-bar-text');
  if (statusBar) statusBar.textContent = 'Idle - press Start Live Chain Simulation to trigger the agents.';
}}

window.copyDemoPayload = function() {{
  const data = window.SCENARIOS_DATA[currentDemoKey] || {{}};
  const payloadData = {{
    scenario_key: currentDemoKey,
    friendly_name: data.friendlyName,
    problem: data.friendlyProblem,
    mission: data.friendlyGoal,
    nodes: data.nodes,
    timestamp: new Date().toISOString(),
    hmac_signature: "0x9F41A82C" + Math.floor(Math.random()*900000 + 100000).toString(16).toUpperCase()
  }};
  navigator.clipboard.writeText(JSON.stringify(payloadData, null, 2)).then(() => {{
    const btn = document.getElementById('copy-demo-payload-btn');
    if (btn) {{
      const orig = btn.innerText;
      btn.innerText = 'Copied to Clipboard! ✓';
      setTimeout(() => {{ btn.innerText = orig; }}, 2000);
    }}
  }});
}};

document.addEventListener('DOMContentLoaded', function() {{
  document.querySelectorAll('.demo-tab').forEach(tab => {{
    const key = tab.getAttribute('onclick')?.match(/['"]([^'"]+)['"]/)?.[1];
    if (key) tab.setAttribute('data-key', key);
  }});
  renderActiveStoryCard();
  renderDemoRows();
}});
if (document.readyState === 'interactive' || document.readyState === 'complete') {{
  document.querySelectorAll('.demo-tab').forEach(tab => {{
    const key = tab.getAttribute('onclick')?.match(/['"]([^'"]+)['"]/)?.[1];
    if (key) tab.setAttribute('data-key', key);
  }});
  renderActiveStoryCard();
  renderDemoRows();
}}
"""
        idx_content = idx_content[:js_start] + js_replacement + "\n" + idx_content[js_end:]

    with open(os.path.join(WORKSPACE, "index.html"), "w", encoding="utf-8") as f:
        f.write(idx_content)
    print("index.html structure updated.")

def update_demo():
    with open(os.path.join(WORKSPACE, "demo", "index.html"), "r", encoding="utf-8") as f:
        demo_content = f.read()

    if "/* ─── SIMPLIFIED AGENT CHAIN STYLING" not in demo_content:
        demo_content = demo_content.replace("</style>", CSS_BLOCK + "\n</style>", 1)

    if '<div class="primer-box' not in demo_content:
        demo_content = demo_content.replace('<div class="demo-tabs">', PRIMER_HTML + '\n    <div class="demo-tabs">')

    if '<div id="active-story-card"' not in demo_content:
        demo_content = demo_content.replace('    <div class="demo-container">', STORY_CARD_HTML + '\n    <div class="demo-container">')

    controls_pattern = re.compile(r'<div class="demo-controls">.*?</div>', re.DOTALL)
    demo_controls = """
      <!-- Action Controls -->
      <div class="demo-controls" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:22px;">
        <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
          <button id="run-demo-btn" onclick="runDemoGraph()" class="btn btn-p" style="font-size:14px;padding:12px 24px;font-weight:800;box-shadow:0 0 20px var(--cyan-glow);">▶️ Start Live Chain Simulation</button>
          <button id="step-demo-btn" onclick="stepDemoGraph()" class="btn btn-o" style="font-size:13px;padding:10px 18px;font-weight:700;">⏭️ Step-by-Step Mode (Learn)</button>
          <button id="reset-demo-btn" onclick="resetDemoGraph()" class="btn btn-o" style="font-size:13px;padding:10px 16px;">🔄 Reset</button>
        </div>
        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
          <div style="display:flex;align-items:center;gap:4px;background:rgba(6,7,12,0.8);border:1px solid var(--border);border-radius:8px;padding:4px 8px;">
            <span style="font-family:var(--font-fm);font-size:10.5px;color:var(--text-dim);margin-right:4px;">SPEED:</span>
            <button class="speed-btn" onclick="setSpeed(0.5, this)" title="Slow speed for learning">🐢 0.5x</button>
            <button class="speed-btn active" onclick="setSpeed(1, this)" title="Normal speed">⚡ 1x</button>
            <button class="speed-btn" onclick="setSpeed(2, this)" title="Fast speed">🚀 2x</button>
          </div>
          <button id="view-mode-toggle-btn" onclick="toggleViewMode()" class="btn btn-o" style="font-size:12px;padding:8px 14px;font-family:var(--font-fm);">💡 Plain English View</button>
          <button id="toggle-view-btn" onclick="toggleDagCanvasView()" class="btn btn-o" style="font-size:12px;padding:8px 14px;">View: DAG Graph 🌐</button>
          <button id="download-pipeline-yaml-btn" onclick="downloadPipelineYaml()" class="btn btn-o" style="font-size:12px;padding:8px 14px;">Export YAML ⚡</button>
          <button id="copy-demo-payload-btn" onclick="copyDemoPayload()" class="btn btn-o" style="font-size:12px;padding:8px 14px;">📋 Copy Telemetry</button>
        </div>
      </div>

      <!-- Live Dynamic Storyteller & Progress Bar -->
      <div id="live-progress-box" class="live-progress-box">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
          <span id="live-storyteller-title" style="font-family:var(--font-fm);font-size:12px;font-weight:800;color:var(--cyan);letter-spacing:0.08em;text-transform:uppercase;">⚡ AGENTS COLLABORATING LIVE IN REAL TIME</span>
          <span id="live-progress-pct" style="font-family:var(--font-fm);font-size:12px;font-weight:800;color:var(--magenta);">0%</span>
        </div>
        <div style="width:100%;height:6px;background:rgba(255,255,255,0.08);border-radius:100px;overflow:hidden;margin-bottom:10px;">
          <div id="live-progress-bar-fill" style="width:0%;height:100%;background:linear-gradient(90deg,var(--cyan),var(--magenta));transition:width 0.25s ease;border-radius:100px;"></div>
        </div>
        <div id="live-storyteller-caption" style="font-size:13.5px;color:var(--text-strong);line-height:1.5;font-weight:600;">
          Initializing multi-agent graph...
        </div>
      </div>
"""
    if controls_pattern.search(demo_content):
        demo_content = controls_pattern.sub(demo_controls, demo_content, count=1)

    if '<div id="completion-celebration-card"' not in demo_content:
        demo_content = demo_content.replace('<div class="demo-status-bar">', '<!-- Completion Celebration Card -->\n      <div id="completion-celebration-card" class="completion-celebration-card"></div>\n      <div class="demo-status-bar">')

    scenarios_start = demo_content.find("const scenarios = {")
    footer_script_end = demo_content.rfind("</script>")
    if scenarios_start != -1 and footer_script_end != -1:
        demo_js = f"""
window.SCENARIOS_DATA = {json.dumps(SCENARIOS_DATA, indent=2)};
let currentScenarioKey = 'receptionist';
let currentDemoKey = 'receptionist';
let isRunning = false;
let isStepMode = false;
let currentStepIdx = 0;
let simulationSpeed = 1.0;
let isDevView = false;
let currentCategory = 'all';
let simTimer = null;
let dagCanvasVisible = false;

function filterCategory(cat, btn) {{
  currentCategory = cat;
  document.querySelectorAll('.cat-chip').forEach(c => c.classList.remove('active'));
  if (btn) btn.classList.add('active');

  const tabs = document.querySelectorAll('.demo-tab');
  let firstVisible = null;
  tabs.forEach(tab => {{
    const key = tab.getAttribute('data-key') || tab.getAttribute('onclick')?.match(/['"]([^'"]+)['"]/)?.[1];
    if (!key) return;
    tab.setAttribute('data-key', key);
    const meta = window.SCENARIOS_DATA[key];
    const match = (cat === 'all') || (meta && meta.category === cat);
    if (match) {{
      tab.style.display = 'inline-block';
      if (!firstVisible) firstVisible = tab;
    }} else {{
      tab.style.display = 'none';
    }}
  }});

  const activeTab = document.querySelector('.demo-tab.active');
  if (activeTab && activeTab.style.display === 'none' && firstVisible) {{
    firstVisible.click();
  }}
}}

function switchDemo(key, btn) {{
  if (isRunning) resetDemoGraph();
  currentScenarioKey = key;
  currentDemoKey = key;

  document.querySelectorAll('.demo-tab').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  else {{
    const target = document.querySelector(`.demo-tab[data-key="${{key}}"]`);
    if (target) target.classList.add('active');
  }}

  renderActiveStoryCard();
  renderDemoRows();
  updatePayloadHeader();
  renderSpecDrawer();
  if (dagCanvasVisible) renderDagCanvas();

  const statusBar = document.getElementById('demo-status-bar-text');
  if (statusBar) statusBar.textContent = 'Idle - press Start Live Chain Simulation to trigger the agents.';

  const celebCard = document.getElementById('completion-celebration-card');
  if (celebCard) celebCard.style.display = 'none';

  const progressBox = document.getElementById('live-progress-box');
  if (progressBox) progressBox.style.display = 'none';
}}

function updatePayloadHeader() {{
  const meta = window.SCENARIOS_DATA[currentDemoKey] || {{}};
  const pType = document.getElementById('demo-payload-type');
  const pText = document.getElementById('demo-payload-text');
  if (pType) pType.textContent = `LIVE INBOUND SIGNAL — ${{meta.techName || currentDemoKey.toUpperCase()}}`;
  if (pText) pText.textContent = `INBOUND EVENT: "${{meta.friendlyProblem || 'Inbound trigger received.'}}"`;
}}

function renderActiveStoryCard() {{
  const card = document.getElementById('active-story-card');
  if (!card) return;
  const data = window.SCENARIOS_DATA[currentDemoKey];
  if (!data) return;

  card.innerHTML = `
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:14px;">
      <div style="display:flex;align-items:center;gap:12px;">
        <span style="font-size:32px;background:rgba(0,212,255,0.1);padding:8px 12px;border-radius:12px;border:1px solid rgba(0,212,255,0.3);">${{data.icon}}</span>
        <div>
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
            <span style="font-family:var(--font-fm);font-size:15px;font-weight:800;color:var(--text-strong);">${{data.friendlyName}}</span>
            <span style="font-family:var(--font-fm);font-size:10px;color:var(--cyan);background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.3);padding:2px 8px;border-radius:100px;">${{data.badge}}</span>
          </div>
          <div style="font-family:var(--font-fm);font-size:11.5px;color:var(--text-dim);">${{data.techName}} · 8 Autonomous Specialist Nodes</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:12px;font-family:var(--font-fm);font-size:11px;">
        <span style="color:var(--cyan);background:rgba(0,212,255,0.06);padding:6px 12px;border-radius:6px;border:1px solid rgba(0,212,255,0.2);">⏱️ Duration: ~2.4s</span>
        <span style="color:#00FF66;background:rgba(0,255,102,0.06);padding:6px 12px;border-radius:6px;border:1px solid rgba(0,255,102,0.2);">🛡️ RAM Enclave ZDR</span>
      </div>
    </div>

    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin-bottom:16px;">
      <div style="background:rgba(255,50,75,0.06);border:1px solid rgba(255,50,75,0.25);border-radius:var(--r-md);padding:14px 18px;">
        <div style="font-family:var(--font-fm);font-size:11px;font-weight:800;color:#FF5252;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:6px;">🚨 The Real-World Problem</div>
        <p style="font-size:13.5px;line-height:1.55;color:var(--text-strong);margin:0;">${{data.friendlyProblem}}</p>
      </div>

      <div style="background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.25);border-radius:var(--r-md);padding:14px 18px;">
        <div style="font-family:var(--font-fm);font-size:11px;font-weight:800;color:var(--cyan);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:6px;">🤖 The Autonomous AI Mission</div>
        <p style="font-size:13.5px;line-height:1.55;color:var(--text-strong);margin:0;">${{data.friendlyGoal}}</p>
      </div>
    </div>

    <div style="background:rgba(0,0,0,0.35);border:1px solid var(--border);border-radius:var(--r-md);padding:12px 16px;display:flex;align-items:center;gap:10px;">
      <span style="font-size:18px;">💡</span>
      <div style="font-size:12.5px;line-height:1.5;color:var(--text-body);">
        <strong style="color:var(--cyan)">Why This Is Revolutionary:</strong> ${{data.friendlyTakeaway}}
      </div>
    </div>
  `;
}}

function renderDemoRows() {{
  const container = document.getElementById('demo-rows-container');
  if (!container) return;
  const data = window.SCENARIOS_DATA[currentDemoKey];
  if (!data || !data.nodes) return;

  container.innerHTML = '';
  data.nodes.forEach((node, i) => {{
    const row = document.createElement('div');
    row.className = 'demo-row';
    row.id = `demo-node-${{i}}`;
    row.style.cssText = 'background:var(--elevated);border:1px solid var(--border);border-radius:var(--r-md);padding:14px 18px;margin-bottom:10px;display:grid;grid-template-columns:clamp(60px,8vw,80px) 1fr auto;gap:14px;align-items:center;transition:all .3s ease;';

    if (isDevView) {{
      row.innerHTML = `
        <div style="font-family:var(--font-fm);font-size:12px;font-weight:800;color:var(--cyan)">NODE 0${{i+1}}</div>
        <div>
          <div style="font-family:var(--font-fm);font-size:13px;font-weight:700;color:var(--text-strong);margin-bottom:4px">${{node.name}} [LIV: node_0${{i+1}}]</div>
          <div style="font-family:var(--font-fm);font-size:11.5px;color:var(--text-dim);line-height:1.4">${{node.friendlyDesc}}</div>
          <div style="margin-top:6px;font-family:var(--font-fm);font-size:10px;color:var(--magenta)">HMAC: 0x${{(Math.sin(i+1)*10000000).toString(16).slice(0,8).toUpperCase()}} · Tool: ${{node.tools}}</div>
        </div>
        <div id="demo-status-${{i}}" class="node-status-badge" style="font-family:var(--font-fm);font-size:11px;font-weight:800;color:var(--text-dim);text-align:right">⚪ Ready</div>
      `;
    }} else {{
      row.innerHTML = `
        <div style="font-family:var(--font-fm);font-size:12px;font-weight:800;color:var(--cyan);background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.25);padding:6px 10px;border-radius:6px;text-align:center">Step 0${{i+1}}</div>
        <div>
          <div style="font-size:14px;font-weight:800;color:var(--text-strong);margin-bottom:3px">${{node.friendlyTitle}}</div>
          <div style="font-size:12.5px;color:var(--text-body);line-height:1.5">${{node.friendlyDesc}}</div>
          <div style="margin-top:6px;display:flex;align-items:center;gap:6px">
            <span style="font-family:var(--font-fm);font-size:10.5px;color:var(--text-dim);background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:2px 8px;border-radius:4px">🛠️ Tools: ${{node.tools}}</span>
          </div>
        </div>
        <div id="demo-status-${{i}}" class="node-status-badge" style="font-family:var(--font-fm);font-size:11.5px;font-weight:800;color:var(--text-dim);text-align:right">⚪ Ready in Queue</div>
      `;
    }}

    container.appendChild(row);
  }});
}}

function renderSpecDrawer() {{
  const drawerEl = document.getElementById('demo-spec-drawer');
  if (drawerEl && window.agentSpecsData && window.agentSpecsData[currentScenarioKey]) {{
    const spec = window.agentSpecsData[currentScenarioKey];
    drawerEl.innerHTML = `
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;border-bottom:1px solid var(--border);padding-bottom:12px;">
        <div style="display:flex;align-items:center;gap:10px;">
          <div style="width:10px;height:10px;border-radius:50%;background:var(--cyan);box-shadow:0 0 10px var(--cyan);"></div>
          <span style="font-family:var(--font-fm);font-size:14px;font-weight:800;color:var(--cyan);letter-spacing:0.08em;text-transform:uppercase;">${{spec.title || currentScenarioKey}} ARCHITECTURE SPEC</span>
        </div>
        <span style="font-family:var(--font-fm);font-size:11px;color:var(--magenta);background:rgba(224,64,255,0.1);border:1px solid rgba(224,64,255,0.3);padding:3px 8px;border-radius:4px;">LIV RUNTIME READY</span>
      </div>
      <div style="font-size:13.5px;line-height:1.65;color:var(--text-body);margin-bottom:16px;">
        ${{spec.duties || 'Autonomous multi-agent execution pipeline.'}}
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;font-family:var(--font-fm);font-size:11.5px;">
        <div style="background:rgba(3,7,18,0.7);padding:10px 14px;border-radius:6px;border:1px solid var(--border);"><strong style="color:var(--cyan)">Skills:</strong> <span style="color:var(--text-strong)">${{spec.skills || 'N/A'}}</span></div>
        <div style="background:rgba(3,7,18,0.7);padding:10px 14px;border-radius:6px;border:1px solid var(--border);"><strong style="color:var(--cyan)">MCP Connectors:</strong> <span style="color:var(--text-strong)">${{spec.mcp || 'N/A'}}</span></div>
        <div style="background:rgba(3,7,18,0.7);padding:10px 14px;border-radius:6px;border:1px solid var(--border);"><strong style="color:var(--cyan)">Handoff Mode:</strong> <span style="color:#00FF66">${{spec.a2a || 'Mistral Native Handoff'}}</span></div>
        <div style="background:rgba(3,7,18,0.7);padding:10px 14px;border-radius:6px;border:1px solid var(--border);"><strong style="color:var(--cyan)">Security / RBAC:</strong> <span style="color:var(--magenta)">${{spec.rbac || 'Zero-Trust Scoped'}}</span></div>
      </div>
    `;
  }}
}}

function renderDagCanvas() {{
  const wrapper = document.getElementById('dag-svg-wrapper');
  if (!wrapper) return;
  const data = window.SCENARIOS_DATA[currentDemoKey];
  if (!data || !data.nodes) return;

  const total = data.nodes.length;
  let svgHtml = `<svg width="100%" height="300" viewBox="0 0 900 300" xmlns="http://www.w3.org/2000/svg" style="overflow:visible;">`;
  
  const coords = [
    {{ x: 80, y: 70 }}, {{ x: 300, y: 70 }}, {{ x: 520, y: 70 }}, {{ x: 740, y: 70 }},
    {{ x: 740, y: 220 }}, {{ x: 520, y: 220 }}, {{ x: 300, y: 220 }}, {{ x: 80, y: 220 }}
  ];

  for (let i = 0; i < coords.length - 1; i++) {{
    svgHtml += `<line x1="${{coords[i].x}}" y1="${{coords[i].y}}" x2="${{coords[i+1].x}}" y2="${{coords[i+1].y}}" stroke="rgba(0,212,255,0.3)" stroke-width="2" stroke-dasharray="4" id="dag-svg-edge-${{i}}"/>`;
  }}

  data.nodes.forEach((node, i) => {{
    const pt = coords[i];
    svgHtml += `
      <g id="dag-svg-node-${{i}}">
        <rect id="dag-svg-rect-${{i}}" x="${{pt.x - 70}}" y="${{pt.y - 30}}" width="140" height="60" rx="8" fill="rgba(6,7,12,0.9)" stroke="rgba(0,212,255,0.4)" stroke-width="1.5"/>
        <text x="${{pt.x}}" y="${{pt.y - 10}}" fill="#00D4FF" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="bold" text-anchor="middle">NODE 0${{i+1}}</text>
        <text x="${{pt.x}}" y="${{pt.y + 6}}" fill="#FFFFFF" font-family="'Space Grotesk', sans-serif" font-size="11" font-weight="bold" text-anchor="middle">${{node.name}}</text>
        <text id="dag-svg-stat-${{i}}" x="${{pt.x}}" y="${{pt.y + 20}}" fill="#7B8CA4" font-family="'JetBrains Mono', monospace" font-size="9" text-anchor="middle">READY</text>
      </g>
    `;
  }});

  svgHtml += `</svg>`;
  wrapper.innerHTML = svgHtml;
}}

function toggleDagCanvasView() {{
  const container = document.getElementById('demo-dag-canvas-container');
  const btn = document.getElementById('toggle-view-btn');
  if (!container) return;
  dagCanvasVisible = !dagCanvasVisible;
  container.style.display = dagCanvasVisible ? 'block' : 'none';
  if (btn) btn.textContent = dagCanvasVisible ? 'View: Step Cards 📋' : 'View: DAG Graph 🌐';
  if (dagCanvasVisible) renderDagCanvas();
}}

function downloadPipelineYaml() {{
  const data = window.SCENARIOS_DATA[currentDemoKey] || {{}};
  const yamlContent = `apiVersion: pipefish.io/v1alpha1
kind: AgentMeshPipeline
metadata:
  name: pipefish-${{currentDemoKey}}-mesh
  namespace: production
spec:
  scenario: "${{currentDemoKey}}"
  title: "${{data.friendlyName}}"
  handoff_mode: "mistral_native"
  zdr_enclave: true
  nodes:
${{data.nodes.map((n, i) => `    - id: "node-0${{i+1}}"
      title: "${{n.friendlyTitle}}"
      tools: "${{n.tools}}"
      zdr: true`).join('\\n')}}
`;
  const blob = new Blob([yamlContent], {{ type: 'text/yaml' }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `pipefish-${{currentDemoKey}}-pipeline.yaml`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}}

function setSpeed(speed, btn) {{
  simulationSpeed = speed;
  document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
}}

function toggleViewMode() {{
  isDevView = !isDevView;
  const btn = document.getElementById('view-mode-toggle-btn');
  if (btn) {{
    btn.textContent = isDevView ? '🧑‍💻 Developer View' : '💡 Plain English View';
  }}
  renderDemoRows();
}}

function runDemoGraph() {{
  if (isRunning) return;
  isRunning = true;
  isStepMode = false;
  currentStepIdx = 0;

  const runBtn = document.getElementById('run-demo-btn');
  const stepBtn = document.getElementById('step-demo-btn');
  if (runBtn) runBtn.disabled = true;
  if (stepBtn) stepBtn.disabled = true;

  const progressBox = document.getElementById('live-progress-box');
  if (progressBox) progressBox.style.display = 'block';

  const celebCard = document.getElementById('completion-celebration-card');
  if (celebCard) celebCard.style.display = 'none';

  executeSimulationStep();
}}

function stepDemoGraph() {{
  if (!isRunning) {{
    isRunning = true;
    isStepMode = true;
    currentStepIdx = 0;
    const progressBox = document.getElementById('live-progress-box');
    if (progressBox) progressBox.style.display = 'block';
    const celebCard = document.getElementById('completion-celebration-card');
    if (celebCard) celebCard.style.display = 'none';
  }}

  const stepBtn = document.getElementById('step-demo-btn');
  if (stepBtn) stepBtn.textContent = '⏭️ Next Agent Step →';

  executeSimulationStep(true);
}}

function executeSimulationStep(isManualStep = false) {{
  const data = window.SCENARIOS_DATA[currentDemoKey];
  if (!data || !data.nodes) return;

  const total = data.nodes.length;

  if (currentStepIdx > 0) {{
    const prevIdx = currentStepIdx - 1;
    const prevRow = document.getElementById(`demo-node-${{prevIdx}}`);
    const prevStatus = document.getElementById(`demo-status-${{prevIdx}}`);
    if (prevRow) {{
      prevRow.style.borderColor = 'rgba(0,255,102,0.4)';
      prevRow.style.background = 'rgba(0,255,102,0.04)';
      prevRow.style.boxShadow = 'none';
    }}
    if (prevStatus) {{
      prevStatus.style.color = '#00FF66';
      prevStatus.textContent = isDevView ? 'PASSED ✓' : '🟢 Done & Handed Off ✓';
    }}

    const prevSvgRect = document.getElementById(`dag-svg-rect-${{prevIdx}}`);
    const prevSvgStat = document.getElementById(`dag-svg-stat-${{prevIdx}}`);
    if (prevSvgRect) {{
      prevSvgRect.setAttribute('stroke', '#00FF66');
      prevSvgRect.setAttribute('fill', 'rgba(0,255,102,0.12)');
    }}
    if (prevSvgStat) {{
      prevSvgStat.textContent = 'PASSED ✓';
      prevSvgStat.setAttribute('fill', '#00FF66');
    }}
  }}

  if (currentStepIdx < total) {{
    const curIdx = currentStepIdx;
    const node = data.nodes[curIdx];
    const curRow = document.getElementById(`demo-node-${{curIdx}}`);
    const curStatus = document.getElementById(`demo-status-${{curIdx}}`);

    if (curRow) {{
      curRow.style.borderColor = 'var(--cyan)';
      curRow.style.background = 'rgba(0,212,255,0.09)';
      curRow.style.boxShadow = '0 0 24px rgba(0,212,255,0.25)';
      curRow.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
    }}
    if (curStatus) {{
      curStatus.style.color = 'var(--cyan)';
      curStatus.textContent = isDevView ? 'EXECUTING (140ms)...' : '🟡 Working on it...';
    }}

    const curSvgRect = document.getElementById(`dag-svg-rect-${{curIdx}}`);
    const curSvgStat = document.getElementById(`dag-svg-stat-${{curIdx}}`);
    if (curSvgRect) {{
      curSvgRect.setAttribute('stroke', '#00D4FF');
      curSvgRect.setAttribute('fill', 'rgba(0,212,255,0.25)');
    }}
    if (curSvgStat) {{
      curSvgStat.textContent = 'EXECUTING';
      curSvgStat.setAttribute('fill', '#00D4FF');
    }}

    const pct = Math.round(((curIdx + 1) / total) * 100);
    const fill = document.getElementById('live-progress-bar-fill');
    const pctText = document.getElementById('live-progress-pct');
    const caption = document.getElementById('live-storyteller-caption');

    if (fill) fill.style.width = `${{pct}}%`;
    if (pctText) pctText.textContent = `${{pct}}%`;
    if (caption) {{
      caption.innerHTML = `
        <span style="color:var(--cyan);font-weight:800;">Step ${{curIdx+1}} of ${{total}}:</span>
        ${{node.friendlyDesc}} <span style="color:var(--text-dim);font-size:12px;">(Tools: ${{node.tools}})</span>
      `;
    }}

    const statusBar = document.getElementById('demo-status-bar-text');
    if (statusBar) {{
      statusBar.textContent = `Node 0${{curIdx+1}} Active: ${{node.friendlyTitle}} (Native Mistral Handoff)`;
    }}

    currentStepIdx++;

    if (!isManualStep) {{
      const baseDelay = 420;
      const delay = baseDelay / simulationSpeed;
      simTimer = setTimeout(() => executeSimulationStep(false), delay);
    }}
  }} else {{
    isRunning = false;
    isStepMode = false;
    const runBtn = document.getElementById('run-demo-btn');
    const stepBtn = document.getElementById('step-demo-btn');
    if (runBtn) runBtn.disabled = false;
    if (stepBtn) {{
      stepBtn.disabled = false;
      stepBtn.textContent = '⏭️ Step-by-Step Mode (Learn)';
    }}

    const statusBar = document.getElementById('demo-status-bar-text');
    if (statusBar) {{
      statusBar.textContent = 'Pipeline Complete - All 8 Nodes Executed & Synchronized Cleanly (0 Errors).';
    }}

    const caption = document.getElementById('live-storyteller-caption');
    if (caption) {{
      caption.innerHTML = `
        <span style="color:#00FF66;font-weight:800;">🎉 Mission Accomplished!</span> All 8 specialist agents finished the workflow in ~2.1s with 100% verified accuracy.
      `;
    }}

    showCelebrationCard();
  }}
}}

function showCelebrationCard() {{
  const card = document.getElementById('completion-celebration-card');
  if (!card) return;
  const data = window.SCENARIOS_DATA[currentDemoKey];
  if (!data) return;

  card.style.display = 'block';
  card.innerHTML = `
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:16px;">
      <span style="font-size:36px;">🎉</span>
      <div>
        <div style="font-family:var(--font-fm);font-size:18px;font-weight:900;color:#00FF66;letter-spacing:0.04em;">
          Mission Complete: ${{data.friendlyName}} Finished!
        </div>
        <div style="font-size:13px;color:var(--text-body);">
          All 8 autonomous specialist agents executed in <strong>2.1 seconds</strong> with zero errors and zero manual human delay.
        </div>
      </div>
    </div>

    <div style="background:rgba(6,7,12,0.8);border:1px solid rgba(0,255,102,0.3);border-radius:var(--r-md);padding:18px 22px;margin-bottom:20px;">
      <div style="font-family:var(--font-fm);font-size:12px;font-weight:800;color:var(--cyan);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;">
        🧠 What You Just Learned:
      </div>
      <ul style="margin:0;padding-left:20px;font-size:13.5px;line-height:1.7;color:var(--text-strong);">
        <li><strong style="color:var(--cyan)">1. Zero Human Lag:</strong> Traditional business operations require humans to manually copy-paste between CRM, email, Jira, and calendars. Agent chains solve the whole problem in seconds.</li>
        <li><strong style="color:var(--cyan)">2. The Relay Race Baton:</strong> Each specialist agent does one job perfectly, then passes cryptographically verified state directly to the next agent without buggy middleware.</li>
        <li><strong style="color:var(--cyan)">3. 100% Tamper-Proof Audit:</strong> Every action is sealed with post-quantum cryptography and zero data retention for complete security.</li>
      </ul>
    </div>

    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
      <button onclick="randomDemoScenario()" class="btn btn-p" style="font-size:13.5px;padding:10px 20px;font-weight:800;">
        🎲 Try Another Scenario Next →
      </button>
      <a href="/book-a-demo-contact/" class="btn btn-o" style="font-size:13px;padding:10px 18px;border-color:var(--cyan);color:var(--cyan);">
        📅 Book a 90-Min Architecture Audit ↗
      </a>
    </div>
  `;
  card.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
}}

function randomDemoScenario() {{
  const keys = Object.keys(window.SCENARIOS_DATA);
  const next = keys[Math.floor(Math.random() * keys.length)];
  switchDemo(next);
  const storyCard = document.getElementById('active-story-card');
  if (storyCard) storyCard.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
}}

function resetDemoGraph() {{
  if (simTimer) clearTimeout(simTimer);
  isRunning = false;
  isStepMode = false;
  currentStepIdx = 0;

  const runBtn = document.getElementById('run-demo-btn');
  const stepBtn = document.getElementById('step-demo-btn');
  if (runBtn) runBtn.disabled = false;
  if (stepBtn) {{
    stepBtn.disabled = false;
    stepBtn.textContent = '⏭️ Step-by-Step Mode (Learn)';
  }}

  const progressBox = document.getElementById('live-progress-box');
  if (progressBox) progressBox.style.display = 'none';

  const celebCard = document.getElementById('completion-celebration-card');
  if (celebCard) celebCard.style.display = 'none';

  renderDemoRows();
  if (dagCanvasVisible) renderDagCanvas();

  const statusBar = document.getElementById('demo-status-bar-text');
  if (statusBar) statusBar.textContent = 'Idle - press Start Live Chain Simulation to trigger the agents.';
}}

window.copyDemoPayload = function() {{
  const data = window.SCENARIOS_DATA[currentDemoKey] || {{}};
  const payloadData = {{
    scenario_key: currentDemoKey,
    friendly_name: data.friendlyName,
    problem: data.friendlyProblem,
    mission: data.friendlyGoal,
    nodes: data.nodes,
    timestamp: new Date().toISOString(),
    hmac_signature: "0x9F41A82C" + Math.floor(Math.random()*900000 + 100000).toString(16).toUpperCase()
  }};
  navigator.clipboard.writeText(JSON.stringify(payloadData, null, 2)).then(() => {{
    const btn = document.getElementById('copy-demo-payload-btn');
    if (btn) {{
      const orig = btn.innerText;
      btn.innerText = 'Copied to Clipboard! ✓';
      setTimeout(() => {{ btn.innerText = orig; }}, 2000);
    }}
  }});
}};

document.addEventListener('DOMContentLoaded', function() {{
  document.querySelectorAll('.demo-tab').forEach(tab => {{
    const key = tab.getAttribute('onclick')?.match(/['"]([^'"]+)['"]/)?.[1];
    if (key) tab.setAttribute('data-key', key);
  }});
  renderActiveStoryCard();
  renderDemoRows();
  renderSpecDrawer();
}});
if (document.readyState === 'interactive' || document.readyState === 'complete') {{
  document.querySelectorAll('.demo-tab').forEach(tab => {{
    const key = tab.getAttribute('onclick')?.match(/['"]([^'"]+)['"]/)?.[1];
    if (key) tab.setAttribute('data-key', key);
  }});
  renderActiveStoryCard();
  renderDemoRows();
  renderSpecDrawer();
}}
"""
        demo_content = demo_content[:scenarios_start] + demo_js + "\n" + demo_content[footer_script_end:]

    with open(os.path.join(WORKSPACE, "demo", "index.html"), "w", encoding="utf-8") as f:
        f.write(demo_content)
    print("demo/index.html updated successfully.")

update_index()
update_demo()
print("All pages successfully upgraded with simplified educational Agent Chain simulator.")
