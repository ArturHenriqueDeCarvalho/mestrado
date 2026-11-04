# O Que Cada Método Agrega: Análise Cumulativa e Síntese Técnico-Científica

---

## 1. Propósito Epistemológico

Na defesa do **Artigo Científico Preparatório (Banca de Dezembro de 2026)** e na **Dissertação de Mestrado**, é imperativo demonstrar domínio rigoroso sobre a genealogia técnica e matemática de cada método analisado, respondendo com precisão:
1. *Qual limitação algorítmica ou metodológica motivou a criação do método?*
2. *Qual mecanismo computacional/matemático exato foi introduzido para superá-la?*
3. *Qual evidência quantitativa comprova seu ganho e onde residem suas fronteiras de falha?*

Abaixo sintetizamos o aporte técnico-científico exclusivo de cada uma das 6 pesquisas do nosso corpus.

---

## 2. Aporte Técnico Detalhado por Pesquisa

### 🔬 Pesquisa 1 — LLM-SZZ (Siqi Fan et al., 2024)
* **O que agrega tecnicamente**:
  - **Fusão Semântica Multimodal (Descrição de CVE NVD + Unified Diff Anotado)**: Supera a cegueira semântica das variantes estáticas de SZZ e de redes baseadas apenas em grafos de código (`NEURAL-SZZ` / HAN) ao injetar a descrição em linguagem natural da CVE juntamente com o hunk numerado do commit de correção via *Prompt Chaining* reflexivo.
  - **Rastreamento Híbrido em Profundidade (*Vulnerability Backtrace Decision*)**: Substitui o retrocesso cego de linhas do `V-SZZ` por um filtro sintático de **Similaridade de Edição de Levenshtein** calibrado em $\tau = 0.5$ (`Levenshtein.ratio >= 0.5` sobre strings sem *whitespace*) acoplado ao julgamento semântico do LLM, que detém autoridade autônoma para emitir o comando de parada (`-1`) quando a linha ancestral deixa de ter relação causal com a vulnerabilidade.
  - **Desambiguação de *Tangled Commits* via *Optimal Candidate Selection* e *Voting Strategy***: Agrega os candidatos por arquivo e utiliza uma etapa final de seleção pelo LLM estabilizada por votação majoritária (3 a 5 execuções via `collections.Counter`), atingindo $F_1 = 0.834$ ($\text{FPR} = 0.162$) em C/C++ e $F_1 = 0.774$ ($\text{FPR} = 0.232$) em Java, além de $0.900$ de Recall em vulnerabilidades profundas (*deep vulnerabilities*).

---

### 🔬 Pesquisa 2 — PySZZ v2 (Giovanni Rosa et al., ICSE 2021 / JSS 2023)
* **O que agrega tecnicamente**:
  - **Oráculo Informado por Desenvolvedores via Árvores Sintáticas `spaCy`**: Elimina o viés de validação circular do SZZ minerando **19.603.736 commits** do GH Archive com 3 heurísticas de processamento de linguagem natural (H1: exclusão de reverts; H2: verificação se o verbo `introduce` é ancestral sintático do hash na árvore de dependências do `spaCy`; H3: filtro fino gramatical e *stop-words*), seguido de validação manual conservadora por 4 avaliadores independentes, resultando em `oracle_all` (1.115 BFCs em 8 linguagens) e `oracle_issues` (129 BFCs).
  - **Arquitetura Modular Orientada a Objetos (`AbstractSZZ`)**: Unifica 9 variantes e ferramentas (`B-SZZ`, `AG-SZZ`, `MA-SZZ`, `L-SZZ`, `R-SZZ`, `RA-SZZ*`, `SZZ@PYD`, `SZZ@UNL`, `SZZ@OPN`, além de `ASZZ` e `DFSZZ`), integrando `srcML` para poda de comentários, `RefactoringMiner 2.0` para refatorações Java e flags `-M`/`-C` do `git blame`.
  - **Demonstração da Superioridade do `R-SZZ` e Diagnóstico dos 311 Casos de Falha Unânime**: Comprova que a heurística de seleção do commit mais recente (`R-SZZ`) combinada ao filtro de data da issue (`issue_date_filter: true`) atinge a maior precisão ($73\%$) e $F_1$ ($0.64$), além de categorizar por que todas as variantes falham em correções puramente aditivas (ex.: guardas `if (x != null)`).

