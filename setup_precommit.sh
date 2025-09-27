#!/bin/bash

# Setup script for pre-commit hooks
echo "Setting up pre-commit hooks for the email analysis project..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: This script must be run from the root of a git repository."
    exit 1
fi

# Install pre-commit if not already installed
echo "Installing pre-commit..."
pip install pre-commit

# Install the pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Run pre-commit on all files to format them
echo "Running pre-commit on all files to format them..."
pre-commit run --all-files

echo "Pre-commit setup complete!"
echo ""
echo "From now on, pre-commit hooks will run automatically before each commit."
echo "To run the hooks manually on all files: pre-commit run --all-files"
echo "To run the hooks on staged files only: pre-commit run"
