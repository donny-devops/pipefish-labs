#!/usr/bin/env node
/**
 * PipeFish Labs - Live Edge Verification Script (Node.js)
 *
 * Verifies all 9 live production edge endpoints at https://pipefishlabs.io.
 * Pure Node.js using native fetch.
 */

const base = 'https://pipefishlabs.io';

export async function testEndpoints() {
  console.log(`Testing live PipeFish Cloudflare edge deployment at ${base} ...\n`);

  // 1. API Docs
  const res1 = await fetch(`${base}/api-docs/`, { headers: { 'User-Agent': 'PipeFishVerifier/1.0' } });
  const body1 = await res1.text();
  if (res1.status !== 200) throw new Error(`1. Expected 200, got ${res1.status}`);
  if (!body1.toLowerCase().includes('scalar')) throw new Error('Scalar not found in /api-docs/');
  console.log(`[PASS] 1. GET  /api-docs/                    -> HTTP ${res1.status} (Scalar UI rendered, ${body1.length} bytes)`);

  // 2. Trust Center
  const res2 = await fetch(`${base}/trust/`, { headers: { 'User-Agent': 'PipeFishVerifier/1.0' } });
  const body2 = await res2.text();
  if (res2.status !== 200) throw new Error(`2. Expected 200, got ${res2.status}`);
  if (!body2.includes('Enterprise Trust Center')) throw new Error('Trust Center header missing');
  console.log(`[PASS] 2. GET  /trust/                       -> HTTP ${res2.status} (Trust Center rendered, ${body2.length} bytes)`);

  // 3. Booking / Leads Endpoint
  const leadPayload = JSON.stringify({ name: 'Enterprise Tester', work_email: 'ciso@enterprise.com', tier: 'Growth' });
  const res3 = await fetch(`${base}/api/v1/leads`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'User-Agent': 'PipeFishVerifier/1.0' },
    body: leadPayload,
  });
  const leadResp = await res3.json();
  if (res3.status !== 200) throw new Error(`3. Expected 200, got ${res3.status}`);
  if (leadResp.status !== 'success') throw new Error(`3. Expected status success, got ${leadResp.status}`);
  if (!leadResp.receipt_hash || !leadResp.receipt_hash.startsWith('0x')) throw new Error('receipt_hash missing or malformed');
  console.log(`[PASS] 3. POST /api/v1/leads                 -> HTTP ${res3.status} (Receipt Hash: ${leadResp.receipt_hash.slice(0, 18)}...)`);

  // 4. Twilio Voice Webhook
  const twParams = new URLSearchParams({ From: '+14155552671', CallSid: 'CAtest123' });
  const res4 = await fetch(`${base}/api/v1/webhooks/voice/twilio`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'TwilioProxy/1.1' },
    body: twParams.toString(),
  });
  const twBody = await res4.text();
  if (res4.status !== 200) throw new Error(`4. Expected 200, got ${res4.status}`);
  if (!twBody.includes('<Response>') || !twBody.includes('<Say voice="Polly.Danielle-Neural">')) {
    throw new Error('TwiML XML response malformed');
  }
  console.log(`[PASS] 4. POST /api/v1/webhooks/voice/twilio -> HTTP ${res4.status} (TwiML Voice XML valid)`);

  // 5. Vapi Voice Webhook
  const vapiPayload = JSON.stringify({
    type: 'end-of-call-report',
    call: { customer: { number: '+14155552671' }, transcript: 'Test transcript' },
  });
  const res5 = await fetch(`${base}/api/v1/webhooks/voice/vapi`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'User-Agent': 'VapiWebhook/1.0' },
    body: vapiPayload,
  });
  const vapiResp = await res5.json();
  if (res5.status !== 200) throw new Error(`5. Expected 200, got ${res5.status}`);
  if (!['ACCEPTED', 'ingested'].includes(vapiResp.status)) throw new Error(`Unexpected vapi status: ${vapiResp.status}`);
  console.log(`[PASS] 5. POST /api/v1/webhooks/voice/vapi   -> HTTP ${res5.status} (Carrier: ${vapiResp.carrier}, Status: ${vapiResp.status})`);

  // 6. Status Page UI
  const res6 = await fetch(`${base}/status/`, { headers: { 'User-Agent': 'PipeFishVerifier/1.0' } });
  const statusBody = await res6.text();
  if (res6.status !== 200) throw new Error(`6. Expected 200, got ${res6.status}`);
  if (!statusBody.includes('Live Edge Mesh Status')) throw new Error('Status page title missing');
  console.log(`[PASS] 6. GET  /status/                      -> HTTP ${res6.status} (Status Dashboard rendered, ${statusBody.length} bytes)`);

  // 7. Mesh Status API Endpoint
  const res7 = await fetch(`${base}/api/v1/status`, { headers: { 'User-Agent': 'PipeFishVerifier/1.0' } });
  const apiStatus = await res7.json();
  if (res7.status !== 200) throw new Error(`7. Expected 200, got ${res7.status}`);
  if (apiStatus.status !== 'OPERATIONAL') throw new Error(`Expected OPERATIONAL, got ${apiStatus.status}`);
  if (apiStatus.total_registered_agents !== 26) throw new Error(`Expected 26 agents, got ${apiStatus.total_registered_agents}`);
  console.log(
    `[PASS] 7. GET  /api/v1/status                 -> HTTP ${res7.status} (Mesh: ${apiStatus.status}, Swarms: ${Object.keys(apiStatus.swarms).length}, Agents: ${apiStatus.total_registered_agents})`
  );

  // 8. Chaos Status API Endpoint
  const res8 = await fetch(`${base}/api/v1/chaos/status`, { headers: { 'User-Agent': 'PipeFishVerifier/1.0' } });
  const chaosStatus = await res8.json();
  if (res8.status !== 200) throw new Error(`8. Expected 200, got ${res8.status}`);
  if (chaosStatus.mesh_health !== 'OPERATIONAL') throw new Error(`Expected OPERATIONAL, got ${chaosStatus.mesh_health}`);
  if (chaosStatus.self_healing_engine !== 'ACTIVE') throw new Error(`Expected ACTIVE, got ${chaosStatus.self_healing_engine}`);
  console.log(`[PASS] 8. GET  /api/v1/chaos/status           -> HTTP ${res8.status} (Mesh: ${chaosStatus.mesh_health}, Engine: ${chaosStatus.self_healing_engine})`);

  // 9. Chaos Injection API Endpoint
  const chaosPayload = JSON.stringify({ fault_type: 'packet_loss', target: 'IAD_Edge_PoP' });
  const res9 = await fetch(`${base}/api/v1/chaos/inject`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'User-Agent': 'PipeFishVerifier/1.0' },
    body: chaosPayload,
  });
  const chaosInject = await res9.json();
  if (res9.status !== 200) throw new Error(`9. Expected 200, got ${res9.status}`);
  if (chaosInject.status !== 'CHAOS_INJECTED') throw new Error(`Expected CHAOS_INJECTED, got ${chaosInject.status}`);
  if (chaosInject.mesh_status !== 'SELF_HEALED') throw new Error(`Expected SELF_HEALED, got ${chaosInject.mesh_status}`);
  console.log(
    `[PASS] 9. POST /api/v1/chaos/inject           -> HTTP ${res9.status} (Fault: ${chaosInject.fault_type}, Failover: ${chaosInject.ebpf_reroute.failover_latency_ms}ms, Status: ${chaosInject.mesh_status})`
  );

  console.log('\nALL 9 LIVE PRODUCTION EDGE ENDPOINTS VERIFIED SUCCESSFULLY!');
}

if (process.argv[1] && process.argv[1].endsWith('verify_live_edge.js')) {
  testEndpoints().catch((err) => {
    console.error('[FAIL]', err.message);
    process.exit(1);
  });
}
