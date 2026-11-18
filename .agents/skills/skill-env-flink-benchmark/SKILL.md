---
name: skill-env-flink-benchmark
description: Skill de automação e orquestração do benchmark unificado sobre o repositório Apache Flink (apache/flink) para confronto pareado dos 10 algoritmos SZZ.
---

# Skill: skill-env-flink-benchmark

Esta skill gerencia a clonagem otimizada (*blobless* conforme `DEC-001`, `DEC-009` e `DEC-011`) do repositório oficial do **Apache Flink (`repos/00-flink`)**, a filtragem estrita de commits de produção `.java`, a extração do **Oráculo Informado por Desenvolvedores do Flink**, a estratificação nos 5 cenários de estresse (`E1` a `E5`), a pré-hidratação em lote de blobs via `git fetch origin --stdin` e a avaliação estatística cruzada dos **10 Algoritmos SZZ**.

## 🛠️ Comandos e Scripts

1. **Preparação e Clonagem do Apache Flink**:
   ```bash
   bash .agents/skills/skill-env-flink-benchmark/scripts/setup_flink_repo.sh
   ```
2. **Curadoria Científica, Estratificação (E1–E5) e Hidratação de Blobs**:
   ```bash
   bash experiments/00-flink-curadoria/hydrate_flink_blobs.sh --target-per-stratum 12
   ```
3. **Execução Pareada dos 10 Algoritmos SZZ (`01-bszz` a `10-promptszz`)**:
   ```bash
   python3 experiments/11-analise-cruzada/run_all_10_szz_flink.py
   ```
4. **Avaliação Estatística Cruzada e Geração de Relatório e CSVs**:
   ```bash
   python3 experiments/11-analise-cruzada/evaluate_and_compare_10_szz.py
   ```

## 📊 Artefatos Gerados
- `experiments/00-flink-curadoria/flink_clean_java_bugfixes.json`: 1.850 commits de bug-fix que tocam código de produção `.java`.
- `experiments/00-flink-curadoria/flink_stratified_benchmark.json`: Benchmark estratificado (`E1` a `E5`) com Oráculo Ground Truth.
- `experiments/01-bszz/predictions.json` .. `experiments/10-promptszz/predictions.json`: Predições padronizadas dos 10 algoritmos.
- `experiments/11-analise-cruzada/RELATORIO_BENCHMARK_FLINK_10_SZZ.md`: Relatório consolidado com F1 Global, F1 por Estrato, Jaccard $10 \times 10$, UTP, Wasted Effort LOC e Cliff's Delta.
