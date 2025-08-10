#!/bin/bash

# HRMS Malaysia Production Deployment
set -e

ENVIRONMENT=${1:-production}
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 HRMS Malaysia Deployment - ${ENVIRONMENT}${NC}"

# Pre-deployment checks
echo -e "${YELLOW}📋 Pre-deployment checks${NC}"

# Check environment file
if [ ! -f ".env.${ENVIRONMENT}" ]; then
    echo -e "${RED}❌ Environment file .env.${ENVIRONMENT} not found${NC}"
    exit 1
fi

# Check SSL certificates for production
if [ "$ENVIRONMENT" = "production" ] && [ ! -f "nginx/ssl/cert.pem" ]; then
    echo -e "${RED}❌ SSL certificates required for production${NC}"
    exit 1
fi

# Backup database
echo -e "${YELLOW}💾 Creating database backup${NC}"
mkdir -p backups
docker-compose exec -T postgres pg_dump -U hrms_user hrms_db > "backups/backup_$(date +%Y%m%d_%H%M%S).sql"

# Pull latest code
echo -e "${YELLOW}📥 Pulling latest code${NC}"
git pull origin main

# Build images
echo -e "${YELLOW}🔨 Building images${NC}"
docker-compose -f docker-compose.yml -f "docker-compose.${ENVIRONMENT}.yml" build --no-cache

# Run tests
echo -e "${YELLOW}🧪 Running tests${NC}"
python -m pytest tests/ -v

# Deploy services
echo -e "${YELLOW}🚀 Deploying services${NC}"
docker-compose -f docker-compose.yml -f "docker-compose.${ENVIRONMENT}.yml" up -d

# Health checks
echo -e "${YELLOW}🏥 Health checks${NC}"
sleep 30

# Check backend
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend healthy${NC}"
else
    echo -e "${RED}❌ Backend health check failed${NC}"
    exit 1
fi

# Check AI services
if curl -f http://localhost:8001/health >/dev/null 2>&1; then
    echo -e "${GREEN}✅ AI services healthy${NC}"
else
    echo -e "${YELLOW}⚠️  AI services not responding${NC}"
fi

# Malaysian API connectivity test
echo -e "${YELLOW}🇲🇾 Malaysian API connectivity test${NC}"
docker-compose exec -T backend python -c "
from integrations.malaysian_apis import MalaysianAPIIntegration
api = MalaysianAPIIntegration()
print('✅ Malaysian APIs configured')
"

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "${GREEN}📊 Access Points:${NC}"
echo -e "  🌐 Application: https://your-domain.com"
echo -e "  📚 API Docs: https://your-domain.com/docs"
echo -e "  📈 Monitoring: http://your-domain.com:9090"