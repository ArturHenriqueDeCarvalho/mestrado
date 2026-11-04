# Topologia Multi-Ambiente e Protocolo de Orquestração — Mestrado ESE/AI4SE

## 1. Isolamento de Dependências por Ambiente Virtual

Os 6 projetos possuem restrições estritas e conflitantes de versões (por exemplo, `02-pyszz-v2` exige `GitPython==3.1.7` e `PyDriller==1.15.2`, enquanto `01-llm-szz` exige `GitPython==3.1.18`, `PyDriller==1.15.5` e `pydantic>=2.9.2`). Por essa razão, a arquitetura do workspace adota **isolamento estrito por repositório**:

1. `repos/01-llm-szz/.venv-llm-szz` (Python 3 + OpenAI SDK + Levenshtein + PyDriller 1.15.5)
2. `repos/02-pyszz-v2/.venv-pyszz-v2` (Python 3 + PyDriller 1.15.2 + RefactoringMiner 2.0 + srcML)
3. `repos/03-szz-unleashed/.venv-szz-unleashed` + `szz_find_bug_introducers-0.1.jar` (Java JGit 4.10.0 + Python scikit-learn / imbalanced-learn + code-maat)
4. `repos/04-szz-tse/.venv-szz-tse` + R Statistical Engine (10 CSVs Apache = 126.526 commits + OOB Bootstrap 1.000x + Scott-Knott ESD)
5. `repos/05-cc2vec/.venv-cc2vec` (PyTorch + NLTK + 3-Level Bi-GRU HAN + Neural Tensor Network)
6. `repos/06-jit-smart/.venv-jit-smart` (PyTorch + Transformers CodeBERT + DLN BiLSTM + MultiFocalLoss + JIT-Defect4J 21 projetos Java)

## 2. Fluxo de Replicação e Auditoria Final

1. **Fase A (Execução Individual)**: Cada agente `expert-*` aciona sua `skill-env-*` para rodar seus testes de replicação e salvar os logs/CSVs de saída dentro de sua pasta `repos/0X-*/`.
2. **Fase B (Análise Comparativa Cruzada)**: O `analista-documental-comparativo` lê os artefatos gerados nas 6 pastas, verifica a consistência estatística e atualiza `docs/03-analise-comparativa/matriz-comparativa.md`.
3. **Fase C (Consolidação Científica)**: O `redator-artigo-cientifico`, supervisionado pelo `professor-orientador`, incorpora as tabelas auditadas e discussões no artigo da Banca de Dezembro em `docs/02-artigo-cientifico/`.
