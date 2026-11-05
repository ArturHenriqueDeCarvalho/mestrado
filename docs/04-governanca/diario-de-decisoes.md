# Diário de Decisões Metodológicas e Rastreabilidade Científica

Este documento registra formalmente todas as escolhas, adaptações, critérios de inclusão/exclusão e decisões de desenho experimental tomadas ao longo da pesquisa. Ele serve como fonte direta de evidência para a redação da **Seção de Metodologia**, **Desenho Experimental** e **Ameaças à Validade** do artigo científico (Banca de Dezembro) e da Dissertação de Mestrado.

---

## 📌 Registro de Decisões

### DEC-001: Estratégia de Coleta de Dados e Amostragem Baseada em Replication Packages Oficiais

* **Data**: 03/11/2026
* **Decisão Metodológica**: 
  - Não realizar o download integral do histórico Git completo (dezenas a centenas de GBs) de todos os ecossistemas de software analisados nos artigos originais (ex.: repositórios inteiros da Apache Foundation, Linux Kernel ou Chromium).
  - Adotar como padrão de **Engenharia de Software Empírica (ESE)** a utilização direta dos **Replication Packages oficiais** disponibilizados pelos autores (arquivos pré-extraídos, JSONs estruturados, tabelas consolidadas no Figshare/Zenodo e benchmarks como JIT-Fine).
  - Para testes empíricos de algoritmos e validações locais de execução, aplicar **amostragem controlada (sample-based replication)** e, quando estritamente necessária a inspeção de histórico versionado, utilizar **Git Blobless Clones (`--filter=blob:none`)**.
* **Motivo & Racional Científico**:
  1. **Fidelidade aos Estudos Originais**: Os pacotes de replicação preservam os exatos commits, diffs e rótulos selecionados e filtrados pelos autores (evitando variações temporais de repositórios que continuaram evoluindo após a publicação dos papers).
  2. **Viabilidade e Eficiência Computacional**: Permite a execução, auditoria e depuração direta 100% local no workspace do agente e do pesquisador sem estouro de armazenamento ou estrangulamento de I/O em disco.
  3. **Reprodutibilidade Exata**: Qualquer outro pesquisador pode reproduzir os experimentos a partir dos pacotes de dados oficiais arquivados com DOI persistente (Figshare/Zenodo).
* **Pesquisas Afetadas**: Pesquisas 1, 2, 3, 4, 5 e 6.
* **Impacto na Escrita do Artigo (Seções Afetadas)**:
  - *Metodologia / Procedimentos de Coleta*: Detalhar a rastreabilidade aos pacotes de replicação arquivados e critérios de corte.
  - *Ameaças à Validade (Validade de Construção / Externa)*: Discutir a representatividade da amostragem e a estabilidade dos conjuntos de teste frente aos repositórios vivos.

---

### DEC-002: Arquitetura de Execução 100% Local-First para Auditoria por Agentes

* **Data**: 03/11/2026
* **Decisão Metodológica**:
  - Centralizar a execução de scripts, logs brutos, testes e geração de métricas diretamente no disco local do workspace (`/home/artur-carvalho/mestrado`), priorizando CPU para SZZ/mineração e inferência de checkpoints pré-treinados em CPU local (ou API gratuita do Gemini com cota estudantil para LLM-SZZ).
* **Motivo & Racional Científico**:
  1. **Auditoria Contínua**: Permite ao sistema de agentes e ao pesquisador inspecionar artefatos brutos em tempo real, sem pontos cegos resultantes de ambientes remotos desacoplados.
  2. **Rastreabilidade Fim a Fim**: Cada tabela e gráfico do artigo é gerado diretamente a partir de arquivos inspecionáveis no repositório local.
* **Pesquisas Afetadas**: Todas as 6 pesquisas.


---

### DEC-003: Retificação e Rastreabilidade do Artigo Científico da Pesquisa 2 (PySZZ v2)

