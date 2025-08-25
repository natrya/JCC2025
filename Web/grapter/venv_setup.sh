#!/bin/zsh
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Venv ready. Activate with: source .venv/bin/activate"
source .venv/bin/activate

