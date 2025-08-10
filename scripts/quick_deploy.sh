#!/bin/bash

# Quick HRMS Malaysia Deployment (Development Mode)
set -e

echo "🚀 Quick HRMS Malaysia Deployment"

# Start minimal services
echo "🏗️ Starting core services..."
docker-compose up -d postgres redis

# Wait for database
echo "⏳ Waiting for database..."
sleep 10

# Start backend in development mode
echo "🔧 Starting backend..."
cd backend
pip install -r requirements.txt > /dev/null 2>&1 || echo "Dependencies already installed"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend
sleep 5

# Run tests
echo "🧪 Running integration tests..."
python tests/integration_test.py

# Cleanup
echo "🧹 Cleaning up..."
kill $BACKEND_PID 2>/dev/null || true
docker-compose down

echo "✅ Deployment test completed!"