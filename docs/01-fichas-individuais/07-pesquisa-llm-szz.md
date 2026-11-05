# Ficha Estruturada de Pesquisa Científica — PESQUISA 1: LLM-SZZ

---

## 1. Identificação

* **Título**: LLM-SZZ: Novel Vulnerability-Inducing Commit Identification Driven by Large Language Model and CVE Description
* **Autores**: Siqi Fan, Xin Liu, Yingli Zhang, Yuan Tan, Luxing Yin, Zhaorun Chen, Song Li, Lei Qiao, Rui Zhou
* **Afiliações**: School of Information Science and Engineering, Lanzhou University; The State Key Laboratory of Blockchain and Data Security, Zhejiang University; Department of Computer Science, University of Chicago
* **Ano**: 2024
* **Venue**: Preprint oficial / Submissão (Apoiado pelo National Key R&D Program of China No. 2024YFE0203800 e Open Research Fund of Zhejiang University)
* **DOI**: Informação não identificada nas fontes disponíveis (preprint disponibilizado pelo autor Song Li).
* **URL**: https://songli.io/papers/LLM-SZZ.pdf
* **Repositório Oficial**: https://github.com/juzizi44/LLM_SZZ
* **Identificação Interna**: **PESQUISA 1**

---

## 2. Problema

* **Problema Científico**: 
  A baixa precisão e o alto índice de falsos positivos dos métodos tradicionais de SZZ (e suas variantes estáticas ou baseadas em aprendizado superficial) na identificação de commits indutores de vulnerabilidades (Vulnerability-Inducing Commits - VIC).
* **Causas Raízes Identificadas pelos Autores** [Seção I, Linhas 16-27]:
  1. *Ruído em Métodos Estáticos*: Variantes estáticas analisam muitos arquivos e linhas irrelevantes dentro de um commit fixador de vulnerabilidade. Abordagens que tentam filtrar arquivos usando discussões de bugs (ex.: FI-SZZ) falham na prática porque a maioria das CVEs não possui discussões públicas detalhadas de bugs.
  2. *Capacidade Semântica Insuficiente em Modelos de Aprendizado*: Métodos baseados em grafos/redes neurais (como NEURAL-SZZ via Heterogeneous Graph Attention Network - HAN) focam exclusivamente no código e possuem representação semântica limitada, reduzindo falsos positivos à custa de derrubar drasticamente a identificação de commits indutores reais.
  3. *Incapacidade de Rastreamento em Profundidade*: A dependência de algoritmos simples de mapeamento de linhas (line mapping) falha em vulnerabilidades complexas ou antigas ("deep vulnerabilities"), onde o commit indutor está obscurecido em versões muito anteriores do software. Métodos como V-SZZ tentam múltiplos rastreamentos para trás, mas geram explosão de falsos positivos por rastrearem todas as linhas deletadas sem discriminação semântica.

---

## 3. Perguntas de Pesquisa (Research Questions)

As cinco RQs apresentadas literalmente pelos autores [Seção IV, Linhas 399-407]:

* **RQ1**: Which LLM is the best for LLM-SZZ?
* **RQ2**: How does the Levenshtein distance affect the experimental results?
* **RQ3**: How do the CVE description and the fixing-commit diff affect the experimental results?
* **RQ4**: How does LLM-SZZ perform in comparison to previous SZZ methods?
* **RQ5**: What is the performance of LLM-SZZ on deep vulnerabilities?

---

## 4. Hipóteses

* **Hipótese 1 [FATO DOCUMENTADO - Seção I & III]**: A integração de informações em linguagem natural provenientes das descrições oficiais de CVEs com as alterações sintáticas do diff de correção (`fixing-commit diff`) permite que Modelos de Linguagem de Grande Porte (LLMs) compreendam a real natureza da vulnerabilidade e identifiquem com maior precisão a linha deletada causadora da falha (root cause line).
* **Hipótese 2 [FATO DOCUMENTADO - Seção III-B]**: Combinar o cálculo de distância de edição (Levenshtein) com o julgamento semântico do LLM (concedendo ao modelo a autoridade de interromper o rastreamento autônomo) reduz o ruído em múltiplos saltos históricos, superando as limitações do mapeamento estático de linhas em vulnerabilidades profundas.

