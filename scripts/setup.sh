#!/bin/bash
# Installation script for WiFi Indoor Positioning

set -e

echo "🔧 WiFi Indoor Positioning - Installation Script"
echo "================================================"

# Check Python version
echo "✓ Checking Python installation..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $PYTHON_VERSION"

# Check Node.js version
echo "✓ Checking Node.js installation..."
NODE_VERSION=$(node --version)
echo "  Found Node.js $NODE_VERSION"

# Create virtual environment
echo "✓ Setting up Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "✓ Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "✓ Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Create directories
echo "✓ Creating necessary directories..."
mkdir -p logs models/checkpoints datasets/{raw,processed,labeled}

# Initialize database
echo "✓ Initializing database..."
cd backend
python3 -c "from database.session import init_db; init_db()"
cd ..

echo ""
echo "✅ Installation complete!"
echo ""
echo "To start development servers:"
echo "  Terminal 1: cd backend && python main.py"
echo "  Terminal 2: cd frontend && npm start"
echo ""
echo "For Docker setup:"
echo "  docker-compose -f docker/docker-compose.yml up -d"