---

### 🔬 Pesquisa 3 — SZZ Unleashed (Markus Borg et al., 2019)
* **O que agrega tecnicamente**:
  - **Motor Java Nativo em `Eclipse JGit` com *Line Number Mapping* via Distância de Jaccard**: Dispensa chamadas lentas ao binário CLI do Git operando diretamente sobre objetos internos do JGit (`FileAnnotationGraph`, `DistanceIntroducerFinder`) e mapeia blocos de linhas modificadas entre revisões através da distância de conjuntos de Jaccard ($d_J(A,B) = 1 - \frac{|A \cap B|}{|A \cup B|}$) com busca em profundidade configurável (`depth = 3`).
  - **Engenharia de 16 Features JIT Incluindo Acoplamento Evolutivo (`code-maat`)**: Introduz, além das métricas tradicionais de churn, difusão, entropia e experiência, 3 métricas de acoplamento temporal (`Ft14`, `Ft15`, `Ft16` extraídas pelo `code-maat 1.1`) sobre 12 anos do **Jenkins Core** (26.378 commits).
  - **Desmascaramento do Vazamento Temporal em Validação Cruzada (*10-Fold CV vs. Online Change Classification*)**: Demonstra empiricamente que a validação cruzada estratificada infla artificialmente o Recall em quase o dobro ($0.212$ vs. $0.104$ com SMOTE) por violar a cronologia dos commits, estabelecendo que a avaliação *Time-Sensitive* (`OCC` com `SMOTE+Tomek`, $F_1 = 0.137$) é obrigatória para refletir cenários reais de produção.

---

### 🔬 Pesquisa 4 — SZZ-TSE (Yuanrui Fan et al., IEEE TSE 2019/2021)
* **O que agrega tecnicamente**:
  - **Auditoria Controlada de Ruído de Rotulagem sobre 126.526 Commits Apache**: Compara sistematicamente modelos JIT treinados com rótulos de `B-SZZ` (`buggy_B2`), `AG-SZZ` (`buggy_AG`) e `MA-SZZ` (`buggy_MA`) avaliados contra o oráculo consciente de refatoração `RA-SZZ` (`buggy_RA`) em 10 projetos Apache (`activemq`, `camel`, `derby`, `geronimo`, `hbase`, `hcommon`, `mahout`, `openjpa`, `pig`, `tuscany`), com remoção prévia de multicolinearidade via VIF/Spearman (`collinearity.csv`) e 1.000 iterações de *Out-of-Bag Bootstrap*.
  - **Descoberta do Custo Oculto de Esforço Desperdiçado (*Wasted Inspection Effort LOC*)**: Prova que métricas globais como AUC e F1 mascaram o impacto industrial do ruído: embora o `B-SZZ` não degrade significativamente o AUC de Random Forest ou Regressão Logística, ele **infla em 9% a 10% o número de linhas de código inspecionadas inutilmente em falsos positivos (`waste_effort`)**, enquanto o `AG-SZZ` reduz significativamente o AUC/F1/G-Mean em 1%–5% e eleva o desperdício de esforço em até 15%.
  - **Instabilidade de Interpretabilidade (Scott-Knott ESD)**: Demonstra via agrupamento estatístico `ScottKnottESD` que o ruído de `B-SZZ` e `AG-SZZ` distorce severamente o ranking de importância das métricas secundárias e terciárias dos classificadores.

---