---

## 5. Objetivos

* **Objetivo Geral**:
  Desenvolver, implementar e avaliar o framework **LLM-SZZ**, um método híbrido orientado por LLMs e descrições textuais de CVEs capaz de identificar commits indutores de vulnerabilidades com alta precisão e baixo índice de falsos positivos.
* **Objetivos Específicos**:
  1. Construir uma cadeia de prompts estruturada (*prompt chaining*) para guiar o LLM na seleção da linha raiz deletada em cada arquivo modificado.
  2. Implementar um mecanismo iterativo de decisão de retrocesso (*Vulnerability Backtrace Decision*) com filtro de distância de Levenshtein (limiar calibrado empiricamente) e parada autônoma por LLM.
  3. Desenvolver uma etapa de seleção ótima de candidatos (*Optimal Candidate Selection*) para resolver o problema de commits emaranhados (*tangled commits*).
  4. Comparar empiricamente o LLM-SZZ contra 5 baselines de referência (B-SZZ, AG-SZZ, MA-SZZ, V-SZZ e NEURAL-SZZ) sobre um benchmark verificado de projetos em C/C++ e Java.

---

## 6. Contexto

* **Contexto Tecnológico e de Segurança**:
  Segurança da cadeia de suprimentos de software (Software Supply Chain Security) e conformidade de bancos de vulnerabilidades (NVD / CVE). Estudos anteriores demonstraram que até 57.5% das faixas de versões afetadas registradas no NVD estão incorretas ou incompletas, gerando alocação indevida de recursos de segurança e janelas de exposição a ataques cibernéticos.

---

## 7. Dados

* **Origem do Dataset**:
  Base de 172 vulnerabilidades reais manualmente verificadas originalmente compiladas por Bao et al. (ICSE 2022 - V-SZZ) [Seção IV-A].
* **Revisão e Correção do Dataset pelos Autores**:
  Os autores realizaram um processo de verificação manual independente conduzido por 3 revisores com resolução de discrepâncias por consenso.
  - O projeto Java `blynk-server` foi removido por indisponibilidade pública no GitHub.
  - Duas vulnerabilidades foram excluídas por ausência de commits indutores válidos verificáveis.
* **Tamanho Final do Dataset**:
  - **Dataset C/C++**: 100 vulnerabilidades | 60 superficiais (*shallow*) | 40 profundas (*deep*) | 100 commits fixadores (*vulnerability-fixing commits*).
  - **Dataset Java**: 69 vulnerabilidades | 25 superficiais (*shallow*) | 44 profundas (*deep*) | 82 commits fixadores (uma vulnerabilidade em Java frequentemente possui múltiplos commits fixadores).
  - **Total de Vulnerabilidades**: 169 (100 C/C++ e 69 Java).
  - **Total de Commits Fixadores**: 182 (100 C/C++ e 82 Java).
* **Período Analisado**:
  Informação não explicitada diretamente em datas-limite no texto do paper; os dados herdam o período temporal das CVEs do benchmark de Bao et al. (exemplos no artigo cobrem CVEs de 2009 a 2021).
* **Critérios de Inclusão e Exclusão**:
  - *Inclusão*: CVEs que possuem commits fixadores mapeados em repositórios Git públicos com histórico acessível e descrição oficial no NVD/CVE.
  - *Exclusão*: Projetos deletados do GitHub e vulnerabilidades sem commits indutores localizáveis.

---

## 8. Metodologia

O procedimento experimental e a arquitetura do método seguem a sequência estrita:

```
[DADOS] ──> CVE Description (NVD) + Fixing Commits (Git)
   │
[PRÉ-PROCESSAMENTO] ──> Extração de linhas deletadas + isolamento de hunks relevantes por arquivo
   │
[MÉTODO: ETAPA 1] ──> LLM Root Cause Line Identification (Prompt Chain por arquivo)
   │
[MÉTODO: ETAPA 2] ──> Vulnerability Backtrace Decision:
                       ├── Git Blame -> commit anterior
                       ├── Filtro Levenshtein Distance (limiar = 0.5)
                       └── LLM Backtrace Decision (autoridade de continuar ou parar)
   │
[MÉTODO: ETAPA 3] ──> Optimal Candidate Selection (LLM avalia candidatos para desatar tangled commits)
   │
[MÉTRICAS] ──> Recall, Precision, F1-Score, False Positive Rate, Estabilidade (Voting Strategy)
   │
[RESULTADOS] ──> Avaliação das RQs (RQ1 a RQ5)
```

### Detalhamento dos Três Passos do Algoritmo [Seção III]:
1. **Passo 1 — Identificação da Linha Deletada Raiz (Root Cause Deleted Line)**:
   - Analisa cada arquivo separadamente para evitar sobrecarregar o contexto do LLM.
   - Entradas para o LLM: (a) Descrição da CVE do NVD; (b) Números das linhas deletadas candidatas; (c) Informações do diff (hunk contendo o contexto das linhas deletadas).
   - Utiliza *Prompt Chaining* dividindo a tarefa em subtarefas reflexivas.
2. **Passo 2 — Decisão de Retrocesso da Vulnerabilidade (Vulnerability Backtrace Decision)**:
   - Executa `git blame` na linha raiz identificada.
   - Se o commit anterior contiver linhas deletadas, calcula a Distância de Levenshtein normalizada entre as linhas. Linhas com distância $< 0.5$ são filtradas como dissimilares.
   - As linhas restantes são submetidas ao LLM com diffs e contexto.
   - O LLM possui autoridade para **interromper o retrocesso** se concluir que as linhas não possuem mais relação com a vulnerabilidade, ou escolher a linha raiz anterior.
   - O processo itera até a parada, identificando o commit mais antigo como candidato indutor daquele arquivo.
3. **Passo 3 — Seleção Ótima de Candidatos (Optimal Candidate Selection)**:
   - Para resolver *tangled commits* (commits que modificam múltiplos arquivos não relacionados), o LLM analisa a lista final de commits candidatos de todos os arquivos junto com o diff e a descrição da CVE, selecionando o commit indutor mais provável.
4. **Estratégia de Votação (Voting Strategy)**:
   - Para mitigar a aleatoriedade e não-determinismo do LLM, cada requisição é submetida a até 5 execuções, adotando a resposta da maioria.

---

## 9. Ferramentas

| Ferramenta | Versão Documentada | Finalidade | Configuração / Parâmetros |
| :--- | :--- | :--- | :--- |
| **Git / GitPython** | GitPython 3.1.18 | Mineração de histórico de repositórios | Execução de `git blame`, diffs e inspeção de árvores de commits |
| **PyDriller** | 1.15.5 | Extração automatizada de commits, diffs e modificações | Configuração padrão em Python |
| **OpenAI Python SDK** | 1.50.0 | Comunicação com modelos de linguagem via API | Conexão aos modelos OpenAI e DeepSeek |
| **Levenshtein / RapidFuzz** | 0.26.0 / 3.10.0 | Cálculo da distância de edição de strings | Limiar de corte $D \ge 0.5$ |
| **unidiff** | 0.6.0 | Parsing estruturado de patches unificados | Separação de hunks e números de linhas |

---

## 10. Algoritmos e Classificadores

* **Modelos de Linguagem Avaliados (RQ1)**:
  - `GPT-3.5-Turbo-0125` (Closed-source OpenAI) — *Modelo principal selecionado*
  - `GPT-4o` (Closed-source OpenAI)
  - `GPT-4o mini` (Closed-source OpenAI)
  - `OpenAI o1-mini` (Closed-source OpenAI - reasoning model)
  - `DeepSeek-V2.5` (Open-source / MoE)
  - `Mixtral-8x7B-Instruct-v0.1` (Open-source / SMoE)
