#!/bin/bash

# Email Analysis Service Deployment Script
# This script updates requirements.txt from pyproject.toml and deploys to AWS

set -e  # Exit on any error

echo "🚀 Starting deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if pyproject.toml exists
if [ ! -f "pyproject.toml" ]; then
    print_error "pyproject.toml not found in current directory"
    exit 1
fi

# Check if serverless.yml exists
if [ ! -f "serverless.yml" ]; then
    print_error "serverless.yml not found in current directory"
    exit 1
fi

# Check if serverless is installed
if ! command -v serverless &> /dev/null; then
    print_error "Serverless Framework is not installed. Please install it first:"
    echo "npm install -g serverless"
    exit 1
fi

print_status "Updating requirements.txt from pyproject.toml..."

# Extract dependencies from pyproject.toml and create requirements.txt
# This uses a simple approach to extract dependencies from the [project] section
python3 -c "
import tomllib
import sys

try:
    with open('pyproject.toml', 'rb') as f:
        data = tomllib.load(f)
    
    dependencies = data.get('project', {}).get('dependencies', [])
    
    with open('requirements.txt', 'w') as f:
        for dep in dependencies:
            f.write(f'{dep}\n')
    
    print(f'Updated requirements.txt with {len(dependencies)} dependencies')
    
except Exception as e:
    print(f'Error updating requirements.txt: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    print_success "requirements.txt updated successfully"
else
    print_error "Failed to update requirements.txt"
    exit 1
fi

# Show what's in requirements.txt
print_status "Current dependencies:"
cat requirements.txt

# Check if AWS credentials are configured
print_status "Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    print_warning "AWS credentials not configured or invalid"
    print_warning "Please configure AWS credentials before deployment"
    echo "You can use: aws configure"
    exit 1
fi

print_success "AWS credentials are configured"

# Deploy with serverless
print_status "Deploying to AWS..."
echo "Running: serverless deploy"

if serverless deploy; then
    print_success "Deployment completed successfully! 🎉"
    print_status "Your function is now live on AWS Lambda"
else
    print_error "Deployment failed"
    exit 1
fi

print_status "Deployment process completed"
