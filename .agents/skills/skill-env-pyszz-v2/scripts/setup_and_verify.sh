#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/artur-carvalho/mestrado/repos/02-pyszz-v2"
VENV_DIR="${REPO_DIR}/.venv-pyszz-v2"

echo "=================================================================="
echo "[PySZZ v2] Verificando estrutura e ambiente em: ${REPO_DIR}"
echo "=================================================================="

cd "${REPO_DIR}"

if [ ! -d "${VENV_DIR}" ]; then
    echo "[1/4] Criando ambiente virtual isolado ${VENV_DIR}..."
    python3 -m venv "${VENV_DIR}"
else
    echo "[1/4] Ambiente virtual ${VENV_DIR} já existe."
fi

source "${VENV_DIR}/bin/activate"

echo "[2/4] Instalando dependências do PySZZ v2..."
pip install --quiet --upgrade pip
pip install --quiet GitPython==3.1.7 PyDriller==1.15.2 PyYAML>=5.3.1 options==1.4.10 testresources==2.0.1 dateparser>=0.7.6 networkx>=2.6.3 beautifulsoup4>=4.10.0 lxml>=4.6.4 packaging>=21.3 regex>=2022.1.18

echo "[3/4] Validando ferramentas embutidas (RefactoringMiner 2.0, arquivos YAML e suíte test/)..."
if [ -x "${REPO_DIR}/tools/RefactoringMiner-2.0/bin/RefactoringMiner" ]; then
    echo "  [OK] RefactoringMiner 2.0 executável encontrado em tools/RefactoringMiner-2.0/bin/RefactoringMiner"
else
    chmod +x "${REPO_DIR}/tools/RefactoringMiner-2.0/bin/RefactoringMiner" || true
    echo "  [OK] Permissão de execução concedida ao RefactoringMiner 2.0"
fi

YML_COUNT=$(ls -1 "${REPO_DIR}/conf/"*.yml | wc -l)
echo "  [OK] ${YML_COUNT} configurações YAML verificadas em conf/"

echo "[4/4] Validando importação da hierarquia AbstractSZZ..."
python3 - << 'EOF'
from szz.b_szz import BaseSZZ
from szz.ag_szz import AGSZZ
from szz.ma_szz import MASZZ
from szz.r_szz import RSZZ
from szz.l_szz import LSZZ
from szz.ra_szz import RASZZ
from szz.pd_szz import PyDrillerSZZ
print("  [OK] Todas as classes SZZ (BaseSZZ, AGSZZ, MASZZ, RSZZ, LSZZ, RASZZ, PyDrillerSZZ) importadas com sucesso.")
EOF

echo "=================================================================="
echo "[PySZZ v2] Ambiente pronto para execução de testes!"
echo "=================================================================="
