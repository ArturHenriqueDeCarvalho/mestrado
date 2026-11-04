---
name: skill-env-pyszz-v2
description: >-
  Use this skill to configure the isolated Python environment (.venv-pyszz-v2),
  verify external binaries (srcML, RefactoringMiner-2.0, git), inspect the object-oriented
  AbstractSZZ architecture, and execute or replicate any of the SZZ variants (B, AG, MA, L, R, RA, PD, A, DF)
  and automated test suites in /home/artur-carvalho/mestrado/repos/02-pyszz-v2.
---

# Skill: Arquitetura de Software e Execução Isolada do Ambiente PySZZ v2 (Pesquisa 2)

Este runbook instrui o agente (`expert-pyszz-v2` ou `professor-orientador`) a inicializar o ambiente virtual isolado `.venv-pyszz-v2`, validar o binário embutido `tools/RefactoringMiner-2.0` e o parser `srcML`, e executar as variantes do PySZZ v2 tanto nas suítes de regressão locais (`test/repos_test*.zip`) quanto nos subconjuntos do oráculo informado por desenvolvedores.

## 1. Referência de Arquitetura Interna

Para o diagrama completo da hierarquia de classes (`AbstractSZZ` e suas 9 subclasses), parâmetros declarativos dos 32 arquivos YAML em `conf/` e integração com `srcML` e `RefactoringMiner 2.0`, consulte:
- [Arquitetura de Software e Diagnóstico de Ambiente](./references/architecture_and_env.md)

## 2. Provisionamento e Verificação do Ambiente Isolado

1. Execute o script de provisionamento e smoke test:
   [setup_and_verify.sh](./scripts/setup_and_verify.sh)
   ```bash
   bash /home/artur-carvalho/mestrado/.agents/skills/skill-env-pyszz-v2/scripts/setup_and_verify.sh
   ```
2. O script cria `/home/artur-carvalho/mestrado/repos/02-pyszz-v2/.venv-pyszz-v2`, instala `GitPython==3.1.7`, `PyDriller==1.15.2`, `PyYAML`, `dateparser`, `networkx`, `beautifulsoup4`, `lxml`, `options`, `testresources`, verifica `tools/RefactoringMiner-2.0` e executa a validação de dependências de `szz/util/check_requirements.py`.

## 3. Comandos de Execução Individual e Replicação das Variantes

Com o ambiente `.venv-pyszz-v2` ativo em `/home/artur-carvalho/mestrado/repos/02-pyszz-v2`:

```bash
source /home/artur-carvalho/mestrado/repos/02-pyszz-v2/.venv-pyszz-v2/bin/activate
cd /home/artur-carvalho/mestrado/repos/02-pyszz-v2

# 1. Execução dos Exemplos Empacotados (Smoke Tests de Ponta a Ponta):
bash start_example1.sh   # MA-SZZ sem filtro de data de issue sobre test/repos_test.zip
bash start_example2.sh   # Variantes com filtro de data de issue sobre test/repos_test_with_issues.zip
bash start_example3.sh   # Pós-filtragem R-SZZ / L-SZZ

# 2. Execução Individual de Qualquer Variante via CLI:
# Sintaxe: python3 main.py <input_bugfix.json> conf/<variante>.yml <pasta_repos_git>
unzip -q -o test/repos_test.zip -d test/
python3 main.py test/bugfix_commits_test.json conf/bszz.yml test/repos_test/
python3 main.py test/bugfix_commits_test.json conf/agszz.yml test/repos_test/
python3 main.py test/bugfix_commits_test.json conf/maszz.yml test/repos_test/
python3 main.py test/bugfix_commits_test.json conf/rszz.yml test/repos_test/
python3 main.py test/bugfix_commits_test.json conf/lszz.yml test/repos_test/
python3 main.py test/bugfix_commits_test.json conf/pdszz.yml test/repos_test/

# 3. Execução da Variante Consciente de Refatoração (RA-SZZ com RefactoringMiner 2.0):
bash test/start_test_raszz.sh

# 4. Execução das Suítes Automatizadas de Regressão (L-SZZ, R-SZZ, A-SZZ, DF-SZZ, Reverts):
bash test/start_test_rszz.sh
bash test/start_test_lszz.sh
bash test/start_test_rszz_revert.sh
bash test/start_test_aszz.sh
bash test/start_test_dfszz.sh
```
