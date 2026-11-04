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
  - O arquivo em [`papers/02-pyszz-v2.pdf`](file:///home/artur-carvalho/mestrado/papers/02-pyszz-v2.pdf) foi imediatamente atualizado com o PDF legítimo e todo o fichamento foi executado sobre o texto integral autêntico.
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
