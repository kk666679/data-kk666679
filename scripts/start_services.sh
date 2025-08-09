#!/bin/bash

echo "🚀 Starting HRMS Malaysia v2.0 Services..."

# Start main services
docker-compose up -d postgres redis backend frontend

# Start monitoring and AI interfaces
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d streamlit gradio prometheus

echo "✅ Services started:"
echo "   - API: http://localhost:8000"
echo "   - Frontend: http://localhost:3000"
echo "   - Dashboard: http://localhost:8501"
echo "   - AI Interface: http://localhost:7860"
echo "   - Monitoring: http://localhost:9090"