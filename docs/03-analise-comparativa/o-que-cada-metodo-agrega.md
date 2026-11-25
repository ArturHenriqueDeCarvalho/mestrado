# Síntese Científica: O que Cada Algoritmo SZZ Agrega e Onde Cada um é Superior

> [!IMPORTANT]
> **Fundamentação Teórica (`DEC-008`, `DEC-010`, `DEC-012`, `DEC-013`)**: Este documento detalha a tese científica, a contribuição original e o **nicho exato de superioridade de cada um dos 10 algoritmos SZZ**, permitindo interpretar com precisão os resultados na base unificada do **Apache Flink** e o roadmap para as 20 bases empíricas.

---

## 🏛️ 1. Família Heurística Tradicional

### 1.1 B-SZZ (Śliwerski, Zimmermann & Zeller, ACM SIGSOFT FSE 2005)
* **Contribuição Original**: Estabeleceu o algoritmo seminal SZZ para identificar commits indutores de defeito cruzando o `git blame` nas linhas alteradas pelo commit de correção com links de bug trackers.
* **Onde é Superior**:
  - Em alterações atômicas e mono-linha (ex.: correção de um operador booleano ou uma constante), onde a linha modificada no fix é diretamente e sem ambiguidades a linha onde o bug nasceu.
  - Oferece a **maior taxa de revocação bruta (*High Raw Recall*)** e o menor custo computacional de execução ($O(1)$ chamadas de blame por arquivo).

### 1.2 AG-SZZ (Kim et al., IEEE/ACM ASE 2006)
* **Contribuição Original**: Introduziu filtros baseados em anotações de código e cabeçalhos de arquivo.
* **Onde é Superior**:
  - Em bases com alto uso de anotações sintáticas de frameworks (ex.: `@Override`, `@Deprecated`, `@SuppressWarnings` e anotações Spring/Jakarta).
  - Evita que modificações em metadados de compilação sejam falsamente apontadas como introdutoras de falha.

### 1.3 MA-SZZ (da Costa et al., Empirical Software Engineering 2017)
* **Contribuição Original**: Meta-algoritmo que formalizou o impacto de ignorar comentários, linhas em branco e alterações cosméticas na data de introdução do bug.
* **Onde é Superior**:
  - Em commits onde o desenvolvedor atualiza simultaneamente o código e a documentação (*Javadoc*, comentários inline, cabeçalhos de licença).
  - Elimina até 30% do ruído cosmético sem necessidade de compilar a árvore sintática completa.

---

## 🔬 2. Família Sintática e Refatoração

### 2.1 L-SZZ (Rosa et al., IEEE/ACM ICSE 2021 / JSS 2023)
* **Contribuição Original**: Integrador de análise sintática profunda via Árvore Sintática Abstrata (AST) utilizando a ferramenta `srcML 1.2.0`.
* **Onde é Superior**:
  - Em mutações cosméticas que alteram texto mas preservam a AST (ex.: quebra de linha de argumentos, adição de parênteses redundantes, indentação).
  - Comprovou experimentalmente a capacidade de **eliminar 50% dos falsos positivos** em comparação com algoritmos baseados em texto puro.

### 2.2 RA-SZZ (Neto et al., 2018; Fan et al., IEEE TSE 2021)
* **Contribuição Original**: Integração com o `RefactoringMiner 2.0` para rastrear histórico através de 15 operações de refatoração estrutural (extração de método, movimentação de classe, renomeação de variáveis).
* **Onde é Superior**:
  - Padrão-ouro em projetos maduros orientados a objetos onde classes são reorganizadas e métodos são extraídos.
  - No ecossistema Apache (126.526 commits), eliminou **6.409 commits incorretamente culpados pelo B-SZZ clássico (5,07% de ruído sistêmico)**.

### 2.3 SZZ Unleashed (Borg et al., ACM/IEEE ESEM 2019)
* **Contribuição Original**: Implementação baseada em Eclipse JGit que utiliza grafos de anotação de arquivos e Line Number Mapping via similaridade de Jaccard com busca em profundidade (*depth $\ge 3$*).
* **Onde é Superior**:
  - Em repositórios com histórico longo e complexo de merges e ramificações (como o Jenkins Core), onde a linha mudou de número dezenas de vezes antes da correção.

---

## 🤖 3. Família Baseada em Inteligência Artificial e LLMs

