#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="/home/artur-carvalho/mestrado/repos/06-jit-smart"
JITSMART_DIR="${REPO_ROOT}/jit-smart"
VENV_DIR="${REPO_ROOT}/.venv-jit-smart"

echo "=================================================================="
echo "[JIT-Smart] Verificando estrutura e ambiente em: ${JITSMART_DIR}"
echo "=================================================================="

cd "${JITSMART_DIR}"

if [ ! -d "${VENV_DIR}" ]; then
    echo "[1/4] Criando ambiente virtual isolado ${VENV_DIR} (com --system-site-packages)..."
    python3 -m venv --system-site-packages "${VENV_DIR}"
else
    echo "[1/4] Ambiente virtual ${VENV_DIR} já existe."
fi

source "${VENV_DIR}/bin/activate"

echo "[2/4] Verificando/instalando pacotes essenciais (torch, transformers, scikit-learn, pandas, openpyxl)..."
pip install --quiet --upgrade pip
pip install --quiet transformers scikit-learn pandas numpy tqdm openpyxl

echo "[3/4] Organizando e verificando diretórios de dados (data/jitfine e data/jitsmart)..."
if [ ! -f "${JITSMART_DIR}/data/jitfine/changes_train.pkl" ]; then
    echo "  Descompactando data/data.zip..."
    unzip -q -o "${JITSMART_DIR}/data/data.zip" -d "${JITSMART_DIR}/"
fi

mkdir -p "${JITSMART_DIR}/data/jitsmart"
for pkl in train_buggy_commit_lines_df.pkl valid_buggy_commit_lines_df.pkl test_buggy_commit_lines_df.pkl; do
    if [ ! -f "${JITSMART_DIR}/data/jitsmart/${pkl}" ]; then
        ln -sf "${JITSMART_DIR}/JITSmart/process and label defect code lines/${pkl}" "${JITSMART_DIR}/data/jitsmart/${pkl}"
    fi
done

echo "[4/4] Validando os datasets Pickle e a arquitetura MultiFocalLoss + HAN_MODEL..."
python3 - << 'EOF'
import os, pandas as pd, torch
from JITSmart.concat.model import MultiFocalLoss, Attention, HAN_MODEL

base = "/home/artur-carvalho/mestrado/repos/06-jit-smart/jit-smart"
for sub in ["data/jitfine/changes_train.pkl", "data/jitfine/features_train.pkl", "data/jitsmart/train_buggy_commit_lines_df.pkl"]:
    p = os.path.join(base, sub)
    assert os.path.exists(p), f"Arquivo não encontrado: {p}"

df_lines = pd.read_pickle(os.path.join(base, "data/jitsmart/test_buggy_commit_lines_df.pkl"))
emb = torch.nn.Embedding(100, 768)
han = HAN_MODEL(emb)
fl = MultiFocalLoss(num_class=2, alpha=0.25, gamma=2)
print(f"  [OK] test_buggy_commit_lines_df.pkl carregado ({len(df_lines)} linhas anotadas no conjunto de teste).")
print(f"  [OK] HAN_MODEL (DLN BiLSTM) e MultiFocalLoss instanciados com sucesso.")
EOF

echo "=================================================================="
echo "[JIT-Smart] Ambiente e datasets (JIT-Defect4J) prontos para execução!"
echo "=================================================================="
