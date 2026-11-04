# Arquitetura de Software e Diagnóstico de Ambiente — LLM-SZZ (Pesquisa 1)

## 1. Diagrama de Arquitetura de Software (`repos/01-llm-szz/`)

```
+-----------------------------------------------------------------------------------+
|                        CLI Entrypoints & Orchestration                            |
|  - main.py (Full LLM-SZZ: CVE Desc + Diff)                                        |
|  - main_with_des.py (Ablation RQ3: Only CVE Desc)                                 |
|  - main_with_diff.py (Ablation RQ3: Only Diff)                                    |
|  - run.sh (Multi-model batch runner)                                              |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                      Config & Data Loading Layer                                  |
|  - setting.py: WORK_DIR, REPOS_DIR, DATA_FOLDER, SZZ_FOLDER, LOG_DIR              |
|  - data_loader.py: fixing_commit_to_CVE(), carrega data/*.json                    |
|  - cvelistV5-main/cves/: Base oficial NVD JSON v5 (1999-2024)                     |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                      Core SZZ Engine (SZZ/szz/)                                   |
|  - core/abstract_szz.py: AbstractSZZ, ImpactedFile (PyDriller + GitPython)        |
|  - core/llm.py: Classe LLM (OpenAI SDK client, system_prompt, run_model)          |
|  - llm_szz.py:                                                                    |
|      * remove_whitespace() + compute_line_ratio() -> Levenshtein.ratio >= 0.5     |
|      * add_line_numbers_to_hunk() -> Anota old_line / new_line no Unified Diff    |
|      * vote(times, model, text) -> Voting Strategy (3-5 rodadas via Counter)      |
|      * find_bic() -> Estágio 1 (Root Line) + Estágio 2 (Backtrace) + Estágio 3    |
|      * map_modified_line() -> Decisão de parada (-1) ou avanço no git blame       |
|  - Baselines: b_szz.py, ag_szz.py, ma_szz.py, v_szz.py                            |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                      Git Log & Evaluation Layer                                   |
|  - log_generation.py & git_analysis/: Extração de git numstat/namestat/logs       |
|  - evaluate.py: eval_vulnerable_version() -> Recall, Precision, F1, FPR           |
+-----------------------------------------------------------------------------------+
```

## 2. Esquema dos Dados de Entrada (`data/`)

- `verified_cve_with_versions_C.json` (100 CVEs) & `verified_cve_with_versions_Java.json` (69 CVEs):
  - Chaves por item: `cve_id`, `repo_name`, `fixing_commit`, `inducing_commits` (lista ground-truth validada por 3 especialistas), `affected_versions`.
- `c_cve_fix_detail.json` & `java_cve_fix_detail.json`:
  - Pré-mapeamento de commits fixadores e detalhes dos arquivos modificados.
- `label.json`:
  - Mapeamento consolidado de rótulos para avaliação rápida.

## 3. Pontos de Atenção no Ambiente Local

1. **`PYTHONPATH` Obrigatório**: Os arquivos dentro de `main.py` importam `from szz.llm_szz import LLM_SZZ`, enquanto `SZZ/` é um subdiretório. Portanto, `export PYTHONPATH="$PWD:$PWD/SZZ"` é mandatório.
2. **Clonagem sob Demanda vs. Pacote Local**: O script `download_repos.py` clona repositórios listados nos JSONs para `REPOS_DIR`. Para testes em amostras controladas (`DEC-001`), pode-se filtrar a lista em `verified_cve_with_versions_*.json` para rodar apenas sobre 1 ou $N$ CVEs específicas usando `--filter=blob:none`.
