# Arquitetura de Software e Diagnóstico de Ambiente — SZZ-TSE (Pesquisa 4)

## 1. Diagrama da Arquitetura Experimental (`repos/04-szz-tse/`)

```
+-----------------------------------------------------------------------------------+
| CAMADA DE ROTULAGEM SZZ & EXTRAÇÃO DE FEATURES (Upstream)                         |
|  - ma-szz/ (Java): Implementação do MA-SZZ (Da Costa et al.)                      |
|  - raszzprime/ (Java + RefDiff + RefactoringMiner): Implementação do RA-SZZ       |
|  - szz-tse/features/jit-features/ (Python + MySQL): Extração das 14 features      |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| CAMADA DE DADOS CONSOLIDADOS (szz-tse/data_results/)                              |
|  - data_csvs/*.csv (10 projetos Apache, features log-transformadas ln(x+1))       |
|  - data_csvs2/*.csv (10 projetos Apache, features em escala bruta para LOC)       |
|  - collinearity.csv: Features excluídas por VIF / Spearman por projeto            |
|  - 18 Colunas: buggy_B2, buggy_AG, buggy_MA, buggy_RA (Labels)                    |
|                + ns, nd, nf, entropy, la, ld, lt, fix, ndev, age, nuc, exp,       |
|                  rexp, sexp (14 Change Metrics)                                   |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| MOTOR ESTATÍSTICO EM R (szz-tse/code/)                                            |
|  - calculation/classification_importance.R:                                       |
|      * Loop: study_methods (imbalance, balance, oneway)                           |
|              x classifiers (naive_bayes, logistic_regression, random_forest)      |
|              x projects (10 Apache)                                               |
|      * Out-of-Bag (OOB) Bootstrap (1.000 iterações)                               |
|      * Treino em buggy_{B2,AG,MA,RA} -> Teste SEMPRE avaliado em buggy_RA         |
|  - packages/measures.R: AUC, Precision, Recall, F1, G-Mean, FP, FN,               |
|                         waste_effort (LOC), all_effort (LOC)                      |
|  - packages/CBS.R: Recall@20%Effort via Classify-Before-Sorting (CBS+)            |
|  - packages/one-way.R: Modelo supervisionado simples One-Way (oneway_r20)         |
|  - packages/VarImportance.R: Importância de features + ScottKnottESD              |
+-----------------------------------------------------------------------------------+
```

## 2. Detalhamento da Matriz de Exclusão de Multicolinearidade (`collinearity.csv`)

Para evitar instabilidade nos coeficientes da Regressão Logística e viés de importância no Random Forest, os autores aplicaram análise de correlação hierárquica de Spearman e VIF, removendo por projeto:
- **Removidas nos 10 projetos**: `nd`, `entropy`.
- **Removidas adicionalmente por projeto**:
  - `activemq`, `camel`, `hcommon`: `nuc`, `rexp`, `fix`
  - `derby`: `rexp`, `sexp`, `fix`
  - `geronimo`, `hbase`, `mahout`, `openjpa`, `tuscany`: `rexp`, `fix`
  - `pig`: `nuc`, `rexp`, `sexp`, `fix`
