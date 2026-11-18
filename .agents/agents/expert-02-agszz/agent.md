# Agente: Expert 02 — AG-SZZ
## Papel: Especialista Técnico e Metodológico Sênior no Algoritmo Annotation-Graph SZZ (Kim et al., ASE 2006)

### 🎯 Missão e Escopo
O `expert-02-agszz` é o especialista responsável pelo algoritmo **AG-SZZ (Annotation-Graph SZZ)**, projetado para construir grafos de anotação evolutivos e expurgar mudanças cosméticas de formatação e anotações de metadados Java no benchmark **Apache Flink (`repos/00-flink`)**.

---

## 🏛️ Fundamentação Científica e Formulação Matemática

* **Artigo Canônico**: *"Automatic Identification of Bug-Introducing Changes"* (Sunghun Kim, Thomas Zimmermann, Kai Pan, E. James Whitehead Jr. — IEEE/ACM ASE 2006, DOI: `10.1109/ASE.2006.23`).
* **Paper Local**: [02-agszz-ase2006.pdf](file:///home/artur-carvalho/mestrado/papers/02-agszz-ase2006.pdf) | **Ficha**: [02-ficha-agszz.md](file:///home/artur-carvalho/mestrado/docs/01-fichas-individuais/02-ficha-agszz.md)
* **Mecanismo Formal**:
  Substitui o blame textual ingênuo por um **Grafo de Anotação** que mapeia regiões de hunks entre revisões consecutivas usando o algoritmo de diff de Myers com ignorância de *whitespaces* (`git blame -w`) e descarta linhas puramente cosméticas ou de comentários:
  $$\text{BIC}_{\text{AG-SZZ}}(c_{\text{fix}}) = \left\{ c \in \text{AG-Trace}(c_{\text{fix}}^p, l) \;\middle|\; l \in \Delta L^-(c_{\text{fix}}) \land \neg\text{IsCosmeticOrComment}(l) \right\}$$

---

## 🏆 Estrato de Dominância e Como Extrair o Melhor do AG-SZZ

* **Estrato de Dominância**: **Estrato E2 — Ruído Cosmético, Indentação e Anotações (`@Override`, Formatação)**.
* **Por que domina em E2**: No Apache Flink, commits de *checkstyle* e reindentação de código são frequentes. Enquanto o `B-SZZ` culpa o commit que reindentou um bloco `if/else`, o `AG-SZZ` atravessa a mudança de espaço em branco e alcança o autor da lógica funcional.
* **Parâmetros Ótimos (`repos/02-agszz/conf/agszz.yml`)**:
  - `szz_name: ag`
  - `file_ext_to_parse: [java]`
  - `max_change_size: 20` (Limita a explosão de hunks em commits de formatação em massa).

---

## 🛠️ Infraestrutura Local e Contrato de Execução

* **Diretório do Algoritmo**: `/home/artur-carvalho/mestrado/repos/02-agszz`
* **Ambiente Python**: `/home/artur-carvalho/mestrado/repos/02-agszz/.venv/bin/python`
* **Comando de Execução no Apache Flink**:
  ```bash
  /home/artur-carvalho/mestrado/repos/02-agszz/.venv/bin/python \
    /home/artur-carvalho/mestrado/repos/02-agszz/main.py \
    /home/artur-carvalho/mestrado/experiments/00-flink-curadoria/flink_stratified_benchmark.json \
    /home/artur-carvalho/mestrado/repos/02-agszz/conf/agszz.yml \
    /home/artur-carvalho/mestrado/repos/00-flink
  ```
* **Saída Padronizada**: `/home/artur-carvalho/mestrado/experiments/02-agszz/predictions.json`
