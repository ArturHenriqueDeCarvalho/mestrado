#!/usr/bin/env bash
# ==============================================================================
# Setup e Verificação do Ambiente Isolado: Pesquisa 2 (PySZZ v2)
# Local: /home/artur-carvalho/mestrado/repos/02-pyszz-v2/.venv-pyszz-v2
# ==============================================================================
set -euo pipefail

REPO_DIR="/home/artur-carvalho/mestrado/repos/02-pyszz-v2"
VENV_DIR="${REPO_DIR}/.venv-pyszz-v2"
UV_BIN="${HOME}/.local/bin/uv"

echo "=================================================================="
echo "[PySZZ v2] Configurando e verificando ambiente isolado Python 3.10..."
echo "=================================================================="

# 1. Garantir uv
if [[ ! -x "${UV_BIN}" ]]; then
    echo "Instalando uv standalone..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# 2. Criar venv se não existir
if [[ ! -f "${VENV_DIR}/bin/python" ]]; then
    echo "[1/4] Criando ambiente virtual isolado em ${VENV_DIR}..."
    "${UV_BIN}" venv --python 3.10 "${VENV_DIR}"
else
    echo "[1/4] Ambiente virtual já existente em ${VENV_DIR}."
fi

# 3. Instalar dependências pinadas + pandas
echo "[2/4] Instalando dependências do PySZZ v2..."
"${UV_BIN}" pip install --python "${VENV_DIR}/bin/python" -r "${REPO_DIR}/requirements.txt" pandas

# 4. Validar binário srcML
echo "[3/4] Verificando binário srcML..."
srcml --version || { echo "ERRO: srcml não encontrado no PATH."; exit 1; }

# 5. Testar execução do main.py
echo "[4/4] Validando execução do CLI main.py..."
"${VENV_DIR}/bin/python" "${REPO_DIR}/main.py" -h > /dev/null

echo "=================================================================="
echo "[PySZZ v2] Ambiente isolado e dependências validadas com sucesso!"
echo "=================================================================="