* **Data**: 03/11/2026
* **Decisão Metodológica**:
  - Retificar o link de acesso aberto do paper da Pesquisa 2. A referência inicial continha o link `https://arxiv.org/pdf/2103.02388` (que corresponde a um paper não-relacionado de dinâmica de fluidos devido a erro de digitação de dígito no identificador).
  - A fonte oficial correta do trabalho de Giovanni Rosa et al. (*A comprehensive evaluation of SZZ Variants through a developer-informed oracle* / ICSE 2021 / JSS 2023, DOI: `10.1016/j.jss.2023.111729`) é o **arXiv:2102.03300** (`https://arxiv.org/abs/2102.03300`).
  - O arquivo em [`papers/04-lszz-pyszz-icse2021.pdf`](file:///home/artur-carvalho/mestrado/papers/04-lszz-pyszz-icse2021.pdf) foi imediatamente atualizado com o PDF legítimo e todo o fichamento foi executado sobre o texto integral autêntico.
* **Motivo & Racional Científico**:
  Garantir a integridade absoluta da literatura científica de referência e evitar contaminação do referencial teórico da dissertação e do artigo da banca de Dezembro.
* **Pesquisas Afetadas**: Pesquisa 2 (PySZZ v2).


---

### DEC-004: Retificação e Rastreabilidade do Artigo Científico da Pesquisa 4 (SZZ-TSE)

* **Data**: 03/11/2026
* **Decisão Metodológica**:
  - Retificar a referência documental da Pesquisa 4. O link fornecido preliminarmente (`https://arxiv.org/pdf/1908.01234`) correspondia a um artigo de dosimetria eletromagnética biomédica devido a colisão de dígitos no identificador arXiv.
  - O artigo científico autêntico associado ao repositório `https://github.com/YuanruiZJU/SZZ-TSE` é **"The Impact of Changes Mislabeled by SZZ on Just-in-Time Defect Prediction"** (Yuanrui Fan, Xin Xia, Daniel Alencar da Costa, David Lo, Ahmed E. Hassan, Shanping Li), publicado no periódico *IEEE Transactions on Software Engineering (TSE)*, DOI: `10.1109/TSE.2019.2929761`.
  - A análise documental e a auditoria de replicação são conduzidas com base no artigo da IEEE TSE e no repositório oficial `YuanruiZJU/SZZ-TSE`.
* **Motivo & Racional Científico**:
  Garantir fidelidade metodológica absoluta e rastreabilidade documental inviolável para a banca de qualificação do Mestrado e redação do artigo científico.
* **Pesquisas Afetadas**: Pesquisa 4 (SZZ-TSE).

---

### DEC-005: Retificação Documental e Rastreabilidade Científica da Pesquisa 6 (JIT-Smart / JIT-Fine)

* **Data**: 03/11/2026
* **Decisão Metodológica**:
  - Retificar a referência documental da Pesquisa 6. O link fornecido preliminarmente (`https://arxiv.org/pdf/2112.08630`) correspondia a um artigo de física de matéria condensada (*"Spin Hall Conductivity... in Full Heusler compounds"*) decorrente de colisão/typo de identificador no prompt original.
  - A publicação científica legítima e canônica correspondente ao repositório `https://github.com/JIT-A/JIT-Smart` é:
    - **Artigo**: *"JIT-Smart: A Multi-Task Learning Framework for Just-In-Time Defect Prediction and Localization"*
    - **Autores**: Xiangping Chen, Furen Xu, Yuan Huang, Neng Zhang, Zibin Zheng (Sun Yat-sen University / Zhejiang University)
    - **Veículo**: *Proceedings of the ACM on Software Engineering* (PACMSE / ACM FSE 2024), DOI: `10.1145/3643727`.
  - O repositório associado integra diretamente o ecossistema e o pacote de dados do trabalho seminal que serviu de base e dataset de linhagem direta:
    - **Artigo Base (Linha de Base & Dataset)**: *"The Best of Both Worlds: Integrating Semantic Features with Expert Features for Defect Prediction and Localization"* (Chao Ni, Wei Wang, Kaiwen Yang, Xin Xia, Kui Liu, David Lo), publicado na *30th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE 2022)*, DOI: `10.1145/3540250.3549165` (Repositório: `https://github.com/jacknichao/JIT-Fine`).
    - **Dataset Canônico**: **JIT-Defect4J** (21 projetos Java com rotulagem bivariada: nível de commit e nível de linha de código).
  - O fichamento da Pesquisa 6 documenta de forma explícita e rigorosa tanto a arquitetura multi-tarefa inovadora do JIT-Smart (DLN + CodeBERT + MultiFocalLoss) quanto a linhagem empírica herdada do JIT-Fine/JIT-Defect4J.
* **Motivo & Racional Científico**:
  Assegurar fidelidade documental inquestionável, prevenir qualquer alucinação e respaldar a redação da dissertação e do artigo científico nas publicações arbitradas oficiais da ACM (FSE 2022 e FSE 2024).
* **Pesquisas Afetadas**: Pesquisa 6 (JIT-Smart / JIT-Fine).

