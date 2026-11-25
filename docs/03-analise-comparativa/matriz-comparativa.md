# Matriz Comparativa: 10 Algoritmos SZZ x 20 Bases Empíricas (12 Atuais + 8 Futuras) e Benchmark Unificado Apache Flink (E1 a E8)

> [!IMPORTANT]
> **Governança Metodológica (`DEC-008`, `DEC-011`, `DEC-012`, `DEC-013`)**: Esta matriz consolida os **10 Algoritmos SZZ** (incluindo as 4 abordagens de LLMs com ablação), as **12 Bases Locais Atuais (`B01–B12`, 191.704 commits já presentes no disco)**, o roadmap para as **20 Bases Maximizadas (`B01–B20`, >309k commits curados, 14 Java + 6 Python)** e o benchmark unificado do **Apache Flink** (`apache/flink`) com **8 Cenários de Estresse (`E1` a `E8`)**.

---

## 🏛️ 1. Mapeamento dos 10 Algoritmos SZZ e seus Artigos de Origem

| ID | Algoritmo SZZ | Família Técnica | Artigo Científico Publicado | Veículo / Ano / DOI | Ponto Exato de Superioridade (Tese do Paper) |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **A01** | **B-SZZ** | Heurística Clássica | Śliwerski et al.: *"When Do Changes Induce Fixes?"* | ACM SIGSOFT FSE (2005)<br>`10.1145/1083142.1083147` | Alta revocação (*recall*) bruta e simplicidade operacional em bugs mono-linha diretos ($O(1)$ blame). |
| **A02** | **AG-SZZ** | Heurística Anotação | Kim et al.: *"Automatic Identification of Bug-Introducing Changes"* | IEEE/ACM ASE (2006)<br>`10.1109/ASE.2006.23` | Imunidade a ruídos em anotações de código (`@Override`, cabeçalhos de licença). |
| **A03** | **MA-SZZ** | Heurística Metadados | da Costa et al.: *"Evaluating the Impact of Min. Age, Comments and Blank Lines"* | Empirical Software Engineering (EMSE 2017)<br>`10.1007/s10664-016-9466-9` | Eliminação de falsos positivos decorrentes de comentários, Javadoc e linhas em branco. |
| **A04** | **L-SZZ** | Sintático AST | Rosa et al.: *"A Comprehensive Evaluation of SZZ Variants through a Developer-Informed Oracle"* | IEEE/ACM ICSE (2021) / JSS (2023)<br>`10.1016/j.jss.2023.111729` | Imunidade a alterações cosméticas que preservam a AST compilada (`srcML 1.2.0`). |
| **A05** | **RA-SZZ** | Sintático Refatoração | Neto et al. (2018) & Fan et al.: *"The Impact of Changes Mislabeled by SZZ"* | IEEE Transactions on Software Engineering (TSE 2021)<br>`10.1109/TSE.2019.2929761` | Padrão-ouro na detecção e filtragem de métodos extraídos e classes renomeadas (`RefactoringMiner 2.0`). |
| **A06** | **SZZ Unleashed** | Sintático JGit | Borg et al.: *"SZZ Unleashed: An Open Implementation of the SZZ Algorithm"* | ACM/IEEE ESEM / arXiv (2019)<br>`arXiv:1903.01742` | Rastreamento em profundidade através de grafos de anotação de arquivo (Jaccard depth $\ge 3$). |
| **A07** | **LLM-SZZ** *(LLM 1)* | LLM Prompt Chaining | Fan et al.: *"Vulnerability-Inducing Commit Identification Driven by LLMs & CVE"* | ACM PACMSE / FSE (2024)<br>`songli.io/papers/LLM-SZZ.pdf` | Desambiguação de commits emaranhados (*tangled*) e patches onde o fix apenas adiciona checagens defensivas sem deletar linhas. |
| **A08** | **LLM4SZZ** *(LLM 2)* | LLM Ability Check | Tang et al.: *"LLM4SZZ: Enhancing SZZ Algorithm with Context-Enhanced Assessment on LLMs"* | arXiv (2025 / ACM TOSEM)<br>`arXiv:2504.01404` | Chaveamento via *Ability Check* entre *Context-Enhanced Identification* e *Rank-based Suspicious Statement Identification*. |
| **A09** | **AgentSZZ** *(LLM 3)* | LLM ReAct Agent | Risse & Böhme: *"AgentSZZ: Teaching the LLM Agent to Play Detective with Bug-Inducing Commits"* | IEEE/ACM ASE (2026)<br>`niklasrisse/agents-for-szz` | Auditoria investigativa multi-turn atuando como um detetive autônomo com comandos de histórico Git. |
| **A10** | **Prompt-SZZ** *(LLM 4)* | LLM Zero-Shot CoT | Baseline Canônico de LLM (Tang et al., 2025; Fan et al., 2024) | Baseline padronizado em LLM4SZZ e LLM-SZZ | Raciocínio rápido passo a passo (*Chain-of-Thought*) em turno único para medição de custo-benefício. |

