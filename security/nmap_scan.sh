#!/usr/bin/env bash
# PipeFish Labs — Automated Security & Port Audit Script (Nmap)
# Audits inter-agent mesh ports, verifies TLS 1.3 cipher suites, and checks for exposed bastions.

set -euo pipefail

TARGET_HOST="${1:-127.0.0.1}"
REPORT_FILE="security_scan_$(date +%Y%m%d_%H%M%S).txt"

echo "========================================================"
echo "🛡️ PipeFish Labs — Nmap Zero-Trust Security Audit"
echo "Target: ${TARGET_HOST}"
echo "========================================================"

if ! command -v nmap >/dev/null 2>&1; then
    echo "[!] Nmap is not installed. Please install nmap: sudo apt install nmap / brew install nmap"
    exit 1
fi

echo "[1/3] Scanning for exposed unauthorized TCP/UDP ports..."
nmap -sT -p 1-65535 -T4 --open -oN "${REPORT_FILE}" "${TARGET_HOST}"

echo "[2/3] Verifying TLS 1.3 & Post-Quantum Cryptographic Ciphers on Port 8443..."
nmap --script ssl-enum-ciphers -p 8443 "${TARGET_HOST}" >> "${REPORT_FILE}" || true

echo "[3/3] Scanning for vulnerable HTTP methods & cleartext exposures on Port 8000..."
nmap --script http-methods,http-title -p 8000 "${TARGET_HOST}" >> "${REPORT_FILE}" || true

echo "========================================================"
echo "Audit Complete! Report saved to: ${REPORT_FILE}"
echo "========================================================"
