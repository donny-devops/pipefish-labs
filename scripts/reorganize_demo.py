#!/usr/bin/env python3
"""
scripts/reorganize_demo.py
Eliminates all black space in the demo section, repositions the interactive simulator
to the top of .demo-container, adds Agent 26 (LLMOps & Prompt Evaluation Agent),
and wires up category filter chips and active story card.
"""

import re
import sys
import shutil

INDEX_PATH = 'index.html'

def main():
    print("[1] Reading index.html...")
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Backup
    shutil.copyfile(INDEX_PATH, INDEX_PATH + '.bak')

    # 1. Update <style> to guarantee zero opacity/visibility bugs
    style_patch = """
    #demo, #demo .demo-container, #demo .demo-payload-box, #demo .ai {
      opacity: 1 !important;
      transform: none !important;
      visibility: visible !important;
      transition: none !important;
    }
    #active-story-card:empty {
      display: none !important;
    }
"""
    if '#active-story-card:empty' not in content:
        content = content.replace('.hero-logo-col { display: none !important; }',
                                  '.hero-logo-col { display: none !important; }' + style_patch)
        print("  -> Injected instant-visibility CSS rules into <style>.")

    # 2. Fix primer-box, category-filter-chips, demo-tabs, active-story-card, demo-container classes
    content = content.replace('<div class="primer-box ai">', '<div class="primer-box">')
    content = content.replace('<div class="category-filter-chips ai">', '<div class="category-filter-chips">')
    content = content.replace('🌐 All Scenarios (25)', '🌐 All Scenarios (26)')
    content = content.replace('<div class="demo-tabs ai">', '<div class="demo-tabs">')
    content = content.replace('<div id="active-story-card" class="active-story-card ai"></div>',
                              '<div id="active-story-card" class="active-story-card"></div>')
    content = content.replace('<div class="demo-container ai">', '<div class="demo-container">')

    # 3. Add Agent 26 tab if not present
    llmops_tab = '<button class="demo-tab" onclick="switchDemo(\'llmops\', this)">LLMOps &amp; Prompt Evaluation Agent</button>'
    if "switchDemo('llmops'" not in content:
        missed_call_tab = '<button class="demo-tab" onclick="switchDemo(\'missedcalltextback\', this)">Missed Call / Text Back Agent</button>'
        content = content.replace(missed_call_tab, missed_call_tab + '\n      ' + llmops_tab)
        print("  -> Added Agent 26 demo tab.")

    # 4. Extract Interactive Simulator and Payload/Agent Cards blocks inside .demo-container
    # Boundary markers:
    # Payload starts: <!-- Inbound Payload Display -->
    # Controls starts: <!-- Action Controls -->
    # Voice ends: </div>\n    </div>\n  </div>\n</section>

    marker_payload = '<!-- Inbound Payload Display -->'
    marker_controls = '<!-- Action Controls -->'
    marker_demo_end = '</section>\n\n<div class="divider"></div>\n\n<!-- ─── PROBLEM ─── -->'

    pos_payload = content.find(marker_payload)
    pos_controls = content.find(marker_controls)
    pos_demo_end = content.find(marker_demo_end)

    if pos_payload != -1 and pos_controls != -1 and pos_controls > pos_payload:
        print("  -> Extracting sections inside .demo-container...")
        # Payload block: from pos_payload to pos_controls
        payload_and_cards = content[pos_payload:pos_controls].strip()
        
        # Interactive block: from pos_controls to the closing tags of .demo-container
        # Notice that before pos_demo_end there are closing </div> tags:
        # </div> (closes demo-container)
        # </div> (closes container)
        # </section>
        
        # Find closing </div> of demo-container before pos_demo_end
        sub_content = content[pos_controls:pos_demo_end]
        # The last </div></div> in sub_content closes .demo-container and .container
        last_div_idx = sub_content.rfind('</div>\n  </div>')
        if last_div_idx != -1:
            interactive_block = sub_content[:last_div_idx].strip()
            closing_tags = sub_content[last_div_idx:]
            
            # Add Agent Card 26 to payload_and_cards if not present
            if '26 — LLMOps &amp; Prompt Evaluation Agent' not in payload_and_cards:
                agent_26_card = '''
            <!-- 26: LLMOps & Prompt Evaluation Agent -->
            <div class="agent-grid-card" style="background:rgba(12,14,24,0.85);border:1px solid var(--border-strong);border-radius:var(--r-md);padding:20px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 4px 20px rgba(0,0,0,0.25);transition:transform .25s,border-color .25s">
              <div>
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
                  <span style="font-family:var(--font-mono);font-size:13.5px;font-weight:800;color:var(--cyan);letter-spacing:0.04em">26 — LLMOps &amp; Prompt Evaluation Agent</span>
                  <span style="font-family:var(--font-mono);font-size:10px;color:var(--cyan);background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.25);padding:2px 7px;border-radius:4px">NODE 26</span>
                </div>
                <div style="font-family:var(--font-display);font-size:13px;font-weight:700;color:var(--magenta);margin-bottom:10px;line-height:1.35">Continuous Prompt Evaluation, Semantic Drift Detection &amp; Canary Benchmark Router</div>
                <p style="font-size:12.5px;line-height:1.6;color:var(--text-body);margin-bottom:14px">Continuously tests prompt templates against golden ground-truth evaluation suites, detects semantic drift and hallucination rate anomalies, benchmarks latency and cost across frontier models (Gemini 2.5 Flash, Mistral Large, Claude 3.7 Sonnet), and dynamically routes traffic to the optimal model while blocking regressions in CI/CD.</p>
                <table style="width:100%;border-collapse:collapse;font-size:11px;font-family:var(--font-mono);margin-bottom:14px;background:rgba(3,7,18,0.6);border-radius:4px;overflow:hidden">
                  <tbody>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05)"><td style="padding:5px 8px;color:var(--text-dim);font-weight:600;width:38%">Domain</td><td style="padding:5px 8px;color:var(--text-strong);font-weight:700">AI-INFRA · SRE</td></tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05)"><td style="padding:5px 8px;color:var(--text-dim);font-weight:600;width:38%">Trigger</td><td style="padding:5px 8px;color:var(--text-strong);font-weight:700">EVENT-DRIVEN · CI/CD WEBHOOK · TELEMETRY STREAM</td></tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05)"><td style="padding:5px 8px;color:var(--text-dim);font-weight:600;width:38%">I/O Mode</td><td style="padding:5px 8px;color:var(--text-strong);font-weight:700">EVALUATE → BENCHMARK → ROUTE</td></tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05)"><td style="padding:5px 8px;color:var(--text-dim);font-weight:600;width:38%">Channel</td><td style="padding:5px 8px;color:var(--text-strong);font-weight:700">DSPY · FRONTIER LLMS · GITHUB ACTIONS · PROMETHEUS</td></tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.05)"><td style="padding:5px 8px;color:var(--text-dim);font-weight:600;width:38%">Sub-Agents</td><td style="padding:5px 8px;color:var(--text-strong);font-weight:700">PROMPT INGESTOR · DRIFT ANALYZER · BENCHMARKER · PARETO ROUTER</td></tr>
                    <tr><td style="padding:5px 8px;color:var(--text-dim);font-weight:600;width:38%">Latency Target</td><td style="padding:5px 8px;color:var(--text-strong);font-weight:700">&lt; 180ms (Drift Scoring) · &lt; 2.5s (Canary Eval)</td></tr>
                  </tbody>
                </table>
              </div>
              <div style="background:rgba(3,7,18,0.75);border:1px solid rgba(0,212,255,0.15);border-radius:6px;padding:10px 12px;font-size:11.5px;line-height:1.55;font-family:var(--font-mono)">
                <div style="margin-bottom:6px"><strong style="color:var(--cyan)">Consumes:</strong> <span style="color:var(--text-body)">Prompt template, golden evaluation test suite, model output completions, RAG retrieval context, cost/latency budget thresholds, prior benchmark baseline</span></div>
                <div><strong style="color:var(--magenta)">Emits:</strong> <span style="color:var(--text-strong)">Semantic drift score, hallucination/groundedness index, Pareto optimal routing directive, DSPy prompt patch candidate, CI/CD PR status check seal, OpenTelemetry trace payload</span></div>
              </div>
            </div>
'''
                # Insert right before the last 3 closing divs in payload_and_cards
                # The end of payload_and_cards has:
                # </div>\n          </div>\n        </div>\n      </div>
                last_cards_end = payload_and_cards.rfind('</div>\n            </div>\n          </div>')
                if last_cards_end != -1:
                    insert_pos = last_cards_end + len('</div>\n            </div>')
                    payload_and_cards = payload_and_cards[:insert_pos] + '\n' + agent_26_card + payload_and_cards[insert_pos:]
                    print("  -> Inserted Agent Card 26 into agent grid.")

            # Construct new demo-container body: INTERACTIVE FIRST, THEN PAYLOAD & AGENT CARDS
            reorganized_inner = f"""
      {interactive_block}

      <div style="margin-top:40px;margin-bottom:30px;border-top:1px dashed rgba(0,212,255,0.25);"></div>

      {payload_and_cards}
      {closing_tags}"""

            # Splice back into content
            content = content[:pos_payload] + reorganized_inner + content[pos_demo_end:]
            print("  -> Repositioned interactive simulator to the TOP of .demo-container.")
        else:
            print("  [WARN] Could not find closing tags before pos_demo_end.")
    else:
        print("  [WARN] Could not locate payload or controls markers in content.")

    # 5. Add llmops to window.agentSpecsData
    llmops_spec = '''"llmops": {"title": "LLMOps & Prompt Evaluation Agent", "duties": "The LLMOps & Prompt Evaluation Agent continuously monitors, evaluates, and optimizes enterprise prompt templates and model routing:<br><br>• Continuous Evaluation & Drift Detection: Automatically evaluates prompt outputs against golden ground-truth datasets, flagging semantic drift before users experience degradation.<br>• Hallucination Rate Verification: Computes RAG groundedness, answer relevance, and context faithfulness scores to maintain zero-hallucination standards.<br>• Canary Benchmark Routing: Benchmarks latency, quality, and token costs across frontier models (Gemini 2.5 Flash, Mistral Large, Claude 3.7 Sonnet) to dynamically route traffic.<br>• Automated Prompt Patching: Employs autonomous reflection and DSPy optimization loops to mutate failing prompts and verify patches before deployment.<br>• CI/CD Quality Gatekeeping: Integrates directly with GitHub Actions to block breaking prompt changes from merging to production without human intervention.", "skills": "prompt-evaluation-engine, semantic-drift-detector, hallucination-verifier, canary-benchmark-router, dspy-optimizer, model-cost-router, git-pr-gatekeeper", "mcp": "mcp-server-llmops-evals, mcp-server-dspy, mcp-server-langsmith, mcp-server-github-actions", "webhooks": "https://api.pipefishlabs.io/v1/webhooks/llmops-eval-trigger | mailhook://evals@pipefishlabs.io", "secrets": "LangSmith API Key, DSPy Master Key, Frontier Model Provider API Keys (Vault KV v2)", "apis": "DSPy Optimizer API, LangSmith REST API, Gemini API, Mistral AI API, Anthropic API, GitHub Actions API", "a2a": "Mistral Native Handoff (Prompt Ingestion → Semantic Drift Run → Multi-Model Canary Benchmark → Pareto Router → CI/CD Seal)", "rbac": "Role: LLMOpsEvaluatorBot | Perms: prompt.evaluate, eval.benchmark, model.route, ci.gate_check"}, '''
    
    if '"llmops":' not in content:
        content = content.replace('window.agentSpecsData = {', 'window.agentSpecsData = {' + llmops_spec)
        print("  -> Added llmops to window.agentSpecsData.")

    # 6. Add llmops to demoScenarios
    llmops_scenario = '''
  llmops: {
    payload: 'LLMOPS EVALUATION TRIGGER - "Evaluate prompt template enterprise_system_prompt_v2 across golden evaluation test suite (2,400 runs). Benchmark latency, semantic drift, hallucination rate, and compute cost across Gemini 2.5 Flash, Mistral Large, and Claude 3.7 Sonnet."',
    channel: 'Channels Enabled: DSPy Teleprompter · Braintrust API · LangSmith · OpenTelemetry Tracing · GitHub Actions CI · HuggingFace Evals · Litellm',
    nodes: [
      { n: '01', name: 'Prompt Template Ingestion Agent', sub: '(Golden Dataset)', status: 'awaiting upstream signal…' },
      { n: '02', name: 'Semantic Drift & Cosine Distance Engine', sub: '(Vector Embeddings)', status: 'awaiting upstream signal…' },
      { n: '03', name: 'Hallucination & Groundedness Verifier', sub: '(DSPy / RAG Triad)', status: 'awaiting upstream signal…' },
      { n: '04', name: 'Multi-Model Canary Benchmark Runner', sub: '(Gemini / Mistral / Claude)', status: 'awaiting upstream signal…' },
      { n: '05', name: 'Cost & Latency Pareto Frontier Router', sub: '(Token Optimization)', status: 'awaiting upstream signal…' },
      { n: '06', name: 'Automated Prompt Patch & Refine Agent', sub: '(Self-Improving Loop)', status: 'awaiting upstream signal…' },
      { n: '07', name: 'CI/CD Gatekeeper & Pull Request Seal', sub: '(GitHub Actions / Git Hook)', status: 'awaiting upstream signal…' },
      { n: '08', name: 'Zero-Retention Eval Attestation Verifier', sub: '(Cryptographic Proof)', status: 'awaiting upstream signal…' }
    ]
  },'''

    if 'llmops:' not in content:
        content = content.replace('missedcalltextback: {', 'llmops: {' + llmops_scenario.split('llmops: {')[1] + '\n  missedcalltextback: {')
        print("  -> Added llmops to demoScenarios.")

    # 7. Add filterCategory and activeStoryCard render logic if not present
    filter_script = '''
window.agentCategoryMap = {
  receptionist: 'beginner',
  sales: 'sales',
  logistics: 'beginner',
  integration: 'it',
  quantum: 'security',
  reverse: 'security',
  crypto: 'security',
  errorcorr: 'it',
  trend: 'sales',
  market: 'finance',
  codescan: 'security',
  docs: 'it',
  observability: 'it',
  revops: 'sales',
  analytics: 'finance',
  auditing: 'finance',
  logtriage: 'it',
  erp: 'finance',
  trafficrouter: 'it',
  networkdispatch: 'it',
  selfimproving: 'it',
  systemoptimizing: 'it',
  finops: 'finance',
  contractintel: 'finance',
  missedcalltextback: 'beginner',
  llmops: 'it'
};

window.filterCategory = function(cat, btn) {
  document.querySelectorAll('.cat-chip').forEach(c => c.classList.remove('active'));
  if (btn) btn.classList.add('active');

  const tabs = document.querySelectorAll('.demo-tab');
  let firstVisible = null;
  tabs.forEach(tab => {
    const onclickStr = tab.getAttribute('onclick') || '';
    const m = onclickStr.match(/['"]([^'"]+)['"]/);
    const key = m ? m[1] : '';
    if (!key) return;

    let match = (cat === 'all');
    if (!match && window.agentCategoryMap) {
      match = (window.agentCategoryMap[key] === cat);
    }
    if (match) {
      tab.style.display = 'inline-block';
      if (!firstVisible) firstVisible = tab;
    } else {
      tab.style.display = 'none';
    }
  });

  const activeTab = document.querySelector('.demo-tab.active');
  if (activeTab && activeTab.style.display === 'none' && firstVisible) {
    firstVisible.click();
  }
};

function renderActiveStoryCard(key) {
  const card = document.getElementById('active-story-card');
  if (!card) return;
  const spec = (window.agentSpecsData && window.agentSpecsData[key]) || null;
  if (!spec) {
    card.style.display = 'none';
    return;
  }
  card.style.display = 'block';
  card.innerHTML = `
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:12px;">
      <div style="display:flex;align-items:center;gap:10px;">
        <span style="font-size:26px;">⚡</span>
        <div>
          <div style="font-family:var(--font-fm);font-size:14.5px;font-weight:800;color:var(--text-strong);">${spec.title}</div>
          <div style="font-family:var(--font-fm);font-size:11px;color:var(--cyan);margin-top:2px;">8-Node Asynchronous Chain · Native Mistral Handoffs · RAM-Only Enclave</div>
        </div>
      </div>
      <div style="display:flex;gap:8px;font-family:var(--font-fm);font-size:11px;">
        <span style="color:var(--cyan);background:rgba(0,212,255,0.08);padding:4px 10px;border-radius:6px;border:1px solid rgba(0,212,255,0.25);">⏱️ Latency: &lt; 2.5s</span>
        <span style="color:#00FF66;background:rgba(0,255,102,0.08);padding:4px 10px;border-radius:6px;border:1px solid rgba(0,255,102,0.25);">🛡️ 0-Byte Disk Retention</span>
      </div>
    </div>
    <p style="font-size:13px;line-height:1.65;color:var(--text-body);margin:0;">${spec.duties ? spec.duties.split('<br><br>')[0] : 'Autonomous enterprise scenario execution.'}</p>
  `;
}
'''

    if 'window.filterCategory' not in content:
        content = content.replace('function switchDemo(type, btn) {', filter_script + '\nfunction switchDemo(type, btn) {')
        print("  -> Injected filterCategory and renderActiveStoryCard functions.")

    # Call renderActiveStoryCard inside switchDemo
    if 'renderActiveStoryCard(type);' not in content:
        content = content.replace('if (btn) btn.classList.add(\'active\');\n  renderDemoRows();',
                                  'if (btn) btn.classList.add(\'active\');\n  renderActiveStoryCard(type);\n  renderDemoRows();')
        print("  -> Wired renderActiveStoryCard call into switchDemo.")

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[SUCCESS] index.html updated successfully.")

if __name__ == '__main__':
    main()
