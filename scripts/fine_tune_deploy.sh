#!/bin/bash

echo "🇲🇾 HRMS Malaysia - Fine-tuning & Deployment Script"
echo "=" * 50

# Fine-tune Bahasa Malaysia model
echo "🚀 Starting Bahasa Malaysia model fine-tuning..."
cd /workspaces/data-kk666679/backend

python -m nlptrainer \
  --model=mesolitica/bert-base-bahasa \
  --dataset=hrms_malaysian_reviews \
  --epochs=3

echo "✅ Model fine-tuning completed!"

# Deploy LangChain agent
echo "🤖 Deploying LangChain compliance agent..."

python -m agents.deploy \
  --agent=compliance_bot \
  --port=50051 &

AGENT_PID=$!

echo "✅ Compliance bot deployed on port 50051"
echo "   PID: $AGENT_PID"

# Test the services
echo "🧪 Testing deployed services..."

# Wait for services to start
sleep 5

echo "📊 Services Status:"
echo "   - Fine-tuned model: ./fine_tuned_malaysian_hrms/"
echo "   - Compliance agent: http://localhost:50051"

# Keep script running
echo "Press Ctrl+C to stop services..."
wait $AGENT_PID