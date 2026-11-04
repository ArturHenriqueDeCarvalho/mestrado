# Relatório de Execução Experimental: Etapa 01 (SZZ-TSE)

- **Branch**: `step-01/setup-e-replicacao-szz-tse`
- **Data da Execução**: 04/11/2026
- **Ambiente Isolado**: `/home/artur-carvalho/mestrado/repos/04-szz-tse/.venv-szz-tse` (Python 3.10.22, pandas 2.3.3, scikit-learn 1.7.2, scipy 1.15.3)
- **Origem dos Dados**: Replication Package oficial de Yuanrui Fan et al. (*IEEE TSE 2019/2021*, DOI: `10.1109/TSE.2019.2929761`) em `repos/04-szz-tse/szz-tse/data_results/`

---

## 📊 1. Distribuição de Rótulos SZZ por Projeto (126.526 Commits)

| Projeto Apache | Commits Totais | B-SZZ (`buggy_B2`) | AG-SZZ (`buggy_AG`) | MA-SZZ (`buggy_MA`) | RA-SZZ (`buggy_RA`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **activemq** | 7.753 | 1.697 (21,89%) | 1.157 (14,92%) | 1.336 (17,23%) | 1.245 (16,06%) |
| **camel** | 17.374 | 2.957 (17,02%) | 2.032 (11,70%) | 2.186 (12,58%) | 2.018 (11,62%) |
| **derby** | 9.775 | 1.772 (18,13%) | 1.799 (18,40%) | 1.559 (15,95%) | 1.153 (11,80%) |
| **geronimo** | 16.152 | 2.309 (14,30%) | 1.245 (7,71%) | 1.999 (12,38%) | 1.856 (11,49%) |
| **hbase** | 14.581 | 3.323 (22,79%) | 2.449 (16,80%) | 3.072 (21,07%) | 2.670 (18,31%) |
| **hcommon** | 27.077 | 1.951 (7,21%) | 1.469 (5,43%) | 1.907 (7,04%) | 1.681 (6,21%) |
| **mahout** | 2.762 | 539 (19,51%) | 354 (12,82%) | 456 (16,51%) | 420 (15,21%) |
| **openjpa** | 6.368 | 810 (12,72%) | 659 (10,35%) | 853 (13,40%) | 692 (10,87%) |
| **pig** | 3.089 | 549 (17,77%) | 441 (14,28%) | 528 (17,09%) | 467 (15,12%) |
| **tuscany** | 21.595 | 2.157 (9,99%) | 1.021 (4,73%) | 1.594 (7,38%) | 1.506 (6,97%) |
| **TOTAL APACHE** | **126.526** | **18.064 (14,28%)** | **12.626 (9,98%)** | **15.490 (12,24%)** | **13.708 (10,83%)** |

---

## 🔍 2. Quantificação do Ruído de Rotulagem frente ao Baseline RA-SZZ

O algoritmo `RA-SZZ` atua como a linha de base filtrada por refatorações (usando o `RefactoringMiner` para eliminar falsas acusações onde linhas foram apenas movidas/renomeadas). Comparando com o RA-SZZ nos 126.526 commits:

1. **B-SZZ (`buggy_B2`)**:
   - Total rotulado como buggy: **18.064** commits.
   - **Falsos positivos (mislabeled by refactoring)**: **6.409** commits (5,07% de todo o histórico Apache foi incorretamente rotulado como indutor de bug pelo B-SZZ clássico).
2. **AG-SZZ (`buggy_AG`)**:
   - Total rotulado como buggy: **12.626** commits.
   - **Falsos positivos**: **3.078** commits (2,43%).
3. **MA-SZZ (`buggy_MA`)**:
   - Total rotulado como buggy: **15.490** commits.
   - **Falsos positivos**: **2.340** commits (1,85%).
4. **RA-SZZ (`buggy_RA`)**:
   - Total genuíno: **13.708** commits indutores de defeito.

---

## 📁 3. Artefatos Gerados e Prontos para a Fase 2 (Sobreposição & Classificadores)

- Dados tabulados em CSV: [`experiments/01-szz-tse/apache_10_projects_szz_summary.csv`](file:///home/artur-carvalho/mestrado/experiments/01-szz-tse/apache_10_projects_szz_summary.csv)
- Estatísticas de auditoria em JSON: [`experiments/01-szz-tse/szz_tse_replication_audit.json`](file:///home/artur-carvalho/mestrado/experiments/01-szz-tse/szz_tse_replication_audit.json)
- Script de execução reproduzível: [`experiments/01-szz-tse/replicate_szz_tse.py`](file:///home/artur-carvalho/mestrado/experiments/01-szz-tse/replicate_szz_tse.py)
- Script de automação da skill atualizado: [`.agents/skills/skill-env-szz-tse/scripts/setup_and_verify.sh`](file:///home/artur-carvalho/mestrado/.agents/skills/skill-env-szz-tse/scripts/setup_and_verify.sh)