### 3.1 LLM-SZZ (Fan et al., ACM PACMSE / FSE 2024)
* **Contribuição Original**: Arquitetura reflexiva com *Prompt Chaining*, *Backtrace Decision* com corte Levenshtein ($\ge 0.5$) e desambiguação de commits emaranhados (*tangled commits*).
* **Onde é Superior**:
  - Em commits de segurança onde o patch de correção apenas **adiciona verificações defensivas** (*null checks*, limites de buffer) sem deletar nenhuma linha de código pré-existente (cenário onde o `git blame` tradicional falha 100% das vezes).
  - Desambigua commits mistos onde o desenvolvedor corrigiu o bug e aproveitou para fazer melhorias não relacionadas.

### 3.2 LLM4SZZ (Tang et al., 2025 - arXiv:2504.01404 / ACM TOSEM)
* **Contribuição Original**: Mecanismo adaptativo de **Ability Check** integrando duas frentes:
  1. *Rank-based Suspicious Statement Identification*: Ranqueia as declarações deletadas por probabilidade causal $P(\text{RootCause} \mid \text{Patch, Msg})$ para guiar o blame focado;
  2. *Context-Enhanced Candidate Assessment*: Fornece contexto semântico alargado para patches onde a causa raiz reside fora das linhas removidas.
* **Onde é Superior**:
  - Em patches com múltiplas linhas deletadas onde apenas uma sub-expressão é causal (*Tangled Commits* — `E4`), reduzindo o *Wasted Inspection Effort LOC* ao nível mais baixo da literatura.

### 3.3 AgentSZZ (Risse & Böhme, IEEE/ACM ASE 2026)
* **Contribuição Original**: Agente autônomo baseado no paradigma ReAct (Reasoning + Acting) que formula consultas dinâmicas de `git log` e `git diff` para inspecionar causalmente o histórico evolutivo.
* **Onde é Superior**:
  - Em falhas complexas multi-arquivo, regressões de concorrência (`E7`) e bugs arquiteturais que cruzam vários componentes do sistema distribuído.

### 3.4 Prompt-SZZ / CoT-SZZ (Baseline Canônico de Raciocínio)
* **Contribuição Original**: Aplicação de *Chain-of-Thought (CoT)* e *Zero-Shot Reasoning* direto sobre o diff unificado da correção e a mensagem do commit.
* **Onde é Superior**:
  - Como linha de base ágil e econômica para quantificar o ganho marginal de abordagens baseadas em agentes multi-turn (*AgentSZZ*) versus inferência direta em etapa única.

---

## 🎯 4. Matriz de Cobertura nos 8 Cenários de Erro (`E1` a `E8`)

| Cenário de Erro | Algoritmo Recomendado | Família | Justificativa Técnica |
| :--- | :---: | :---: | :--- |
| **E1 (Bugs Atômicos Diretos)** | `01-bszz` / `04-lszz` | Heurística / AST | Blame direto atinge alta precisão sem custo de inferência de IA. |
| **E2 (Ruído Cosmético & Metadados)** | `04-lszz` | AST (`srcML`) | AST descarta 100% de mudanças cosméticas sem custo de LLM. |
| **E3 (Refatorações Estruturais Java)** | `05-raszz` | Refatoração | `RefactoringMiner 2.0` rastreia movimentações de métodos com precisão determinística. |
| **E4 (Tangled & Large Patches)** | `08-llm4szz` | LLM Ability Check | Ranqueamento causal isola as declarações defeituosas dentre dezenas de mudanças cosméticas. |
| **E5 (Add-Only Fixes & Multi-Arquivo)**| `07-llm-szz` / `08-llm4szz` | LLM Contextual | Métodos heurísticos e sintáticos falham ($F_1 = 0.00$); apenas LLMs recuperam o contexto. |
| **E6 (Vulnerabilidades / CVEs)** | `07-llm-szz` | LLM Reflexivo | Conexão semântica entre a descrição da CVE no NVD e a introdução da vulnerabilidade. |
| **E7 (Concorrência & Estado Distribuído)**| `09-agentszz` | LLM ReAct Agent | Investigação multi-turn analisa locks, canais e condições de corrida entre múltiplos arquivos. |
| **E8 (Alta Latência de Verificação)** | `08-llm4szz` / `09-agentszz` | LLM Adaptativo | Resiliente ao acúmulo de commits intermediários durante o período dormente (>180 dias). |
