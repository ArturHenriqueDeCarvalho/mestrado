# Ficha de Pesquisa Individual: JIT-Smart (JIT-Defect4J / JIT-Fine)

---

## 1. Identificação

* **Título do Artigo Principal**: *JIT-Smart: A Multi-Task Learning Framework for Just-In-Time Defect Prediction and Localization*
* **Autores**: Xiangping Chen, Furen Xu, Yuan Huang, Neng Zhang, Zibin Zheng
* **Instituições**: Sun Yat-sen University (Guangzhou, China) e Zhejiang University (Hangzhou, China)
* **Veículo de Publicação / Ano**: *Proceedings of the ACM on Software Engineering* (PACMSE), Volume 1, Issue FSE (ACM International Conference on the Foundations of Software Engineering), Julho de 2024.
* **DOI / Link Oficial**: [10.1145/3643727](https://doi.org/10.1145/3643727)
* **Artigo Seminal da Linhagem / Baseline**:
  * **Título**: *The Best of Both Worlds: Integrating Semantic Features with Expert Features for Defect Prediction and Localization*
  * **Autores**: Chao Ni, Wei Wang, Kaiwen Yang, Xin Xia, Kui Liu, David Lo
  * **Veículo**: *Proceedings of the 30th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE 2022)*, pp. 672–683.
  * **DOI**: [10.1145/3540250.3549165](https://doi.org/10.1145/3540250.3549165)
* **Repositórios de Código-Fonte e Replicação**:
  * JIT-Smart (FSE 2024): [`https://github.com/JIT-A/JIT-Smart`](https://github.com/JIT-A/JIT-Smart) (Clone local em [`/home/artur-carvalho/mestrado/repos/06-jit-smart/jit-smart`](file:///home/artur-carvalho/mestrado/repos/06-jit-smart/jit-smart))
  * JIT-Fine (ESEC/FSE 2022): [`https://github.com/jacknichao/JIT-Fine`](https://github.com/jacknichao/JIT-Fine) (Clone local em [`/home/artur-carvalho/mestrado/repos/06-jit-smart/jit-fine`](file:///home/artur-carvalho/mestrado/repos/06-jit-smart/jit-fine))
* **Rastreabilidade de Governança**: Registrado em DEC-001 (Amostragem empírica via replication packages), DEC-002 (Execução Local-First) e DEC-005 (Retificação do DOI/arXiv e linhagem documental em [`docs/04-governanca/diario-de-decisoes.md`](file:///home/artur-carvalho/mestrado/docs/04-governanca/diario-de-decisoes.md)).

---

## 2. Problema

* **Problema Abordado**: `[FATO DOCUMENTADO]` A garantia de qualidade de software através da predição de defeitos Just-in-Time (JIT-DP - *Just-In-Time Defect Prediction*) e da localização de defeitos Just-in-Time (JIT-DL - *Just-In-Time Defect Localization*).
* **Lacunas Críticas na Literatura Anterior**:
  1. *Desconexão entre Granularidades*: Estudos tradicionais tratavam JIT-DP (nível de commit, determinando **se** uma alteração induz defeito) e JIT-DL (nível de linha de código, localizando **onde** na alteração o defeito reside) de maneira estritamente desacoplada ou sequencial.
  2. *Supervisão Indireta e Fraca em Linhas de Código*: Abordagens prévias de Deep Learning para JIT-DL (como JITLine e JIT-Fine) dependiam de mecanismos post-hoc e heurísticos para inferir defeitos em linhas — tais como pesos de atenção de transformadores (*attention weights* da última camada de CodeBERT) ou aproximações via LIME (*Local Interpretable Model-agnostic Explanations*) —, sem nunca introduzir os rótulos reais de linha de código (*ground-truth line labels*) durante o treinamento supervisionado.
  3. *Isolamento de Características Semânticas vs. Especialistas*: Modelos baseados exclusivamente em métricas de processo/histórico (como LApredict) ignoram a sintaxe e semântica do diff; inversamente, redes neurais profundas puras (como DeepJIT e CC2Vec) negligenciam o histórico de esforço e dispersão do repositório. O JIT-Fine introduziu a fusão dessas características no nível de commit, mas não resolveu a aprendizagem supervisionada no nível de linha.
  4. *Desbalanceamento Severo de Classes*: A proporção de linhas defeituosas em commits é drasticamente minoritária (menos de 5% das linhas modificadas em média), gerando taxas proibitivas de alarmes falsos (*False Alarms*) quando não há funções de perda adaptadas.

---

## 3. Perguntas de Pesquisa / Tarefas de Avaliação

As perguntas de pesquisa formuladas *verbatim* no estudo JIT-Smart são:

* **RQ1**: *How effective is JIT-Smart in just-in-time defect prediction task?*
  - Avalia o desempenho na classificação binária de commits (indutor de defeito vs. limpo) em comparação com as linhas de base estado da arte (LApredict, Deeper, DeepJIT, CC2Vec, JITLine e JIT-Fine).
* **RQ2**: *How well can JIT-Smart locate defective lines in just-in-time defect localization task?*
  - Avalia a capacidade de identificar e ranquear as linhas de código defeituosas dentro dos commits sob esforço inspecionado reduzido (Top-5, Top-10, Recall@20%Effort, IFA).
* **RQ3**: *What is the accuracy of JIT-Smart compared to the state-of-the-art baseline under the cross-project experimental setting?*
  - Avalia o poder de generalização do modelo quando treinado em um conjunto de projetos de software e testado em um projeto não visto (*cross-project defect prediction and localization*).
* **RQ4**: *How do the different loss function weight assignments affect the performance of JIT-Smart?*
  - Analisa a sensibilidade e o equilíbrio da função de perda multi-tarefa variando os pesos $w_{dp}$ (nível de commit) e $w_{dl}$ (nível de linha) entre 0.1 e 0.9.

---

## 4. Hipóteses

* **Hipótese 1 (H1 - Aprendizado Co-Supervisionado Multi-Tarefa)**: `[INTERPRETAÇÃO]` O co-treinamento simultâneo entre a predição no nível de commit (JIT-DP) e a localização no nível de linha (JIT-DL) permite que os gradientes de ambas as tarefas guiem a representação latente compartilhada, melhorando a precisão em ambos os níveis em comparação ao treinamento isolado.
* **Hipótese 2 (H2 - Supervisão Direta de Linhas via DLN)**: `[INTERPRETAÇÃO]` Introduzir explicitamente os rótulos reais de linha de código através de uma rede especializada de localização de defeitos (DLN - *Defect Localization Network*) reduz drasticamente os alarmes iniciais falsos (IFA) e aumenta o acerto nas primeiras linhas inspecionadas (Top-k Acc) em relação a aproximações baseadas em pesos de atenção desprovidas de supervisão.
* **Hipótese 3 (H3 - Complementaridade de Espaços de Atributos)**: `[FATO DOCUMENTADO]` A concatenação de representações semânticas profundas aprendidas do código (CodeBERT) com 14 métricas clássicas de engenharia de software (*expert features*) produz separabilidade superior à utilização isolada de qualquer um dos conjuntos.

---

## 5. Objetivos

1. **Objetivo Metodológico**: Desenvolver uma arquitetura neural unificada de aprendizado multi-tarefa (*multi-task co-learning*) que execute simultaneamente JIT-DP e JIT-DL.
2. **Objetivo Arquitetural**: Projetar a DLN (*Defect Localization Network*), fundamentada em Redes de Atenção Hierárquica (HAN - *Hierarchical Attention Network*), compartilhando embeddings de tokens com o encoder CodeBERT e aplicando atenção em nível de palavra e nível de linha.
3. **Objetivo Teórico-Empírico**: Formular uma função de perda adaptativa (*MultiFocalLoss*) para mitigar o desbalanceamento extremo de classes presente tanto entre commits limpos/defeituosos quanto entre linhas normais/defeituosas.
4. **Objetivo de Benchmark**: Avaliar rigorosamente a técnica sobre o benchmark JIT-Defect4J (21 projetos Java), fornecendo dados de replicação para cenários *within-project* e *cross-project*.

---

## 6. Contexto

* **Linguagem Alvo**: Java (projetos do ecossistema Apache e Defects4J).
* **Ambiente de Versionamento**: Git e repositórios de rastreamento de issues (JIRA / Bugzilla).
* **Natureza da Mineração**: Repositórios de código aberto consolidados com longo histórico evolutivo.
* **Paradigma Tecnológico**: Deep Learning com Modelos de Linguagem Pré-treinados de Código (*Pre-trained Code Language Models - CodeBERT/RoBERTa*) associados a Redes Neurais Recorrentes Bidirecionais (BiLSTM) e Redes de Atenção Hierárquica (HAN).

---

## 7. Dados

* **Origem do Benchmark**: **JIT-Defect4J**, construído sobre o dataset seminal **LLTC4J** (*Large-scale Line-level Testable Commits for Java*, Herbold et al., TSE 2022).
* **Extensão Realizada pelo JIT-Fine e JIT-Smart**:
  1. Coleta tanto de commits defeituosos (*bug-inducing*) quanto de commits limpos (*clean commits*).
  2. Extração manual e automatizada dos rótulos exatos de linha de código introduzidos nos commits indutores de defeito (e não apenas nos commits de correção).
* **Projetos Selecionados (21 Projetos Java)**:
  1. `commons-math`
  2. `commons-lang`
  3. `commons-configuration`
  4. `commons-collections`
  5. `ant-ivy`
  6. `commons-compress`
  7. `commons-io`
  8. `commons-net`
  9. `parquet-mr`
  10. `commons-vfs`
  11. `opennlp`
  12. `commons-digester`
  13. `commons-dbcp`
  14. `giraph`
  15. `commons-jcs`
  16. `commons-bcel`
  17. `commons-codec`
  18. `commons-beanutils`
  19. `commons-validator`
  20. `gora`
  21. `commons-scxml`
* **Divisão dos Dados**:
  - `changes_train.pkl` / `features_train.pkl` / `train_buggy_commit_lines_df.pkl`
  - `changes_valid.pkl` / `features_valid.pkl` / `valid_buggy_commit_lines_df.pkl`
  - `changes_test.pkl` / `features_test.pkl` / `test_buggy_commit_lines_df.pkl`
* **Formato dos Dados no Pacote**: Arquivos Pickle (`.pkl`) contendo tuplas de hashes de commit, rótulos booleanos, mensagens de commit, dicionários de linhas adicionadas/removidas, vetores numéricos de 14 métricas e matrizes de rótulos por linha de código.

---

## 8. Metodologia

O fluxo metodológico estrito segue a cadeia sequencial:
$$\text{DATA} \longrightarrow \text{PREPROCESSING} \longrightarrow \text{METHOD} \longrightarrow \text{CLASSIFICATION} \longrightarrow \text{METRICS} \longrightarrow \text{RESULTS}$$

```
+--------------------------------------------------------------------------------------------------+
| 1. DATA: JIT-Defect4J (21 Projetos Java: 14 Change Metrics, Diffs de Commits, Rótulos de Linha) |
+--------------------------------------------------------------------------------------------------+
                                                |
                                                v
+--------------------------------------------------------------------------------------------------+
| 2. PREPROCESSING: Tokenização BPE CodeBERT (max 512 tokens), Extração de 14 Expert Features,    |
|    Estruturação Hierárquica em Matriz 2D: [Linhas x Palavras] (max 256 linhas x 64 tokens)      |
+--------------------------------------------------------------------------------------------------+
                                                |
                                                v
+--------------------------------------------------------------------------------------------------+
| 3. METHOD: Co-Aprendizado Multi-Tarefa (JIT-Smart)                                               |
|    - Ramo Commit (JIT-DP): CodeBERT RoBERTa Encoder + Projeção Densa tanh(14 Expert Features)    |
|    - Ramo Linha (JIT-DL): DLN Hierarchical Attention Network (Word BiLSTM + Line BiLSTM + Attn)  |
|    - Otimização Conjunta: MultiFocalLoss (alpha=0.25, gamma=2), Perda = 0.3*L_dp + 0.7*L_dl      |
+--------------------------------------------------------------------------------------------------+
                                                |
                                                v
+--------------------------------------------------------------------------------------------------+
| 4. CLASSIFICATION:                                                                              |
|    - Commit-level: Fusão das Probabilidades Sigmoid( (Logits_commit + mean(Logits_DLN)) / 2 )    |
|    - Line-level: Softmax binário por linha através da camada linear final da DLN                 |
+--------------------------------------------------------------------------------------------------+
                                                |
                                                v
+--------------------------------------------------------------------------------------------------+
| 5. METRICS:                                                                                      |
|    - Commit: AUC, F1, DistHeaven, FAR, Recall@20%Effort, Effort@20%Recall, P_opt                 |
|    - Linha: Top-1-ACC, Top-5-ACC, Top-10-ACC, Recall@20%Effort_line, IFA                         |
+--------------------------------------------------------------------------------------------------+
                                                |
                                                v
+--------------------------------------------------------------------------------------------------+
| 6. RESULTS: JIT-Smart supera todos os baselines (CC2Vec, DeepJIT, JITLine, JIT-Fine)            |
|    com redução substancial de falso alarme e ganhos expressivos na localização de linhas         |
+--------------------------------------------------------------------------------------------------+
```

### Detalhamento das Etapas:
1. **Pré-Processamento**:
   - Para o ramo do commit, a mensagem do commit e o diff de código são tokenizados usando o vocabulário Byte-Pair Encoding (BPE) do CodeBERT (truncados em 512 tokens).
   - As 14 métricas tradicionais de processo/produto de Kamei et al. são normalizadas e convertidas para ponto flutuante:
     - Métricas de Difusão: *NS* (Number of Modified Subsystems), *ND* (Number of Modified Directories), *NF* (Number of Modified Files), *Entropy*.
     - Métricas de Tamanho: *LA* (Lines of Code Added), *LD* (Lines of Code Deleted), *LT* (Lines of Code in Files before change).
     - Métricas de Histórico: *NDEV* (Number of Developers), *AGE* (Age from last change), *NUC* (Number of Unique Changes).
     - Métricas de Experiência: *EXP* (Developer Experience), *REXP* (Recent Experience), *SEXP* (Subsystem Experience).
     - Métrica de Propósito: *FIX* (Indica se o commit é de correção).
   - Para a DLN, o diff é fatiado linha a linha em uma estrutura bidimensional (máximo de 256 linhas por alteração, e no máximo 64 tokens por linha de código).
2. **Arquitetura da DLN (*Defect Localization Network*)**:
   - Compartilha a matriz de pesos de embedding (`encoder.embeddings.word_embeddings`) com o CodeBERT.
   - Nível Palavra: BiLSTM com dimensão oculta de 256 unidades seguido de camada de Atenção com agregação linear, comprimindo os tokens de cada linha em um vetor de estado.
   - Nível Linha: BiLSTM com dimensão oculta de 256 unidades recebendo a sequência de vetores de linha, mantendo a dimensionalidade sem compressão temporal final (`need_aggregation=False`).
   - Camada Linear de Classificação: Projeção densa de 512 para 128 neurônios com ativação `Tanh` e projeção para 2 classes com Dropout de 0.5.
3. **Função de Perda Adaptativa (*MultiFocalLoss*)**:
   - Para contrabalançar o desbalanceamento severo:
     $$\mathcal{L}_{focal} = - \alpha_t (1 - p_t)^\gamma \log(p_t)$$
     onde $\alpha = 0.25$ e $\gamma = 2.0$.
   - A perda global multi-tarefa pondera ambas as tarefas:
     $$\mathcal{L}_{total} = w_{dp} \cdot \mathcal{L}_{commit} + w_{dl} \cdot \mathcal{L}_{line}$$
     com configuração ótima demonstrada em $w_{dp} = 0.3$ e $w_{dl} = 0.7$.

---

## 9. Ferramentas

* **Framework de Deep Learning**: PyTorch (`torch==1.9.0+cu111` ou versões equivalentes para CPU/CUDA).
* **Biblioteca de Modelos de Linguagem**: Hugging Face `transformers==4.9.1` (modelo base `microsoft/codebert-base`).
* **Processamento de Dados**: Python 3.8, Pandas, NumPy, Scikit-learn, Pickle, OpenPyXL.
* **Ambiente de Treinamento e Scripts**: Shell Bash (`train_jitsmart.sh`, `train_jitfine.sh`, `train_jitsmart_loss_weight.sh`).
* **Análise Estatística dos Baselines**: R (com pacotes `tidyverse`, `ScottKnottESD`, `effsize`, `pROC`).

---

## 10. Algoritmos e Classificadores

* **Modelo Proposto**:
  - **JIT-Smart**: Rede neural multi-tarefa acoplando CodeBERT (RoBERTa 12-layer), Classificador Linear com 14 Métricas Especialistas, e DLN (Hierarchical Attention Network BiLSTM).
* **Linhas de Base (Baselines Comparados)**:
  1. **LApredict** (Kamei et al., TSE 2013): Modelo linear não-supervisionado / supervisionado clássico baseado puramente nas 14 métricas de mudança.
  2. **Deeper** (Yang et al., FSE 2015): Autoencoder profundo para extração de atributos e classificação com árvore de decisão / regressão logística.
  3. **DeepJIT** (Hoang et al., MSR 2019): Rede neural convolucional (CNN) profunda de múltiplos canais modelando mensagem de commit e diffs de código.
  4. **CC2Vec** (Hoang et al., ICSE 2020): Modelo de atenção hierárquica guiado por mensagens para aprender representações vetoriais de commits.
  5. **JITLine** (Pornprasit & Tantithamthavorn, TSE 2021): Random Forest / XGBoost sobre métricas de mudança associado a LIME e contagem de frequência de palavras para localização de linhas.
  6. **JIT-Fine** (Ni et al., ESEC/FSE 2022): Modelo baseado em CodeBERT + 14 Expert Features com localização de linhas via pesos de atenção desprovida de supervisão direta de linhas.

---

## 11. Métricas

### A. Métricas no Nível de Commit (JIT-DP):
1. **AUC-ROC**: Área sob a curva ROC (capacidade de discriminação global independente de limiar).
2. **F1-Score**: Média harmônica entre Precisão e Revocação (limiar padrão 0.5).
3. **FAR (False Alarm Rate)**: Taxa de alarmes falsos ($\frac{FP}{FP + TN}$).
4. **DistHeaven**: Distância Euclidiana até o ponto ótimo de predição perfeita $(FAR=0, Recall=1)$:
   $$\text{DistHeaven} = \sqrt{\frac{(1 - Recall)^2 + (0 - FAR)^2}{2}}$$
5. **Recall@20%Effort**: Revocação de commits defeituosos inspecionando-se no máximo 20% das linhas de código modificadas acumuladas.
6. **Effort@20%Recall**: Fração de esforço de código necessária para alcançar 20% de revocação dos defeitos.
7. **$P_{opt}$**: Métrica de esforço normalizada de Chen et al. calculada pela área sob a curva de revocação cumulativa por esforço.

### B. Métricas no Nível de Linha (JIT-DL):
1. **Top-k Accuracy (Top-1, Top-5, Top-10)**: Proporção de linhas defeituosas identificadas entre as primeiras $k$ linhas ranqueadas.
2. **Recall@20%Effort_line**: Proporção de linhas defeituosas recuperadas inspecionando as primeiras 20% das linhas da alteração.
3. **Effort@20%Recall_line**: Esforço em percentual de linhas para encontrar 20% das linhas defeituosas.
4. **IFA (Initial False Alarms)**: Quantidade de linhas limpas inspecionadas incorretamente antes que a primeira linha genuinamente defeituosa seja encontrada.

---

## 12. Resultados

### A. Desempenho dos Baselines no Benchmark JIT-Defect4J (Commit-level):
*Registrado diretamente nos artefatos oficiais de resultado do repositório (`baselines/results/result.csv`):*

| Método | F1-Score | AUC-ROC | Recall@20%Effort | Effort@20%Recall | $P_{opt}$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **LApredict** | 0.0591 | 0.6938 | 0.6253 | 0.0198 | 0.8137 |
| **Deeper** | 0.2455 | 0.6819 | 0.6379 | 0.0209 | 0.8273 |
| **DeepJIT** | 0.2927 | 0.7748 | 0.6758 | 0.0138 | 0.8596 |
| **CC2Vec** | 0.2445 | 0.7906 | 0.6758 | 0.0139 | 0.8597 |

### B. Estudos de Ablação Documentados no Repositório Oficial:
Os autores documentam os resultados das arquiteturas monolíticas isoladas vs. JIT-Smart:

* **Tentativa 1 (Apenas CodeBERT isolado com modelagem por camadas)**:
  - *Commit-level*: F1 = 0.456, AUC = 0.887, Recall@20%Effort = 0.813, Effort@20%Recall = 0.012, $P_{opt}$ = 0.943.
  - *Line-level*: Top-5-ACC = 0.231, Top-10-ACC = 0.235, Recall@20%Effort = 0.259, Effort@20%Recall = 0.294, **IFA = 96.618**.
  - *Diagnóstico*: Sem a DLN supervisionada, o IFA explode para quase 100 linhas inspecionadas em falso e o acerto no Top-5 cai para 23.1%.
* **Tentativa 2 (Apenas DLN isolada sem CodeBERT de commit)**:
  - *Commit-level*: F1 = 0.360, AUC = 0.853, Recall@20%Effort = 0.782, Effort@20%Recall = 0.512, $P_{opt}$ = 0.935.
  - *Line-level*: Top-5-ACC = 0.430, Top-10-ACC = 0.290, Recall@20%Effort = 0.605, Effort@20%Recall = 0.290, **IFA = 0.405**.
  - *Diagnóstico*: A DLN isolada alcança excelente IFA (0.4), mas perde poder discriminatório global no nível de commit (F1 cai para 0.360).
* **JIT-Smart Completo (Multi-Task Co-Learning)**:
  - `[FATO DOCUMENTADO]` A união das duas redes com a ponderação ótima de perda ($0.3 \cdot \mathcal{L}_{dp} + 0.7 \cdot \mathcal{L}_{dl}$) e fusão dos logits combina o alto poder preditivo de commit do CodeBERT (AUC > 0.89) com a extrema precisão localizadora da DLN supervisionada (baixo IFA e alto Top-5), superando o JIT-Fine tanto em predição quanto em redução de falsos alarmes de linha.

---

## 13. Ameaças à Validade

* **Validade de Construção**:
  - A marcação das linhas defeituosas no JIT-Defect4J depende de oráculos empíricos derivados de commits de correção e rastreadores de bugs (SZZ e anotação manual). Se o oráculo original contiver ruídos de linhas cosmeticamente modificadas, a DLN pode aprender ruídos pontuais.
* **Validade Interna**:
  - Dependência de hiperparâmetros de ponderação de perda ($w_{dp}, w_{dl}$) e taxa de decaimento do `MultiFocalLoss`. O estudo mitiga isso conduzindo a RQ4 para varredura completa da grade de parâmetros.
  - Variabilidade estocástica do pré-treinamento de Transformers e inicialização de pesos BiLSTM (mitigada por fixação explícita de `set_seed(42)` e sementes do PyTorch/cuDNN).
* **Validade Externa**:
  - Os 21 projetos avaliados são exclusivamente escritos em Java e hospedados no ecossistema de código aberto. Os resultados podem diferir em linguagens não orientadas a objetos, linguagens fracamente tipadas (JavaScript, Python) ou sistemas legados fechados.

---

## 14. Artefatos Disponibilizados

* **Código-Fonte Completo**:
  - Pacote JIT-Smart: scripts de treinamento (`train_jitsmart.sh`, `train_jitsmart_loss_weight.sh`), modelo neural (`JITSmart/concat/model.py`), scripts de pré-processamento de linhas (`JITSmart/process and label defect code lines/`).
  - Pacote JIT-Fine: rotinas de base para LApredict, Deeper, DeepJIT, CC2Vec, JITLine.
* **Pacote de Dados Estruturado (`data.zip`)**:
  - Arquivo arquivado de 75 MB contendo dados processados em `.pkl` para todos os 21 projetos (sem necessidade de clonar gigabytes de repositórios externos).
  - Anotações de linhas defeituosas em arquivos `.pkl` e planilhas `.xlsx` em `JITSmart/process and label defect code lines/`.

---

## 15. Replicabilidade

* **Classificação de Replicabilidade**: **Alta / Imediata (Pacote Completo Pré-estruturado)**.
* **Dependência de Treinamento**:
  - Treinamento completo (*fine-tuning* do CodeBERT por 50 épocas em 21 projetos) exige GPU de alta performance (CUDA).
  - No entanto, a **inferência**, auditoria arquitetural, validação de baselines e extração de métricas operam de forma nativa e rápida em **CPU local** com zero custo financeiro.

---

## 16. Protocolo de Replicação Local (17 Itens)

1. **Hardware Mínimo Recomendado**: Processador x86_64 multinúcleo (o Intel Core i7-1255U local com 12 threads é plenamente suportado para inferência e inspeção de dados), 8 GB de memória RAM (14 GB disponíveis localmente).
2. **Sistema Operacional Homologado**: Linux Ubuntu 22.04 LTS / Linux x86_64.
3. **Versão do Python**: Python 3.8 ou compatível.
4. **Dependências Primárias**: `torch`, `transformers`, `scikit-learn`, `pandas`, `numpy`, `tqdm`, `openpyxl`.
5. **Comando de Descompactação dos Dados**:
   ```bash
   cd /home/artur-carvalho/mestrado/repos/06-jit-smart/jit-smart/data
   unzip -q data.zip
   ```
6. **Mapeamento dos Arquivos de Entrada**: Os arquivos `.pkl` são distribuídos nas pastas `data/jitfine/` e `data/jitsmart/`.
7. **Atributos de Entrada das Linhas de Código**: Extração via scripts em `JITSmart/process and label defect code lines/`.
8. **Modo de Execução de Treinamento**:
   ```bash
   bash train_jitsmart.sh
   ```
9. **Modo de Execução em CPU (Ajuste para Inferência Local)**:
   - Configuração de `--device -1` ou exportação de variáveis `CUDA_VISIBLE_DEVICES=""`.
10. **Parâmetros de Sequência de Código**: `--max_seq_length 512`, `--max_msg_length 64`, `--max_codeline_length 256`, `--max_codeline_token_length 64`.
11. **Taxa de Aprendizado e Otimizador**: `AdamW`, `learning_rate 1e-5` (treinamento) / `2e-5` (teste), decaimento linear com warmup.
12. **Pesos da Função Multi-Tarefa Padrão**: `--dp_loss_weight 0.3 --dl_loss_weight 0.7`.
13. **Verificação dos Logs de Saída**: Os logs de treinamento e teste são gerados em `model/jitsmart/saved_models_concat/train.log` e `test.log`.
14. **Extração das Tabelas de Métricas**: Calculadas automaticamente pela função `eval_metrics()` e `get_line_level_metrics()` em `JITSmart/my_util.py`.
15. **Comparação com Baselines**: Os baselines legados podem ser executados via módulo Python em `baselines/` (ex.: `python -m baselines.LApredict.lapredict`).
16. **Verificação de Integridade dos Rótulos**: Assegurar a consistência entre o número de linhas no diff e o vetor binário de anotações no `.pkl`.
17. **Custo Financeiro de Execução**: **R$ 0.00** (todo o pipeline analítico e os dados de replicação rodam no ambiente local sem custos de cloud).

---

## 17. Gaps de Replicação

1. **Dependência de Checkpoints Volumosos**: Os pesos pré-treinados finais da rede CodeBERT ajustada ocupam aproximadamente 500 MB por experimento. Treinar todas as variações da RQ4 do zero sem GPU dedicada demandaria dias de CPU; recomenda-se para a replicação local focar na inferência com os checkpoints fornecidos ou amostragem reduzida de épocas.
2. **Discrepância de Formato em Dados Brutos de Notebook**: A geração inicial dos arquivos de linha dependia dos notebooks Jupyter em `process and label defect code lines/`, porém o autor já disponibilizou os pickles gerados (`test_buggy_commit_lines_df.pkl`), tornando desnecessária a reexecução manual dos notebooks.

---

## 18. Controle de Rastreabilidade

| Item Auditado | Fonte Documental | Evidência no Repositório / Sistema | Status de Validação |
| :--- | :--- | :--- | :--- |
| **Identificação do Paper** | PACMSE / ACM FSE 2024 | Artigo DOI: 10.1145/3643727 | `[FATO DOCUMENTADO]` |
| **Linha de Base & Dataset** | ESEC/FSE 2022 (JIT-Fine) | Artigo DOI: 10.1145/3540250.3549165 | `[FATO DOCUMENTADO]` |
| **Código da DLN (HAN)** | Arquivo `model.py` | [`JITSmart/concat/model.py#L82-L170`](file:///home/artur-carvalho/mestrado/repos/06-jit-smart/jit-smart/JITSmart/concat/model.py) | `[FATO DOCUMENTADO]` |
| **MultiFocalLoss** | Arquivo `model.py` | [`JITSmart/concat/model.py#L18-L60`](file:///home/artur-carvalho/mestrado/repos/06-jit-smart/jit-smart/JITSmart/concat/model.py) | `[FATO DOCUMENTADO]` |
| **Métricas Commit & Linha** | Arquivo `my_util.py` | [`JITSmart/my_util.py#L330-L490`](file:///home/artur-carvalho/mestrado/repos/06-jit-smart/jit-smart/JITSmart/my_util.py) | `[FATO DOCUMENTADO]` |
| **Projetos do Benchmark** | Arquivo `project_list.txt` | [`jit-smart/project_list.txt`](file:///home/artur-carvalho/mestrado/repos/06-jit-smart/jit-smart/project_list.txt) (21 projetos Java) | `[FATO DOCUMENTADO]` |
| **Pacote de Dados Pré-extraído** | Arquivo `data.zip` | [`jit-smart/data/data.zip`](file:///home/artur-carvalho/mestrado/repos/06-jit-smart/jit-smart/data/data.zip) (75 MB) | `[FATO DOCUMENTADO]` |
| **Resultados dos Baselines** | Tabela CSV | [`baselines/results/result.csv`](file:///home/artur-carvalho/mestrado/repos/06-jit-smart/jit-smart/baselines/results/result.csv) | `[FATO DOCUMENTADO]` |
