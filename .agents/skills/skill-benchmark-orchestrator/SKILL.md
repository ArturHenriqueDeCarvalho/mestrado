---
name: skill-benchmark-orchestrator
description: Use this skill to orchestrate cross-study benchmark verification across the 10 isolated SZZ algorithm environments (01-bszz to 10-promptszz) on the unified Apache Flink repository (00-flink), aggregate empirical metrics (Precision, Recall, F1, UTP, Wasted Effort LOC), run non-parametric statistical comparisons (Wilcoxon, Cliff's Delta), and synchronize experimental outputs with the Comparative Matrix and Scientific Article.
---

# Skill: skill-benchmark-orchestrator

Orquestra o benchmark cruzado dos **10 Algoritmos SZZ (`01-bszz` a `10-promptszz`)** sobre a base unificada **Apache Flink (`repos/00-flink`)**, coordenando os **10 Agentes Especialistas (`expert-01-bszz` a `expert-10-promptszz`)**.

## 🏛️ Mapa Canônico de Execução (`00` a `10`)

- `repos/00-flink/` $\rightarrow$ Base Unificada Apache Flink (~38.800 commits | 1.850 bugfixes `.java` de produção)
- `repos/01-bszz/` $\rightarrow$ `expert-01-bszz` (`experiments/01-bszz/predictions.json`)
- `repos/02-agszz/` $\rightarrow$ `expert-02-agszz` (`experiments/02-agszz/predictions.json`)
- `repos/03-maszz/` $\rightarrow$ `expert-03-maszz` (`experiments/03-maszz/predictions.json`)
- `repos/04-lszz/` $\rightarrow$ `expert-04-lszz` (`experiments/04-lszz/predictions.json`)
- `repos/05-raszz/` $\rightarrow$ `expert-05-raszz` (`experiments/05-raszz/predictions.json`)
- `repos/06-szz-unleashed/` $\rightarrow$ `expert-06-szz-unleashed` (`experiments/06-szz-unleashed/predictions.json`)
- `repos/07-llm-szz/` $\rightarrow$ `expert-07-llm-szz` (`experiments/07-llm-szz/predictions.json`)
- `repos/08-llm4szz/` $\rightarrow$ `expert-08-llm4szz` (`experiments/08-llm4szz/predictions.json`)
- `repos/09-agentszz/` $\rightarrow$ `expert-09-agentszz` (`experiments/09-agentszz/predictions.json`)
- `repos/10-promptszz/` $\rightarrow$ `expert-10-promptszz` (`experiments/10-promptszz/predictions.json`)

## 🚀 Pipeline Completo End-to-End

```bash
python3 experiments/00-flink-curadoria/curate_and_stratify_flink.py --target-per-stratum 12
python3 experiments/11-analise-cruzada/run_all_10_szz_flink.py
python3 experiments/11-analise-cruzada/evaluate_and_compare_10_szz.py
```
