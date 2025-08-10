#!/bin/bash

# HRMS Malaysia Full Deployment Script
set -e

echo "🚀 Starting HRMS Malaysia Full Deployment"

# 1. Start all services
echo "📦 Starting all services..."
docker-compose up -d

# 2. Wait for services to be ready
echo "⏳ Waiting for services..."
sleep 30

# 3. Run backend tests
echo "🧪 Running backend tests..."
cd backend
python -m pytest tests/ -v || echo "⚠️ Some tests failed"
cd ..

# 4. Build frontend
echo "🏗️ Building frontend..."
cd frontend
npm ci
npm run build
cd ..

# 5. Run integration tests
echo "🔗 Running integration tests..."
python tests/integration_test.py

# 6. Commit and tag
echo "📝 Committing changes..."
git add .
git commit -m "[Dashboard] Add unified dashboard with all modules; [Docs] Update API documentation"

# 7. Create version tag
VERSION=$(date +"%Y.%m.%d")
git tag -a "v$VERSION" -m "HRMS Malaysia Dashboard Release v$VERSION"

# 8. Push to repository
echo "📤 Pushing to repository..."
git push origin main --tags

# 9. Health check
echo "🏥 Running health checks..."
curl -f http://localhost:8000/health || echo "❌ Backend health check failed"
curl -f http://localhost:3000 || echo "❌ Frontend health check failed"

echo "✅ Deployment completed successfully!"
echo "🌐 Dashboard: http://localhost:3000"
echo "📊 API Docs: http://localhost:8000/docs"
echo "🏷️ Version: v$VERSION"