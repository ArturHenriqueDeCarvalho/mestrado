# Ficha Estruturada de Pesquisa Científica — PESQUISA 4: SZZ-TSE

---

## 1. Identificação

* **Título**: The Impact of Changes Mislabeled by SZZ on Just-in-Time Defect Prediction
* **Autores**: Yuanrui Fan, Xin Xia, Daniel Alencar da Costa, David Lo, Ahmed E. Hassan, Shanping Li
* **Afiliações**: College of Computer Science and Technology, Zhejiang University (China); Faculty of Information Technology, Monash University (Austrália); School of Information Systems, Singapore Management University (Cingapura); School of Computing, Queen's University (Canadá)
* **Ano**: 2019 (Accepted) / 2021 (Publicado)
* **Venue**: IEEE Transactions on Software Engineering (TSE), Volume 47, Número 8, págs. 1559–1586, 2021
* **DOI**: https://doi.org/10.1109/TSE.2019.2929761
* **URL**: https://doi.org/10.1109/TSE.2019.2929761 *(Preprint institucional: InK@SMU / Queen's University)*
* **Repositório Oficial**: https://github.com/YuanruiZJU/SZZ-TSE
* **Repositórios Auxiliares Oficiais**:
  - MA-SZZ: https://github.com/danielcalencar/ma-szz
  - RA-SZZ: https://github.com/danielcalencar/raszzprime
* **Identificação Interna**: **PESQUISA 4**

---

## 2. Problema

* **Problema Científico**:
  Investigar como o ruído nos rótulos de dados (commits incorretamente rotulados como indutores de defeito ou limpos por diferentes variantes do SZZ) impacta o **desempenho estatístico**, a **interpretação das métricas mais importantes** e o **esforço prático de inspeção de código pelos desenvolvedores** em modelos de predição de defeitos Just-in-Time (JIT Defect Prediction).
* **Causas Raízes e Relevância do Problema**:
  1. *Dependência Crítica do SZZ em JIT*: Modelos preditivos de defeitos a nível de commit treinam sobre o histórico versionado rotulado heuristicamente por variantes do SZZ.
  2. *Contradição na Literatura*: Estudos prévios apontavam que o SZZ gera ruído substancial, mas não havia uma avaliação sistemática e estatisticamente controlada em larga escala comparando o efeito isolado de cada variante seminal (B-SZZ, AG-SZZ, MA-SZZ) contra um oráculo robusto tolerante a refatorações (RA-SZZ).
  3. *Métricas Teóricas vs. Realidade Industrial*: Modelos que parecem performar bem em métricas agregadas (ex.: AUC ou F1) podem, na prática, induzir os desenvolvedores a inspecionar centenas de linhas de código desnecessárias (*wasted inspection effort*).

---

## 3. Perguntas de Pesquisa (Research Questions)

As três RQs apresentadas literalmente pelos autores:

* **RQ1**: How do mislabeled changes by SZZ impact the performance of JIT defect prediction models trained using the original data?
* **RQ2**: How do mislabeled changes by SZZ impact the interpretation (metric importance) of JIT defect prediction models?
* **RQ3**: How do mislabeled changes by SZZ impact the practical usage (and developer inspection effort) of JIT defect prediction models?

---

## 4. Hipóteses

* **Hipótese 1 [FATO DOCUMENTADO]**: Como o **RA-SZZ** utiliza técnicas conscientes de refatoração (`RefactoringMiner`) para descartar linhas de código modificadas puramente por reestruturações de design sem alteração de comportamento, os dados rotulados pelo RA-SZZ contêm a menor probabilidade de ruído, constituindo a linha de base (*baseline*) mais confiável para treinar e testar modelos de predição JIT.
* **Hipótese 2 [FATO DOCUMENTADO]**: A degradação na acurácia preditiva agregada de um modelo JIT não é linear ao ruído de rotulagem do SZZ, mas o esforço desperdiçado de revisão de código em ambientes industriais é altamente sensível aos falsos positivos gerados por variantes gulosas (como o B-SZZ).

---

