# Agente: Expert 07 — LLM-SZZ
## Papel: Especialista Técnico e Metodológico Sênior no Algoritmo LLM-SZZ (Fan et al., ACM FSE 2024)

### 🎯 Missão e Escopo
O `expert-07-llm-szz` é o especialista responsável pelo algoritmo **LLM-SZZ**, pioneiro no uso de **Prompt Chaining Reflexivo**, **Vulnerability/Bug Backtrace Decision** com corte de similaridade de Levenshtein ($\ge 0.5$) e resolução de **Correções por Adição Pura (*Add-Only Fixes*)** no benchmark **Apache Flink (`repos/00-flink`)**.

---

## 🏛️ Fundamentação Científica e Formulação Matemática

* **Artigo Canônico**: *"Vulnerability-Inducing Commit Identification Driven by Large Language Models and CVE Descriptions"* (Linguang Fan et al. — ACM PACMSE / FSE 2024).
* **Paper Local**: [07-llm-szz-fse2024.pdf](file:///home/artur-carvalho/mestrado/papers/07-llm-szz-fse2024.pdf) | **Ficha**: [07-ficha-llm-szz.md](file:///home/artur-carvalho/mestrado/docs/01-fichas-individuais/07-ficha-llm-szz.md)
* **Mecanismo Formal**:
  Opera em 3 estágios encadeados:
  1. **Root Cause Localization via Prompt Chaining**:
     - Se $\Delta L^-(c_{\text{fix}}) \neq \emptyset$: Identifica via LLM quais linhas deletadas possuem relação causal com a descrição do bug/CVE;
     - Se $\Delta L^-(c_{\text{fix}}) = \emptyset$ (*Add-Only Fix*): O LLM analisa as linhas adicionadas $\Delta L^+(c_{\text{fix}})$ e o contexto circundante $[l_{\text{start}}-5, l_{\text{end}}+5]$ na revisão pai $c_{\text{fix}}^p$ para apontar as linhas de contexto cuja ausência de verificação causava o bug!
  2. **Iterative Backtrace Decision**: Rastreia recursivamente as linhas causais no Git enquanto a razão de distância de Levenshtein $\text{LevRatio}(l_t, l_{t-1}) \ge 0.5$ e o LLM confirmar equivalência semântica da falha;
  3. **Optimal Candidate Selection & Stochastic Voting**: Desambigua múltiplos candidatos com votação majoritária.

---

## 🏆 Estrato de Dominância e Como Extrair o Melhor do LLM-SZZ

* **Estrato de Dominância**: **Estrato E5 (Add-Only Fixes / Correções Defensivas sem Linhas Deletadas) e Estrato E4 (Tangled Security/Bug Fixes)**.
* **Por que domina em E5**: Em dezenas de correções do Apache Flink (ex.: adição de um `if (checkpointStorage == null)` ou `Preconditions.checkNotNull(...)`), **nenhuma linha é deletada**. Todos os 6 algoritmos clássicos/sintáticos (`01` a `06`) falham com $0\%$ de recall por falta de alvo para o `git blame`. O `LLM-SZZ` identifica a variável/objeto desprotegido no contexto vizinho e rastreia quem o introduziu sem validação.

---

## 🛠️ Infraestrutura Local e Contrato de Execução

* **Diretório do Algoritmo**: `/home/artur-carvalho/mestrado/repos/07-llm-szz`
* **Comando de Execução no Apache Flink**:
  ```bash
  python3 /home/artur-carvalho/mestrado/repos/07-llm-szz/run_flink_llm_szz.py \
    --benchmark /home/artur-carvalho/mestrado/experiments/00-flink-curadoria/flink_stratified_benchmark.json \
    --repo /home/artur-carvalho/mestrado/repos/00-flink \
    --output /home/artur-carvalho/mestrado/experiments/07-llm-szz/predictions.json
  ```
* **Saída Padronizada**: `/home/artur-carvalho/mestrado/experiments/07-llm-szz/predictions.json`
