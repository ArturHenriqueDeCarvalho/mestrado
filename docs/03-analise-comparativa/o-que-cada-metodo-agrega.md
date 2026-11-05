# Síntese Científica: O que Cada Algoritmo SZZ Agrega e Onde Cada um é Superior

> [!IMPORTANT]
> **Fundamentação Teórica (`DEC-008`, `DEC-010`)**: Este documento detalha a tese científica, a contribuição original e o **nicho exato de superioridade de cada um dos 10 algoritmos SZZ**, permitindo interpretar com precisão os resultados na base unificada do **Apache Flink** e nas 10 bases históricas.

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

### 3.2 LLM4SZZ (Tang et al., 2025 - arXiv:2504.01404)
* **Contribuição Original**: Abordagem em duas fases: ranqueamento de linhas suspeitas com LLM e avaliação de contexto estendido para filtrar falsas causalidades no patch.
* **Onde é Superior**:
  - Em correções extensas com múltiplos blocos de código deletados, ranqueando com probabilidade semântica qual bloco continha a causa raiz da falha antes de invocar o rastreador de versão.

### 3.3 AgentSZZ (Risse & Böhme, IEEE/ACM ASE 2026)
* **Contribuição Original**: Agente autônomo baseado no paradigma ReAct que atua como um "detetive", formulando consultas dinâmicas de `git log` e `git diff` para inspecionar causalmente o histórico.
* **Onde é Superior**:
  - Em falhas complexas multi-arquivo e bugs arquiteturais que cruzam vários componentes do sistema (cenário muito comum no Apache Flink).

### 3.4 Prompt-SZZ / CoT-SZZ (Baseline Canônico de Raciocínio)
* **Contribuição Original**: Aplicação de *Chain-of-Thought (CoT)* e *Zero-Shot Reasoning* direto sobre o diff unificado da correção e a mensagem do commit.
* **Onde é Superior**:
  - Como linha de base ágil e econômica para quantificar o ganho marginal de abordagens baseadas em agentes multi-turn (*AgentSZZ*) versus inferência direta em etapa única.
