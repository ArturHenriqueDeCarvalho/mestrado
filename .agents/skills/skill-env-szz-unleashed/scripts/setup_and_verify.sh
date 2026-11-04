#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/artur-carvalho/mestrado/repos/03-szz-unleashed"
VENV_DIR="${REPO_DIR}/.venv-szz-unleashed"
JAR_PATH="${REPO_DIR}/examples/data/jars/szz_find_bug_introducers-0.1.jar"

echo "=================================================================="
echo "[SZZ Unleashed] Verificando estrutura e ambiente em: ${REPO_DIR}"
echo "=================================================================="

cd "${REPO_DIR}"

echo "[1/4] Verificando Java Runtime e fatJar pré-compilado..."
java -version 2>&1 | head -n 2
if [ -f "${JAR_PATH}" ]; then
    echo "  [OK] fatJar pré-compilado verificado: ${JAR_PATH} ($(du -h "${JAR_PATH}" | cut -f1))"
else
    echo "  [ERRO] fatJar não encontrado em ${JAR_PATH}"
    exit 1
fi

if [ ! -d "${VENV_DIR}" ]; then
    echo "[2/4] Criando ambiente virtual Python isolado ${VENV_DIR}..."
    python3 -m venv "${VENV_DIR}"
else
    echo "[2/4] Ambiente virtual ${VENV_DIR} já existe."
fi

source "${VENV_DIR}/bin/activate"

echo "[3/4] Instalando pacotes Python (scikit-learn, imbalanced-learn, pandas, numpy)..."
pip install --quiet --upgrade pip
pip install --quiet scikit-learn imbalanced-learn pandas numpy scipy requests

echo "[4/4] Validando artefatos JSON do estudo Jenkins em examples/data/..."
python3 - << 'EOF'
import json, os

base = "/home/artur-carvalho/mestrado/repos/03-szz-unleashed/examples/data"
for fname in ["issue_list.json", "gitlog.json", "fix_and_introducers_pairs.json"]:
    fpath = os.path.join(base, fname)
    assert os.path.exists(fpath), f"Ausente: {fpath}"
    with open(fpath) as f:
        data = json.load(f)
    print(f"  [OK] {fname}: {len(data)} registros verificados.")
EOF

echo "=================================================================="
echo "[SZZ Unleashed] Ambiente híbrido Java/Python pronto para testes!"
echo "=================================================================="
