---
name: skill-benchmark-orchestrator
description: >-
  Use this skill to orchestrate cross-study benchmark verification, inspect or invoke
  any of the 6 isolated research environments (01-llm-szz to 06-jit-smart), aggregate empirical metrics,
  run non-parametric statistical comparisons (Wilcoxon, Cliff's Delta, Scott-Knott ESD),
  and synchronize experimental outputs with the Comparative Matrix and Scientific Article.
---

# Skill: Orquestração Multi-Ambiente de Benchmarks e Análises Cruzadas (Pesquisas 1 a 6)

Este runbook habilita o `professor-orientador`, o `analista-documental-comparativo` e o `redator-artigo-cientifico` a coordenar a validação e execução individual ou sequencial dos 6 ambientes experimentais, auditar logs de replicação e consolidar as análises comparativas e tabelas estatísticas do artigo científico.

## 1. Referência de Topologia Multi-Ambiente

Para o mapa de integração dos 6 ambientes virtuais isolados, fluxos de dados compartilhados (Apache Commons, Jenkins, Linux Kernel) e protocolo de auditoria de resultados, consulte:
- [Topologia Multi-Ambiente e Protocolo de Orquestração](./references/architecture_and_env.md)

## 2. Verificação Global de Todos os 6 Ambientes Isolados

1. Para verificar o status de prontidão de todos os 6 repositórios, datasets e scripts de ambiente de uma só vez, execute:
   [setup_and_verify.sh](./scripts/setup_and_verify.sh)
   ```bash
   bash /home/artur-carvalho/mestrado/.agents/skills/skill-benchmark-orchestrator/scripts/setup_and_verify.sh
   ```

## 3. Invocação Individual de Cada Ambiente Especializado

Sempre execute cada experimento de forma isolada em seu próprio ambiente virtual para evitar conflitos de versões de bibliotecas (`PyDriller 1.15.2` vs `1.15.5`, `GitPython 3.1.7` vs `3.1.18`, etc.):

| Pesquisa | Agente Responsável | Skill de Ambiente Dedicada | Script de Setup & Smoke Test |
| :--- | :--- | :--- | :--- |
| **P1: LLM-SZZ** | `expert-llm-szz` | `skill-env-llm-szz` | `.agents/skills/skill-env-llm-szz/scripts/setup_and_verify.sh` |
| **P2: PySZZ v2** | `expert-pyszz-v2` | `skill-env-pyszz-v2` | `.agents/skills/skill-env-pyszz-v2/scripts/setup_and_verify.sh` |
| **P3: SZZ Unleashed** | `expert-szz-unleashed` | `skill-env-szz-unleashed` | `.agents/skills/skill-env-szz-unleashed/scripts/setup_and_verify.sh` |
| **P4: SZZ-TSE** | `expert-szz-tse` | `skill-env-szz-tse` | `.agents/skills/skill-env-szz-tse/scripts/setup_and_verify.sh` |
| **P5: CC2Vec** | `expert-cc2vec` | `skill-env-cc2vec` | `.agents/skills/skill-env-cc2vec/scripts/setup_and_verify.sh` |
| **P6: JIT-Smart** | `expert-jit-smart` | `skill-env-jit-smart` | `.agents/skills/skill-env-jit-smart/scripts/setup_and_verify.sh` |
