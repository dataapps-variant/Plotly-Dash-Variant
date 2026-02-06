#!/bin/bash
# Setup script for Variant Analytics Dashboard (Dash Version)

echo "Setting up Variant Analytics Dashboard (Dash)..."

# Check Python version
python3 --version || { echo "Python 3 is required"; exit 1; }

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To run the dashboard:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Set environment variables:"
echo "     export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json"
echo "     export GCS_CACHE_BUCKET=your-bucket-name  # Optional"
echo "  3. Run: python app/main.py"
echo "  4. Open http://localhost:8050 in your browser"
echo ""
echo "Demo credentials:"
echo "  Admin: admin / admin123"
echo "  Viewer: viewer / viewer123"
