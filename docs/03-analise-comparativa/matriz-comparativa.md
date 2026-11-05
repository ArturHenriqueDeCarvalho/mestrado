# Matriz Comparativa: 10 Algoritmos SZZ x 10 Bases Empíricas e Benchmark Unificado Apache Flink

> [!IMPORTANT]
> **Governança Metodológica (`DEC-008`, `DEC-009`, `DEC-010`)**: Esta matriz consolida os **10 Algoritmos SZZ** (incluindo as 4 abordagens de LLMs), as **10 Bases Empíricas com oráculos científicos** e o repositório unificado de confronto **Apache Flink** (`apache/flink`).

---

## 🏛️ 1. Mapeamento dos 10 Algoritmos SZZ e seus Artigos de Origem

| ID | Algoritmo SZZ | Família Técnica | Artigo Científico Publicado | Veículo / Ano / DOI | Ponto Exato de Superioridade (Tese do Paper) |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **A01** | **B-SZZ** | Heurística Clássica | Śliwerski et al.: *"When Do Changes Induce Fixes?"* | ACM SIGSOFT FSE (2005)<br>`10.1145/1083142.1083147` | Alta revocação (*recall*) e simplicidade operacional em bugs mono-linha diretos. |
| **A02** | **AG-SZZ** | Heurística Anotação | Kim et al.: *"Automatic Identification of Bug-Introducing Changes"* | IEEE/ACM ASE (2006)<br>`10.1109/ASE.2006.23` | Imunidade a ruídos em anotações de código (`@Override`, cabeçalhos de licença). |
| **A03** | **MA-SZZ** | Heurística Metadados | da Costa et al.: *"Evaluating the Impact of Min. Age, Comments and Blank Lines"* | Empirical Software Engineering (EMSE 2017)<br>`10.1007/s10664-016-9466-9` | Eliminação de falsos positivos decorrentes de comentários, Javadoc e linhas em branco. |
| **A04** | **L-SZZ** | Sintático AST | Rosa et al.: *"A Comprehensive Evaluation of SZZ Variants through a Developer-Informed Oracle"* | IEEE/ACM ICSE (2021) / JSS (2023)<br>`10.1016/j.jss.2023.111729` | Imunidade a alterações cosméticas que preservam a AST compilada (`srcML 1.2.0`). |
| **A05** | **RA-SZZ** | Sintático Refatoração | Neto et al. (2018) & Fan et al.: *"The Impact of Changes Mislabeled by SZZ"* | IEEE Transactions on Software Engineering (TSE 2021)<br>`10.1109/TSE.2019.2929761` | Padrão-ouro na detecção e filtragem de métodos extraídos e classes renomeadas (`RefactoringMiner`). |
| **A06** | **SZZ Unleashed** | Sintático JGit | Borg et al.: *"SZZ Unleashed: An Open Implementation of the SZZ Algorithm"* | ACM/IEEE ESEM / arXiv (2019)<br>`arXiv:1903.01742` | Rastreamento em profundidade através de grafos de anotação de arquivo (Jaccard depth $\ge 3$). |
| **A07** | **LLM-SZZ** *(LLM 1)* | LLM Prompt Chaining | Fan et al.: *"Vulnerability-Inducing Commit Identification Driven by LLMs & CVE"* | ACM PACMSE / FSE (2024)<br>`songli.io/papers/LLM-SZZ.pdf` | Desambiguação de commits emaranhados (*tangled*) e patches onde o fix apenas adiciona checagens sem deletar linhas. |
| **A08** | **LLM4SZZ** *(LLM 2)* | LLM Rank-based | Tang et al.: *"LLM4SZZ: Enhancing SZZ Algorithm with Context-Enhanced Assessment on LLMs"* | arXiv (2025 / Figshare 27418236)<br>`arXiv:2504.01404` | Ranqueamento semântico de causalidade das linhas deletadas no patch de correção. |
| **A09** | **AgentSZZ** *(LLM 3)* | LLM ReAct Agent | Risse & Böhme: *"AgentSZZ: Teaching the LLM Agent to Play Detective with Bug-Inducing Commits"* | IEEE/ACM ASE (2026)<br>`niklasrisse/agents-for-szz` | Auditoria investigativa multi-turn atuando como um detetive autônomo com comandos Git. |
| **A10** | **Prompt-SZZ** *(LLM 4)* | LLM Zero-Shot CoT | Baseline Canônico de LLM (Tang et al., 2025; Fan et al., 2024) | Baseline padronizado em LLM4SZZ e LLM-SZZ | Raciocínio rápido passo a passo (*Chain-of-Thought*) para medição de custo-benefício. |

