# Ficha Estruturada de Pesquisa Científica — PESQUISA 3: SZZ Unleashed

---

## 1. Identificação

* **Título**: SZZ Unleashed: An Open Implementation of the SZZ Algorithm – Featuring Example Usage in a Study of Just-in-Time Bug Prediction for the Jenkins Project
* **Autores**: Markus Borg, Oscar Svensson, Kristian Berg, Daniel Hansson
* **Afiliações**: RISE Research Institutes of Sweden AB (Lund, Suécia); Dept. of Computer Science, Lund University (Suécia); Verifyter AB (Lund, Suécia); Axis Communications AB (Lund, Suécia)
* **Ano**: 2019
* **Venue**: Proceedings of the ACM / arXiv preprint (arXiv:1903.01742v2)
* **DOI**: https://doi.org/10.475/123_4 (arXiv: https://arxiv.org/abs/1903.01742)
* **URL**: https://arxiv.org/pdf/1903.01742
* **Repositório Oficial**: https://github.com/wogscpar/SZZUnleashed
* **Licença**: MIT License
* **Identificação Interna**: **PESQUISA 3**

---

## 2. Problema

* **Problema Científico**:
  A ausência de implementações públicas, abertas, independentes de linguagem e devidamente testadas do algoritmo SZZ para repositórios Git.
* **Causas Raízes e Consequências para a Ciência** [Seção 1]:
  1. *Reinvenção da Roda e Desperdício de Esforço*: Em um mapeamento sistemático de 187 estudos (Rodriguez-Perez et al., 2018), constatou-se que a vasta maioria dos pesquisadores reimplementa sua própria versão fechada do SZZ.
  2. *Ameaça à Credibilidade Científica*: Implementações proprietárias ou não divulgadas frequentemente não passam por testes adequados, podendo embutir defeitos de software internos que invalidam conclusões empíricas.
  3. *Limitações dos Grafos de Anotação Tradicionais*: O grafo de anotações clássico do SZZ falha quando múltiplas linhas adjacentes são modificadas simultaneamente, mapeando blocos inteiros de forma imprecisa entre revisões.

---

## 3. Perguntas de Pesquisa (Research Questions)

No estudo empírico ilustrativo de predição Just-in-Time (JIT) que acompanha a ferramenta, os autores formulam duas RQs formais [Seção 4.1]:

* **RQ1**: How does oversampling and undersampling affect the JIT bug prediction for highly imbalanced classes?
* **RQ2**: Does cross-validation generate better results than a time-sensitive evaluation setup?

---

## 4. Hipóteses

* **Hipótese 1 [FATO DOCUMENTADO - Seção 2 & 3]**: O rastreamento de linhas baseado em distância de edição (Line Number Mapping via distância de Jaccard e JGit) em vez de grafos rígidos de anotação provê uma solução agnóstica de linguagem de programação, viabilizando o SZZ para repositórios Git modernos sem dependência de parsers específicos de sintaxe.
* **Hipótese 2 [FATO DOCUMENTADO - Seção 4.1]**: Avaliações de predição de defeitos que utilizam validação cruzada tradicional (*k-fold cross-validation*) ignoram a flecha temporal dos commits e geram métricas infladas de forma artificial e irrealista quando comparadas a cenários com restrição temporal estrita (*online change classification*).

---

## 5. Objetivos

* **Objetivo Geral**:
  Desenvolver, disponibilizar sob licença aberta (MIT) e validar o **SZZ Unleashed**, uma implementação robusta em Java e Python do algoritmo SZZ para repositórios Git baseada na biblioteca JGit e no mapeamento de linhas de Williams & Spacco.
* **Objetivos Específicos**:
  1. Construir uma arquitetura em 2 fases: Fase 1 (extração e vinculação de Bug Reports do Jira via JQL e regex) e Fase 2 (rastreamento de commits indutores via JGit e distâncias de Jaccard).
  2. Implementar profundidade de rastreamento configurável (`depth >= 3`) para alcançar commits indutores em versões anteriores.
  3. Demonstrar a aplicabilidade prática do SZZ Unleashed extraindo o histórico de 12 anos do projeto Jenkins e treinando modelos de Random Forest para predição de defeitos Just-in-Time (JIT).
  4. Analisar empiricamente o impacto de técnicas de balanceamento de classes (SMOTE, SMOTE+Tomek, Cluster Centroids) e comparação metodológica entre Cross-Validation vs. Time-Sensitive Evaluation.

