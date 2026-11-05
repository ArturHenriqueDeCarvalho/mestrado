# Diagnóstico Técnico de Execução Local: Os 10 Algoritmos SZZ e a Base Apache Flink

> [!IMPORTANT]
> **Padrão de Execução Local-First (`DEC-002`)**: Este documento consolida a arquitetura de runtime, comandos de invocação, versões de dependências e testes de sanidade para cada um dos 10 algoritmos SZZ na máquina de desenvolvimento local, apontados para a base de código unificada **Apache Flink** (`repos/00-flink/`).

---

## 🏛️ 1. Mapeamento das 10 Instâncias Isoladas de Algoritmo

```text
mestrado/repos/
├── 00-flink/             # Base Unificada: apache/flink (~35k commits)
├── 01-bszz/              # Algoritmo 01: B-SZZ (Śliwerski et al., FSE 2005)
├── 02-agszz/             # Algoritmo 02: AG-SZZ (Kim et al., ASE 2006)
├── 03-maszz/             # Algoritmo 03: MA-SZZ (da Costa et al., EMSE 2017)
├── 04-lszz/              # Algoritmo 04: L-SZZ (Rosa et al., ICSE 2021)
├── 05-raszz/             # Algoritmo 05: RA-SZZ (Neto/Fan et al., TSE 2021)
├── 06-szz-unleashed/     # Algoritmo 06: SZZ Unleashed (Borg et al., ESEM 2019)
├── 07-llm-szz/           # Algoritmo 07: LLM-SZZ (Fan et al., FSE 2024)
├── 08-llm4szz/           # Algoritmo 08: LLM4SZZ (Tang et al., 2025)
├── 09-agentszz/          # Algoritmo 09: AgentSZZ (Risse & Böhme, ASE 2026)
└── 10-promptszz/         # Algoritmo 10: Prompt-SZZ (Zero-Shot CoT Baseline)
```

---

## 🛠️ 2. Diagnóstico Técnico por Algoritmo

### 01. B-SZZ (`repos/01-bszz/`)
- **Runtime**: Python 3.10 isolado em `.venv-bszz/`.
- **Dependências**: `GitPython==3.1.7`, `PyDriller==1.15.2`, `PyYAML==5.3.1`.
- **Execução**:
  ```bash
  python main.py <bugfix_commits.json> conf/bszz.yml /path/to/flink
  ```
- **Saída**: `out/bic_bszz_<timestamp>.json` com pares `(fix_commit, inducing_commits)`.

### 02. AG-SZZ (`repos/02-agszz/`)
- **Runtime**: Python 3.10 isolado em `.venv-agszz/`.
- **Dependências**: `GitPython==3.1.7`, `PyDriller==1.15.2`, parser de anotações.
- **Execução**:
  ```bash
  python main.py <bugfix_commits.json> conf/agszz.yml /path/to/flink
  ```
- **Saída**: `out/bic_agszz_<timestamp>.json`.

### 03. MA-SZZ (`repos/03-maszz/`)
- **Runtime**: Python 3.10 isolado em `.venv-maszz/`.
- **Dependências**: `GitPython==3.1.7`, `PyDriller==1.15.2`, filtros regex para comentários e linhas em branco.
- **Execução**:
  ```bash
  python main.py <bugfix_commits.json> conf/maszz.yml /path/to/flink
  ```
- **Saída**: `out/bic_maszz_<timestamp>.json`.

### 04. L-SZZ (`repos/04-lszz/`)
- **Runtime**: Python 3.10 isolado em `.venv-lszz/` + Binário Nativo **`srcML 1.2.0`** (`~/.local/bin/srcml` com `libsrcml.so.1`).
- **Dependências**: `GitPython==3.1.7`, `PyDriller==1.15.2`, `beautifulsoup4`, `lxml`.
- **Execução**:
  ```bash
  python main.py <bugfix_commits.json> conf/lszz.yml /path/to/flink
  ```
- **Saída**: `out/bic_lszz_<timestamp>.json` (AST diffs semânticos).

### 05. RA-SZZ (`repos/05-raszz/`)
- **Runtime**: Java OpenJDK 11/17 + Python 3.10 isolado em `.venv-raszz/`.
- **Dependências**: `RefactoringMiner-2.0` (`tools/RefactoringMiner-2.0/bin/RefactoringMiner`), `DiffJ`.
- **Execução**:
  ```bash
  python main.py <bugfix_commits.json> conf/raszz.yml /path/to/flink
  ```
- **Saída**: Rastreamento com descarte de 15 operações de refatoração estrutural.

### 06. SZZ Unleashed (`repos/06-szz-unleashed/`)
- **Runtime**: Java OpenJDK 11/17 + fatJar compilado `szz_find_bug_introducers-0.1.jar`.
- **Execução**:
  ```bash
  java -jar examples/data/jars/szz_find_bug_introducers-0.1.jar \
    -i issue_list.json -r /path/to/flink -d 3
  ```
- **Saída**: `build/reports/szz/fix_and_introducers_pairs.json`.

### 07. LLM-SZZ (`repos/07-llm-szz/`)
- **Runtime**: Python 3.10 isolado em `.venv-llm-szz/`.
- **Dependências**: `requests`, `google-genai` / `openai`, `GitPython`, `Levenshtein`.
- **Execução**:
  ```bash
  python main.py --repo /path/to/flink --cve-file flink_cve_commits.json --threshold 0.5
  ```
- **Saída**: Classificação reflexiva com prompt chaining e desambiguação de tangled commits.

### 08. LLM4SZZ (`repos/08-llm4szz/`)
- **Runtime**: Python 3.10 isolado em `.venv-llm4szz/`.
- **Dependências**: `pandas`, `scikit-learn`, `requests`, API LLM.
- **Execução**: Pipeline em 2 estágios: (1) Rank-based suspicious lines, (2) Context-enhanced candidate assessment.
- **Saída**: `out/llm4szz_flink_results.json`.

### 09. AgentSZZ (`repos/09-agentszz/`)
- **Runtime**: Python 3.10 isolado em `.venv-agentszz/`.
- **Dependências**: `GitPython`, framework ReAct, `google-genai` / `openai`.
- **Execução**:
  ```bash
  python -m agents_for_szz.main --repo /path/to/flink --fix-commit <hash>
  ```
- **Saída**: Trilha de investigação forense com árvores de evidências de `git log` / `git diff`.

### 10. Prompt-SZZ (`repos/10-promptszz/`)
- **Runtime**: Python 3.10 isolado em `.venv-promptszz/`.
- **Dependências**: `google-genai` / `openai`, `pydantic`.
- **Execução**: Inferência Zero-Shot e Chain-of-Thought direta sobre os diffs unificados.
- **Saída**: `out/promptszz_flink_results.json`.

---

## ⚡ 3. A Base Unificada: Apache Flink (`repos/00-flink/`)

- Clone otimizado via `--filter=blob:none` para assegurar integridade completa do histórico de commits e árvores sem estourar armazenamento.
- Extração de pares de teste através do script [`skill-env-flink-benchmark/scripts/setup_flink_repo.sh`](file:///home/artur-carvalho/mestrado/.agents/skills/skill-env-flink-benchmark/scripts/setup_flink_repo.sh).
