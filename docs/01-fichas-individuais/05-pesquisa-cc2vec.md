# Ficha Estruturada de Pesquisa Científica — PESQUISA 5: CC2Vec

---

## 1. Identificação

* **Título**: CC2Vec: Distributed Representations of Code Changes
* **Autores**: Thong Hoang, Hong Jin Kang, David Lo, Julia Lawall
* **Afiliações**: School of Information Systems, Singapore Management University (Cingapura); Sorbonne University / Inria / LIP6 (França)
* **Ano**: 2020
* **Venue**: Proceedings of the 42nd International Conference on Software Engineering (ICSE 2020), Seoul, Coreia do Sul, págs. 518–529
* **DOI**: https://doi.org/10.1145/3377811.3380361
* **URL**: https://arxiv.org/pdf/2003.05620
* **Repositório Oficial**: https://github.com/soarsmu/CC2Vec (espelho: https://github.com/CC2Vec/CC2Vec)
* **Bases de Dados e Checkpoints Pré-Treinados (Zenodo)**: https://zenodo.org/record/3965149 (DOI: 10.5281/zenodo.3965149)
* **Identificação Interna**: **PESQUISA 5**

---

## 2. Problema

* **Problema Científico**:
  A dependência de features manuais (*handcrafted features*) e específicas para tarefas isoladas na representação de alterações de código (*software patches* / *code changes*), demandando esforço humano intensivo de engenharia de atributos e falhando em capturar a semântica contextual profunda e estruturada das mudanças.
* **Causas Raízes Identificadas pelos Autores** [Seção 1]:
  1. *Falta de Generalidade das Abordagens Prévias*: A maioria das soluções extrai propriedades pontuais (ex.: contagem de linhas adicionadas/removidas, arquivos modificados, métricas de churn), criando representações isoladas que não se transferem entre diferentes tarefas de engenharia de software.
  2. *Ignorância da Estrutura Hierárquica do Diff*: Alterações de código possuem uma hierarquia intrínseca rígida (*tokens/palavras formam linhas $\rightarrow$ linhas formam hunks $\rightarrow$ hunks formam arquivos $\rightarrow$ arquivos formam o commit*). Modelos lineares de texto ou CNNs simples (como DeepJIT original) ignoram essa hierarquia.
  3. *Incapacidade de Modelar o Contraste Deletado vs. Adicionado*: O significado semântico de um patch reside fundamentalmente na *diferença e intenção transformacional* entre o código que foi removido e o código que foi adicionado.

---

## 3. Perguntas de Pesquisa / Tarefas de Avaliação

O artigo formula o problema através de **três tarefas seminais de Engenharia de Software** orientadas a patches e um estudo de ablação formal [Seção 3 e 4]:

* **Tarefa 1 (Log Message Generation - Seção 3.1)**:
  *Como o CC2Vec performa na geração automática da primeira linha de mensagens de commit (sumarização semântica do diff)?*
* **Tarefa 2 (Bug Fixing Patch Identification - Seção 3.2)**:
  *A representação distribuída do CC2Vec auxilia classificadores supervisionados a distinguir patches de correção de bugs contra alterações comuns?*
* **Tarefa 3 (Just-in-Time Defect Prediction - Seção 3.3)**:
  *A integração dos vetores de código do CC2Vec melhora a capacidade de modelos de ponta (DeepJIT) na predição de commits que introduzem defeitos?*
* **Estudo de Ablação (Ablation Study - Seção 4.1)**:
  *Qual é a contribuição individual de cada uma das 5 funções de comparação (Neural Tensor, Feed-forward NN, Similaridade, Subtração, Multiplicação) no espaço latente?*

---

## 4. Hipóteses

* **Hipótese 1 [FATO DOCUMENTADO - Seção 1 & 2]**: A primeira linha da mensagem de commit escrita por desenvolvedores expressa a intenção semântica da alteração com o menor ruído possível. Treinar uma rede neural para predizer as palavras dessa mensagem a partir do diff bruto força o modelo a aprender um espaço vetorial distribuído denso (*distributed representation*) onde alterações semanticamente similares convergem.
* **Hipótese 2 [FATO DOCUMENTADO - Seção 2.4]**: Modelar separadamente o código removido e o código adicionado por meio de uma Rede de Atenção Hierárquica (HAN) e combiná-los através de múltiplas funções de comparação não-lineares (especialmente Neural Tensor Networks) captura relacionamentos semânticos muito mais ricos do que simples vetores concatenados.

