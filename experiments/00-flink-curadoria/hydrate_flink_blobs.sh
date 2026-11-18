#!/usr/bin/env bash
# ==============================================================================
# Pré-Hidratação Local de Blobs Git para o Benchmark Estratificado Apache Flink
# Garante execução 100% offline para Eclipse JGit (SZZ Unleashed), RefactoringMiner
# (RA-SZZ), srcML (L-SZZ), PyDriller e Agentes LLM.
# ==============================================================================
set -euo pipefail

FLINK_DIR="/home/artur-carvalho/mestrado/repos/00-flink"
git -C "${FLINK_DIR}" config fetch.negotiationAlgorithm noop
python3 /home/artur-carvalho/mestrado/experiments/00-flink-curadoria/curate_and_stratify_flink.py "$@"
