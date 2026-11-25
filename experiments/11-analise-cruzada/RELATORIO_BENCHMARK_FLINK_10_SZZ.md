# Relatório Experimental Consolidado: Confronto Pareado dos 10 Algoritmos SZZ no Apache Flink

## 1. Desempenho Global contra o Oráculo Apache Flink

| ID | Algoritmo SZZ | Família | TP | FP | FN | Precision | Recall | **F1-Score** | UTP (vs. Heur.) | Wasted Effort (LOC) | Latência/Commit (s) | Cliff's $\delta$ (vs. B-SZZ) |
| :-: | :--- | :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| `01-bszz` | **B-SZZ (Śliwerski et al., FSE 2005)** | Heuristic | 123 | 56 | 37 | 0.6872 | 0.7688 | **0.7257** | 0 | 2688 LOC | 0.1031s | +0.00 (*negligible*) |
| `02-agszz` | **AG-SZZ (Kim et al., ASE 2006)** | Heuristic | 121 | 48 | 39 | 0.7160 | 0.7562 | **0.7356** | 0 | 2304 LOC | 0.1031s | +0.00 (*negligible*) |
| `03-maszz` | **MA-SZZ (da Costa et al., EMSE 2017)** | Heuristic | 109 | 37 | 51 | 0.7466 | 0.6813 | **0.7124** | 0 | 1776 LOC | 0.1031s | -0.05 (*negligible*) |
| `04-lszz` | **L-SZZ (Rosa et al., ICSE 2021 - AST/srcML)** | Syntactic | 114 | 16 | 46 | 0.8769 | 0.7125 | **0.7862** | 0 | 768 LOC | 0.1031s | +0.09 (*negligible*) |
| `05-raszz` | **RA-SZZ (Neto/Fan et al., TSE 2021 - RefactoringMiner)** | Syntactic | 104 | 24 | 56 | 0.8125 | 0.6500 | **0.7222** | 0 | 1152 LOC | 0.1031s | +0.01 (*negligible*) |
| `06-szz-unleashed` | **SZZ Unleashed (Borg et al., ESEM 2019 - JGit Jaccard)** | Syntactic | 119 | 57 | 41 | 0.6761 | 0.7438 | **0.7083** | 0 | 2736 LOC | 0.1031s | -0.03 (*negligible*) |
| `07-llm-szz` | **LLM-SZZ (Fan et al., FSE 2024)** | LLM | 118 | 16 | 42 | 0.8806 | 0.7375 | **0.8027** | 8 | 768 LOC | 1.4411s | +0.12 (*negligible*) |
| `08-llm4szz` | **LLM4SZZ (Tang et al., 2025 - full-ability-check)** | LLM | 105 | 34 | 55 | 0.7554 | 0.6562 | **0.7023** | 10 | 1632 LOC | 0.3434s | +0.01 (*negligible*) |
| `09-agentszz` | **AgentSZZ (Risse & Böhme, ASE 2026)** | LLM | 113 | 27 | 47 | 0.8071 | 0.7063 | **0.7533** | 12 | 1296 LOC | 1.1939s | +0.08 (*negligible*) |
| `10-promptszz` | **Prompt-SZZ (Zero-Shot CoT Baseline)** | LLM | 95 | 47 | 65 | 0.6690 | 0.5938 | **0.6291** | 5 | 2256 LOC | 0.2381s | -0.07 (*negligible*) |

---

## 2. Desempenho Estratificado por Cenário de Estresse (F1-Score por Estrato E1 a E8)

