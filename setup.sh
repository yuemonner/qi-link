#!/bin/bash
# Qi-Link Setup Script

set -e

echo "================================"
echo "Qi-Link Installation Script"
echo "================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Deactivate conda if active
echo "[1/7] Deactivating Conda environment..."
conda deactivate 2>/dev/null || true

# Remove old venv
echo "[2/7] Cleaning old environment..."
rm -rf venv

# Create venv using system Python (avoid Anaconda)
echo "[3/7] Creating virtual environment..."
/usr/bin/python3 -m venv venv

# Activate venv
echo "[4/7] Activating virtual environment..."
source venv/bin/activate

# Verify environment
echo "[5/7] Verifying paths..."
echo "  Python: $(which python)"
echo "  Pip: $(which pip)"

# Upgrade pip
echo "[6/7] Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies (compatible versions)
echo "[7/7] Installing dependencies..."
pip install 'numpy<2' --quiet
pip install 'streamlit>=1.28.0,<1.30.0' --quiet
pip install lunar_python --quiet
pip install openai --quiet
pip install web3 --quiet
pip install psutil --quiet
pip install pydantic pydantic-settings --quiet

echo ""
echo "================================"
echo "Installation Complete"
echo "================================"
echo ""
echo "Python: $(which python)"
echo "Streamlit: $(which streamlit)"
echo ""

# Verify streamlit is in venv
if [[ "$(which streamlit)" == *"/venv/"* ]]; then
    echo "[OK] Streamlit installed in virtual environment"
else
    echo "[WARNING] Streamlit may not be in virtual environment"
fi

echo ""
echo "Starting application..."
echo "================================"
streamlit run app.py --server.headless true
