#!/usr/bin/env bash
# ==============================================================================
# Setup e Verificação do Ambiente Isolado: Pesquisa 4 (SZZ-TSE)
# Local: /home/artur-carvalho/mestrado/repos/04-szz-tse/.venv-szz-tse
# ==============================================================================
set -euo pipefail

REPO_DIR="/home/artur-carvalho/mestrado/repos/04-szz-tse"
VENV_DIR="${REPO_DIR}/.venv-szz-tse"
UV_BIN="${HOME}/.local/bin/uv"

echo "=================================================================="
echo "[SZZ-TSE] Configurando e verificando ambiente isolado Python 3.10..."
echo "=================================================================="

# 1. Garantir uv
if [[ ! -x "${UV_BIN}" ]]; then
    echo "Instalando uv standalone..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# 2. Criar venv se não existir
if [[ ! -f "${VENV_DIR}/bin/python" ]]; then
    echo "[1/3] Criando ambiente virtual isolado em ${VENV_DIR}..."
    "${UV_BIN}" venv --python 3.10 "${VENV_DIR}"
else
    echo "[1/3] Ambiente virtual já existente em ${VENV_DIR}."
fi

# 3. Instalar dependências de ciência de dados
echo "[2/3] Instalando dependências (pandas, scikit-learn, scipy, matplotlib, seaborn)..."
"${UV_BIN}" pip install --python "${VENV_DIR}/bin/python" pandas numpy scikit-learn scipy matplotlib seaborn

# 4. Validar importações
echo "[3/3] Validando importações..."
"${VENV_DIR}/bin/python" -c "
import pandas as pd
import numpy as np
import sklearn
import scipy
print(f'Ambiente operacional: pandas={pd.__version__}, scikit-learn={sklearn.__version__}, scipy={scipy.__version__}')
"

echo "=================================================================="
echo "[SZZ-TSE] Ambiente isolado configurado com sucesso!"
echo "=================================================================="
