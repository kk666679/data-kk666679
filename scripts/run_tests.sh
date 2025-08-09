#!/bin/bash

echo "Running HRMS Malaysia test suite..."

# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
cd /workspaces/data-kk666679
python -m pytest tests/ -v

echo "Test suite completed."