## 5. Objetivos

* **Objetivo Geral**:
  Avaliar em escala empírica o impacto de rótulos incorretos gerados por 4 variantes do SZZ (B-SZZ, AG-SZZ, MA-SZZ e RA-SZZ) no treinamento de classificadores JIT em 10 projetos da Apache Software Foundation.
* **Objetivos Específicos**:
  1. Extrair e rotular 126.526 alterações de código utilizando 4 implementações formais de SZZ.
  2. Treinar 3 famílias de classificadores de aprendizado de máquina (Naive Bayes, Regressão Logística e Random Forest) em cenários balanceados e desbalanceados com 1.000 iterações de *bootstrap*.
  3. Mensurar o impacto no poder preditivo através de AUC, F1-Score, G-Mean e Recall@20%.
  4. Analisar a estabilidade da interpretação de features e importância de métricas via teste de efeito de tamanho de Scott-Knott ESD (*Scott-Knott Effect Size Difference*).
  5. Quantificar o esforço desperdiçado de inspeção de linhas de código (*wasted LOC inspection effort*).

---

## 6. Contexto

* **Contexto Tecnológico e Empírico**:
  Mineração de Repositórios da Apache Software Foundation (projetos maduros em Java/C++) e integração contínua de garantia de qualidade (JIT Quality Assurance).

---

## 7. Dados

* **Origem dos Dados**:
  10 grandes projetos de código aberto do ecossistema **Apache Software Foundation** [Tabela no Repositório / Paper]:
  - `activemq`, `camel`, `derby`, `geronimo`, `hbase`, `hcommon`, `mahout`, `openjpa`, `pig`, `tuscany`.
* **Tamanho do Dataset**:
  - **Total de Commits / Alterações Analisadas**: **126.526 commits**.
  - Todos os arquivos com features já extraídas estão consolidados em formato CSV em `data_results/data_csvs/` no repositório oficial (`szz-tse`).
* **Rótulos de SZZ Gerados para Cada Commit**:
  - `buggy_B2`: Rótulo gerado pela variante B-SZZ.
  - `buggy_AG`: Rótulo gerado pela variante AG-SZZ.
  - `buggy_MA`: Rótulo gerado pela variante MA-SZZ.
  - `buggy_RA`: Rótulo gerado pela variante RA-SZZ (adotado formalmente como o *ground truth baseline*).
* **Critérios de Inclusão e Filtragem**:
  - Análise de colinearidade conduzida previamente via VIF (*Variance Inflation Factor*) e análise hierárquica de correlação de Spearman para remover features redundantes (armazenadas em `data_results/collinearity.csv`).

---

## 8. Metodologia

O fluxo experimental do SZZ-TSE opera de acordo com a sequência:

```
[DADOS: 10 Projetos Apache (126.526 commits em CSV)]
   │
[ROTULAGEM SZZ: B-SZZ, AG-SZZ, MA-SZZ vs RA-SZZ (Baseline)]
   │
[PRÉ-PROCESSAMENTO: Filtragem de Colinearidade (collinearity.csv)]
   │
[BOOTSTRAP RESAMPLING: 1.000 Iterações por Projeto e Classificador]
   ├── Cenário Desbalanceado (dados originais)
   └── Cenário Balanceado (técnicas de re-sampling)
   │
[TREINAMENTO DE 3 CLASSIFICADORES: Naive Bayes, Logistic Regression, Random Forest]
   │
[CÁLCULO DE MÉTRICAS MULTIDIMENSIONAIS]
   ├── Preditivas: AUC, Precision, Recall, F1, G-Mean
   ├── Esforço Prático: Recall@20%, Wasted Effort LOC, All Effort LOC
   └── Interpretação: Ranking de Importância de Features (ANOVA / VarImportance)
   │
[TESTE ESTATÍSTICO: Scott-Knott ESD Test (comparações entre grupos sem overlap)]
   │
[RESULTADOS & RESPOSTA ÀS RQS]
```

---

## 9. Ferramentas

