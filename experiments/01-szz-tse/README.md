# Relatório de Execução Experimental: Etapa 01 (SZZ-TSE)

- **Branch**: `step-01/setup-e-replicacao-szz-tse` (integrada via Pull Request/Merge na `main`)
- **Data da Execução**: 04/11/2026
- **Ambiente Isolado**: `/home/artur-carvalho/mestrado/repos/04-szz-tse/.venv-szz-tse` (Python 3.10.22, pandas 2.3.3, scikit-learn 1.7.2, scipy 1.15.3)
- **Artigo Científico de Referência**: *"The Impact of Changes Mislabeled by SZZ on Just-in-Time Defect Prediction"* (Yuanrui Fan, Xin Xia, Daniel Alencar da Costa, David Lo, Ahmed E. Hassan, Shanping Li), publicado no periódico *IEEE Transactions on Software Engineering (IEEE TSE 2019/2021)*, DOI: `10.1109/TSE.2019.2929761`.
- **Origem dos Dados**: Replication Package oficial arquivado pelos autores em `repos/04-szz-tse/szz-tse/data_results/` e código R/Python em `code/calculation/`.

---

## 🏛️ 1. Contexto Epistemológico e Racional Metodológico do Estudo

O estudo seminal de Fan et al. (IEEE TSE) abordou uma questão central da Engenharia de Software Empírica:
> *"Até que ponto o ruído introduzido por algoritmos SZZ ingênuos contamina a predição Just-in-Time (JIT) e induz os desenvolvedores a inspecionar código desnecessariamente?"*

### O Problema da Rotulagem por Refatoração:
- Algoritmos tradicionais como o **B-SZZ** (Śliwerski et al., 2005) usam o `git blame` ingenuamente na linha que foi modificada pelo commit corretor (*bug-fix*).
- Quando um desenvolvedor faz uma **refatoração** (ex.: renomear variáveis, extrair métodos, mover classes), a linha muda de lugar ou de formato. O `git blame` clássico aponta a refatoração como a introdutora do defeito, gerando falsos positivos graves (*Mislabeled Changes*).
- Para resolver isso, os autores implementaram e compararam 4 gerações de SZZ:
  1. **B-SZZ**: Algoritmo base original sem filtros.
  2. **AG-SZZ**: Adiciona filtro de anotações sintáticas.
  3. **MA-SZZ**: Adiciona filtro de comentários, linhas em branco e meta-informações.
  4. **RA-SZZ** (*Refactoring-Aware SZZ*): Utiliza o analisador sintático de refatorações **`RefactoringMiner`** para ignorar alterações estruturais que não introduzem falhas lógicas, servindo como o **oráculo/baseline de verdade fundamental limpa**.

---

## 📦 2. Os 10 Projetos da Fundação Apache Analisados (126.526 Commits)

A base empírica abrange 10 sistemas de grande porte, maduros e de múltiplos domínios técnicos da Apache Software Foundation, totalizando **126.526 commits**:

| # | Projeto | Domínio Técnico / Papel na Indústria | Commits Totais | B-SZZ (`buggy_B2`) | AG-SZZ (`buggy_AG`) | MA-SZZ (`buggy_MA`) | RA-SZZ (`buggy_RA` - Limpo) |
| :-: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **1** | **ActiveMQ** | Servidor corporativo de mensageria assíncrona (*message broker*) Java | 7.753 | 1.697 (21,89%) | 1.157 (14,92%) | 1.336 (17,23%) | 1.245 (16,06%) |
| **2** | **Camel** | Framework de integração de sistemas empresariais (*Enterprise Integration Patterns*) | 17.374 | 2.957 (17,02%) | 2.032 (11,70%) | 2.186 (12,58%) | 2.018 (11,62%) |
| **3** | **Derby** | Banco de dados relacional transacional (*RDBMS*) em Java puro | 9.775 | 1.772 (18,13%) | 1.799 (18,40%) | 1.559 (15,95%) | 1.153 (11,80%) |
| **4** | **Geronimo** | Servidor de aplicação corporativo Java EE certificado | 16.152 | 2.309 (14,30%) | 1.245 (7,71%) | 1.999 (12,38%) | 1.856 (11,49%) |
| **5** | **HBase** | Banco de dados NoSQL distribuído em larga escala (Google Bigtable model) | 14.581 | 3.323 (22,79%) | 2.449 (16,80%) | 3.072 (21,07%) | 2.670 (18,31%) |
| **6** | **Hadoop Common (`hcommon`)** | Módulo central de utilitários, abstração de arquivos e RPC do Hadoop | 27.077 | 1.951 (7,21%) | 1.469 (5,43%) | 1.907 (7,04%) | 1.681 (6,21%) |
| **7** | **Mahout** | Biblioteca e framework de Machine Learning distribuído | 2.762 | 539 (19,51%) | 354 (12,82%) | 456 (16,51%) | 420 (15,21%) |
| **8** | **OpenJPA** | Implementação de referência do padrão Java Persistence API (JPA) | 6.368 | 810 (12,72%) | 659 (10,35%) | 853 (13,40%) | 692 (10,87%) |
| **9** | **Pig** | Plataforma de fluxo e análise em lote para processamento Hadoop | 3.089 | 549 (17,77%) | 441 (14,28%) | 528 (17,09%) | 467 (15,12%) |
| **10** | **Tuscany** | Arquitetura corporativa orientada a serviços (*Service Component Architecture*) | 21.595 | 2.157 (9,99%) | 1.021 (4,73%) | 1.594 (7,38%) | 1.506 (6,97%) |
| — | **TOTAL CONSOLIDADO** | **Ecossistema Apache (Java Corporativo)** | **126.526** | **18.064 (14,28%)** | **12.626 (9,98%)** | **15.490 (12,24%)** | **13.708 (10,83%)** |