* **Parâmetros dos Modelos**:
  - Temperatura: Padrão dos provedores (temperatura de amostragem padrão; em código local `temperature` não é explicitamente fixado em 0, mas utiliza Voting Strategy de 3 a 5 rodadas para estabilização).
* **Algoritmo de Filtragem Sintática**:
  - Distância de Levenshtein com custo de substituição 1 e limiar empírico fixado em $0.5$.
* **Classificação / Decisão**:
  - Classificação categórica via Prompt Chaining com saída esperada em número da linha raiz ou `-1` (para comando de parada de retrocesso).

---

## 11. Métricas

As métricas são estritamente definidas como [Seção IV-C]:

1. **Recall (R)**:
   $$R = \frac{|\text{correct}_c \cap \text{identified}_c|}{|\text{correct}_c|}$$
2. **Precision (P)**:
   $$P = \frac{|\text{correct}_c \cap \text{identified}_c|}{|\text{identified}_c|}$$
3. **F1-Score**:
   $$\text{F1} = 2 \times \frac{P \times R}{P + R}$$
4. **Taxa de Falsos Positivos (False Positive Rate)**:
   $$\text{FPR} = \frac{|\text{identified}_c| - |\text{correct}_c \cap \text{identified}_c|}{|\text{identified}_c|}$$
5. **Métrica de Estabilidade (Stability Rate)**:
   Proporção de execuções onde as primeiras 3 rodadas repetidas retornam saídas idênticas (ou 3 em 4 rodadas). Resultados com $\le 2$ saídas idênticas após 5 rodadas são classificados como instáveis.

*Nota Crítica dos Autores sobre Deduplicação*: Os autores alertam que o trabalho de V-SZZ aplicou deduplicação em $|\text{correct}_c|$ e $|\text{identified}_c|$, o que distorce a avaliação quando vulnerabilidades distintas compartilham o mesmo commit indutor (ex: CVE-2009-1378, CVE-2009-1379 e CVE-2014-0221). O LLM-SZZ corrigiu esse viés avaliativo.

---

## 12. Resultados

### RQ1: Desempenho dos Diferentes LLMs
* **Fato Documentado [Tabela II]**:
  - No dataset **C/C++**: GPT-3.5 Turbo obteve os maiores índices (Recall: 0.830, Precision: 0.838, F1: 0.834).
  - No dataset **Java**: GPT-3.5 Turbo também foi o líder (Recall: 0.779, Precision: 0.768, F1: 0.774).
  - DeepSeek-V2.5 obteve desempenho muito próximo a custo negligível (C/C++: Recall 0.810, Precision 0.818; Java: Recall 0.765, Precision 0.732).
  - Estabilidade [Tabela III]: DeepSeek-V2.5 apresentou a maior estabilidade (1.000 em Java e 0.960 em C/C++). GPT-3.5 Turbo obteve 0.859 (C/C++) e 0.873 (Java).

### RQ2: Impacto da Distância de Levenshtein
* **Fato Documentado [Seção IV-E]**:
  - Testes variando o limiar de 0 a 1.0 com passos de 0.1 demonstraram que o limiar ótimo é exatamente **0.5**. Limiares menores admitem ruído excessivo; limiares maiores excluem linhas vulneráveis legítimas.

### RQ3: Estudo de Ablação (Descrição de CVE e Diff de Correção)
* **Fato Documentado [Tabelas IV e V]**:
  - Remover a descrição da CVE ou o diff causa queda de desempenho em todos os modelos.
  - A remoção do **diff de correção** causa um impacto negativo mais severo que a remoção da descrição da CVE, pois o diff fornece os detalhes específicos do código alterado. O melhor resultado ocorre com ambos combinados.

### RQ4: Comparação com Métodos SZZ Existentes
* **Fato Documentado [Tabelas VI e VII]**:

| Método | Dataset | Recall | Precision | F1-Score | Identified Commits | False Positive Rate |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **B-SZZ** | C/C++<br>Java | 0.630<br>0.681 | 0.578<br>0.362 | 0.603<br>0.472 | 109<br>130 | 0.422<br>0.638 |
| **MA-SZZ** | C/C++<br>Java | 0.660<br>0.783 | 0.520<br>0.432 | 0.581<br>0.557 | 127<br>125 | 0.480<br>0.568 |
| **AG-SZZ** | C/C++<br>Java | 0.680<br>0.739 | 0.548<br>0.531 | 0.607<br>0.618 | 124<br>96 | 0.452<br>0.469 |
| **V-SZZ** | C/C++<br>Java | 0.800<br>0.841 | 0.650<br>0.504 | 0.717<br>0.630 | 123<br>115 | 0.350<br>0.496 |
| **NEURAL-SZZ** | Java | 0.682 | 0.690 | 0.686 | 81 | 0.310 |
| **LLM-SZZ** | C/C++<br>Java | **0.830**<br>**0.779** | **0.838**<br>**0.768** | **0.834**<br>**0.774** | **99**<br>**71** | **0.162**<br>**0.232** |

* Ganhos do LLM-SZZ sobre o melhor baseline (V-SZZ):
  - Em C/C++: +18.8% em Precisão, +3.0% em Recall, +11.7% em F1-Score. Redução da taxa de falsos positivos de 0.350 para 0.162.
  - Em Java: +26.4% em Precisão sobre V-SZZ (+7.8% sobre NEURAL-SZZ), +14.4% em F1-Score.

### RQ5: Desempenho em Vulnerabilidades Profundas (Deep Vulnerabilities)
* **Fato Documentado [Tabela VIII]**:
  - Em vulnerabilidades profundas (que exigem múltiplos saltos de blame):
    - C/C++: Recall do LLM-SZZ foi **0.900** vs 0.675 do V-SZZ (+22.5%).
    - Java: Recall do LLM-SZZ foi **0.787** vs 0.773 do V-SZZ.
  - Em vulnerabilidades superficiais (*shallow*), o V-SZZ obteve recall superior (0.867 vs 0.767 em C/C++), pois o LLM-SZZ ocasionalmente sofre de *excessive backtracking* (recua além do commit indutor).

---

## 13. Ameaças à Validade

* **Validade de Construção (Construct Validity)**:
  - O benchmark é herdado de Bao et al. (172 casos). Para mitigar erros nos rótulos de verdade fundamental (ground truth), foi aplicado um protocolo de revisão independente por 3 pesquisadores com consenso por discussão.
* **Validade Interna (Internal Validity)**:
  - *Premissa Básica do SZZ*: Assume-se que statements relacionados ao bug são deletados, enquanto as correções são adicionadas. Vulnerabilidades corrigidas puramente por adições de linhas não são capturadas.
  - *Estocasticidade do LLM*: O não-determinismo intrínseco dos LLMs foi mitigado através de uma estratégia formal de votação majoritária (3 a 5 iterações).
* **Validade Externa (External Validity)**:
  - Avaliação restrita a 169 casos em duas linguagens (C/C++ e Java). Embora compatível com estudos empíricos anteriores da literatura, pode não generalizar para outras linguagens (ex.: Python, Go, Rust) ou para bugs comuns não relacionados a segurança.
* **Limitações Reconhecidas pelos Autores [Seção IV-I]**:
  - *Excessive Backtracking*: LLM-SZZ sofre mais de retrocesso excessivo (14 casos vs 10 no V-SZZ) porque o LLM pode interpretar que uma linha continuou evoluindo de uma versão limpa anterior, recuando além do ponto em que a falha foi de fato introduzida.

---

## 14. Artefatos Disponibilizados

