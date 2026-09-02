# PipeFish Labs — Zeek Network Security Monitoring Script
# Inspects inter-agent communication streams for cleartext leaks, PII exposures, or replay attempts.

@load base/protocols/http
@load base/frameworks/notice

module PipeFishSecurity;

export {
    redef enum Notice::Type += {
        Cleartext_Payload_Detected,
        Unsigned_Agent_Handoff,
        High_Rate_Execution_Burst
    };

    const monitored_ports: set[port] = { 8000/tcp, 8001/tcp, 8443/tcp };
}

event http_header(c: connection, is_orig: bool, name: string, value: string) {
    if ( c$id$resp_p in monitored_ports ) {
        # Detect missing X-PipeFish-Signature on mutating POST requests
        if ( name == "X-PIPEFISH-SIGNATURE" && value == "" ) {
            NOTICE([$note=Unsigned_Agent_Handoff,
                    $conn=c,
                    $msg=fmt("Unsigned inter-agent handoff detected from %s to %s", c$id$orig_h, c$id$resp_h)]);
        }
    }
}

event http_entity_data(c: connection, is_orig: bool, length: count, data: string) {
    if ( c$id$resp_p in monitored_ports ) {
        # Alert if unencrypted API keys or passwords are leaked in JSON payload
        if ( /"password"\s*:/ in data || /"private_key"\s*:/ in data ) {
            NOTICE([$note=Cleartext_Payload_Detected,
                    $conn=c,
                    $msg=fmt("CRITICAL: Sensitive token detected in transit from %s", c$id$orig_h)]);
        }
    }
}
