#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/artur-carvalho/mestrado/repos/05-cc2vec"
VENV_DIR="${REPO_DIR}/.venv-cc2vec"

echo "=================================================================="
echo "[CC2Vec] Verificando estrutura e ambiente em: ${REPO_DIR}"
echo "=================================================================="

cd "${REPO_DIR}"

if [ ! -d "${VENV_DIR}" ]; then
    echo "[1/3] Criando ambiente virtual isolado ${VENV_DIR} (com --system-site-packages)..."
    python3 -m venv --system-site-packages "${VENV_DIR}"
else
    echo "[1/3] Ambiente virtual ${VENV_DIR} já existe."
fi

source "${VENV_DIR}/bin/activate"

echo "[2/3] Verificando pacotes essenciais (torch, nltk, scikit-learn, numpy, tqdm)..."
pip install --quiet --upgrade pip
pip install --quiet nltk scikit-learn numpy tqdm

echo "[3/3] Validando importação e instanciação das arquiteturas neurais do CC2Vec..."
python3 - << 'EOF'
import argparse
import torch
from jit_cc2ftr_model import WordRNN, SentRNN, HunkRNN, HierachicalRNN
from jit_DExtended_model import DeepJITExtended
from bfp_PNExtended_model import PatchNetExtended

args = argparse.Namespace(
    vocab_code=100, vocab_msg=100, batch_size=2, embed_size=16, embedding_dim=16,
    hidden_size=8, hidden_units=8, class_num=1, dropout_keep_prob=0.5,
    embedding_ftr=52, num_filters=4, filter_sizes=[1, 2]
)
han = HierachicalRNN(args)
dext = DeepJITExtended(args)
print(f"  [OK] PyTorch {torch.__version__} carregado.")
print(f"  [OK] HierachicalRNN (fc1 in_features={han.fc1.in_features}) e DeepJITExtended (fc1 in_features={dext.fc1.in_features}) instanciados com sucesso.")
EOF

echo "=================================================================="
echo "[CC2Vec] Ambiente e modelos neurais validados!"
echo "=================================================================="
