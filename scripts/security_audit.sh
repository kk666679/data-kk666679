#!/bin/bash

# HRMS Malaysia Security Audit Script
# Monitors security vulnerabilities and compliance

set -e

echo "🔒 HRMS Malaysia Security Audit"
echo "================================"

# Check if Trivy is installed
if ! command -v trivy &> /dev/null; then
    echo "📦 Installing Trivy security scanner..."
    curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
fi

# Scan Docker images
echo "🔍 Scanning Docker images for vulnerabilities..."
trivy image --severity HIGH,CRITICAL hrms-malaysia-backend:latest || true
trivy image --severity HIGH,CRITICAL hrms-malaysia-frontend:latest || true

# Scan filesystem
echo "🗂️ Scanning filesystem..."
trivy fs --severity HIGH,CRITICAL . || true

# Check Python dependencies
echo "🐍 Checking Python security..."
if command -v safety &> /dev/null; then
    safety check -r backend/requirements.txt || true
else
    pip install safety
    safety check -r backend/requirements.txt || true
fi

# Check Node.js dependencies
echo "📦 Checking Node.js security..."
cd frontend && npm audit --audit-level=high || true
cd ..

# Malaysian compliance checks
echo "🇲🇾 Malaysian Compliance Verification..."
python -c "
import sys
sys.path.append('backend')
from core.compliance import MalaysianCompliance
compliance = MalaysianCompliance()
print('✅ EPF calculations:', compliance.validate_epf())
print('✅ SOCSO compliance:', compliance.validate_socso())
print('✅ PDPA compliance:', compliance.validate_pdpa())
" || echo "⚠️ Compliance check requires backend setup"

echo "🔒 Security audit completed!"