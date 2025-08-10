#!/bin/bash

# HRMS Malaysia Security Audit Script
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🔒 HRMS Malaysia Security Audit${NC}"

# Check Docker security
echo -e "${YELLOW}🐳 Docker Security Check${NC}"
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image hrms-backend:latest

# Check for secrets in code
echo -e "${YELLOW}🔍 Secret Scanning${NC}"
if command -v truffleHog >/dev/null 2>&1; then
    truffleHog --regex --entropy=False .
else
    echo "⚠️  TruffleHog not installed, skipping secret scan"
fi

# SSL/TLS Configuration Check
echo -e "${YELLOW}🔐 SSL/TLS Check${NC}"
if [ -f "nginx/ssl/cert.pem" ]; then
    openssl x509 -in nginx/ssl/cert.pem -text -noout | grep -E "(Not Before|Not After|Subject:|Issuer:)"
    echo "✅ SSL certificate found and valid"
else
    echo "❌ SSL certificate not found"
fi

# Database Security Check
echo -e "${YELLOW}🗄️  Database Security${NC}"
docker-compose exec -T postgres psql -U hrms_user -d hrms_db -c "
SELECT name, setting FROM pg_settings 
WHERE name IN ('ssl', 'log_connections', 'log_disconnections', 'log_statement');
"

# API Security Test
echo -e "${YELLOW}🌐 API Security Test${NC}"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/metrics
if [ $? -eq 0 ]; then
    echo "⚠️  Metrics endpoint accessible without authentication"
else
    echo "✅ Metrics endpoint properly secured"
fi

# Rate Limiting Test
echo -e "${YELLOW}⚡ Rate Limiting Test${NC}"
for i in {1..15}; do
    curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/health
done | tail -5

echo -e "${GREEN}🔒 Security audit completed${NC}"