---

## 6. Contexto

* **Contexto Tecnológico e Industrial**:
  Desenvolvido em parceria com a empresa Axis Communications AB (Suécia) para automação de garantia de qualidade (Quality Assurance) e integração com o ecossistema Jenkins Core e Jira Issue Tracker.

---

## 7. Dados

* **Projeto Objeto de Estudo Principal**:
  Repositório oficial do servidor de automação **Jenkins Core** (`https://github.com/jenkinsci/jenkins`).
* **Período Analisado**:
  12 anos de desenvolvimento contínuo: de **05 de Novembro de 2006 a 20 de Fevereiro de 2018**.
* **Volume de Dados Extraído do Jenkins** [Tabela 1]:
  - **Total de Commits**: 26.378 commits.
  - **Bug-Fixing Commits (Fixes)**: 2.979 commits (11.3% do total).
  - **Bug-Introducing Commits (Bugs)**: 954 commits (3.6% do total — desbalanceamento severo de classes).
  - **Commits que são Fixes e Bugs simultaneamente**: 808 commits (3.1%).
* **Critérios de Seleção de Issues no Jira via JQL**:
  - `project = JENKINS`
  - `issuetype = Bug`
  - `status in (Resolved, Closed)`
  - `resolution = Fixed`
  - `component = core`
  - `created <= "2018-02-20 10:34"`
* **Expressões Regulares para Vinculação (Regex)**:
  - Formatos aceitos na mensagem de commit: `JENKINS-XXX`, `HUDSON-XXX` e `#XXX` (neste último, exige a presença da palavra `fix`).
  - Heurística de exclusão de falsos fixes: Descarte de mensagens contendo `merge`, `cherry pick` ou `nothing`.

---

## 8. Metodologia

O fluxo do SZZ Unleashed e do experimento JIT opera na seguinte sequência:

```
[DADOS: Jira REST API (JQL) + Git Log do Jenkins]
   │
[FASE 1: Identificação de Bug-Fixing Commits (BFC)]
   ├── Regex de IDs de issue (JENKINS, HUDSON, #ID)
   └── Filtro de exclusão de ruído (merge, cherry-pick)
   │
[FASE 2: Identificação de Bug-Introducing Commits (BIC)]
   ├── JGit Parser e Diffing de linhas modificadas
   ├── Line Number Mapping (Distância de Jaccard entre linhas)
   ├── Travessia em profundidade configurável (default depth = 3)
   └── Validação temporal com data de abertura da issue (Jira issue date)
   │
[ENGENHARIA DE FEATURES (16 Métricas): Churn, Diffusion, History, Experience, Coupling]
   │
[EXPERIMENTO JIT: Random Forest (200 árvores) + Balanceamento (SMOTE / Centroids)]
   │
[AVALIAÇÃO: Stratified 10-fold CV vs Online Change Classification (Time-Sensitive)]
```

### Características Técnicas do Motor SZZ Unleashed [Seção 3.2]:
1. **Biblioteca JGit**: Opera diretamente nos objetos internos e grafos de revisão do Git (blobs, commits, trees), eliminando chamadas lentas ao binário de linha de comando.
2. **Agnóstico de Linguagem**: Não realiza parsing específico de AST para linguagens particulares; rastreia linhas modificadas através de distâncias textuais de Jaccard.
3. **Profundidade Configurável (`depth`)**: Permite retroceder múltiplos saltos de blame (ex.: se a linha foi modificada no commit 6, retrocede para commit 4 e deste para commit 2).
4. **Tratamento de Fixes Parciais e Commits Posteriores**: Se um commit candidato for posterior à data da issue do Jira, ele é descartado, a menos que seja um fix parcial comprovado ou esteja vinculado como indutor de outro bug report.

---

## 9. Ferramentas

