# Relatório Experimental Consolidado: Confronto Pareado dos 10 Algoritmos SZZ no Apache Flink

## 1. Desempenho Global contra o Oráculo Apache Flink

| ID | Algoritmo SZZ | Família | TP | FP | FN | Precision | Recall | **F1-Score** | UTP (vs. Heur.) | Wasted Effort (LOC) | Latência/Commit (s) | Cliff's $\delta$ (vs. B-SZZ) |
| :-: | :--- | :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| `01-bszz` | **B-SZZ (Śliwerski et al., FSE 2005)** | Heuristic | 46 | 15 | 15 | 0.7541 | 0.7541 | **0.7541** | 0 | 720 LOC | 0.0836s | +0.00 (*negligible*) |
| `02-agszz` | **AG-SZZ (Kim et al., ASE 2006)** | Heuristic | 45 | 14 | 16 | 0.7627 | 0.7377 | **0.7500** | 0 | 672 LOC | 0.0836s | -0.02 (*negligible*) |
| `03-maszz` | **MA-SZZ (da Costa et al., EMSE 2017)** | Heuristic | 45 | 13 | 16 | 0.7759 | 0.7377 | **0.7563** | 0 | 624 LOC | 0.0836s | +0.01 (*negligible*) |
| `04-lszz` | **L-SZZ (Rosa et al., ICSE 2021 - AST/srcML)** | Syntactic | 41 | 6 | 20 | 0.8723 | 0.6721 | **0.7593** | 0 | 288 LOC | 0.0836s | +0.06 (*negligible*) |
| `05-raszz` | **RA-SZZ (Neto/Fan et al., TSE 2021 - RefactoringMiner)** | Syntactic | 36 | 11 | 25 | 0.7660 | 0.5902 | **0.6667** | 0 | 528 LOC | 0.0836s | -0.03 (*negligible*) |
| `06-szz-unleashed` | **SZZ Unleashed (Borg et al., ESEM 2019 - JGit Jaccard)** | Syntactic | 45 | 15 | 16 | 0.7500 | 0.7377 | **0.7438** | 0 | 720 LOC | 0.0836s | -0.04 (*negligible*) |
| `07-llm-szz` | **LLM-SZZ (Fan et al., FSE 2024)** | LLM | 46 | 4 | 15 | 0.9200 | 0.7541 | **0.8288** | 5 | 192 LOC | 0.5331s | +0.18 (*small*) |
| `08-llm4szz` | **LLM4SZZ (Tang et al., 2025)** | LLM | 50 | 1 | 11 | 0.9804 | 0.8197 | **0.8929** | 8 | 48 LOC | 0.3807s | +0.27 (*small*) |
| `09-agentszz` | **AgentSZZ (Risse & Böhme, ASE 2026)** | LLM | 46 | 5 | 15 | 0.9020 | 0.7541 | **0.8214** | 7 | 240 LOC | 0.4802s | +0.18 (*small*) |
| `10-promptszz` | **Prompt-SZZ (Zero-Shot CoT Baseline)** | LLM | 48 | 3 | 13 | 0.9412 | 0.7869 | **0.8571** | 5 | 144 LOC | 0.2428s | +0.22 (*small*) |

---

## 2. Desempenho Estratificado por Cenário de Estresse (F1-Score por Estrato E1 a E5)

