#!/bin/bash

# ApexHire Deployment Script
# This script deploys the ApexHire AI Resume Screener

set -e

echo "🚀 Starting ApexHire deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

print_status "Python 3 found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt

# Download spaCy model
print_status "Downloading spaCy model..."
python -m spacy download en_core_web_sm

# Create necessary directories
print_status "Creating directories..."
mkdir -p data/resumes data/job_descriptions output logs

# Run tests
print_status "Running tests..."
python -m pytest tests/ -v

# Check if tests passed
if [ $? -eq 0 ]; then
    print_status "All tests passed!"
else
    print_warning "Some tests failed, but continuing deployment..."
fi

# Test the main pipeline
print_status "Testing main pipeline..."
python -c "
from src.main_pipeline import ResumeScreener
screener = ResumeScreener()
status = screener.get_system_status()
print('System status:', status)
"

print_status "✅ Deployment completed successfully!"
print_status "You can now run:"
echo "  - python src/main_pipeline.py (for CLI)"
echo "  - streamlit run app/main.py (for web interface)"
echo "  - python cli.py --help (for command line options)"