| Ferramenta | Versão / Descrição | Finalidade | Configuração / Parâmetros |
| :--- | :--- | :--- | :--- |
| **R** | 3.6+ / 4.x | Ambiente de computação estatística e modelagem | Scripts em `code/calculation/classification_importance.R` |
| **ScottKnottESD** | Pacote R | Agrupamento estatístico com tamanho de efeito | Separação não-paramétrica de classificadores e variantes |
| **randomForest** | Pacote R | Implementação do ensemble Random Forest | 100 árvores por iteração de bootstrap |
| **pROC / PRROC** | Pacotes R | Cálculo de curvas ROC e Precision-Recall | Cálculo de AUC e Precision-Recall AUC |
| **caret / e1071** | Pacotes R | Treinamento de Naive Bayes e regressões | Modelagem supervisionada |
| **Python / MySQL** | Python 3 + MySQL | Pipeline upstream de mineração e extração de features | Módulos em `features/jit-features/` |
| **RefactoringMiner** | 1.x / 2.0 | Extração de refatorações Java | Utilizado no `raszzprime` |

---

## 10. Algoritmos e Classificadores

* **3 Classificadores JIT de Referência**:
  1. **Random Forest (RF)**: Ensemble de árvores de decisão.
  2. **Logistic Regression (LR)**: Modelo linear clássico para estimativa de probabilidade de risco.
  3. **Naive Bayes (NB)**: Modelo probabilístico baseado no teorema de Bayes.
* **Protocolo de Validação**:
  - **1.000 iterações de Bootstrap**: Em cada iteração, seleciona-se uma amostra com reposição do mesmo tamanho para treino e avalia-se nas instâncias fora da bolsa (*out-of-bag*).
  - Testes conduzidos com dados desbalanceados originais e balanceados.

---

## 11. Métricas

1. **AUC (Area Under the ROC Curve)**: Métrica padrão de discriminação independente de limiar de corte.
2. **Precision, Recall e F1-Measure**: Acurácia no ponto de corte padrão (0.5).
3. **G-Mean**: $\sqrt{\text{TPR} \times \text{TNR}}$ (avalia acurácia balanceada entre commits limpos e defeituosos).
4. **Recall@20%**: Proporção de commits defeituosos capturados ao inspecionar os 20% commits com maior risco predito ordenados pelo modelo.
5. **Esforço Desperdiçado de Inspeção (Wasted Effort LOC)**:
   Número total de Linhas de Código (LOC) inspecionadas em commits falsos positivos (commits limpos que o modelo classificou erroneamente como defeituosos, fazendo o engenheiro revisar código sem bugs).
6. **All Effort LOC**: Total de linhas de código inspecionadas pelo desenvolvedor.
7. **Scott-Knott ESD Rank**: Agrupamento estatístico que determina se as diferenças de desempenho entre duas variantes são estatisticamente significativas com base no d de Cohen.

---

## 12. Resultados

### RQ1: Impacto no Desempenho Preditivo Geral
* **Fato Documentado**:
  - Mislabeled changes de **B-SZZ** e **MA-SZZ** **NÃO causam degradação drástica ou estatisticamente significativa** nas métricas agregadas de classificação (AUC, F1-Score, G-Mean e Recall@20%). Modelos de Random Forest e Regressão Logística demonstraram resiliência moderada a esse ruído em métricas globais.
  - Por outro lado, rótulos ruidosos de **AG-SZZ** causam uma queda consistente e estatisticamente significativa no desempenho preditivo, reduzindo AUC, F1 e G-Mean em **1% a 5%** em média. Isso ocorre porque o AG-SZZ descarta linhas cosméticas no grafo de anotações, mas sem filtrar meta-changes ou refatorações, distorcendo os padrões de aprendizado.

### RQ2: Impacto na Interpretação do Modelo (Importância de Métricas)
* **Fato Documentado**:
  - A métrica mais importante em quase todos os modelos (o número de arquivos alterados no commit — `NF` / `entropy`) permanece no topo mesmo com dados ruidosos.
  - Contudo, **a ordem e o peso relativo das métricas secundárias e terciárias são fortemente distorcidos** pelo ruído do SZZ. Um pesquisador ou gestor que tentar interpretar "quais fatores induzem falhas" com base em B-SZZ chegará a conclusões causais diferentes daquelas obtidas com RA-SZZ.

