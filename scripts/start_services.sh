#!/bin/bash

# Enhanced HRMS Malaysia deployment script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting HRMS Malaysia v3.0 - AI-Powered HR System${NC}"

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"
command -v docker >/dev/null 2>&1 || { echo -e "${RED}❌ Docker is required but not installed.${NC}" >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo -e "${RED}❌ Docker Compose is required but not installed.${NC}" >&2; exit 1; }

# Check environment file
if [ ! -f .env.production ]; then
    echo -e "${YELLOW}⚠️  Creating .env.production from template...${NC}"
    cp .env.example .env.production
    echo -e "${YELLOW}⚠️  Please update .env.production with your actual values${NC}"
fi

# Create necessary directories
echo -e "${YELLOW}📁 Creating directories...${NC}"
mkdir -p logs nginx/ssl monitoring/data

# Pull latest images
echo -e "${YELLOW}📥 Pulling latest images...${NC}"
docker-compose pull

# Build custom images
echo -e "${YELLOW}🔨 Building custom images...${NC}"
docker-compose build --no-cache

# Start infrastructure services first
echo -e "${YELLOW}🗄️  Starting infrastructure services...${NC}"
docker-compose up -d postgres redis prometheus grafana

# Wait for database to be ready
echo -e "${YELLOW}⏳ Waiting for database to be ready...${NC}"
until docker-compose exec -T postgres pg_isready -U hrms_user -d hrms_db; do
    echo "Waiting for PostgreSQL..."
    sleep 2
done
echo -e "${GREEN}✅ Database is ready${NC}"

# Start AI services
echo -e "${YELLOW}🤖 Starting AI services...${NC}"
docker-compose up -d ai-services

# Wait for AI services to load models
echo -e "${YELLOW}⏳ Waiting for AI models to load...${NC}"
sleep 30

# Start application services
echo -e "${YELLOW}🚀 Starting application services...${NC}"
docker-compose up -d backend frontend nginx

# Health checks
echo -e "${YELLOW}🏥 Performing health checks...${NC}"
sleep 10

# Check backend health
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${RED}❌ Backend health check failed${NC}"
    exit 1
fi

# Check frontend
if curl -f http://localhost:3000 >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is healthy${NC}"
else
    echo -e "${RED}❌ Frontend health check failed${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 All services started successfully!${NC}"
echo -e "${GREEN}📊 Access Points:${NC}"
echo -e "  🌐 Frontend: http://localhost:3000"
echo -e "  🔧 Backend API: http://localhost:8000"
echo -e "  📚 API Docs: http://localhost:8000/docs"
echo -e "  📈 Monitoring: http://localhost:9090 (Prometheus)"
echo -e "  📊 Dashboards: http://localhost:3001 (Grafana)"
echo -e "  🔍 Logs: docker-compose logs -f [service_name]"

echo -e "${YELLOW}💡 Malaysian Features Ready:${NC}"
echo -e "  ✅ EPF/SOCSO Calculations"
echo -e "  ✅ HRDF Claims Processing"
echo -e "  ✅ Multi-language Support (BM/EN/ZH)"
echo -e "  ✅ AI-powered Resume Screening"
echo -e "  ✅ Blockchain Audit Trail"

echo -e "${GREEN}🚀 HRMS Malaysia is ready for production!${NC}"