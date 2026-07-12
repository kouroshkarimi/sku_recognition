#!/usr/bin/env bash
set -e

# -----------------------------
# Configuration
# -----------------------------
ENV1_NAME="cangen"
ENV2_NAME="loma"

ENV1_REQ="envs/retrieval/requirements.txt"
ENV2_REQ="envs/matcher/requirements.txt"


# -----------------------------
# Check Conda
# -----------------------------
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed."
    exit 1
fi

eval "$(conda shell.bash hook)"

# -----------------------------
# Environment 1
# -----------------------------
echo "Creating ${ENV1_NAME}..."

conda create -y -n ${ENV1_NAME} python=3.12.13

conda activate ${ENV1_NAME}

pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121
pip install --upgrade pip
pip install -r ${ENV1_REQ}

conda deactivate

# -----------------------------
# Environment 2
# -----------------------------
echo "Creating ${ENV2_NAME}..."

conda create -y -n ${ENV2_NAME} python=3.9.25

conda activate ${ENV2_NAME}

pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121
pip install --upgrade pip
pip install -r ${ENV2_REQ}

conda deactivate

echo ""
echo "======================================"
echo "Installation completed."
echo ""
echo "Activate with:"
echo "conda activate ${ENV1_NAME}"
echo "or"
echo "conda activate ${ENV2_NAME}"
echo "======================================"