### RQ3: Impacto no Esforço Prático de Inspeção (Wasted Developer Effort)
* **Fato Documentado**:
  - Quando se avalia a utilidade sob a ótica de engenharia de software real (linhas de código inspecionadas), **o impacto das variantes de SZZ torna-se brutal**.
  - Modelos treinados com dados rotulados por **B-SZZ** geram de **9% a 10% mais esforço desperdiçado de revisão de código** (centenas de horas-homem e milhares de LOCs revisadas à toa).
  - Modelos treinados com **AG-SZZ** geram de **1% a 15% de esforço desperdiçado adicional**.
  - O **B-SZZ é a variante que introduz o maior custo econômico de desperdício em produção**, comprovando que métricas como AUC escondem prejuízos industriais severos.

---

## 13. Ameaças à Validade

* **Validade de Construção (Construct Validity)**:
  - Uso do RA-SZZ como linha de base (*ground truth*). Embora o RA-SZZ mitigue refatorações, ele ainda é uma heurística automatizada e pode conter pequenas margens de ruído remanescentes.
* **Validade Interna (Internal Validity)**:
  - Fatores estocásticos no treino dos classificadores. Mitigado através da execução de 1.000 iterações de bootstrap para cada projeto e classificador.
* **Validade Externa (External Validity)**:
  - Todos os 10 projetos pertencem ao ecossistema da Apache Software Foundation e são desenvolvidos prioritariamente em Java. Projetos de outras organizações ou com processos de code review distintos podem apresentar distribuições de ruído diferentes.

---

## 14. Artefatos Disponibilizados

* **Repositório GitHub**: `https://github.com/YuanruiZJU/SZZ-TSE`
* **Código e Scripts R**:
  - `code/calculation/classification_importance.R`: Pipeline central de 1.000 bootstraps.
  - `code/packages/`: Scripts auxiliares de métricas (`measures.R`, `imbalance.R`, `VarImportance.R`, `ScottKnottESD`).
* **Datasets e Features Consolidadas**:
  - `data_results/data_csvs/`: 10 arquivos CSV pré-calculados para cada projeto Apache (`activemq.csv`, `camel.csv`, ..., `tuscany.csv`).
  - `labeled-data.zip` (16 MB): Mapeamento de CVS IDs de commits rotulados pelas 4 variantes.
  - `data_results/collinearity.csv`: Tabela com features não-colineares selecionadas por projeto.

---

## 15. Replicabilidade

* **Classificação**: **Diretamente replicável** (com altíssima integridade de dados)
* **Justificativa**:
  O repositório já disponibiliza todas as 126.526 instâncias de commits com features e rótulos das 4 variantes calculados e prontos em CSVs dentro de `data_results/data_csvs/`. O script R de execução é autocontido e não requer re-minerar o Git ou re-executar o SZZ do zero.

---

## 16. Protocolo de Replicação Local

1. **Pré-requisitos**:
   - R instalado no sistema (`sudo apt install r-base` ou versão $\ge 3.6$).
   - Pacotes R listados no cabeçalho do script instalados.
2. **Ambiente**:
   - Sistema Operacional: Linux / Ubuntu.
   - CPU: Processador multi-core.
   - RAM: $\ge 8$ GB.
3. **Instalação de Dependências no R**:
   ```R
   install.packages(c("pROC", "randomForest", "naivebayes", "reshape", "e1071", "ScottKnottESD", "caret", "pracma", "PRROC", "data.table"))
   ```
4. **Código e Datasets Necessários**:
   - Repositório `repos/04-szz-tse/szz-tse` já clonado localmente com os CSVs em `data_results/data_csvs/`.
5. **Preparação de Diretórios de Saída**:
   ```bash
   cd /home/artur-carvalho/mestrado/repos/04-szz-tse/szz-tse
   mkdir -p data_results/importance data_results/oneway data_results/results_imbalance data_results/results_balance
   ```
