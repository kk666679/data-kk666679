#!/bin/bash
set -e  # Exit on any error

echo "Running HRMS Malaysia test suite..."

# Install test dependencies
if ! pip install pytest pytest-asyncio; then
    echo "Error: Failed to install test dependencies"
    exit 1
fi

# Run tests
cd /workspaces/data-kk666679
if ! python -m pytest tests/ -v; then
    echo "Error: Tests failed"
    exit 1
fi

echo "Test suite completed successfully."