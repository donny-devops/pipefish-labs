import json
import urllib.parse
import urllib.request

base = 'https://pipefishlabs.io'

def test_endpoints():
    print("Testing live PipeFish Cloudflare edge deployment at https://pipefishlabs.io ...\n")

    # 1. API Docs
    req = urllib.request.Request(f'{base}/api-docs/', headers={'User-Agent': 'PipeFishVerifier/1.0'})
    res = urllib.request.urlopen(req, timeout=10)
    body = res.read().decode('utf-8')
    assert res.getcode() == 200, f"Expected 200, got {res.getcode()}"
    assert "Scalar" in body or "scalar" in body, "Scalar not found in /api-docs/"
    print(f"[PASS] 1. GET  /api-docs/                    -> HTTP {res.getcode()} (Scalar UI rendered, {len(body)} bytes)")

    # 2. Trust Center
    req = urllib.request.Request(f'{base}/trust/', headers={'User-Agent': 'PipeFishVerifier/1.0'})
    res = urllib.request.urlopen(req, timeout=10)
    body = res.read().decode('utf-8')
    assert res.getcode() == 200, f"Expected 200, got {res.getcode()}"
    assert "Enterprise Trust Center" in body, "Trust Center header missing"
    print(f"[PASS] 2. GET  /trust/                       -> HTTP {res.getcode()} (Trust Center rendered, {len(body)} bytes)")

    # 3. Booking / Leads Endpoint
    lead_data = json.dumps({'name': 'Enterprise Tester', 'work_email': 'ciso@enterprise.com', 'tier': 'Growth'}).encode('utf-8')
    req = urllib.request.Request(f'{base}/api/v1/leads', data=lead_data, headers={'Content-Type': 'application/json', 'User-Agent': 'PipeFishVerifier/1.0'})
    res = urllib.request.urlopen(req, timeout=10)
    lead_resp = json.loads(res.read().decode('utf-8'))
    assert res.getcode() == 200, f"Expected 200, got {res.getcode()}"
    assert lead_resp.get("status") == "success"
    assert lead_resp.get("receipt_hash", "").startswith("0x"), "receipt_hash missing or malformed"
    print(f"[PASS] 3. POST /api/v1/leads                 -> HTTP {res.getcode()} (Receipt Hash: {lead_resp['receipt_hash'][:18]}...)")

    # 4. Twilio Voice Webhook
    tw_data = urllib.parse.urlencode({'From': '+14155552671', 'CallSid': 'CAtest123'}).encode('utf-8')
    req = urllib.request.Request(f'{base}/api/v1/webhooks/voice/twilio', data=tw_data, headers={'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'TwilioProxy/1.1'})
    res = urllib.request.urlopen(req, timeout=10)
    tw_body = res.read().decode('utf-8')
    assert res.getcode() == 200, f"Expected 200, got {res.getcode()}"
    assert "<Response>" in tw_body and "<Say voice=\"Polly.Danielle-Neural\">" in tw_body, "TwiML XML response malformed"
    print(f"[PASS] 4. POST /api/v1/webhooks/voice/twilio -> HTTP {res.getcode()} (TwiML Voice XML valid)")

    # 5. Vapi Voice Webhook
    vapi_data = json.dumps({'type': 'end-of-call-report', 'call': {'customer': {'number': '+14155552671'}, 'transcript': 'Test transcript'}}).encode('utf-8')
    req = urllib.request.Request(f'{base}/api/v1/webhooks/voice/vapi', data=vapi_data, headers={'Content-Type': 'application/json', 'User-Agent': 'VapiWebhook/1.0'})
    res = urllib.request.urlopen(req, timeout=10)
    vapi_resp = json.loads(res.read().decode('utf-8'))
    assert res.getcode() == 200, f"Expected 200, got {res.getcode()}"
    assert vapi_resp.get("status") in ["ACCEPTED", "ingested"]
    assert vapi_resp.get("carrier") == "vapi_neural_voice"
    print(f"[PASS] 5. POST /api/v1/webhooks/voice/vapi   -> HTTP {res.getcode()} (Carrier: {vapi_resp['carrier']}, Status: {vapi_resp['status']})")

    # 6. Status Page UI
    req = urllib.request.Request(f'{base}/status/', headers={'User-Agent': 'PipeFishVerifier/1.0'})
    res = urllib.request.urlopen(req, timeout=10)
    status_body = res.read().decode('utf-8')
    assert res.getcode() == 200, f"Expected 200, got {res.getcode()}"
    assert "Live Edge Mesh Status" in status_body, "Status page title missing"
    print(f"[PASS] 6. GET  /status/                      -> HTTP {res.getcode()} (Status Dashboard rendered, {len(status_body)} bytes)")

    # 7. Mesh Status API Endpoint
    req = urllib.request.Request(f'{base}/api/v1/status', headers={'User-Agent': 'PipeFishVerifier/1.0'})
    res = urllib.request.urlopen(req, timeout=10)
    api_status = json.loads(res.read().decode('utf-8'))
    assert res.getcode() == 200, f"Expected 200, got {res.getcode()}"
    assert api_status.get("status") == "OPERATIONAL"
    assert api_status.get("total_registered_agents") == 26
    print(f"[PASS] 7. GET  /api/v1/status                 -> HTTP {res.getcode()} (Mesh: {api_status['status']}, Swarms: {len(api_status['swarms'])}, Agents: {api_status['total_registered_agents']})")

    # 8. Chaos Status API Endpoint
    req = urllib.request.Request(f'{base}/api/v1/chaos/status', headers={'User-Agent': 'PipeFishVerifier/1.0'})
    res = urllib.request.urlopen(req, timeout=10)
    chaos_status = json.loads(res.read().decode('utf-8'))
    assert res.getcode() == 200, f"Expected 200, got {res.getcode()}"
    assert chaos_status.get("mesh_health") == "OPERATIONAL"
    assert chaos_status.get("self_healing_engine") == "ACTIVE"
    print(f"[PASS] 8. GET  /api/v1/chaos/status           -> HTTP {res.getcode()} (Mesh: {chaos_status['mesh_health']}, Engine: {chaos_status['self_healing_engine']})")

    # 9. Chaos Injection API Endpoint
    chaos_payload = json.dumps({'fault_type': 'packet_loss', 'target': 'IAD_Edge_PoP'}).encode('utf-8')
    req = urllib.request.Request(f'{base}/api/v1/chaos/inject', data=chaos_payload, headers={'Content-Type': 'application/json', 'User-Agent': 'PipeFishVerifier/1.0'})
    res = urllib.request.urlopen(req, timeout=10)
    chaos_inject = json.loads(res.read().decode('utf-8'))
    assert res.getcode() == 200, f"Expected 200, got {res.getcode()}"
    assert chaos_inject.get("status") == "CHAOS_INJECTED"
    assert chaos_inject.get("mesh_status") == "SELF_HEALED"
    print(f"[PASS] 9. POST /api/v1/chaos/inject           -> HTTP {res.getcode()} (Fault: {chaos_inject['fault_type']}, Failover: {chaos_inject['ebpf_reroute']['failover_latency_ms']}ms, Status: {chaos_inject['mesh_status']})")

    print("\nALL 9 LIVE PRODUCTION EDGE ENDPOINTS VERIFIED SUCCESSFULLY!")

if __name__ == '__main__':
    test_endpoints()
