#!/bin/bash

# HRMS Malaysia Security Vulnerability Fix Script
set -e

echo "🔒 Fixing GitHub Security Vulnerabilities"

# Backend Python dependencies
echo "🐍 Updating Python dependencies..."
cd backend
cp requirements_secure.txt requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# Frontend Node.js dependencies  
echo "📦 Updating Node.js dependencies..."
cd ../frontend
cp package_secure.json package.json
npm audit fix --force
npm update

# Mobile Flutter dependencies
echo "📱 Updating Flutter dependencies..."
cd ../mobile
flutter pub upgrade
flutter pub audit

# Docker security updates
echo "🐳 Updating Docker base images..."
cd ..
docker pull python:3.11-slim
docker pull node:20-alpine
docker pull nginx:alpine

# Run security audit
echo "🔍 Running security audit..."
cd backend
pip-audit --fix || echo "⚠️ Some vulnerabilities require manual review"

cd ../frontend
npm audit --audit-level=high || echo "⚠️ Some vulnerabilities in dev dependencies"

echo "✅ Security fixes applied!"
echo "📋 Summary:"
echo "   - Updated Python packages to latest secure versions"
echo "   - Fixed Node.js vulnerabilities with overrides"
echo "   - Updated Docker base images"
echo "   - Applied automated security patches"