---

## 🔬 3. Auditoria de Fidelidade Empírica (Conferência com a Tabela 4 do Artigo IEEE TSE)

Para certificar que a nossa replicação não sofre de discrepâncias ou distorções, os resultados gerados na máquina local foram confrontados com a **Tabela 4 oficial** publicada no paper da IEEE TSE (Fan et al.):

### Confronto de Falsos Positivos (FP), Falsos Negativos (FN) e Mislabeled Changes:
- **Projeto ActiveMQ**:
  - *No Artigo Publicado*: B-SZZ teve 892 mislabeled (672 FP / 10% FPR, 220 FN / 18% FNR); AG-SZZ teve 552 mislabeled (232 FP / 4% FPR, 320 FN / 26% FNR); MA-SZZ teve 149 mislabeled (120 FP / 2% FPR, 29 FN / 2% FNR).
  - *No Script Replicado Localmente*: B-SZZ: 892 mislabeled (672 FP / 10,33%, 220 FN / 17,67%); AG-SZZ: 552 mislabeled (232 FP / 3,56%, 320 FN / 25,70%); MA-SZZ: 149 mislabeled (120 FP / 1,84%, 29 FN / 2,33%).
  - 👉 **Conferência**: **100% Exato.**
- **Projeto Camel**:
  - *No Artigo Publicado*: B-SZZ teve 1.503 mislabeled (1.221 FP / 8% FPR, 282 FN / 14% FNR); AG-SZZ teve 1.186 mislabeled (600 FP / 4% FPR, 586 FN / 29% FNR); MA-SZZ teve 268 mislabeled (218 FP / 1% FPR, 50 FN / 2% FNR).
  - *No Script Replicado Localmente*: B-SZZ: 1.503 mislabeled (1.221 FP / 8%, 282 FN / 14%); AG-SZZ: 1.186 mislabeled (600 FP / 4%, 586 FN / 29%); MA-SZZ: 268 mislabeled (218 FP / 1%, 50 FN / 2%).
  - 👉 **Conferência**: **100% Exato.**

---

## 🔍 4. Quantificação Consolidada do Ruído de Rotulagem frente ao Baseline RA-SZZ

No total de 126.526 commits do Apache, o impacto cumulativo do ruído de rotulagem revelou:

1. **B-SZZ (`buggy_B2`)**:
   - Total rotulado como buggy: **18.064** commits.
   - **Falsos positivos (ruído puro por refatoração)**: **6.409** commits (**5,07% de todo o histórico Apache foi incorretamente rotulado como defeituoso** pelo B-SZZ clássico).
2. **AG-SZZ (`buggy_AG`)**:
   - Total rotulado como buggy: **12.626** commits.
   - **Falsos positivos**: **3.078** commits (2,43%).
3. **MA-SZZ (`buggy_MA`)**:
   - Total rotulado como buggy: **15.490** commits.
   - **Falsos positivos**: **2.340** commits (1,85%).
4. **RA-SZZ (`buggy_RA` - Linha de Base Refactoring-Aware)**:
   - Total de commits indutores genuínos: **13.708**.

---

## 🔗 5. Conexão com as Questões de Pesquisa (RQs) do Artigo de Mestrado

- **Para a RQ1 (Sobreposição dos Métodos)**:
  Fornece a matriz primária em larga escala (126k commits) para calcular o Índice de Jaccard e o Kappa de Cohen entre as variantes tradicionais e o RA-SZZ, mapeando exatamente a "zona cinzenta" onde os algoritmos discordam.
- **Para a RQ2 (Impacto da Rotulagem em Classificadores)**:
  Permite treinar classificadores clássicos (`Random Forest`, `Logistic Regression`, `Naive Bayes`, `XGBoost`) e redes neurais sobre cada um dos 4 rótulos (`B`, `AG`, `MA`, `RA`) e testá-los contra o oráculo limpo, quantificando o **Wasted Effort LOC** (linhas de código desperdiçadas na inspeção manual da equipe devido a falsos positivos da rotulagem).
- **Para a RQ3 (Impacto da IA)**:
  Serve de base para comparar como os modelos baseados em Transformers e IA (ex.: `JIT-Smart` e `CC2Vec`) se comportam quando treinados sobre dados com ruído (`buggy_B2`) versus dados limpos (`buggy_RA`).

---

## 📁 6. Artefatos Persistidos e Reprodutíveis

- Tabela tabular dos 10 projetos em CSV: [`apache_10_projects_szz_summary.csv`](file:///home/artur-carvalho/mestrado/experiments/01-szz-tse/apache_10_projects_szz_summary.csv)
- Estatísticas de auditoria em JSON: [`szz_tse_replication_audit.json`](file:///home/artur-carvalho/mestrado/experiments/01-szz-tse/szz_tse_replication_audit.json)
- Script de replicação automatizada: [`replicate_szz_tse.py`](file:///home/artur-carvalho/mestrado/experiments/01-szz-tse/replicate_szz_tse.py)
- Script de setup da skill: [`.agents/skills/skill-env-szz-tse/scripts/setup_and_verify.sh`](file:///home/artur-carvalho/mestrado/.agents/skills/skill-env-szz-tse/scripts/setup_and_verify.sh)