---

## 📦 2. As 10 Bases de Dados Empíricas com Oráculos Conhecidos

| ID | Base de Dados / Benchmark | Linguagem & Domínio | Volume de Commits | Tipo de Oráculo de Validação | Artigo Científico de Origem |
| :-: | :--- | :---: | :---: | :--- | :--- |
| **D01** | **Apache ActiveMQ** | Java / Mensageria | 7.753 commits | Oráculo Limpo RA-SZZ (`RefactoringMiner`) | Fan et al. (IEEE TSE 2021) |
| **D02** | **Apache Camel** | Java / Integração EIP | 17.374 commits | Oráculo Limpo RA-SZZ (`RefactoringMiner`) | Fan et al. (IEEE TSE 2021) |
| **D03** | **Apache Derby** | Java / Banco de Dados | 9.775 commits | Oráculo Limpo RA-SZZ (`RefactoringMiner`) | Fan et al. (IEEE TSE 2021) |
| **D04** | **Apache HBase** | Java / NoSQL Distribuído | 14.581 commits | Oráculo Limpo RA-SZZ (`RefactoringMiner`) | Fan et al. (IEEE TSE 2021) |
| **D05** | **Apache Hadoop Common** | Java / Infraestrutura | 27.077 commits | Oráculo Limpo RA-SZZ (`RefactoringMiner`) | Fan et al. (IEEE TSE 2021) |
| **D06** | **Jenkins Core** | Java / Servidor CI/CD | 26.378 commits | Oráculo Pareado JGit / CodeMaat | Borg et al. (SZZ Unleashed 2019) |
| **D07** | **Developer-Informed Oracle (DIO)** | Multi-lang (Java/Python/C++) | **1.930 commits** | **Ground Truth de Desenvolvedores + 4 Humanos** (19,6M GH Archive) | Rosa et al. (ICSE 2021 / JSS 2023) |
| **D08** | **CVE Benchmark C/C++** | C / C++ Segurança | 100 CVEs verificados | **Ground Truth de Segurança (NVD / Advisories)** | Fan et al. (LLM-SZZ 2024) |
| **D09** | **CVE Benchmark Java** | Java Segurança | 69 CVEs verificados | **Ground Truth de Segurança (NVD / Advisories)** | Fan et al. (LLM-SZZ 2024) |
| **D10** | **VICBench / VulnCommit** | Multi-lang (Java, C++, Python) | 100 CVEs (88 projetos) | **Dual-Annotation (Especialistas Humanos + Workflows)** | Tang et al. (2025) / VICBench (2024) |

---

## ⚡ 3. A Base de Código Unificada de Confronto: `apache/flink`

- **Repositório Oficial**: `https://github.com/apache/flink`
- **Volume Total**: **~35.000+ commits**
- **Protocolo Experimental**:
  1. Extração dos commits de bug-fixing vinculados a issues Jira (`FLINK-[0-9]+`);
  2. Extração dos commits de segurança vinculados a CVEs reportadas no Apache Security Advisory;
  3. Execução pareada dos **10 algoritmos SZZ sobre os mesmos commits de correção**;
  4. Extração da matriz de sobreposição pareada (Jaccard, Szymkiewicz-Simpson, Kappa de Cohen e UTP);
  5. Quantificação de **Wasted Effort LOC** gerado por ruídos de rotulagem.