* **Repositório GitHub**: `https://github.com/juzizi44/LLM_SZZ`
* **Código-Fonte**:
  - `main.py`, `main_with_des.py`, `main_with_diff.py`: Pontos de entrada de execução.
  - `SZZ/szz/llm_szz.py`: Implementação do algoritmo LLM-SZZ.
  - `SZZ/szz/core/llm.py`: Cliente de API OpenAI/DeepSeek.
  - Implementações comparativas inclusas: `b_szz.py`, `ag_szz.py`, `ma_szz.py`, `v_szz.py`.
* **Datasets e Rótulos**:
  - `data/label.json`: Anotações manuais dos commits indutores e descendentes.
  - `data/c_cve_fix_detail.json` / `java_cve_fix_detail.json`: Diffs estruturados e hashes de correção.
  - `data/verified_cve_with_versions_C.json` / `verified_cve_with_versions_Java.json`: Metadados completos de versões vulneráveis.

---

## 15. Replicabilidade

* **Classificação**: **Replicável com adaptações**
* **Justificativa**:
  1. O código-fonte e todos os datasets rotulados estão disponibilizados no repositório.
  2. Porém, o arquivo `SZZ/szz/core/llm.py` foi disponibilizado com chaves e URLs de API em branco (`self.api_key = ""` e `self.base_url = ""`).
  3. O script `download_repos.py` tenta clonar repositórios Git completos se for executar a mineração do zero; no entanto, a avaliação sobre os dados pré-extraídos em `data/` pode ser executada diretamente após preenchimento do cliente de API.

---

## 16. Protocolo de Replicação Local

1. **Pré-requisitos**:
   - Python 3.8, 3.9 ou 3.10 instalado.
   - Acesso à internet (para chamadas de API do modelo de linguagem) ou LLM local compatível com API OpenAI.
   - Chave de API (OpenAI, DeepSeek ou Google Gemini via endpoint OpenAI-compatível).
2. **Ambiente**:
   - Sistema Operacional: Linux (Ubuntu 20.04/22.04/Debian) ou macOS.
   - Memória RAM mínima: 8 GB.
3. **Dependências**:
   - Instalar pacotes via pip:
     ```bash
     cd /home/artur-carvalho/mestrado/repos/01-llm-szz
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```
4. **Código Necessário**:
   - Diretório `repos/01-llm-szz` já clonado localmente.
5. **Dataset Necessário**:
   - Arquivos `data/label.json`, `data/c_cve_fix_detail.json` e `data/java_cve_fix_detail.json` (já presentes no repositório local).
6. **Como Obter os Dados**:
   - Os dados brutos de entrada já estão commitados dentro de `repos/01-llm-szz/data/`.
7. **Como Preparar os Dados**:
   - Nenhuma conversão adicional necessária para a base pré-extraída.
8. **Como Executar o Experimento**:
   - Ajustar caminhos em `setting.py` (`WORK_DIR = '.'` ou caminho absoluto).
   - Configurar credenciais em `SZZ/szz/core/llm.py`.
   - Executar a avaliação:
     ```bash
     python main.py --method LLMSZZ --model gpt-3.5-turbo-0125 --language C --time 1 --levenshtein_num 0.5
     ```
9. **Parâmetros**:
   - `levenshtein_num`: 0.5
   - `model`: `gpt-3.5-turbo-0125` (ou modelo configurado)
   - `language`: `C` ou `Java`
   - `time`: 1 a 5 (para voting strategy)
10. **Configurações**:
    - Ajustar `SZZ_FOLDER` e `DATA_FOLDER` em `setting.py`.
11. **Algoritmos**:
    - `LLMSZZ`, `VSZZ`, `MASZZ`, `AGSZZ`, `BaseSZZ`.
12. **Classificadores**:
    - Modelos de chat completion com prompt de identificação de linha e critério de parada.
13. **Métricas a Coletar**:
    - Precision, Recall, F1-Score, Total Identified Commits, False Positive Rate.
14. **Resultados Esperados**:
    - C/C++: Recall $\approx 0.83$, Precision $\approx 0.838$, F1 $\approx 0.834$.
    - Java: Recall $\approx 0.779$, Precision $\approx 0.768$, F1 $\approx 0.774$.