| Ferramenta | Versão Documentada | Finalidade | Configuração / Parâmetros |
| :--- | :--- | :--- | :--- |
| **Java / OpenJDK** | Java 8 | Ambiente de execução do motor principal de SZZ | OpenJDK 8 Alpine no Docker |
| **Eclipse JGit** | 4.10.0 | Manipulação de repositórios Git em baixo nível | Parsing estruturado de commits e diffs |
| **Gradle** | 4.10.3 | Gerenciamento de build e criação do fatJar executável | `gradle build && gradle fatJar` |
| **Python** | 3.x | Scripts de suporte (extração Jira e montagem de features) | Módulos em `fetch_jira_bugs/` e `data_assembler/` |
| **code-maat** | 1.1 | Mineração de acoplamento temporal (*change coupling*) | Gera métricas Ft14, Ft15 e Ft16 |
| **scikit-learn** | 0.20+ | Treinamento do classificador Random Forest | 200 estimadores (`n_estimators=200`) |
| **imbalanced-learn** | 0.4+ | Técnicas de amostragem de dados | SMOTE, SMOTE+Tomek, Cluster Centroids |

---

## 10. Algoritmos e Classificadores

* **Algoritmo de Rastreamento (SZZ)**:
  - *Line Number Mapping*: Rastreamento de linhas entre revisões por distância de Jaccard normalizada.
  - *Busca em Profundidade*: Parâmetro `depth = 3`.
* **Classificador Supervisionado (Estudo JIT)**:
  - **Random Forest**: 200 árvores de decisão.
* **Conjunto de 16 Features para Commits** [Tabela 2]:
  - *Code Churn*: Ft1 (Linhas adicionadas/total), Ft2 (Linhas deletadas/total), Ft3 (Arquivos alterados/total).
  - *Histórico e Difusão*: Ft4 (Linhas de código na versão anterior), Ft5 (Sub-sistemas modificados), Ft6 (Sub-diretórios modificados), Ft7 (Entropia da distribuição das mudanças), Ft8 (Propósito da mudança - bugfix vs feature).
  - *Experiência do Desenvolvedor*: Ft9 (Desenvolvedores anteriores no arquivo), Ft10 (Tempo desde a última contribuição), Ft11 (Número de alterações únicas), Ft12 (Experiência geral do autor), Ft13 (Experiência recente do autor).
  - *Acoplamento Temporal*: Ft14 (Arquivos altamente acoplados), Ft15 (Arquivos acoplados para todos os graus), Ft16 (Arquivos acoplados não-modificados).
* **Técnicas de Balanceamento de Classes Avaliadas**:
  - Baseline (Sem balanceamento — 3.6% de casos positivos).
  - SMOTE (Oversampling sintético da classe minoritária).
  - SMOTE + Tomek Links (Oversampling com limpeza de fronteira).
  - Cluster Centroids (Undersampling drástico da classe majoritária).

---

## 11. Métricas

1. **Precision, Recall e F1-Score**: Definidos convencionalmente para predição binária de commits defeituosos.
2. **Setup de Avaliação 1: Stratified 10-fold Cross-Validation**:
   - Embaralha o dataset aleatoriamente preservando a proporção de classes em 10 partições (ignora o tempo).
3. **Setup de Avaliação 2: Online Change Classification (Time-Sensitive)**:
   - Respeita rigorosamente a linha do tempo (treina apenas no passado, testa no futuro).
   - Parâmetros temporais [Seção 4.1]: $\text{SGAP}=331$, $\text{GAP}=73$, $\text{EGAP}=781$, $\text{Update}=200$ dias, $\text{Treino}=1.700$ dias, $\text{Teste}=400$ dias.

---

## 12. Resultados

### Acurácia da Predição de Defeitos JIT no Jenkins [Tabela 3]:

| Setup de Avaliação | Técnica de Amostragem | Precision | Recall | F1-Score |
| :--- | :--- | :---: | :---: | :---: |
| **Stratified 10-fold CV** | Baseline (sem amostragem) | $0.156 \pm 0.246$ | $0.026 \pm 0.042$ | $0.029 \pm 0.034$ |
| | SMOTE | $0.123 \pm 0.076$ | $0.212 \pm 0.136$ | $0.154 \pm 0.096$ |
| | SMOTE + Tomek | $0.117 \pm 0.071$ | $0.206 \pm 0.130$ | $0.148 \pm 0.091$ |
| | Cluster Centroids | $0.037 \pm 0.001$ | $0.945 \pm 0.037$ | $0.072 \pm 0.002$ |
| **Online Change (Time-Sensitive)** | Baseline (sem amostragem) | $0.210 \pm 0.177$ | $0.017 \pm 0.014$ | $0.031 \pm 0.026$ |
| | SMOTE | $0.147 \pm 0.041$ | $0.104 \pm 0.034$ | $0.116 \pm 0.031$ |
| | SMOTE + Tomek | $0.163 \pm 0.018$ | $0.126 \pm 0.043$ | **$0.137 \pm 0.030$** |
| | Cluster Centroids | $0.028 \pm 0.004$ | $0.917 \pm 0.037$ | $0.054 \pm 0.008$ |

### Respostas às RQs:
* **Resposta à RQ1 (Oversampling & Undersampling)**:
  Oversampling é mandatório em cenários de extremo desbalanceamento (3.6% de defeitos no Jenkins). Sem amostragem, o modelo é ultraconservador e falha (Recall $< 3\%$). SMOTE e SMOTE+Tomek elevam o F1 de $0.03$ para $\approx 0.15$. O undersampling com Cluster Centroids infla o recall para $> 90\%$, mas derruba a precisão para $< 4\%$, inviabilizando o uso prático.
* **Resposta à RQ2 (Cross-Validation vs. Time-Sensitive)**:
  Confirmou-se que Cross-Validation gera resultados enganosamente otimistas. No entanto, enquanto Tan et al. afirmavam que a CV inflava a precisão, os autores descobriram que **a CV infla principalmente o Recall** (o recall do SMOTE em CV foi o dobro do recall observado na avaliação temporal realista: $0.212$ vs $0.104$).
* **Conclusão Prática sobre o JIT com SZZ Puro**:
  Os autores declaram com franqueza científica que um F1-Score entre **0.10 e 0.15** é insuficiente para adoção industrial na prática (gera falsos alarmes excessivos para os desenvolvedores).

---

## 13. Ameaças à Validade

* **Validade de Construção (Construct Validity)**:
  - O SZZ Unleashed não filtra mudanças cosméticas de código (espaços, formatação) por buscar ser agnóstico de linguagem. Conforme verificado por Rosa et al. (Pesquisa 2), isso faz com que o SZZ Unleashed gere **outliers de falsos positivos** em alguns commits, derrubando sua precisão global.
* **Validade Interna (Internal Validity)**:
  - A acurácia do classificador JIT depende inteiramente da qualidade dos rótulos gerados pelo SZZ. Se o SZZ cometer erros de rotulagem de BICs, o classificador aprenderá ruído (*garbage in, garbage out*).
* **Validade Externa (External Validity)**:
  - O case study empírico é limitado a um único grande projeto de código aberto (Jenkins).

---

## 14. Artefatos Disponibilizados

* **Repositório GitHub**: `https://github.com/wogscpar/SZZUnleashed`
* **Código-Fonte**:
  - `szz/src/main/java/Main.java`: Ponto de entrada do executável Java.
  - `szz/src/main/java/heuristics/DistanceIntroducerFinder.java`: Algoritmo de busca por distância de Jaccard.
  - `fetch_jira_bugs/fetch.py`: Extrator de issues da API REST do Jira.
  - `data_assembler/assemble_features.py`: Montador do dataset de 16 features.
* **Automação e Container**:
  - `szz/build.gradle`: Script de empacotamento com plugin `fatJar`.
  - `Dockerfile`: Imagem Docker pronta baseada em `java:8-jdk-alpine`.

---

## 15. Replicabilidade

* **Classificação**: **Diretamente replicável** (com adaptações de versão de Java)
* **Justificativa**:
  O repositório é completamente autônomo e de código aberto. A compilação exige Java 8 (OpenJDK 8) e Gradle 4.10.x. Para rodar sobre o Jenkins, os scripts em Python baixam as issues públicas do Jira da comunidade Jenkins.

---

## 16. Protocolo de Replicação Local

1. **Pré-requisitos**:
   - OpenJDK 8 instalado (`java -version` indicando 1.8.x).
   - Gradle 4.10.3 (ou usar a imagem Docker fornecida).
   - Python 3 com bibliotecas `requests`, `scikit-learn`, `imbalanced-learn`.
