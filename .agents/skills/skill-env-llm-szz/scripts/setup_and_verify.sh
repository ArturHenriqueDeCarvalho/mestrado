#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/artur-carvalho/mestrado/repos/01-llm-szz"
VENV_DIR="${REPO_DIR}/.venv-llm-szz"

echo "=================================================================="
echo "[LLM-SZZ] Verificando estrutura e ambiente em: ${REPO_DIR}"
echo "=================================================================="

cd "${REPO_DIR}"

if [ ! -d "${VENV_DIR}" ]; then
    echo "[1/4] Criando ambiente virtual isolado ${VENV_DIR}..."
    python3 -m venv "${VENV_DIR}"
else
    echo "[1/4] Ambiente virtual ${VENV_DIR} já existe."
fi

source "${VENV_DIR}/bin/activate"

echo "[2/4] Verificando/instalando pacotes essenciais do LLM-SZZ..."
pip install --quiet --upgrade pip
pip install --quiet GitPython==3.1.18 PyDriller==1.15.5 openai>=1.50.0 Levenshtein>=0.26.0 RapidFuzz>=3.10.0 unidiff>=0.6.0 tqdm

echo "[3/4] Validando integridade dos arquivos de Oráculo CVE em data/..."
python3 - << 'EOF'
import json, os

data_dir = "/home/artur-carvalho/mestrado/repos/01-llm-szz/data"
for fname in ["verified_cve_with_versions_C.json", "verified_cve_with_versions_Java.json", "label.json"]:
    fpath = os.path.join(data_dir, fname)
    assert os.path.exists(fpath), f"Arquivo ausente: {fpath}"
    with open(fpath) as f:
        data = json.load(f)
    print(f"  [OK] {fname}: {len(data)} registros carregados com sucesso.")
EOF

echo "[4/4] Validando importações dos módulos Core SZZ e cálculo de Levenshtein..."
export PYTHONPATH="${REPO_DIR}:${REPO_DIR}/SZZ"
python3 - << 'EOF'
from szz.llm_szz import remove_whitespace, compute_line_ratio
r = compute_line_ratio("if (ptr == NULL) return -1;", "if(ptr==NULL) return -1;")
assert r == 1.0, f"Ratio inesperado: {r}"
print(f"  [OK] Módulo szz.llm_szz importado e Levenshtein.ratio validado (ratio={r}).")
EOF

echo "=================================================================="
echo "[LLM-SZZ] Ambiente pronto para execução de testes!"
echo "=================================================================="
