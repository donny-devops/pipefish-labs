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

    print("\nALL 5 LIVE PRODUCTION EDGE ENDPOINTS VERIFIED SUCCESSFULLY!")

if __name__ == '__main__':
    test_endpoints()
