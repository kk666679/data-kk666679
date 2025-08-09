#!/bin/bash

echo "Setting up HRMS Malaysia development environment..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# Install frontend dependencies
cd frontend
npm install
cd ..

# Copy environment file
cp .env.example .env

echo "Setup complete! Please update .env file with your configuration."
echo "Run 'docker-compose up' to start the development environment."