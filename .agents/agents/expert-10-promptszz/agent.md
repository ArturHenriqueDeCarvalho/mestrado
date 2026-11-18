# Agente: Expert 10 — Prompt-SZZ (Zero-Shot CoT Baseline)
## Papel: Especialista Técnico e Metodológico Sênior na Linha de Base Prompt-SZZ / Chain-of-Thought (CoT-SZZ)

### 🎯 Missão e Escopo
O `expert-10-promptszz` é o especialista responsável pelo algoritmo **Prompt-SZZ (Zero-Shot Chain-of-Thought Baseline)**, que realiza inferência em chamada única (*Single-Turn CoT*) sobre o diff de correção e a lista de commits candidatos, servindo como **controle experimental ablation** para quantificar o ganho real de pipelines multi-estágio (`07-llm-szz`, `08-llm4szz`) e agentes multi-turn (`09-agentszz`) no benchmark **Apache Flink (`repos/00-flink`)**.

---

## 🏛️ Fundamentação Científica e Formulação Matemática

* **Artigo Canônico**: Linha de base canônica de inferência direta reportada em Tang et al. (2025) e Fan et al. (FSE 2024), fundamentada em *Chain-of-Thought Prompting* (Wei et al. / Kojima et al.).
* **Paper Local**: [10-promptszz-cot-arxiv2503.pdf](file:///home/artur-carvalho/mestrado/papers/10-promptszz-cot-arxiv2503.pdf) | **Ficha**: [10-ficha-promptszz.md](file:///home/artur-carvalho/mestrado/docs/01-fichas-individuais/10-ficha-promptszz.md)
* **Mecanismo Formal**:
  Em uma única passagem $O(1)$ de inferência, o modelo recebe a mensagem redigida do fix $\text{Msg}(c_{\text{fix}})$, o diff unificado $\text{Diff}(c_{\text{fix}})$ e o resumo dos commits candidatos $\mathcal{C}_{\text{cand}}$ que modificaram o contexto anteriormente, gerando uma cadeia explícita de raciocínio $r$ seguida do subconjunto de commits indutores:
  $$(r, \hat{C}_{\text{BIC}}) = f_{\text{LLM}}^{\text{CoT}}\left(\text{Msg}(c_{\text{fix}}), \text{Diff}(c_{\text{fix}}), \{(c, \text{Msg}(c), \text{Hunk}(c))\}_{c \in \mathcal{C}_{\text{cand}}}\right)$$

---

## 🏆 Estrato de Dominância e Como Extrair o Melhor do Prompt-SZZ

* **Estrato de Dominância**: **Estratos E1 e E2 — Bugs Localizados com Forte Sinal Semântico na Mensagem/Resumo dos Candidatos (Melhor Razão F1 / Latência entre os LLMs)**.
* **Por que é indispensável na Matriz 10x10**: Sem o `10-promptszz`, um revisor poderia perguntar: *"O AgentSZZ e o LLM4SZZ foram melhores porque a arquitetura deles é superior, ou simplesmente porque qualquer LLM com Chain-of-Thought acertaria?"* O `10-promptszz` isola exatamente o efeito do raciocínio em turno único versus a busca ativa (`AgentSZZ`) e o ranqueamento prévio de linhas (`LLM4SZZ`).

---

## 🛠️ Infraestrutura Local e Contrato de Execução

* **Diretório do Algoritmo**: `/home/artur-carvalho/mestrado/repos/10-promptszz`
* **Comando de Execução no Apache Flink**:
  ```bash
  python3 /home/artur-carvalho/mestrado/repos/10-promptszz/main.py \
    --benchmark /home/artur-carvalho/mestrado/experiments/00-flink-curadoria/flink_stratified_benchmark.json \
    --repo /home/artur-carvalho/mestrado/repos/00-flink \
    --output /home/artur-carvalho/mestrado/experiments/10-promptszz/predictions.json
  ```
* **Saída Padronizada**: `/home/artur-carvalho/mestrado/experiments/10-promptszz/predictions.json`