---

### DEC-006: Definição do Foco Central da Pesquisa (Análise de Sobreposições e Treinamento de Classificadores para Mensurar o Impacto da IA em Cada Método)

* **Data**: 04/11/2026
* **Decisão Metodológica**:
  - Estruturar a Segunda Parte (Foco Empírico Central da Pesquisa do Artigo de Dezembro e da Dissertação de Mestrado) em dois pilares experimentais acoplados após a replicação individual das 6 pesquisas:
    1. **Investigação de Possíveis Sobreposições entre os Resultados e Conjuntos de Dados (*Overlap & Agreement Analysis*)**:
       - Quantificar matematicamente a interseção, concordância e exclusividade entre os commits indutores de bug/vulnerabilidade identificados pelas variantes SZZ (`B-SZZ`, `AG-SZZ`, `MA-SZZ`, `L-SZZ`, `R-SZZ`, `RA-SZZ`, `PyDriller-SZZ`, `SZZ Unleashed`, `V-SZZ` e `LLM-SZZ`).
       - Utilizar métricas formais de sobreposição: **Índice de Similaridade de Jaccard** ($J(A,B) = \frac{|A \cap B|}{|A \cup B|}$), **Taxa de Sobreposição Direcional / Coeficiente de Szymkiewicz-Simpson** ($\frac{|A \cap B|}{\min(|A|, |B|)}$), **Kappa de Cohen ($\kappa$)** para concordância inter-algoritmos, **Unique True Positives ($UTP$)** e matrizes de discordância de rótulos nos ecossistemas em comum (como os 10 projetos Apache de `04-szz-tse` com 126.526 commits, os 21 projetos Java do `JIT-Defect4J` em `06-jit-smart` e o benchmark de CVEs C/Java em `01-llm-szz` e `02-pyszz-v2`).
    2. **Treinamento de Classificadores para Mensurar o Impacto da IA em Cada Método (*AI Impact Assessment via Classifier Training*)**:
       - Treinar e avaliar sistematicamente classificadores sobre os dados/rótulos gerados por cada método para isolar e quantificar o ganho (ou degradação) real proporcionado pela Inteligência Artificial em duas frentes:
         - **Frente A — Impacto da Rotulagem SZZ (Heurística vs. Sintática vs. LLM) sobre Classificadores Downstream**: Treinar famílias de classificadores tradicionais (`Naive Bayes`, `Logistic Regression`, `Random Forest`, `XGBoost` / `LightGBM`) e modelos neurais sobre os conjuntos rotulados por cada variante (`buggy_B2`, `buggy_AG`, `buggy_MA`, `buggy_RA`, `SZZ Unleashed` e `LLM-SZZ`), avaliando como a qualidade e a sobreposição dos rótulos alteram a performance preditiva (`AUC`, `F1`, `G-Mean`) e o esforço desperdiçado (`Wasted Effort LOC`, `Recall@20%Effort`, $P_{\text{opt}}$).
         - **Frente B — Impacto das Arquiteturas de IA na Predição e Localização Just-in-Time (ML Clássico vs. Deep Learning vs. Transformers/Co-Learning)**: Treinar e comparar sob as mesmas partições de dados (`JIT-Defect4J` / `CC2Vec` / `SZZ-TSE`) classificadores baseados em engenharia de atributos manuais (`LApredict`, `Random Forest`, `Logistic Regression`, `JITLine`) contra arquiteturas de Deep Learning (`Deeper`, `DeepJIT`, `CC2Vec`) e arquiteturas baseadas em Transformers/Multi-Task Learning (`JIT-Fine / CodeBERT`, `JIT-Smart / DLN`), medindo exatamente quanto a IA agrega em cada método e tarefa.