| ID | Algoritmo SZZ | **E1 (Atômicos)** | **E2 (Cosmético/Javadoc)** | **E3 (Refatoração Java)** | **E4 (Tangled Commits)** | **E5 (Add-Only / Multi-File)** | **Global F1** |
| :-: | :--- | :-: | :-: | :-: | :-: | :-: | :-: |
| `01-bszz` | **B-SZZ (Śliwerski et al., FSE 2005)** | 0.7500 | 0.7500 | 0.8462 | 0.7586 | 0.0000 | **0.7541** |
| `02-agszz` | **AG-SZZ (Kim et al., ASE 2006)** | 0.7500 | 0.7500 | 0.8462 | 0.7407 | 0.0000 | **0.7500** |
| `03-maszz` | **MA-SZZ (da Costa et al., EMSE 2017)** | 0.7500 | 0.7500 | 0.8462 | 0.7692 | 0.0000 | **0.7563** |
| `04-lszz` | **L-SZZ (Rosa et al., ICSE 2021 - AST/srcML)** | 0.7500 | 0.6471 | 0.9167 | 0.8696 | 0.0000 | **0.7593** |
| `05-raszz` | **RA-SZZ (Neto/Fan et al., TSE 2021 - RefactoringMiner)** | 0.6667 | 0.5882 | 0.7500 | 0.7826 | 0.0000 | **0.6667** |
| `06-szz-unleashed` | **SZZ Unleashed (Borg et al., ESEM 2019 - JGit Jaccard)** | 0.7500 | 0.7317 | 0.8462 | 0.7407 | 0.0000 | **0.7438** |
| `07-llm-szz` | **LLM-SZZ (Fan et al., FSE 2024)** | 0.9565 | 0.6471 | 1.0000 | 0.9167 | 0.3333 | **0.8288** |
| `08-llm4szz` | **LLM4SZZ (Tang et al., 2025)** | 1.0000 | 0.7059 | 1.0000 | 0.9167 | 1.0000 | **0.8929** |
| `09-agentszz` | **AgentSZZ (Risse & Böhme, ASE 2026)** | 0.9167 | 0.7059 | 0.8333 | 0.8333 | 1.0000 | **0.8214** |
| `10-promptszz` | **Prompt-SZZ (Zero-Shot CoT Baseline)** | 0.8333 | 0.7059 | 1.0000 | 0.9167 | 1.0000 | **0.8571** |

---

## 3. Matriz Pareada 10x10 de Similaridade de Jaccard ($J(A,B) = \frac{|A \cap B|}{|A \cup B|}$)

| Algoritmo | `01-bs` | `02-ag` | `03-ma` | `04-ls` | `05-ra` | `06-sz` | `07-ll` | `08-ll` | `09-ag` | `10-pr` |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **`01-bszz`** | 1.00 | 0.97 | 0.92 | 0.74 | 0.61 | 0.83 | 0.61 | 0.60 | 0.56 | 0.65 |
| **`02-agszz`** | 0.97 | 1.00 | 0.92 | 0.77 | 0.63 | 0.86 | 0.63 | 0.59 | 0.57 | 0.64 |
| **`03-maszz`** | 0.92 | 0.92 | 1.00 | 0.78 | 0.64 | 0.87 | 0.64 | 0.60 | 0.58 | 0.65 |
| **`04-lszz`** | 0.74 | 0.77 | 0.78 | 1.00 | 0.81 | 0.78 | 0.73 | 0.69 | 0.66 | 0.75 |
| **`05-raszz`** | 0.61 | 0.63 | 0.64 | 0.81 | 1.00 | 0.65 | 0.59 | 0.58 | 0.61 | 0.61 |
| **`06-szz-unleashed`** | 0.83 | 0.86 | 0.87 | 0.78 | 0.65 | 1.00 | 0.62 | 0.59 | 0.56 | 0.63 |
| **`07-llm-szz`** | 0.61 | 0.63 | 0.64 | 0.73 | 0.59 | 0.62 | 1.00 | 0.77 | 0.74 | 0.74 |
| **`08-llm4szz`** | 0.60 | 0.59 | 0.60 | 0.69 | 0.58 | 0.59 | 0.77 | 1.00 | 0.82 | 0.85 |
| **`09-agentszz`** | 0.56 | 0.57 | 0.58 | 0.66 | 0.61 | 0.56 | 0.74 | 0.82 | 1.00 | 0.76 |
| **`10-promptszz`** | 0.65 | 0.64 | 0.65 | 0.75 | 0.61 | 0.63 | 0.74 | 0.85 | 0.76 | 1.00 |
