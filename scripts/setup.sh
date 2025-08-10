#!/bin/bash

# HRMS Malaysia Setup Script
set -e

echo "🚀 Setting up HRMS Malaysia..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Setup database
echo "🗄️ Setting up database..."
docker-compose up -d postgres redis
sleep 10

# Initialize database
echo "🔧 Initializing database..."
cd backend
python -c "
from core.database import init_db
init_db()
print('✅ Database initialized')
"
cd ..

# Start services
echo "🏃 Starting all services..."
docker-compose up -d

echo "✅ Setup completed!"
echo "🌐 Access points:"
echo "   - API: http://localhost:8000"
echo "   - Frontend: http://localhost:3000"
echo "   - Docs: http://localhost:8000/docs"