* **Motivo & Racional Científico**:
  1. **Originalidade Científica**: A literatura avalia algoritmos SZZ e modelos JIT-DP/JIT-DL em silos separados. Investigar simultaneamente a **sobreposição de resultados entre os métodos** e **treinar classificadores comparativos para medir o impacto da IA em cada um** cria uma contribuição empírica inédita de síntese cruzada (*cross-cutting empirical study*).
  2. **Rigor Estatístico**: Permite aplicar testes não-paramétricos pareados (*Wilcoxon Signed-Rank Test*, *Cliff's Delta* e agrupamento *Scott-Knott ESD*) sobre as distribuições de desempenho dos classificadores com e sem IA em cada método.
* **Pesquisas Afetadas**: Todas as 6 pesquisas (`01-llm-szz` a `06-jit-smart`).
* **Impacto na Escrita do Artigo (Seções Afetadas)**:
  - *Questões de Pesquisa (RQs)*, *Desenho Experimental*, *Resultados Empíricos* e *Discussão*.

---

### DEC-007: Protocolo de Versionamento Atômico e Rastreabilidade Git por Etapas Experimentais

* **Data**: 04/11/2026
* **Decisão Metodológica**:
  - Adotar estritamente o padrão de **Versionamento Atômico em Engenharia de Software Empírica (ESE)** para toda a execução experimental do Mestrado.
  - O fluxo de trabalho proíbe branches genéricas acumulativas e segue rigorosamente a regra: **1 Branch Atômica por Etapa $\rightarrow$ 1 Conjunto de Scripts/Resultados Específicos $\rightarrow$ 1 Commit Semântico $\rightarrow$ Merge na `main`**.
  - As 10 etapas sequenciais são padronizadas da seguinte forma:
    1. **Fase 1: Replicação e Validação Individual dos Ambientes (Passo a Passo)**
       - `step-01/setup-e-replicacao-szz-tse`: Ambiente, extração dos 126.526 commits e validação dos 4 rótulos SZZ (`B`, `AG`, `MA`, `RA`) nos 10 projetos Apache.
       - `step-02/setup-e-replicacao-pyszz-v2`: Ambiente, binários externos (`srcML`, `RefactoringMiner`) e execução das 9 variantes SZZ sobre repositórios de teste.
       - `step-03/setup-e-replicacao-szz-unleashed`: Ambiente Java/JGit e Python, validação do fatJar e baseline JIT do Jenkins.
       - `step-04/setup-e-replicacao-llm-szz`: Ambiente, cadeias de prompts reflexivos e baseline no benchmark de CVEs C/C++ e Java.
       - `step-05/setup-e-replicacao-cc2vec`: Ambiente PyTorch/CPU, representação vetorial hierárquica e tarefa downstream de predição JIT.
       - `step-06/setup-e-replicacao-jit-smart`: Ambiente CodeBERT/Multi-Task e validação do benchmark `JIT-Defect4J` (21 projetos Java).
    2. **Fase 2: O Foco Central da Pesquisa (Sobreposições e Classificadores com IA)**
       - `step-07/analise-sobreposicao-resultados-szz`: Análise quantitativa de sobreposição (Jaccard, Simpson, Kappa de Cohen, UTP e zona de discordância inter-algoritmos).
       - `step-08/classificadores-impacto-rotulagem-szz`: Treinamento da bateria de classificadores (ML clássico vs. Neural) sobre cada rótulo SZZ e cálculo de `Wasted Effort LOC`.
       - `step-09/classificadores-impacto-arquiteturas-ia`: Treinamento e comparação pareada Sem IA vs. Deep Learning vs. Transformers/Co-Learning no `JIT-Defect4J`.
       - `step-10/resiliencia-ia-zona-consenso-divergencia`: Teste de sensibilidade e resiliência dos classificadores ao ruído na zona cinzenta vs. zona de consenso.
* **Motivo & Racional Científico**:
  1. **Auditabilidade Exata**: Permite que a banca examinadora do Mestrado e revisores de periódicos verifiquem no Git exatamente o commit e o código que produziram cada dado e gráfico do artigo.
  2. **Isolamento de Erros e Regressões**: Se qualquer dependência ou script falhar, apenas a respectiva branch atômica é afetada, sem contaminação dos demais experimentos.
  3. **Rastreabilidade Fim a Fim na Metodologia**: A seção de Metodologia e Procedimentos Experimentais do artigo pode citar com precisão a sequência cronológica e técnica seguida.
* **Pesquisas Afetadas**: Todas as 6 pesquisas (`01-llm-szz` a `06-jit-smart`).
* **Impacto na Escrita do Artigo (Seções Afetadas)**:
  - *Metodologia / Procedimentos Experimentais*, *Reprodutibilidade e Pacote de Replicação (Artifact Badging)*.

---

### DEC-008: Descontinuação de CC2Vec e JIT-Smart e Consolidação Exclusiva em Derivações do SZZ

* **Data**: 05/11/2026
* **Decisão Metodológica**:
  - Descontinuar formalmente as pesquisas `05-cc2vec` e `06-jit-smart` da esteira principal da pesquisa de Mestrado e da redação do artigo científico da banca.
  - O escopo científico passa a ser **100% restrito a algoritmos e derivações do SZZ (identificação e rastreamento de commits indutores de bugs e vulnerabilidades de segurança - Bug/Vulnerability-Inducing Commit Identification)**.
  - O repositório e seus agentes adotam uma matriz comparativa com **10 Algoritmos SZZ** e **10 Bases de Dados Empíricas com oráculos científicos conhecidos**, contemplando obrigatoriamente **4 abordagens baseadas em Modelos de Linguagem Grandes (LLMs)**.
* **Motivo & Racional Científico**:
  1. **Coerência Epistemológica**: Evita dispersão temática entre tarefas de predição/classificação Just-in-Time tradicional (JIT-DP/JIT-DL) e a tarefa estrita de localização causal de indução de falhas (SZZ).
  2. **Alinhamento com a Banca Examinadora**: Atende à orientação direta do professor orientador para avaliar em profundidade as famílias do SZZ.
* **Pesquisas Afetadas**: Pesquisa 5 (`CC2Vec`) e Pesquisa 6 (`JIT-Smart`), transferidas para arquivo histórico (`legacy/`).
* **Impacto na Escrita do Artigo**:
  - *Introdução*, *Trabalhos Relacionados*, *Taxonomia de SZZ* e *Questões de Pesquisa (RQ1, RQ2, RQ3)*.

---

### DEC-009: Seleção do Apache Flink como Base de Código Unificada de Grande Porte para Benchmark Pareado

* **Data**: 05/11/2026
* **Decisão Metodológica**:
  - Adotar o repositório oficial do **Apache Flink** (`apache/flink`) como a base de código unificada para executar, calibrar e confrontar lado a lado todos os 10 algoritmos SZZ.
  - Para conciliar o grande volume do projeto (~35.000+ commits) com o rigor de execução local sem sobrecarga de armazenamento (`DEC-001` e `DEC-002`), o clone será realizado em modo *blobless* (`git clone --filter=blob:none https://github.com/apache/flink.git`).
* **Motivo & Racional Científico**:
  1. **Complexidade e Relevância Industrial**: O Apache Flink é um sistema distribuído de grande porte em Java, com histórico evolutivo maduro, frequentes refatorações estruturais de API e dezenas de vulnerabilidades CVEs documentadas no NVD.
  2. **Discriminação de Desempenho**: Fornece o cenário empírico perfeito para demonstrar onde os métodos heurísticos falham por ruído e onde as abordagens sintáticas (AST/Refatoração) e os agentes de LLM desambiguam a causa raiz.
* **Pesquisas Afetadas**: Todos os 10 Algoritmos SZZ.
* **Impacto na Escrita do Artigo**:
  - *Metodologia / Objeto de Estudo (Subject System)* e *Resultados Empíricos*.

---

### DEC-010: Definição da Matriz Experimental 10x10 com 4 Variantes LLM-SZZ e Oráculos de Ground Truth

* **Data**: 05/11/2026
* **Decisão Metodológica**:
  - Estruturar a avaliação comparativa cruzada em 10 algoritmos SZZ divididos em 3 famílias:
    1. *Heurísticos Tradicionais*: `B-SZZ` (FSE 2005), `AG-SZZ` (ASE 2006), `MA-SZZ` (EMSE 2017).
    2. *Sintáticos e Refatoração*: `L-SZZ` (ICSE 2021), `RA-SZZ` (TSE 2021), `SZZ Unleashed` (ESEM 2019).
    3. *Baseados em LLMs*: `LLM-SZZ` (FSE 2024), `LLM4SZZ` (2025), `AgentSZZ` (ASE 2026), `Prompt-SZZ / CoT` (Baseline).
  - Avaliar o desempenho contra 10 bases com oráculos conhecidos da literatura:
    - 5 Projetos Apache do SZZ-TSE (ActiveMQ, Camel, Derby, HBase, Hadoop Common) com oráculo `RA-SZZ`;
    - Jenkins Core (SZZ Unleashed / JGit Oracle);
    - Developer-Informed Oracle DIO (1.930 commits validados por humanos);
    - 3 Benchmarks de Segurança (CVE C/C++, CVE Java, VICBench/VulnCommit).
* **Motivo & Racional Científico**:
  Garantir comparabilidade científica direta e rigorosa com as publicações arbitrais originais de cada método.
* **Pesquisas Afetadas**: Todos os 10 algoritmos.
* **Impacto na Escrita do Artigo**:
  - *Desenho Experimental*, *Ameaças à Validade* e *Discussão Comparativa*.
