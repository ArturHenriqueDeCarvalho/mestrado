# Diagnóstico Técnico de Execução Local: As 6 Pesquisas Base

Este documento apresenta o levantamento técnico detalhado da estrutura, linguagens, dependências e procedimentos de execução local para cada um dos 6 projetos clonados no diretório `mestrado/repos/`.

---

## 📊 Resumo Executivo das Pilhas Tecnológicas

| ID | Pesquisa | Linguagem / Stack | Gerenciador de Dependências | Requisito Computacional | Forma de Execução Local |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **01** | **LLM-SZZ** | Python 3.8+ (PyDriller, OpenAI Client) | `pip` (`requirements.txt`) | CPU + Chamadas de API (Gemini Studio) | Script Python local (`main.py` / `evaluate.py`) |
| **02** | **PySZZ v2** | Python 3.8+ (GitPython, PyDriller, PyYAML) | `pip` (`requirements.txt`) | CPU (Leve/Rápido) | `python3 main.py <bugfix.json> <conf.yml> <repo>` |
| **03** | **SZZ Unleashed** | Java 8 (OpenJDK 8) + Gradle 4.10.3 | Gradle (`build.gradle` / fatJar) | CPU (Compilação Java) | `gradle build && gradle fatJar` -> Execução JAR |
| **04** | **SZZ-TSE** | R 3.6+ / 4.x + Java / Python | Pacotes R (`data.table`, `ScottKnottESD`, etc.) | CPU (Processamento estatístico) | `Rscript code/calculation/classification_importance.R` |
| **05** | **CC2Vec** | Python 3.6/3.8 + PyTorch 1.2+ + scikit-learn | `pip` (`requirements.txt`) | CPU local (Modo inferência) | `python jit_DExtended.py -predict ...` |
| **06** | **JIT-Smart** | Python 3.8+ + PyTorch + Transformers (CodeBERT) | `pip` / `conda` (`requirements.txt`) | CPU local para inferência / avaliação | `sh train_jitsmart.sh` ou notebooks Jupyter |

---

## 🔍 Detalhamento Técnico Projeto a Projeto

### 1. LLM-SZZ (`repos/01-llm-szz/`)
- **Arquivos-chave**:
  - `requirements.txt`: bibliotecas `PyDriller==1.15.5`, `openai==1.50.0`, `tiktoken`, `GitPython`, `unidiff`, `Levenshtein`.
  - `setting.py`: Configuração dos diretórios de trabalho (`WORK_DIR`) e chaves de API.
  - `data/`: Contém os benchmarks rotulados (`c_cve_fix_detail.json`, `java_cve_fix_detail.json`, `label.json`).
- **Como executar localmente**:
  1. Criar ambiente virtual: `python3 -m venv venv && source venv/bin/activate`
  2. Instalar dependências: `pip install -r requirements.txt`
  3. Configurar endpoint OpenAI-compatível apontando para a API do Google Gemini com a chave de estudante.
  4. Executar: `python evaluate.py` ou `python main_with_diff.py` sobre os dados em `data/`.

---

### 2. PySZZ v2 (`repos/02-pyszz-v2/`)
- **Arquivos-chave**:
  - `requirements.txt`: 11 dependências (`PyDriller`, `GitPython`, `dateparser`, `networkx`, `beautifulsoup4`).
  - `test/repos_test.zip`: Repositórios git compactados de teste prontos para uso.
  - `conf/`: Configurações YAML para todas as variantes do SZZ (`bszz.yml`, `agszz.yml`, `maszz.yml`, `raszz.yml`, `lszz.yml`).
  - `start_example1.sh`: Script funcional pronto para execução demonstrativa.
- **Como executar localmente**:
  1. Criar venv: `python3 -m venv venv && source venv/bin/activate`
  2. `pip install -r requirements.txt`
  3. Descompactar o teste: `unzip test/repos_test.zip -d test/`
  4. Executar: `python3 main.py test/bugfix_commits_test.json conf/maszz.yml test/repos_test/`

---

### 3. SZZ Unleashed (`repos/03-szz-unleashed/`)
- **Arquivos-chave**:
  - `szz/build.gradle` e `szz/settings.gradle`: Configuração de build.
  - `Dockerfile`: Documenta os pré-requisitos exatos (OpenJDK 8 e Gradle 4.10.3).
  - `examples/`: Exemplos de issue trackers (Jira) e mapeamento de bugs.
- **Como executar localmente**:
  1. Instalar OpenJDK 8 (`sudo apt install openjdk-8-jdk` se necessário, ou via SDKMAN/container local).
  2. Executar o wrapper do Gradle ou build: `cd szz && gradle fatJar`
  3. O binário executável gerado é `szz_find_bug_introducers-0.1.jar`.
  4. Executar via comando Java passando o repositório git e o JSON de issues.

---

### 4. SZZ-TSE (`repos/04-szz-tse/szz-tse/`)
- **Arquivos-chave**:
  - `labeled-data.zip` (16 MB): Dataset consolidado de todos os projetos Apache rotulados com B-SZZ, AG-SZZ, MA-SZZ e RA-SZZ.
  - `code/calculation/classification_importance.R`: Script principal de cálculo de métricas de classificação JIT e importância de features.
  - Subprojetos auxiliares clonados: `ma-szz/` e `raszzprime/`.
- **Como executar localmente**:
  1. Descompactar `labeled-data.zip`.
  2. Configurar a variável `DIR_PATH` dentro de `code/calculation/classification_importance.R`.
  3. Criar os diretórios de saída em `data_results/`: `importance`, `oneway`, `results_imbalance`, `results_balance`.
  4. Executar via R local (`Rscript code/calculation/classification_importance.R`).

---

### 5. CC2Vec (`repos/05-cc2vec/`)
- **Arquivos-chave**:
  - `README.md`: Documenta os parâmetros de treino e inferência (`embedding_dim`, `filter_sizes`, `batch_size`).
  - `jit_DExtended.py`, `jit_DExtended_eval.py`: Pipeline para predição de defeitos Just-In-Time.
  - `bfp_PNExtended.py`: Identificação de patches de correção de bugs.
- **Como executar localmente**:
  1. Criar venv com Python e PyTorch: `pip install torch torchvision numpy scikit-learn nltk tqdm`
  2. Baixar os checkpoints pré-treinados do Zenodo (`https://zenodo.org/record/3965149`) para a pasta de modelos.
  3. Executar o script de predição/avaliação em CPU local passando o modelo salvo e o dataset:
     `python jit_DExtended.py -predict -pred_data <path_data> -pred_data_cc2ftr <path_ftr> -dictionary_data <path_dict> -load_model <path_model>`

---

### 6. JIT-Smart & JIT-Fine (`repos/06-jit-smart/`)
- **Arquivos-chave**:
  - `jit-smart/README.md`: Protocolo passo a passo de replicação em 2 etapas (extração de linhas e treino/avaliação).
  - `jit-fine/data.zip` (75 MB): Dataset completo de 21 projetos Java com rótulos a nível de commit e linha de código.
  - Scripts `train_jitsmart.sh` e `train_jitfine.sh`.
- **Como executar localmente**:
  1. Descompactar `jit-fine/data.zip`.
  2. Instalar dependências em Python (`transformers`, `torch`, `scikit-learn`).
  3. Executar o script de avaliação/teste local dos checkpoints pré-treinados para reproduzir as tabelas de AUC e F1.
