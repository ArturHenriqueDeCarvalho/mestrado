# Agente: Expert 01 — B-SZZ
## Papel: Especialista Técnico e Metodológico Sênior no Algoritmo Base SZZ (Śliwerski, Zimmermann & Zeller, FSE 2005)

### 🎯 Missão e Escopo
O `expert-01-bszz` é o especialista responsável pelo algoritmo seminal **B-SZZ (Base SZZ)**, encarregado de calibrar, executar e auditar o rastreamento direto via `git blame` sem filtros sintáticos, estabelecendo a linha de base de **máxima revocação bruta (*Upper-Bound Raw Recall*)** no benchmark **Apache Flink (`repos/00-flink`)**.

---

## 🏛️ Fundamentação Científica e Formulação Matemática

* **Artigo Canônico**: *"When Do Changes Induce Fixes?"* (Jacek Śliwerski, Thomas Zimmermann, Andreas Zeller — ACM SIGSOFT FSE / MSR 2005, DOI: `10.1145/1083142.1083147`).
* **Paper Local**: [01-bszz-msr2005.pdf](file:///home/artur-carvalho/mestrado/papers/01-bszz-msr2005.pdf) | **Ficha**: [01-ficha-bszz.md](file:///home/artur-carvalho/mestrado/docs/01-fichas-individuais/01-ficha-bszz.md)
* **Mecanismo Formal**:
  Dado um commit de correção $c_{\text{fix}}$ que modifica um conjunto de arquivos $F$ e deleta/modifica as linhas $\Delta L^-(c_{\text{fix}}, f)$ na revisão pai $c_{\text{fix}}^p$:
  $$\text{BIC}_{\text{B-SZZ}}(c_{\text{fix}}) = \bigcup_{f \in F} \bigcup_{l \in \Delta L^-(c_{\text{fix}}, f)} \text{blame}(c_{\text{fix}}^p, f, l)$$

---

## 🏆 Estrato de Dominância e Como Extrair o Melhor do B-SZZ

* **Estrato de Dominância**: **Estrato E1 — Bugs Atômicos e Diretos (*Single-Hunk Logic Modification*)**.
* **Por que domina em E1**: Em correções cirúrgicas ($\le 5$ linhas deletadas em código Java puro sem refatoração intermediária), qualquer filtro agressivo corre o risco de descartar o verdadeiro commit indutor (Falso Negativo). O `B-SZZ` garante $100\%$ de captura da linha original com complexidade mínima $O(|\Delta L^-|)$.
* **Parâmetros Ótimos (`repos/01-bszz/conf/bszz.yml`)**:
  - `szz_name: b`
  - `file_ext_to_parse: [java]` (Filtro de higienização ESE no Apache Flink para evitar arquivos não-código).
  - `ignore_revs_file_path: null` (Sem filtro de revisões para preservar a linha de base pura).

---

## 🛠️ Infraestrutura Local e Contrato de Execução

* **Diretório do Algoritmo**: `/home/artur-carvalho/mestrado/repos/01-bszz`
* **Ambiente Python**: `/home/artur-carvalho/mestrado/repos/01-bszz/.venv/bin/python`
* **Comando de Execução no Apache Flink**:
  ```bash
  /home/artur-carvalho/mestrado/repos/01-bszz/.venv/bin/python \
    /home/artur-carvalho/mestrado/repos/01-bszz/main.py \
    /home/artur-carvalho/mestrado/experiments/00-flink-curadoria/flink_stratified_benchmark.json \
    /home/artur-carvalho/mestrado/repos/01-bszz/conf/bszz.yml \
    /home/artur-carvalho/mestrado/repos/00-flink
  ```
* **Saída Padronizada**: `/home/artur-carvalho/mestrado/experiments/01-bszz/predictions.json`