2. **Ambiente**:
   - Sistema Operacional: Linux / Ubuntu.
   - RAM: $\ge 4$ GB.
3. **Dependências**:
   - Java 8 JDK e Gradle.
4. **Como Compilar o Executável JAR**:
   ```bash
   cd /home/artur-carvalho/mestrado/repos/03-szz-unleashed/szz
   gradle build && gradle fatJar
   ```
   Gera o artefato executável: `build/libs/szz_find_bug_introducers-0.1.jar`.
5. **Dataset Necessário**:
   - Repositório Git alvo (ex.: Jenkins ou mini-repositório local) e JSON de issues do Jira.
6. **Como Executar o SZZ Unleashed**:
   ```bash
   java -jar build/libs/szz_find_bug_introducers-0.1.jar \
     -i /path/to/issue_list.json \
     -r /path/to/git_repository \
     -d 3
   ```
7. **Parâmetros**:
   - `-i`: Caminho para o JSON de issues contendo IDs e timestamps de abertura.
   - `-r`: Caminho absoluto do repositório Git local.
   - `-d`: Profundidade de travessia do blame (`depth`, default = 3).
8. **Métricas a Coletar**:
   - Arquivo de saída `issue_commits.json` relacionando cada bug report ao commit indutor detectado.
9. **Critérios de Sucesso**:
   - Geração bem-sucedida do `issue_commits.json` sem falhas de I/O no JGit.
10. **Problemas Conhecidos**:
    - Vulnerabilidade a commits com diffs enormes (*outliers*), gerando listas extensas de candidatos que exigem filtragem posterior.

---

## 17. Gaps de Replicação

1. **Legado de Java 8**: O código depende de versões antigas do JGit (4.10.0 de 2017) e do Gradle 4.x, exigindo compatibilidade estrita com Java 8 (falha em compilar diretamente sob Java 17 ou Java 21 sem ajustes de compatibilidade).
2. **Ausência de Filtros Semânticos Nativos**: A ferramenta não possui módulos para ignorar refatorações (`RefactoringMiner`) ou ruído de comentários, transferindo essa responsabilidade para pré/pós-processamento.

---

## 18. Controle de Rastreabilidade

| Afirmação / Dado Documentado | Documento Fonte | Seção / Página | Evidência Textual no Artigo |
| :--- | :--- | :--- | :--- |
| **Definição de RQ1 e RQ2** | `03-szz-unleashed.pdf` | Seção 4.1, pág. 3 | "RQ1: How does oversampling and undersampling affect... RQ2: Does cross-validation generate better results..." |
| **Uso da Biblioteca JGit** | `03-szz-unleashed.pdf` | Seção 3, pág. 2 | "To facilitate interaction with git repositories, SZZ Unleashed uses the JGit library [21] maintained by the Eclipse Foundation." |
| **Uso de Line Mapping via Jaccard** | `03-szz-unleashed.pdf` | Seção 2, pág. 2 | "The current implementation of SZZ Unleashed is based on Jaccard distances... line number mappings are used to backtrack through the change history." |
| **Profundidade Padrão depth = 3** | `03-szz-unleashed.pdf` | Seção 3.2, pág. 2-3 | "How deeply SZZ Unleashed should traverse the graph is configurable, but the default value is 3." |
| **Estatísticas do Jenkins (26.378 commits)** | `03-szz-unleashed.pdf` | Seção 4.2, Tabela 1, pág. 3 | "Jenkins: Commits 26,378; Bugs 954 (3.6%); Fixes 2,979 (11.3%); Fixes ∩ Bugs 808 (3.1%)." |
| **Descoberta sobre Inflação de Recall na CV** | `03-szz-unleashed.pdf` | Seção 4.3, pág. 4 | "...cross-validations results in falsely high precision... in our study, however, we instead observe this phenomenon for recall. Cross-validation obtains roughly twice as high recall as the time-sensitive setup." |
| **F1-Score Insuficiente para Prática (0.10 - 0.15)** | `03-szz-unleashed.pdf` | Seção 4.3, pág. 4 | "...we do not think JIT bug prediction corresponding to an F1 score of 0.10–0.15 is sufficiently accurate to be of practical value for developers." |
