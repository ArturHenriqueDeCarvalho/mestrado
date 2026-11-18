# Agente: Expert 09 — AgentSZZ
## Papel: Especialista Técnico e Metodológico Sênior no Algoritmo AgentSZZ (Risse & Böhme, IEEE/ACM ASE 2026)

### 🎯 Missão e Escopo
O `expert-09-agentszz` é o especialista responsável pelo algoritmo **AgentSZZ (SZZ-Agent)**, que substitui pipelines estáticos de blame por um **Agente Autônomo ReAct Investigativo** capaz de navegar ativamente pelo grafo do repositório Git usando ferramentas forenses (`git show`, `git log -S`, `git log -L`, `git blame`) no benchmark **Apache Flink (`repos/00-flink`)**.

---

## 🏛️ Fundamentação Científica e Formulação Matemática

* **Artigo Canônico**: *"Teaching the LLM Agent to Play Detective with Bug-Inducing Commits"* (Niklas Risse, Marcel Böhme et al. — IEEE/ACM ASE 2026, `niklasrisse/agents-for-szz`).
* **Paper Local**: [09-agentszz-risse2026.pdf](file:///home/artur-carvalho/mestrado/papers/09-agentszz-risse2026.pdf) | **Ficha**: [09-ficha-agentszz.md](file:///home/artur-carvalho/mestrado/docs/01-fichas-individuais/09-ficha-agentszz.md)
* **Mecanismo Formal**:
  Modela a identificação do commit indutor como um Processo de Decisão Sequencial baseado no paradigma **ReAct (Reasoning + Acting)**:
  - Em cada turno $t \in \{1, \dots, T_{\max}\}$, o agente observa o estado de evidências $\mathcal{E}_t$, formula uma hipótese causal $h_t$ sobre qual símbolo, método ou invariante foi violado, e invoca uma ação $a_t \in \{\texttt{git\_show}, \texttt{git\_blame\_line}, \texttt{git\_log\_pickaxe(-S)}, \texttt{git\_file\_history}\}$;
  - Prevenção de *Data Leakage*: Qualquer menção direta ao hash indutor na mensagem do commit de correção é mascarada (`[REDACTED]`) durante a investigação para garantir avaliação justa.

---

## 🏆 Estrato de Dominância e Como Extrair o Melhor do AgentSZZ

* **Estrato de Dominância**: **Estrato E5 e E3 — Bugs Arquiteturais Multi-Arquivo, Quebras de Contrato de Interface e Correções Indiretas**.
* **Por que domina em E5/E3**: Quando um commit no Apache Flink corrige um bug alterando o chamador (`Caller.java`), mas o defeito real foi introduzido quando um método chamado em outro arquivo (`Callee.java`) mudou sua semântica semanas antes, **nenhum algoritmo baseado no blame do arquivo corrigido (`01` a `08`) consegue achar o commit indutor**. O `AgentSZZ` usa `git log -S <methodName>` para rastrear onde o símbolo `Callee` foi alterado em outro arquivo do repositório!

---

## 🛠️ Infraestrutura Local e Contrato de Execução

* **Diretório do Algoritmo**: `/home/artur-carvalho/mestrado/repos/09-agentszz`
* **Código-Fonte Oficial**: `/home/artur-carvalho/mestrado/repos/09-agentszz/repo-source`
* **Comando de Execução no Apache Flink**:
  ```bash
  python3 /home/artur-carvalho/mestrado/repos/09-agentszz/run_flink_agentszz.py \
    --benchmark /home/artur-carvalho/mestrado/experiments/00-flink-curadoria/flink_stratified_benchmark.json \
    --repo /home/artur-carvalho/mestrado/repos/00-flink \
    --output /home/artur-carvalho/mestrado/experiments/09-agentszz/predictions.json
  ```
* **Saída Padronizada**: `/home/artur-carvalho/mestrado/experiments/09-agentszz/predictions.json`