---

## 5. Objetivos

* **Objetivo Geral**:
  Propor a arquitetura de aprendizado profundo **CC2Vec**, agnóstica de linguagem de programação e não dependente de código compilável/AST, capaz de converter diffs de código em vetores contínuos densos supervisionados pela semântica de mensagens de log.
* **Objetivos Específicos**:
  1. Desenvolver uma Rede de Atenção Hierárquica (HAN) em três níveis de granularidade: Codificador de Palavras (*Word Encoder*), Codificador de Linhas (*Line Encoder*) e Codificador de Hunks (*Hunk Encoder*), com mecanismos de atenção aprendidos com vetores de contexto.
  2. Implementar 5 funções de comparação no nível de arquivo: Neural Tensor Network ($e_{\text{NT}}$), Feed-Forward Neural Network ($e_{\text{NN}}$), Similaridade Euclidiana/Cosseno ($e_{\text{sim}}$), Subtração elemento a elemento ($e_{\text{sub}}$) e Multiplicação elemento a elemento ($e_{\text{mul}}$).
  3. Validar a utilidade das representações em 3 tarefas com baselines competitivos (NNGen, LPU-SVM, PatchNet, DeepJIT).
  4. Disponibilizar os modelos e datasets pré-treinados no Zenodo para reprodutibilidade direta.

---

## 6. Contexto

* **Contexto de Inteligência Artificial para Engenharia de Software (AI4SE / Deep Learning on Code)**:
  Representação vetorial de artefatos de código, predição contínua de risco em pipelines de CI/CD e mineração de grandes repositórios de software livre (Linux Kernel, OpenStack, Qt).

---

## 7. Dados

* **Datasets Utilizados por Tarefa**:
  1. **Tarefa 1 (Log Message Generation)**:
     - Dataset multi-projeto de Jiang et al. contendo **2 milhões de commits** minerados do GitHub, filtrando commits com mensagens de 1 linha de alta qualidade.
  2. **Tarefa 2 (Bug Fixing Patch Identification)**:
     - Dataset oficial do **Linux Kernel** (versões v3.0 a v4.12, período de Julho/2011 a Julho/2017).
     - **42.000 patches de correção de bugs (BFP)** e **40.000 patches neutros (non-BFP)**, limitados a 100 linhas modificadas de acordo com as diretrizes do kernel Linux. Total: 82.000 patches.
  3. **Tarefa 3 (Just-in-Time Defect Prediction - JIT-DP)**:
     - **Dataset QT**: **25.000 patches** cobrindo 2 anos e 9 meses (8% de taxa de patches defeituosos).
     - **Dataset OPENSTACK**: **12.000 patches** cobrindo 2 anos e 3 meses (13% de taxa de patches defeituosos).
* **Critérios de Inclusão e Pré-processamento**:
  - Diffs parseados via NLTK em tokens de código.
  - Eliminação de linhas em branco.
  - Representação tridimensional de tensores: $B \in \mathbb{R}^{H \times L \times W}$ ($H$: hunks, $L$: linhas por hunk, $W$: palavras por linha).

---

## 8. Metodologia

O fluxo arquitetural do CC2Vec opera em 5 camadas sequenciais [Seção 2]:

```
[DADOS: Patch (Diff de Código Removido/Adicionado + 1ª Linha da Mensagem de Log)]
   │
[PRÉ-PROCESSAMENTO: Tokenização NLTK + Vocabulário de Código V_C + Tensor B (H x L x W)]
   │
[HIERARCHICAL ATTENTION NETWORK (HAN)]
   ├── Nível 1: Word Encoder (Embedding + Bi-GRU + Word Attention u_w) ──> Linhas (s_ij)
   ├── Nível 2: Line Encoder (Bi-GRU + Line Attention u_s) ──> Hunks (t_i)
   └── Nível 3: Hunk Encoder (Bi-GRU + Hunk Attention u_t) ──> Vetores e_r e e_a
   │
[CAMADA DE COMPARAÇÃO (5 Funções entre e_r e e_a)]
   ├── e_NT = ReLU(e_r^T T e_a + b_NT)   [Neural Tensor Network]
   ├── e_NN = ReLU(W [e_a || e_r] + b)   [Feed-Forward Network]
   ├── e_sim = [Euclidean || Cosine]     [Similaridades Vetoriais]
   ├── e_sub = e_r - e_a                 [Subtração Element-wise]
   └── e_mul = e_r ⊙ e_a                 [Multiplicação Element-wise]
   │
[FUSÃO DE FEATURES] ──> Concatenação dos arquivos e_p = e_f1 ⊕ ... ⊕ e_fF
   │
[CAMADA DE PREDIÇÃO DE PALAVRAS] ──> Sigmoid Cross-Entropy Loss com Regularização L2 e Adam
   │
[TRANSFERÊNCIA / DOWNSTREAM] ──> Vetor e_p congelado e injetado em DeepJIT / PatchNet / SVM
```

---

## 9. Ferramentas

| Ferramenta | Versão Documentada | Finalidade | Configuração / Parâmetros |
| :--- | :--- | :--- | :--- |
| **Python** | 3.6.9 / 3.8+ | Linguagem de implementação | Ambiente CLI padrão |
| **PyTorch** | 1.2.0 (compatível com 1.x e 2.x) | Construção e treinamento dos tensores e redes neurais | Suporte nativo a CPU (`-device -1`) e GPU CUDA |
| **NLTK** | 3.4.5 | Tokenização de código e texto em linguagem natural | `word_tokenize` |
| **scikit-learn** | 0.22.1 | Cálculo de métricas e baselines de SVM | Classificadores LPU-SVM |
| **NumPy** | 1.16.5 | Operações matriciais e manipulação de pickles | Manipulação de arquivos `.pkl` |
| **tqdm** | 4.46.1 | Monitoramento visual de épocas de treinamento | Barras de progresso |

---

## 10. Algoritmos e Classificadores

* **Arquitetura Base**:
  - `CC2Vec`: HAN com Bi-GRUs de 64 dimensões ocultas, camadas densas com ativação ReLU, tensores bilineares e normalização de atenção por Softmax.
* **Hiperparâmetros do CC2Vec**:
  - `embedding_dim`: 64
  - `filter_sizes`: 1, 2, 3
  - `num_filters`: 64
  - `hidden_units`: 512
  - `dropout_keep_prob`: 0.5
  - `l2_reg_lambda`: $1\text{e-}5$
  - `learning_rate`: $1\text{e-}4$ (Otimizador Adam)
  - `batch_size`: 64
  - `num_epochs`: 50
* **Classificadores em Downstream Tasks**:
  - *DeepJIT + CC2Vec*: CNN convolucional que recebe a concatenação dos embeddings de texto e código originais com o vetor `e_p` do CC2Vec.
  - *PatchNet + CC2Vec*: Rede hierárquica para classificação binária de patches de correção.
  - *LPU-SVM + CC2Vec*: Support Vector Machine treinado sobre as features manuais de Tian et al. concatenadas com o vetor do CC2Vec.

---

## 11. Métricas

1. **BLEU-4**: Métrica de avaliação de tradução e geração de texto para a Tarefa 1 (precisão de n-gramas com penalidade de brevidade).
2. **Accuracy, Precision, Recall e F1-Score**: Para a Tarefa 2 (identificação binária de patches corretores).
3. **AUC (Area Under the ROC Curve)**: Métrica mandatória e principal para a Tarefa 3 (JIT Defect Prediction), imune a variações arbitrárias de limiar de probabilidade.

---

## 12. Resultados

### Tarefa 1: Log Message Generation (BLEU-4)
* CC2Vec superou todos os baselines (LogGen e NNGen), atingindo **BLEU-4 de 20.48**, um ganho de **+24.73%** em relação ao melhor baseline.

### Tarefa 2: Bug Fixing Patch Identification (Linux Kernel) [Tabela 2]