### 🔬 Pesquisa 5 — CC2Vec (Thong Hoang et al., ACM/IEEE ICSE 2020)
* **O que agrega tecnicamente**:
  - **Rede de Atenção Hierárquica Tripla (`WordRNN` $\to$ `SentRNN` $\to$ `HunkRNN` via Bi-GRU)**: Modela a estrutura tridimensional de tensores de diffs ($\mathcal{X} \in \mathbb{Z}^{N \times H \times L \times W}$) separadamente para código adicionado ($e_a$) e código removido ($e_r$), aplicando pesos de atenção em nível de token, linha e hunk.
  - **Camada de Comparação Não-Linear de 5 Famílias (6 Operadores)**: Captura a divergência semântica entre $e_a$ e $e_r$ concatenando Subtração ($e_a - e_r$), Produto de Hadamard ($e_a \odot e_r$), Similaridades Cosseno e Euclidiana, Rede Feed-Forward ($e_{NN}$) e **Neural Tensor Network** ($e_{NT} = \text{ReLU}(e_a^T T^{[1:k]} e_r + V[e_a \parallel e_r] + b)$) em um vetor distribuído denso `cc2ftr` ($\in \mathbb{R}^{3d+4}$), pré-treinado de forma auto-supervisionada para prever palavras da primeira linha da mensagem de commit.
  - **Transferência Universal para 3 Tarefas Downstream**: Eleva o BLEU-4 do `NNGen` em +25.0% ($16.42 \to 20.53$) na geração de logs; atinge $\text{AUC} = 0.909$ e $F_1 = 0.850$ em 82.000 patches do Linux Kernel (`PatchNetExtended`); e supera o `DeepJIT` em +7.0% ($\text{AUC} = 0.822$ no Qt) e +7.7% ($\text{AUC} = 0.809$ no OpenStack) na predição JIT (`DeepJITExtended`).

---

### 🔬 Pesquisa 6 — JIT-Smart & JIT-Defect4J (Xiangping Chen et al., ACM FSE 2024 / Chao Ni et al., ESEC/FSE 2022)
* **O que agrega tecnicamente**:
  - **Fusão Multimodal Semântica + Especialista no Nível de Commit (`CodeBERT` + 14 Expert Features)**: Une o vetor contextual `<s>` ($d=768$) do `microsoft/codebert-base` (RoBERTa 12-layer) com a projeção densa não-linear $\tanh(\text{Linear}_{14 \to 768}(f_{\text{expert}}))$ das 14 métricas de Kamei (`RobertaClassificationHead`).
  - **Defect Localization Network (`DLN` / `HAN_MODEL` BiLSTM) Supervisionada por Rótulos de Linha**: Supera a localização post-hoc cega baseada em atenção do `JIT-Fine` ao introduzir uma rede BiLSTM hierárquica de duas camadas (nível de palavra com agregação de atenção `need_aggregation=True` e nível de linha sem colapso dimensional `need_aggregation=False`), treinada diretamente com os rótulos reais de cada linha modificada (`line_label`).
  - **Co-Otimização Multi-Tarefa com `MultiFocalLoss`**: Mitiga o desbalanceamento severo tanto no nível de commit quanto no nível de linha através da perda focal ponderada $\mathcal{L}_{\text{total}} = 0.3\mathcal{L}_{\text{Focal}}(z_{\text{fused}}, y_{\text{commit}}) + 0.7\mathcal{L}_{\text{Focal}}(z_{\text{han}}, y_{\text{line}})$ ($\alpha=0.25, \gamma=2.0$) e da fusão de logits $z_{\text{fused}} = \frac{1}{2}(z_{\text{commit}} + \overline{z}_{\text{han}})$, reduzindo drasticamente os alarmes falsos iniciais (`IFA`: de $96.618$ no CodeBERT isolado para patamares sub-unitários na DLN) e estabelecendo o estado da arte no benchmark **JIT-Defect4J** (21 projetos Java).
