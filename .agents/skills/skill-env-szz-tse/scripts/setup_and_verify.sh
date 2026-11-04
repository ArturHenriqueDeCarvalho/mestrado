#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/artur-carvalho/mestrado/repos/04-szz-tse"
SZZ_TSE_DIR="${REPO_DIR}/szz-tse"
VENV_DIR="${REPO_DIR}/.venv-szz-tse"

echo "=================================================================="
echo "[SZZ-TSE] Verificando estrutura e datasets em: ${SZZ_TSE_DIR}"
echo "=================================================================="

if [ ! -d "${VENV_DIR}" ]; then
    echo "[1/3] Criando ambiente virtual isolado ${VENV_DIR}..."
    python3 -m venv "${VENV_DIR}"
else
    echo "[1/3] Ambiente virtual ${VENV_DIR} já existe."
fi

source "${VENV_DIR}/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet pandas numpy scikit-learn scipy

echo "[2/3] Auditando os 10 datasets Apache (126.526 commits) e collinearity.csv..."
python3 - << 'EOF'
import os, pandas as pd

base = "/home/artur-carvalho/mestrado/repos/04-szz-tse/szz-tse/data_results"
projects = ["activemq", "camel", "derby", "geronimo", "hcommon", "hbase", "mahout", "openjpa", "pig", "tuscany"]

total_rows = 0
for p in projects:
    f1 = os.path.join(base, "data_csvs", f"{p}.csv")
    f2 = os.path.join(base, "data_csvs2", f"{p}.csv")
    df = pd.read_csv(f1)
    assert os.path.exists(f2), f"Ausente em data_csvs2: {f2}"
    rows = len(df)
    total_rows += rows
    ra_buggy = (df["buggy_RA"] == "buggy").sum()
    b2_buggy = (df["buggy_B2"] == "buggy").sum()
    print(f"  [OK] {p:<10}: {rows:>6} commits | buggy_RA={ra_buggy:>5} | buggy_B2={b2_buggy:>5}")

print(f"  [TOTAL AUDITADO]: {total_rows} commits (Esperado no artigo: 126.526 commits).")
assert total_rows == 126526, f"Total divergente: {total_rows}"
EOF

echo "[3/3] Verificando disponibilidade do interpretador R no sistema..."
if command -v Rscript >/dev/null 2>&1; then
    Rscript --version 2>&1 | head -n 1
else
    echo "  [INFO] Rscript não instalado globalmente; análises estatísticas podem ser executadas via Python (.venv-szz-tse) ou instalando r-base."
fi

echo "=================================================================="
echo "[SZZ-TSE] Auditoria de dados (126.526 commits) concluída com sucesso!"
echo "=================================================================="
