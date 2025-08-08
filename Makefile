# Makefile for ApexHire AI Resume Screener

.PHONY: install setup test run web clean help

# Default target
help:
	@echo "🚀 ApexHire - AI Resume Screener"
	@echo "================================"
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make setup      - Run complete setup"
	@echo "  make test       - Run tests"
	@echo "  make run        - Run main pipeline"
	@echo "  make web        - Launch web interface"
	@echo "  make clean      - Clean temporary files"
	@echo "  make help       - Show this help"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# Complete setup
setup:
	@echo "🚀 Setting up ApexHire..."
	python setup.py
	@echo "✅ Setup completed"

# Run tests
test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v
	@echo "✅ Tests completed"

# Run main pipeline
run:
	@echo "🔍 Running AI Resume Screener..."
	python src/main_pipeline.py

# Launch web interface
web:
	@echo "🌐 Launching web interface..."
	streamlit run app/main.py

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete
	@echo "✅ Clean completed"

# Install development dependencies
dev-install:
	@echo "🔧 Installing development dependencies..."
	pip install -r requirements.txt
	pip install pytest black flake8
	@echo "✅ Development dependencies installed"

# Format code
format:
	@echo "🎨 Formatting code..."
	black src/ app/ tests/
	@echo "✅ Code formatted"

# Lint code
lint:
	@echo "🔍 Linting code..."
	flake8 src/ app/ tests/
	@echo "✅ Code linted"