---

## 📦 2. Matriz das 20 Bases Empíricas (12 Bases Atuais Locais vs. 8 Bases Futuras)

A pesquisa estrutura-se sobre a mesma linhagem canônica de Engenharia de Software Empírica e Just-In-Time Defect Prediction (as 14 métricas de mudança de Kamei et al., 2013), agrupadas em:
- **Fase 1 (Escopo Atual — 100% Local no Disco)**: 12 Bases (`B01–B12`), totalizando **191.704 commits**.
- **Fase 2 (Escalonamento Futuro com Agentes)**: 8 Bases adicionais (`B13–B20`), atingindo **>309.000 commits curados** (>430k no Git).

| ID | Nome do Projeto / Repositório | Linguagem | Volume de Commits | Oráculo & Formato | Origem & Linhagem Científica | Status no Projeto |
| :-: | :--- | :---: | :---: | :--- | :--- | :---: |
| **B01** | **Apache ActiveMQ** | Java | 7.753 commits | `B, AG, MA, RA-SZZ` + 14 JIT Feats | Fan et al. (IEEE TSE 2021) / ApacheJIT (MSR 2022) | **ATUAL (Em disco)** |
| **B02** | **Apache Camel** *(Base-Ponte)* | Java | 17.374 commits | `B, AG, MA, RA-SZZ` + Par Humano | Fan et al. (IEEE TSE 2021) / **Song et al. (FSE 2023)** | **ATUAL (Em disco)** |
| **B03** | **Apache Derby** | Java | 9.775 commits | `B, AG, MA, RA-SZZ` + 14 JIT Feats | Fan et al. (IEEE TSE 2021 — `SZZ-TSE`) | **ATUAL (Em disco)** |
| **B04** | **Apache Geronimo** | Java | 16.152 commits | `B, AG, MA, RA-SZZ` + 14 JIT Feats | Fan et al. (IEEE TSE 2021 — `SZZ-TSE`) | **ATUAL (Em disco)** |
| **B05** | **Apache Hadoop Common** | Java | 27.077 commits | `B, AG, MA, RA-SZZ` + 14 JIT Feats | Fan et al. (IEEE TSE 2021 — `SZZ-TSE`) | **ATUAL (Em disco)** |
| **B06** | **Apache HBase** | Java | 14.581 commits | `B, AG, MA, RA-SZZ` + 14 JIT Feats | Fan et al. (IEEE TSE 2021) / ApacheJIT (MSR 2022) | **ATUAL (Em disco)** |
| **B07** | **Apache Mahout** | Java | 2.762 commits | `B, AG, MA, RA-SZZ` + 14 JIT Feats | Fan et al. (IEEE TSE 2021 — `SZZ-TSE`) | **ATUAL (Em disco)** |
| **B08** | **Apache OpenJPA** | Java | 6.368 commits | `B, AG, MA, RA-SZZ` + 14 JIT Feats | Fan et al. (IEEE TSE 2021 — `SZZ-TSE`) | **ATUAL (Em disco)** |
| **B09** | **Apache Pig** | Java | 3.089 commits | `B, AG, MA, RA-SZZ` + 14 JIT Feats | Fan et al. (IEEE TSE 2021 — `SZZ-TSE`) | **ATUAL (Em disco)** |
| **B10** | **Apache Tuscany** | Java | 21.595 commits | `B, AG, MA, RA-SZZ` + 14 JIT Feats | Fan et al. (IEEE TSE 2021 — `SZZ-TSE`) | **ATUAL (Em disco)** |
| **B11** | **Apache Flink** (`00-flink`) | Java | **~38.800 commits**<br>*(1.850 fixes Java)* | **10 SZZs Pareados** + Oráculo Dev + CVEs | Clone Local Unificado + ApacheJIT (MSR 2022) | **EXECUTADO AGORA** |
| **B12** | **Jenkins Core** (+ CVE Java) | Java | 26.378 commits<br>*(+ 69 CVEs)* | JGit SZZ Unleashed + NVD Advisories | Borg et al. (ESEM 2019) / Fan et al. (FSE 2024) | **ATUAL (Em disco)** |
| **B13** | **Apache Tomcat** | Java | 10.000 commits | Dual Human Labeling ($\kappa=0.65$) | **Song et al. (ACM ESEC/FSE 2023 — `HumLa`)** | *FUTURO (Fase 2)* |
| **B14** | **Broadleaf Commerce** | Java | 10.000 commits | Dual Human Labeling ($\kappa=0.71$) | **Song et al. (ACM ESEC/FSE 2023 — `HumLa`)** | *FUTURO (Fase 2)* |
| **B15** | **Fabric8** | Java | 10.000 commits | Dual Human Labeling ($\kappa=0.64$) | **Song et al. (ACM ESEC/FSE 2023 — `HumLa`)** | *FUTURO (Fase 2)* |
| **B16** | **jGroups** | Java | 10.000 commits | Dual Human Labeling ($\kappa=0.51$) | **Song et al. (ACM ESEC/FSE 2023 — `HumLa`)** | *FUTURO (Fase 2)* |
| **B17** | **Django** | Python | 10.000 commits | Dual Human Labeling ($\kappa=0.78$) | **Song et al. (ACM ESEC/FSE 2023)** & Defectors (2023) | *FUTURO (Fase 2)* |
| **B18** | **OpenStack Nova** | Python | 10.000 commits | Dual Human Labeling ($\kappa=0.55$) | **Song et al. (ACM ESEC/FSE 2023 — `HumLa`)** | *FUTURO (Fase 2)* |
| **B19** | **TensorFlow (Python Core)** | Python / C++ | 10.000 commits | Dual Human Labeling ($\kappa=0.86$) | **Song et al. (ACM ESEC/FSE 2023 — `HumLa`)** | *FUTURO (Fase 2)* |
| **B20** | **Ansible / Airflow** | Python | ~40.000+ commits | SZZ + Git Churn + 14 JIT Feats | Mahbub et al. (`Defectors`, IEEE/ACM MSR 2023) | *FUTURO (Fase 2)* |

