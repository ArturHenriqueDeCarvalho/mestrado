---
name: skill-env-flink-benchmark
description: Skill de automação e orquestração do benchmark unificado sobre o repositório Apache Flink (apache/flink) para confronto pareado dos 10 algoritmos SZZ.
---

# Skill: skill-env-flink-benchmark

Esta skill gerencia a clonagem otimizada (*blobless* conforme `DEC-001` e `DEC-009`) do repositório oficial do **Apache Flink**, a mineração dos commits de bug-fixing vinculados a issues Jira (`FLINK-[0-9]+`) e a extração de commits de segurança (CVEs) para alimentar uniformemente todos os 10 algoritmos SZZ.

## 🛠️ Comandos e Scripts

- Script de Clonagem e Preparação: `scripts/setup_flink_repo.sh`
- Extrator de Bug Fixes e CVEs: `scripts/extract_flink_fixes.py`

## 📊 Saída Padronizada
Os dados minerados são disponibilizados em:
`repos/00-flink/extracted_fixes/`
- `flink_bugfix_commits.json`: Commits de correção mapeados.
- `flink_cve_commits.json`: Commits de segurança e advisories.
