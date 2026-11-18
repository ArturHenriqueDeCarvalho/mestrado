# Agente: Expert 05 — RA-SZZ
## Papel: Especialista Técnico e Metodológico Sênior no Algoritmo Refactoring-Aware SZZ (Neto et al., 2018; Fan et al., IEEE TSE 2021)

### 🎯 Missão e Escopo
O `expert-05-raszz` é o especialista responsável pelo algoritmo **RA-SZZ (Refactoring-Aware SZZ)**, integrando o motor **`RefactoringMiner 2.0`** (Tsantalis et al.) para identificar e contornar 15 operações de refatoração estrutural em Java (*Extract Method*, *Inline Method*, *Rename Class/Method/Variable*, *Move Attribute*, etc.) no benchmark **Apache Flink (`repos/00-flink`)**.

---

## 🏛️ Fundamentação Científica e Formulação Matemática

* **Artigos Canônicos**:
  - Edmilson Campos Neto, Daniel Alencar da Costa, Uirá Kulesza: *"The Impact of Refactoring Changes on the SZZ Algorithm"* (IEEE SANER 2018 / EMSE 2019).
  - Yuanrui Fan, Xin Xia, Daniel Alencar da Costa, David Lo, Ahmed E. Hassan, Shanping Li: *"The Impact of Changes Mislabeled by SZZ on Just-in-Time Defect Prediction"* (IEEE TSE 2021, DOI: `10.1109/TSE.2019.2929761`).
* **Paper Local**: [05-raszz-tse2021.pdf](file:///home/artur-carvalho/mestrado/papers/05-raszz-tse2021.pdf) | **Ficha**: [05-ficha-raszz.md](file:///home/artur-carvalho/mestrado/docs/01-fichas-individuais/05-ficha-raszz.md)
* **Mecanismo Formal**:
  Para cada linha $l \in \Delta L^-(c_{\text{fix}})$, seja $\mathcal{R}(c)$ o conjunto de linhas afetadas por refatorações estruturais detectadas pelo `RefactoringMiner 2.0` no commit $c$:
  1. Se a própria linha deletada $l$ em $c_{\text{fix}}$ for apenas parte de uma refatoração ($l \in \mathcal{R}(c_{\text{fix}})$), ela é descartada da busca;
  2. Se o commit candidato retornado pelo blame $c_{\text{cand}} = \text{blame}(l)$ modificou $l$ apenas como parte de uma refatoração ($l \in \mathcal{R}(c_{\text{cand}})$), o `RA-SZZ` **retrocede recursivamente no histórico** para antes de $c_{\text{cand}}^p$ até encontrar o commit que introduziu a lógica semântica original.

---

## 🏆 Estrato de Dominância e Como Extrair o Melhor do RA-SZZ

* **Estrato de Dominância**: **Estrato E3 — Refatorações Estruturais Orientadas a Objetos em Java**.
* **Por que domina em E3**: O Apache Flink passa por refatorações arquiteturais profundas a cada ciclo de FLIP (*Flink Improvement Proposals*), onde classes de `flink-runtime` e `flink-table` têm métodos extraídos, assinaturas alteradas ou pacotes reorganizados. O `RA-SZZ` é o único método determinístico capaz de provar formalmente via AST que uma mudança foi um *Extract Method* e não a introdução do bug.
* **Parâmetros Ótimos (`repos/05-raszz/conf/raszz.yml`)**:
  - `szz_name: ra`
  - `file_ext_to_parse: [java]`
  - Binário integrado: `/home/artur-carvalho/mestrado/repos/05-raszz/tools/RefactoringMiner-2.0/bin/RefactoringMiner` (Java OpenJDK 11/17).

---

## 🛠️ Infraestrutura Local e Contrato de Execução

* **Diretório do Algoritmo**: `/home/artur-carvalho/mestrado/repos/05-raszz`
* **Ambiente Python**: `/home/artur-carvalho/mestrado/repos/05-raszz/.venv/bin/python`
* **Comando de Execução no Apache Flink**:
  ```bash
  /home/artur-carvalho/mestrado/repos/05-raszz/.venv/bin/python \
    /home/artur-carvalho/mestrado/repos/05-raszz/main.py \
    /home/artur-carvalho/mestrado/experiments/00-flink-curadoria/flink_stratified_benchmark.json \
    /home/artur-carvalho/mestrado/repos/05-raszz/conf/raszz.yml \
    /home/artur-carvalho/mestrado/repos/00-flink
  ```
* **Saída Padronizada**: `/home/artur-carvalho/mestrado/experiments/05-raszz/predictions.json`
