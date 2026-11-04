---
name: skill-env-szz-unleashed
description: >-
  Use this skill to configure the hybrid Java/JGit and Python JIT environment (.venv-szz-unleashed),
  run the pre-built fatJar (examples/data/jars/szz_find_bug_introducers-0.1.jar) or rebuild with mavenCentral(),
  assemble the 16 JIT features (including CodeMaat coupling), and execute the Random Forest JIT evaluation
  (Stratified 10-Fold CV vs Time-Sensitive Online Change Classification) in /home/artur-carvalho/mestrado/repos/03-szz-unleashed.
---

# Skill: Arquitetura de Software e Execução Isolada do Ambiente SZZ Unleashed (Pesquisa 3)

Este runbook capacita o agente (`expert-szz-unleashed` ou `professor-orientador`) a operar a arquitetura de 4 subsistemas do SZZ Unleashed (Coletor Jira Python, Motor Core SZZ em Java/Eclipse JGit, Montador de 16 Features com `code-maat` e Classificador Random Forest JIT sensível ao tempo).

## 1. Referência de Arquitetura Interna

Para o diagrama de pacotes Java (`graph`, `parser`, `diff`, `heuristics`), detalhes da distância de Jaccard (`java-string-similarity`), correção de `jcenter()` para `mavenCentral()` no Gradle e aritmética de janelas do `Online Change Classification (OCC)`, consulte:
- [Arquitetura de Software e Diagnóstico de Ambiente](./references/architecture_and_env.md)

## 2. Provisionamento e Verificação do Ambiente Isolado

1. Execute o script de configuração e verificação:
   [setup_and_verify.sh](./scripts/setup_and_verify.sh)
   ```bash
   bash /home/artur-carvalho/mestrado/.agents/skills/skill-env-szz-unleashed/scripts/setup_and_verify.sh
   ```
2. O script cria `/home/artur-carvalho/mestrado/repos/03-szz-unleashed/.venv-szz-unleashed`, instala `scikit-learn`, `imbalanced-learn`, `pandas`, `numpy`, `scipy`, verifica o fatJar pré-compilado (`examples/data/jars/szz_find_bug_introducers-0.1.jar`) e valida os artefatos de exemplo do Jenkins (`issue_list.json`, `gitlog.json`, `fix_and_introducers_pairs.json`).

## 3. Comandos de Execução Individual e Replicação dos Testes

Com o ambiente `.venv-szz-unleashed` ativo em `/home/artur-carvalho/mestrado/repos/03-szz-unleashed`:

```bash
source /home/artur-carvalho/mestrado/repos/03-szz-unleashed/.venv-szz-unleashed/bin/activate
cd /home/artur-carvalho/mestrado/repos/03-szz-unleashed

# 1. Fase 1 — Vinculação de Issues e Commits Fixadores (BFC):
python3 fetch_jira_bugs/git_log_to_array.py --repo-path <caminho_repo_git> --from-commit <hash>
python3 fetch_jira_bugs/find_bug_fixes.py --gitlog examples/data/gitlog.json --issue-list examples/data/issues --gitlog-pattern "<pattern>"

# 2. Fase 2 — Execução do Motor Core SZZ Unleashed em Java (usando o fatJar oficial pré-compilado):
java -Xms1028m -Xmx2056m -jar examples/data/jars/szz_find_bug_introducers-0.1.jar \
  -i examples/data/issue_list.json \
  -r <caminho_repo_git> \
  -d 3

# 3. Fase 3 — Montagem das 16 Features JIT (Churn, Diffusion, History, Experience, CodeMaat Coupling):
cd data_assembler
python3 assemble_features.py <caminho_repo_git> ../examples/data/fix_and_introducers_pairs.json

# 4. Fase 4 — Execução do Experimento JIT (RQ1: Oversampling/Undersampling & RQ2: 10-Fold CV vs OCC):
cd /home/artur-carvalho/mestrado/repos/03-szz-unleashed/model
# Edite model.ini para alternar:
#   split = kfold | occ
#   sampler = None | smote | smotetomek | cluster
python3 model.py
```