> [!NOTE]
> **Racional Científico da Coorte Bilingue (14 Java + 6 Python)**: Em Java, ferramentas estáticas de AST e refatoração (`srcML` e `RefactoringMiner`) são altamente eficazes. Em Python, a ausência de tais ferramentas maduras torna o SZZ tradicional vulnerável a ruído massivo em commits de refatoração e tipagem dinâmica — exatamente o cenário onde **Agentes LLM autônomos (`AgentSZZ`, `LLM4SZZ`)** oferecem a maior contribuição original.

---

## ⚡ 3. A Base de Código Unificada de Confronto: `apache/flink` e seus 8 Cenários (`E1` a `E8`)

- **Repositório Oficial Local**: `/home/artur-carvalho/mestrado/repos/00-flink/` (~38.800 commits).
- **Amostra Curada**: 1.850 bugfixes de código de produção Java (com exclusão de testes e documentação).
- **Taxonomia dos 8 Cenários de Estresse**:
  - **`E1` (Bugs Atômicos Diretos)**: 1 arquivo `.java`, $1 \le \text{LOC}_{\text{del}} \le 5$, sem ruído cosmético.
  - **`E2` (Ruído Cosmético & Metadados)**: Presença de comentários, Javadoc, indentação e anotações `@Override`/`@Nullable`.
  - **`E3` (Refatorações Estruturais Java)**: *Extract Method*, *Move Class*, renomeação de identificadores e evolução multi-salto.
  - **`E4` (Tangled & Large Patches)**: $\ge 3$ arquivos ou $> 25$ linhas deletadas misturando múltiplos propósitos.
  - **`E5` (Add-Only Fixes & Multi-Arquivo)**: $0$ linhas deletadas (inserção pura de guardas defensivas) ou causa externa.
  - **`E6` (Vulnerabilidades e Segurança / CVEs)**: Falhas de segurança, injeção, desserialização e permissões.
  - **`E7` (Concorrência e Estado Distribuído)**: *Race conditions*, *deadlocks*, `synchronized`, `CompletableFuture` e locks.
  - **`E8` (Alta Latência de Verificação — $\Delta t > 180$ dias)**: Commits com longa latência temporal entre indução e fix (Song et al., FSE 2023).