15. **Critérios de Sucesso da Replicação**:
    - Obter precisão superior a 75% e taxa de falsos positivos inferior a 25%, confirmando a superioridade sobre os baselines estáticos.
16. **Problemas Conhecidos**:
    - Custos de chamadas à API da OpenAI se executado em grande volume.
    - Repositórios originais de código podem falhar no download automático via `download_repos.py` caso commits antigos tenham sido reescritos ou repositórios deletados.
17. **Pontos que Exigirão Adaptação**:
    - Adaptar `SZZ/szz/core/llm.py` para ler chaves de variáveis de ambiente (`os.getenv("GEMINI_API_KEY")` ou `os.getenv("OPENAI_API_KEY")`).
    - Redirecionar o endpoint para a API do Gemini via compatibilidade OpenAI (`base_url="https://generativelanguage.googleapis.com/v1beta/openai/"`), permitindo execução a custo R$ 0,00 com cota educacional.

---

## 17. Gaps de Replicação

1. **Credenciais e Endpoints Omitidos no Código**: `SZZ/szz/core/llm.py` possui strings vazias para chaves de API e URLs de base, exigindo injeção manual.
2. **Hardcoded Paths em `setting.py`**: O arquivo assume caminhos relativos específicos (`LLM_SZZ/data/`) que precisam ser normalizados para o diretório de execução.
3. **Ausência de Seed Fixa para LLMs**: Os autores não especificam semente aleatória (`seed`) nas chamadas da API OpenAI, confiando exclusivamente no comitê de votação majoritária de 3 a 5 rodadas para estabilização.

---

## 18. Controle de Rastreabilidade

| Afirmação / Dado Documentado | Documento Fonte | Seção / Página | Evidência Textual no Artigo |
| :--- | :--- | :--- | :--- |
| **Definição das 5 RQs** | `07-llm-szz-fse2024.pdf` | Seção IV, pág. 2-3 | "We assess the effectiveness of our proposed method by addressing the following five research questions: RQ1... RQ5..." |
| **Limiar Levenshtein = 0.5** | `07-llm-szz-fse2024.pdf` | Seção III-B & IV-E, pág. 3 | "The experiments indicated that the optimal performance was achieved when the Levenshtein distance was set to 0.5." |
| **Tamanho do Dataset (169 CVEs)** | `07-llm-szz-fse2024.pdf` | Seção IV-A, Tabela I, pág. 3 | "Consequently, the Java vulnerability count was adjusted to 69... C/C++ Dataset: 100, Java Dataset: 69." |
| **Resultados Comparativos com SZZs** | `07-llm-szz-fse2024.pdf` | Seção IV-G, Tabela VI, pág. 4 | "In terms of precision, LLM-SZZ performed the best, achieving a precision of 0.838... Java: 0.768..." |
| **Ablação CVE vs Diff** | `07-llm-szz-fse2024.pdf` | Seção IV-F, Tabelas IV e V, pág. 3-4 | "...with the fixing-commit diff having a greater effect... code prompts allow LLMs to better grasp the intricate details..." |
| **Desempenho em Deep Vulnerabilities** | `07-llm-szz-fse2024.pdf` | Seção IV-H, Tabela VIII, pág. 4 | "Deep Vulnerabilities Recall: LLM-SZZ 0.900 (C/C++) vs V-SZZ 0.675..." |
| **Limitação de Excessive Backtracking** | `07-llm-szz-fse2024.pdf` | Seção IV-I, Tabela IX, pág. 4 | "...whereas LLM-SZZ is more prone to excessive backtracking (14 cases vs 10 in V-SZZ)..." |
| **Causa de falha do GPT-4o vs 3.5** | `07-llm-szz-fse2024.pdf` | Seção IV-J, Tabela X, pág. 4-5 | "...GPT-4o’s stricter logic may miss weak or implicit signals... GPT-3.5 Turbo, being more lenient, better identifies potentially relevant cues." |