6. **Configuração do Caminho no Script**:
   - No arquivo `code/calculation/classification_importance.R`, configurar a linha 12:
     ```R
     DIR_PATH = "/home/artur-carvalho/mestrado/repos/04-szz-tse/szz-tse"
     ```
   - Para um teste rápido preliminar, reduzir temporariamente a variável `bootstrap_times <- 1000` para `bootstrap_times <- 10` ou `50` (para evitar horas de processamento antes de validar o pipeline completo).
7. **Como Executar o Experimento**:
   ```bash
   Rscript code/calculation/classification_importance.R
   ```
8. **Parâmetros**:
   - `bootstrap_times`: 1000 (oficial do paper) ou 20 (teste rápido).
   - `classifiers`: Naive Bayes, Logistic Regression, Random Forest.
   - `szz_labels`: `buggy_B2`, `buggy_AG`, `buggy_MA` contra baseline `buggy_RA`.
9. **Métricas a Coletar**:
   - Arquivos CSV gerados em `data_results/results_imbalance/` com valores de AUC, F1, G-Mean, Recall@20 e Wasted Effort LOC.
10. **Critérios de Sucesso**:
    - Geração dos CSVs de resultados para os 10 projetos com médias de AUC e esforço convergindo com os valores reportados no paper da IEEE TSE.
11. **Problemas Conhecidos**:
    - O bootstrap com 1.000 iterações para 10 projetos em 3 classificadores exige elevado tempo de processamento contínuo em CPU se executado em single-thread sequencial.

---

## 17. Gaps de Replicação

1. **Configuração de Caminho Hardcoded**: O script R possui `DIR_PATH = "?"` na linha 12, exigindo intervenção manual antes de rodar.
2. **Custo Computacional do Bootstrap 1.000**: O script oficial original roda em loop sequencial no R sem paralelização (`mclapply` ou `foreach`), o que pode levar muitas horas para concluir 100% das 1.000 iterações em todos os 10 projetos.

---

## 18. Controle de Rastreabilidade

| Afirmação / Dado Documentado | Documento Fonte | Seção / Página | Evidência Textual no Artigo |
| :--- | :--- | :--- | :--- |
| **Definição das RQs 1, 2 e 3** | Artigo IEEE TSE 2019/2021 | Seção 3 / RQ Framing | "RQ1: How do mislabeled changes by SZZ impact the performance... RQ2: How do mislabeled changes impact interpretation... RQ3: How do mislabeled changes impact practical usage..." |
| **Tamanho do Dataset (126.526 commits em 10 Apache)** | Artigo IEEE TSE & `szz-tse/README.md` | Seção 4 (Data Collection) | "Our dataset contains 126,526 changes from ten Apache open-source projects: activemq, camel, derby, geronimo, hbase, hcommon, mahout, openjpa, pig, tuscany." |
| **Uso do RA-SZZ como Baseline Confiável** | Artigo IEEE TSE & `classification_importance.R` | Seção 4, Linha 29 do Script | `szz_baseline <- "buggy_RA"`: RA-SZZ filtra refatorações e é o oráculo de referência com menor probabilidade de ruído. |
| **Estabilidade de AUC em B-SZZ e Queda em AG-SZZ** | Artigo IEEE TSE | Resposta à RQ1 | "Mislabeled changes by B-SZZ and MA-SZZ do not heavily degrade performance... while AG-SZZ causes a statistically significant drop of 1% to 5%." |
| **Desperdício de 9% a 15% de Esforço de Inspeção** | Artigo IEEE TSE | Resposta à RQ3 | "Changes mislabeled by B-SZZ and AG-SZZ lead to 9%-10% and 1%-15% more wasted inspection effort in practice, respectively." |
| **Uso do Teste Scott-Knott ESD** | `classification_importance.R` | Linha 6 do Script | `library("ScottKnottESD")`: aplicado para agrupar estatisticamente as distribuições das 1.000 iterações de bootstrap. |
