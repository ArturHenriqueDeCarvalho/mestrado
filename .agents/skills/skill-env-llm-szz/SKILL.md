---
name: skill-env-llm-szz
description: >-
  Use this skill to configure the isolated Python environment (.venv-llm-szz),
  inspect or modify the software architecture, adapt LLM API endpoints (Gemini/OpenAI/DeepSeek),
  and execute or replicate the vulnerability-inducing commit identification tests (RQ1-RQ5)
  for Pesquisa 1 (LLM-SZZ) in /home/artur-carvalho/mestrado/repos/01-llm-szz.
---

# Skill: Arquitetura de Software e Execução Isolada do Ambiente LLM-SZZ (Pesquisa 1)

Este runbook capacita o agente (`expert-llm-szz` ou `professor-orientador`) a provisionar o ambiente virtual isolado, configurar os caminhos internos de `setting.py`, adaptar o conector `LLM` para APIs compatíveis com OpenAI (incluindo Google Gemini Pro Student Tier) e reexecutar os experimentos das RQs 1 a 5 e o avaliador `evaluate.py`.

## 1. Referência de Arquitetura Interna

Para detalhes de baixo nível sobre o grafo de chamadas de classes (`AbstractSZZ`, `LLM_SZZ`, `LLM`, `GitLog`), esquemas JSON de CVEs e adaptação de endpoints, consulte:
- [Arquitetura de Software e Diagnóstico de Ambiente](./references/architecture_and_env.md)

## 2. Provisionamento e Verificação do Ambiente Isolado

1. Execute o script automatizado de configuração e verificação de integridade do ambiente:
   [setup_and_verify.sh](./scripts/setup_and_verify.sh)
   ```bash
   bash /home/artur-carvalho/mestrado/.agents/skills/skill-env-llm-szz/scripts/setup_and_verify.sh
   ```
2. O script cria/valida o ambiente virtual isolado em `/home/artur-carvalho/mestrado/repos/01-llm-szz/.venv-llm-szz`, instala as dependências críticas (`GitPython==3.1.18`, `PyDriller==1.15.5`, `openai==1.50.0`, `Levenshtein==0.26.0`, `RapidFuzz==3.10.0`, `unidiff==0.6.0`), valida os 5 arquivos JSON de oráculo em `data/` e verifica a resolução de `WORK_DIR` em `setting.py`.

## 3. Configuração Obrigatória Antes da Execução de Testes

1. **Ajuste de `WORK_DIR` em [`setting.py`](file:///home/artur-carvalho/mestrado/repos/01-llm-szz/setting.py)**:
   - Por padrão, `setting.py` define `WORK_DIR = 'LLM_SZZ/'` (caminho relativo externo). Para execução local dentro de `/home/artur-carvalho/mestrado/repos/01-llm-szz`, certifique-se de que `WORK_DIR` aponte para `/home/artur-carvalho/mestrado/repos/01-llm-szz/` (e `PYTHONPATH` inclua `SZZ/`).
2. **Configuração da Chave e Base URL em [`SZZ/szz/core/llm.py`](file:///home/artur-carvalho/mestrado/repos/01-llm-szz/SZZ/szz/core/llm.py)**:
   - Para utilizar a cota gratuita estudantil do Gemini via interface compatível com OpenAI SDK:
     - `base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"`
     - `api_key = os.environ.get("GEMINI_API_KEY")`
     - `model = "gemini-2.5-pro"` ou `"gemini-2.5-flash"` (ou manter `gpt-3.5-turbo-0125` / `deepseek-chat` caso utilize chave OpenAI/DeepSeek).

## 4. Comandos de Replicação dos Experimentos (RQ1 a RQ5)

Com o ambiente `.venv-llm-szz` ativado e posicionado em `/home/artur-carvalho/mestrado/repos/01-llm-szz`:

```bash
source /home/artur-carvalho/mestrado/repos/01-llm-szz/.venv-llm-szz/bin/activate
export PYTHONPATH="/home/artur-carvalho/mestrado/repos/01-llm-szz:/home/artur-carvalho/mestrado/repos/01-llm-szz/SZZ"
cd /home/artur-carvalho/mestrado/repos/01-llm-szz

# 1. Pipeline Completo (CVE Description + Fixing-Commit Diff) — RQ1, RQ2, RQ4, RQ5:
python main.py --method llm --model gpt-3.5-turbo-0125 --language Java --time 01 --levenshtein_num 0.5
python main.py --method llm --model gpt-3.5-turbo-0125 --language C --time 01 --levenshtein_num 0.5

# 2. Ablação RQ3 — Apenas Descrição da CVE (sem Diff):
python main_with_des.py --method llm --model gpt-3.5-turbo-0125 --language Java --time 01 --levenshtein_num 0.5

# 3. Ablação RQ3 — Apenas Diff de Correção (sem Descrição CVE):
python main_with_diff.py --method llm --model gpt-3.5-turbo-0125 --language Java --time 01 --levenshtein_num 0.5

# 4. Execução dos Baselines Nativos (B-SZZ, AG-SZZ, MA-SZZ, V-SZZ) — RQ4:
python main.py --method b --language Java --time 01
python main.py --method ag --language Java --time 01
python main.py --method ma --language Java --time 01
python main.py --method v --language Java --time 01

# 5. Avaliação de Métricas (Recall, Precision, F1, FPR sem viés de deduplicação):
python evaluate.py --lang Java --szz_method llm --model gpt-3.5-turbo-0125 --time 01
```
