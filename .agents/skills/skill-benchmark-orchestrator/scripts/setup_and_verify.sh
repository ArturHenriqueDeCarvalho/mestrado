#!/usr/bin/env bash
set -euo pipefail

SKILLS_ROOT="/home/artur-carvalho/mestrado/.agents/skills"

echo "=================================================================="
echo "[ORQUESTRADOR] Auditando os 6 Ambientes e Skills de Replicação"
echo "=================================================================="

for s in skill-env-llm-szz skill-env-pyszz-v2 skill-env-szz-unleashed skill-env-szz-tse skill-env-cc2vec skill-env-jit-smart; do
    script="${SKILLS_ROOT}/${s}/scripts/setup_and_verify.sh"
    ref="${SKILLS_ROOT}/${s}/references/architecture_and_env.md"
    doc="${SKILLS_ROOT}/${s}/SKILL.md"
    if [ -f "${doc}" ] && [ -f "${ref}" ] && [ -f "${script}" ]; then
        echo "  [OK] ${s}: SKILL.md + architecture_and_env.md + setup_and_verify.sh presentes."
    else
        echo "  [ERRO] Arquivos ausentes na skill ${s}"
        exit 1
    fi
done

echo "=================================================================="
echo "[ORQUESTRADOR] Todas as 6 Skills de Ambiente verificadas!"
echo "Para inicializar um ambiente específico, execute seu script setup_and_verify.sh."
echo "=================================================================="