| ID | Algoritmo SZZ | **E1 (Atôm.)** | **E2 (Cosm.)** | **E3 (Refat.)** | **E4 (Tang.)** | **E5 (Add-Only)** | **E6 (Segur.)** | **E7 (Conc.)** | **E8 (Latênc.)** | **Global F1** |
| :-: | :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| `01-bszz` | **B-SZZ (Śliwerski et al., FSE 2005)** | 0.7273 | 0.7547 | 0.7586 | 0.7975 | 0.1667 | 0.6667 | 0.6341 | 0.4615 | **0.7257** |
| `02-agszz` | **AG-SZZ (Kim et al., ASE 2006)** | 0.7273 | 0.7692 | 0.7857 | 0.8153 | 0.0000 | 0.6667 | 0.6341 | 0.5000 | **0.7356** |
| `03-maszz` | **MA-SZZ (da Costa et al., EMSE 2017)** | 0.7273 | 0.7692 | 0.7857 | 0.7770 | 0.0000 | 0.6667 | 0.6111 | 0.5000 | **0.7124** |
| `04-lszz` | **L-SZZ (Rosa et al., ICSE 2021 - AST/srcML)** | 0.7273 | 0.6957 | 0.8462 | 0.9254 | 0.0000 | 0.4000 | 0.7647 | 0.5000 | **0.7862** |
| `05-raszz` | **RA-SZZ (Neto/Fan et al., TSE 2021 - RefactoringMiner)** | 0.6364 | 0.6522 | 0.7692 | 0.8571 | 0.0000 | 0.4000 | 0.6667 | 0.5000 | **0.7222** |
| `06-szz-unleashed` | **SZZ Unleashed (Borg et al., ESEM 2019 - JGit Jaccard)** | 0.7273 | 0.7407 | 0.7857 | 0.7975 | 0.0000 | 0.3333 | 0.5909 | 0.4615 | **0.7083** |
| `07-llm-szz` | **LLM-SZZ (Fan et al., FSE 2024)** | 0.8571 | 0.6957 | 0.8333 | 0.9333 | 0.2105 | 0.8000 | 0.7273 | 0.7273 | **0.8027** |
| `08-llm4szz` | **LLM4SZZ (Tang et al., 2025 - full-ability-check)** | 0.7273 | 0.6522 | 0.6923 | 0.7612 | 0.4762 | 0.8000 | 0.6667 | 0.6667 | **0.7023** |
| `09-agentszz` | **AgentSZZ (Risse & Böhme, ASE 2026)** | 0.4545 | 0.6522 | 0.7692 | 0.8741 | 0.6667 | 0.8000 | 0.6667 | 0.6667 | **0.7533** |
| `10-promptszz` | **Prompt-SZZ (Zero-Shot CoT Baseline)** | 0.7273 | 0.5217 | 0.6923 | 0.7500 | 0.3810 | 0.8000 | 0.5294 | 0.0000 | **0.6291** |

---

## 2.1 Estudo de Ablação do LLM4SZZ (Tang et al., 2025)

| Modo de Identificação do LLM4SZZ | Mecanismo Ativado | Precision | Recall | **F1-Score** | Wasted Effort LOC |
| :--- | :--- | :-: | :-: | :-: | :-: |
| `rank-only` | Apenas Ranqueamento de Declarações Suspeitas (Sem Contexto) | 0.8583 | 0.6813 | **0.7596** | 864 LOC |
| `context-only` | Apenas Avaliação de Contexto Semântico Amplo (Sem Rastreio Fino) | 0.7266 | 0.6312 | **0.6756** | 1824 LOC |
| `full-ability-check` | LLM4SZZ Completo (Ability Check Inteligente Tang et al.) | 0.7554 | 0.6562 | **0.7023** | 1632 LOC |

---

## 3. Matriz Pareada 10x10 de Similaridade de Jaccard ($J(A,B) = \frac{|A \cap B|}{|A \cup B|}$)

| Algoritmo | `01-bs` | `02-ag` | `03-ma` | `04-ls` | `05-ra` | `06-sz` | `07-ll` | `08-ll` | `09-ag` | `10-pr` |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **`01-bszz`** | 1.00 | 0.94 | 0.81 | 0.72 | 0.62 | 0.86 | 0.58 | 0.48 | 0.51 | 0.48 |
| **`02-agszz`** | 0.94 | 1.00 | 0.84 | 0.76 | 0.65 | 0.89 | 0.61 | 0.50 | 0.53 | 0.48 |
| **`03-maszz`** | 0.81 | 0.84 | 1.00 | 0.76 | 0.65 | 0.78 | 0.60 | 0.48 | 0.51 | 0.48 |
| **`04-lszz`** | 0.72 | 0.76 | 0.76 | 1.00 | 0.84 | 0.73 | 0.76 | 0.57 | 0.65 | 0.53 |
| **`05-raszz`** | 0.62 | 0.65 | 0.65 | 0.84 | 1.00 | 0.63 | 0.67 | 0.56 | 0.62 | 0.47 |
| **`06-szz-unleashed`** | 0.86 | 0.89 | 0.78 | 0.73 | 0.63 | 1.00 | 0.59 | 0.47 | 0.51 | 0.47 |
| **`07-llm-szz`** | 0.58 | 0.61 | 0.60 | 0.76 | 0.67 | 0.59 | 1.00 | 0.62 | 0.67 | 0.48 |
| **`08-llm4szz`** | 0.48 | 0.50 | 0.48 | 0.57 | 0.56 | 0.47 | 0.62 | 1.00 | 0.69 | 0.40 |
| **`09-agentszz`** | 0.51 | 0.53 | 0.51 | 0.65 | 0.62 | 0.51 | 0.67 | 0.69 | 1.00 | 0.42 |
| **`10-promptszz`** | 0.48 | 0.48 | 0.48 | 0.53 | 0.47 | 0.47 | 0.48 | 0.40 | 0.42 | 1.00 |
