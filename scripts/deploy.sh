#!/bin/bash

# HRMS Malaysia Production Deployment Script
# Usage: ./scripts/deploy.sh production

set -e

ENVIRONMENT=${1:-staging}
PROJECT_NAME="hrms-malaysia"
VERSION=$(git describe --tags --always)

echo "🚀 Deploying HRMS Malaysia v${VERSION} to ${ENVIRONMENT}"

# Validate environment
if [[ "$ENVIRONMENT" != "production" && "$ENVIRONMENT" != "staging" ]]; then
    echo "❌ Invalid environment. Use 'production' or 'staging'"
    exit 1
fi

# Pre-deployment checks
echo "🔍 Running pre-deployment checks..."
docker --version || { echo "❌ Docker not installed"; exit 1; }
docker-compose --version || { echo "❌ Docker Compose not installed"; exit 1; }

# Build and deploy
echo "🏗️ Building containers..."
docker-compose -f docker-compose.yml -f docker-compose.${ENVIRONMENT}.yml build

echo "🔄 Stopping existing services..."
docker-compose -f docker-compose.yml -f docker-compose.${ENVIRONMENT}.yml down

echo "🚀 Starting services..."
docker-compose -f docker-compose.yml -f docker-compose.${ENVIRONMENT}.yml up -d

# Health checks
echo "🏥 Running health checks..."
sleep 30

# Check API health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is healthy"
else
    echo "❌ Backend API health check failed"
    exit 1
fi

# Check frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo "📊 Access points:"
echo "   - API: http://localhost:8000"
echo "   - Frontend: http://localhost:3000"
echo "   - Monitoring: http://localhost:9090"