| Abordagem | Accuracy (%) | Precision (%) | Recall (%) | F1-Score (%) | AUC (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **LPU-SVM** (Tian et al.) | 73.1 | 75.1 | 71.6 | 73.3 | 73.1 |
| **LPU-SVM + CC2Vec** | 77.1 (+5.47%) | 77.2 (+2.80%) | 79.8 (+11.45%) | 78.5 (+7.09%) | 76.2 (+4.24%) |
| **PatchNet** (Hoang et al.) | 86.2 | 83.9 | **90.1** | 87.1 | 86.0 |
| **PatchNet + CC2Vec** | **90.7 (+5.22%)** | **91.6 (+9.18%)** | **90.1** | **90.9 (+4.36%)** | **91.6 (+6.51%)** |

### Tarefa 3: Just-in-Time Defect Prediction (JIT-DP) [Tabela 3]

| Abordagem | Dataset QT (AUC %) | Dataset OPENSTACK (AUC %) |
| :--- | :---: | :---: |
| **DeepJIT** (Baseline) | 76.8 | 75.1 |
| **DeepJIT + CC2Vec** | **82.2 (+7.03%)** | **80.9 (+7.72%)** |

* A injeção dos vetores de código do CC2Vec elevou o AUC do DeepJIT em **+5.4 pontos absolutos** no QT e **+5.8 pontos absolutos** no OpenStack.

### Estudo de Ablação das Funções de Comparação [Tabela 4]
* Quando todas as funções de comparação são removidas ($All - all$), o desempenho tem a maior queda em todas as tarefas (queda de 5.84% no AUC do QT e 5.19% no OpenStack).
* Entre as funções individuais, a omissão da **Neural Tensor Network ($All - NT$)** causou a queda mais severa (AUC caiu de 82.2 para 79.8 no QT), comprovando que a interação tensorial bilinear entre linhas removidas e adicionadas é o componente de comparação mais expressivo da rede.

---

## 13. Ameaças à Validade

* **Validade de Construção (Construct Validity)**:
  - Uso de métricas padronizadas e amplamente aceitas (BLEU-4, AUC, F1).
* **Validade Interna (Internal Validity)**:
  - Possíveis vieses de implementação mitigados pelo reuso dos códigos públicos oficiais de DeepJIT e PatchNet.
* **Validade Externa (External Validity)**:
  - Avaliação realizada em 3 tarefas distintas com 4 ecossistemas de linguagens e projetos diferentes (C no Linux Kernel, C++ no QT, Python no OpenStack, Java no dataset geral), garantindo alta generalizabilidade.

---

## 14. Artefatos Disponibilizados

* **Repositório GitHub**: `https://github.com/soarsmu/CC2Vec`
* **Código-Fonte**:
  - `jit_DExtended.py`, `jit_DExtended_model.py`, `jit_DExtended_eval.py`: Pipeline completo para predição JIT.
  - `bfp_PNExtended.py`, `bfp_PNExtended_model.py`: Pipeline para classificação de patches corretores.
  - `lmg_eval.py`, `lmg_cc2ftr.py`: Pipeline de extração de representações e geração de mensagens.
* **Bases de Dados e Checkpoints Pré-treinados**:
  - Repositório Zenodo (DOI: 10.5281/zenodo.3965149): Arquivos compactados contendo os modelos `.pt` já treinados e os datasets `.pkl` para QT, OpenStack e Linux.

---

## 15. Replicabilidade

* **Classificação**: **Diretamente replicável** (com excelente suporte a execução em CPU local)
* **Justificativa**:
  O código PyTorch possui suporte nativo e explícito à execução em CPU (`-device -1`), permitindo rodar a avaliação dos modelos pré-treinados em qualquer computador moderno sem requerer placas de vídeo NVIDIA dedicadas.

---

## 16. Protocolo de Replicação Local

1. **Pré-requisitos**:
   - Python 3.8+ instalado.
   - PyTorch (`torch`), `scikit-learn`, `nltk`, `numpy`, `tqdm`.
2. **Ambiente**:
   - Sistema Operacional: Linux / Ubuntu.
   - Modo de Execução: CPU local (`-device -1`).
   - RAM: $\ge 8$ GB.
3. **Instalação do Ambiente Virtual**:
   ```bash
   cd /home/artur-carvalho/mestrado/repos/05-cc2vec
   python3 -m venv venv
   source venv/bin/activate
   pip install torch torchvision numpy scikit-learn nltk tqdm
   ```
4. **Obtenção dos Modelos Pré-Treinados e Datasets**:
   - Baixar o pacote de dados do Zenodo (`https://zenodo.org/record/3965149/files/data.zip` e `model.zip`) e extrair dentro de `repos/05-cc2vec/`.
5. **Como Executar a Avaliação de JIT Defect Prediction em Modo CPU**:
   ```bash
   python jit_DExtended.py -predict \
     -pred_data data/jit/openstack_test.pkl \
     -pred_data_cc2ftr data/jit/openstack_test_cc2ftr.pkl \
     -dictionary_data data/jit/openstack_dict.pkl \
     -load_model snapshot/deepjit_cc2vec_openstack.pt \
     -device -1
   ```
6. **Parâmetros**:
   - `-predict`: Modo de avaliação/inferência.
   - `-device -1`: Força execução no processador CPU local (Intel Core i7).
   - `-batch_size 64`: Tamanho do lote de teste.
7. **Métricas a Coletar**:
   - AUC gerado no terminal contra os valores de verdade fundamental.
8. **Resultados Esperados**:
   - AUC $\approx 82.2\%$ no dataset QT e $\approx 80.9\%$ no dataset OpenStack.
9. **Critérios de Sucesso**:
   - Inferência executada com sucesso sobre o arquivo `.pkl` de teste retornando o valor de AUC reportado na Tabela 3 do paper da ICSE.
10. **Problemas Conhecidos**:
    - Se tentar rodar sem `-device -1` em máquina sem GPU, o PyTorch tentará alocar memória CUDA e lançará exceção de runtime.

---

## 17. Gaps de Replicação

1. **Dependência de Download Externo do Zenodo**: Os modelos `.pt` e arquivos `.pkl` não estão versionados dentro do Git por excederem o limite de tamanho do GitHub, exigindo o download pontual dos arquivos do Zenodo.
2. **Versões Históricas no README**: O README cita `python 3.6.9` e `torch 1.2.0`; entretanto, a sintaxe de tensores do script é compatível com Python 3.8+ e PyTorch 1.x/2.x com pequenos ajustes de importação de pickle.

---

## 18. Controle de Rastreabilidade

| Afirmação / Dado Documentado | Documento Fonte | Seção / Página | Evidência Textual no Artigo |
| :--- | :--- | :--- | :--- |
| **Definição das 3 Tarefas** | `05-cc2vec.pdf` | Seção 1, pág. 1-2 | "...we use the vectors produced by CC2Vec for three tasks: log message generation, bug fixing patch identification, and just-in-time defect prediction." |
| **Arquitetura HAN com 3 Níveis** | `05-cc2vec.pdf` | Seção 2.4.1, pág. 3-4 | "Our HAN first builds vector representations of lines; these vectors are then used to construct vector representations of hunks; and we then aggregate these vectors to construct the embedding vector of the removed or added code." |
| **As 5 Funções de Comparação** | `05-cc2vec.pdf` | Seção 2.4.2, pág. 4-5 | "Figure 4 shows the five comparison functions: Neural Tensor Network, Neural Network, Similarity (Euclidean + Cosine), Element-wise Subtraction, Element-wise Multiplication." |
| **Desempenho no JIT-DP (QT e OpenStack)** | `05-cc2vec.pdf` | Seção 3.3.5, Tabela 3, pág. 7 | "The use of CC2Vec with DeepJIT improves the AUC score from 76.8 to 82.2 on QT, and from 75.1 to 80.9 on OPENSTACK." |
| **Impacto do Ablation Study (All - NT)** | `05-cc2vec.pdf` | Seção 4.1, Tabela 4, pág. 8 | "All-NT performs the worst among the five variants... suggesting that the neural network tensor comparison function is more important than other functions." |
| **Agnóstico de Linguagem e Não-Exigência de AST** | `05-cc2vec.pdf` | Seção 5, pág. 9 | "...we deliberately designed CC2Vec to not require parseable code in its input... CC2Vec is also programming-language agnostic." |
