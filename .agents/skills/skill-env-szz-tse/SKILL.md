---
name: skill-env-szz-tse
description: >-
  Use this skill to configure the R and Python environments (.venv-szz-tse),
  inspect the 10 Apache project datasets (126,526 commits with buggy_B2, buggy_AG, buggy_MA, buggy_RA labels)
  and collinearity matrix (collinearity.csv), and execute or replicate the 1,000-iteration Out-of-Bag Bootstrap,
  Scott-Knott ESD variable importance, CBS+, One-Way, and Wasted Inspection Effort LOC calculations
  in /home/artur-carvalho/mestrado/repos/04-szz-tse.
---

# Skill: Arquitetura de Software e Execução Isolada do Ambiente SZZ-TSE (Pesquisa 4)

Este runbook habilita o agente (`expert-szz-tse` ou `professor-orientador`) a operar a arquitetura estatística em R (`code/calculation/classification_importance.R` e `code/packages/*.R`), o extrator de features Python (`features/jit-features/`) e os repositórios Java auxiliares (`ma-szz/` e `raszzprime/`) sobre os 126.526 commits dos 10 projetos Apache.

## 1. Referência de Arquitetura Interna

Para o diagrama detalhado dos módulos R (`measures.R`, `imbalance.R`, `CBS.R`, `VarImportance.R`, `one-way.R`), esquema das 18 colunas dos CSVs em `data_results/data_csvs/` e matriz de exclusão de multicolinearidade (`collinearity.csv`), consulte:
- [Arquitetura de Software e Diagnóstico de Ambiente](./references/architecture_and_env.md)

## 2. Provisionamento e Verificação do Ambiente Isolado

1. Execute o script de verificação dos 10 datasets Apache (126.526 commits) e ambiente Python/R:
   [setup_and_verify.sh](./scripts/setup_and_verify.sh)
   ```bash
   bash /home/artur-carvalho/mestrado/.agents/skills/skill-env-szz-tse/scripts/setup_and_verify.sh
   ```
2. O script valida a contagem exata de linhas e colunas dos 10 arquivos CSV em `data_results/data_csvs/` e `data_results/data_csvs2/`, verifica `collinearity.csv`, cria `.venv-szz-tse` e audita os pacotes estatísticos R (`pROC`, `randomForest`, `naivebayes`, `e1071`, `ScottKnottESD`, `caret`, `pracma`, `PRROC`).

## 3. Comandos de Execução e Replicação dos Testes (RQ1, RQ2 e RQ3)

### A. Execução do Pipeline Estatístico Oficial em R (`classification_importance.R`)
1. No arquivo [`szz-tse/code/calculation/classification_importance.R`](file:///home/artur-carvalho/mestrado/repos/04-szz-tse/szz-tse/code/calculation/classification_importance.R), substitua `DIR_PATH = "?"` por:
   ```r
   DIR_PATH = "/home/artur-carvalho/mestrado/repos/04-szz-tse/szz-tse"
   ```
2. Para validação rápida (*smoke test*), ajuste temporariamente `bootstrap_times <- 10` (ou mantenha `1000` para replicação completa) e execute:
   ```bash
   cd /home/artur-carvalho/mestrado/repos/04-szz-tse/szz-tse
   Rscript code/calculation/classification_importance.R
   ```

### B. Inspeção de Rótulos e Cálculo de Discrepância / Wasted Effort via Python (`.venv-szz-tse`)
```bash
source /home/artur-carvalho/mestrado/repos/04-szz-tse/.venv-szz-tse/bin/activate
cd /home/artur-carvalho/mestrado/repos/04-szz-tse/szz-tse
# O ambiente .venv-szz-tse possui pandas, numpy, scikit-learn e scipy para auditoria cruzada instantânea dos CSVs
```
