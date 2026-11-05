#!/usr/bin/env bash
# ==============================================================================
# Setup e Clonagem Blobless do Apache Flink (Base Unificada de Benchmark)
# Local: /home/artur-carvalho/mestrado/repos/00-flink
# Conforme: DEC-001 (Amostragem ESE) e DEC-009 (Apache Flink Unificado)
# ==============================================================================
set -euo pipefail

TARGET_DIR="/home/artur-carvalho/mestrado/repos/00-flink"
REPO_URL="https://github.com/apache/flink.git"

echo "=================================================================="
echo "[FLINK-BENCHMARK] Preparando base unificada Apache Flink..."
echo "=================================================================="

mkdir -p "${TARGET_DIR}"

if [[ ! -d "${TARGET_DIR}/.git" ]]; then
    echo "[1/2] Executando clone blobless (--filter=blob:none) de ${REPO_URL}..."
    git clone --filter=blob:none "${REPO_URL}" "${TARGET_DIR}"
else
    echo "[1/2] Repositório Apache Flink já clonado em ${TARGET_DIR}."
fi

echo "[2/2] Verificando integridade do histórico Git..."
cd "${TARGET_DIR}"
TOTAL_COMMITS=$(git rev-list --count HEAD)
echo "Total de commits indexados no Apache Flink: ${TOTAL_COMMITS}"

echo "=================================================================="
echo "[FLINK-BENCHMARK] Base unificada pronta para a extração de commits!"
echo "=================================================================="
