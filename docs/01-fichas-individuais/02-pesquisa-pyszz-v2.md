# Ficha Estruturada de Pesquisa Científica — PESQUISA 2: PySZZ v2

---

## 1. Identificação

* **Título**: A Comprehensive Evaluation of SZZ Variants Through a Developer-Informed Oracle *(Originalmente apresentado na ICSE 2021 e estendido no Journal of Systems and Software)*
* **Autores**: Giovanni Rosa, Luca Pascarella, Simone Scalabrino, Rosalia Tufano, Gabriele Bavota, Michele Lanza, Rocco Oliveto
* **Afiliações**: University of Molise (Itália); Software Institute @ USI Università della Svizzera italiana (Suíça)
* **Ano**: 2021 (ICSE) / 2023 (Journal of Systems and Software - JSS)
* **Venue**: Journal of Systems and Software (JSS), Volume 202, Artigo 111729, 2023 / IEEE/ACM 43rd International Conference on Software Engineering (ICSE 2021)
* **DOI**: https://doi.org/10.1016/j.jss.2023.111729
* **URL (Preprint Open Access)**: https://arxiv.org/abs/2102.03300 *(Nota de rastreabilidade: o link preliminar continha id 2103.02388 por erro tipográfico; o preprint exato dos autores é o arXiv:2102.03300)*
* **Replication Package Oficial (Figshare)**: https://doi.org/10.6084/m9.figshare.19586500
* **Repositório Oficial**: https://github.com/grosa1/pyszz_v2
* **Identificação Interna**: **PESQUISA 2**

---

## 2. Problema

* **Problema Científico**:
  A ausência de um oráculo confiável, imparcial e independente para avaliar a acurácia de diferentes variantes e implementações do algoritmo SZZ.
* **Causas Raízes e Falhas dos Métodos de Avaliação Anteriores** [Seção I, Linhas 14-27 & Seção II-A]:
  1. *Subjetividade e Falta de Conhecimento do Domínio*: Historicamente, as avaliações de SZZ dependiam de análise manual feita por pesquisadores acadêmicos com conhecimento limitado dos sistemas de software sob teste, ou métricas heurísticas indiretas sem verdade fundamental (*ground truth*).
  2. *Falta de Padronização e Replicabilidade*: Pesquisadores propuseram melhorias pontuais (ex.: AG-SZZ, MA-SZZ, RA-SZZ, L-SZZ, R-SZZ), mas as implementações originais não estavam centralizadas em uma ferramenta extensível, código-aberto e multi-linguagem.
  3. *Dependência Irrealista de Issue Trackers*: A maioria das implementações assume que há datas de abertura de issues em Jira/Bugzilla disponíveis para filtrar falsos positivos; na prática de software real, a vasta maioria dos commits fixadores não referencia issues formais (apenas ~11% no dataset minerado).

---

## 3. Perguntas de Pesquisa (Research Questions)

A pergunta de pesquisa formal apresentada pelos autores [Seção IV, Linhas 748-750]:

* **RQ Principal**: How do different variants of SZZ perform in identifying bug-inducing changes?
  - *Desdobramento Empírico 1*: Qual é o impacto na precisão e recall ao filtrar commits cosméticos, meta-changes, refatorações e aplicar heurísticas de seleção (latest vs largest)?
  - *Desdobramento Empírico 2*: Qual é o impacto real da aplicação do filtro de data da issue (*issue date filter*)?
  - *Desdobramento Empírico 3*: Qual é o grau de sobreposição e complementaridade (*overlap & complementarity*) entre as variantes de SZZ?
  - *Desdobramento Empírico 4*: Quais são as causas raízes de falha nos casos onde todas as variantes de SZZ falham?

---

## 4. Hipóteses

* **Hipótese 1 [FATO DOCUMENTADO - Seção I & III]**: Mensagens de commit escritas pelos próprios desenvolvedores que corrigem bugs contêm, frequentemente, referências explícitas não-ambíguas ao hash do commit que introduziu o defeito (ex.: *"fixes bug introduced by commit X"*). Essas anotações constituem um oráculo "informado pelo desenvolvedor" (*developer-informed oracle*) com fidelidade de domínio superior a oráculos manuais construídos por pesquisadores externos.
* **Hipótese 2 [FATO DOCUMENTADO - Seção IV-A]**: Heurísticas que selecionam apenas o commit mais recente que tocou na linha alterada (R-SZZ) combinadas com exclusão de mudanças cosméticas e meta-mudanças reduzem substancialmente os falsos positivos, alcançando precisão superior às variantes gulosas tradicionais.

---

## 5. Objetivos

* **Objetivo Geral**:
  Construir uma metodologia automatizada e manual para gerar um oráculo de avaliação informado pelos desenvolvedores e criar uma suíte extensível em Python (**PySZZ v2**) que implementa e compara, de forma padronizada, as variantes seminais de SZZ sobre uma base multi-linguagem.
* **Objetivos Específicos**:
  1. Desenvolver um pipeline de mineração sintática (via spaCy e NLP) sobre 19,6 milhões de commits do GitHub Archive para identificar menções explícitas a commits indutores.
  2. Realizar validação manual rigorosa com 4 avaliadores independentes, construindo o oráculo `oracle_all` (1.115 casos) e `oracle_issues` (129 casos).
  3. Re-implementar em Python as principais variantes da literatura: B-SZZ, AG-SZZ, MA-SZZ, L-SZZ, R-SZZ, RA-SZZ* e criar wrappers para ferramentas existentes (PyDriller, SZZ Unleashed e OpenSZZ).
  4. Avaliar empiricamente o desempenho de cada variante com e sem filtro de data de issue, medindo sobreposição (*overlap*) e identificando padrões para evolução do SZZ.

---

## 6. Contexto

* **Contexto de Mineração de Repositórios e Engenharia de Software Empírica (MSR/ESE)**:
  Pesquisa de defeitos, predição de falhas (Defect Prediction) e identificação de fatores humanos e técnicos na introdução de bugs. SZZ é o alicerce fundamental de quase 200 artigos científicos nessa área.

---

## 7. Dados

* **Origem dos Dados Primários**:
  GH Archive (eventos de push públicos do GitHub) cobrindo o período de **01 de Março de 2011 a 30 de Abril de 2020** [Seção III-A].
* **Volume Inicial Minerado**:
  19.603.736 commits.
* **Filtros Sintáticos e Heurísticos via NLP (spaCy)**:
  - *Palavras de Fix e Bug*: Mensagens contendo palavras de correção (*fix, solve*) e de defeito (*bug, issue, problem, error, misfeature*), excluindo a palavra *merge*.
  - *Heurística H1*: Exclusão de commits sem hash ou iniciados com a palavra *revert*.
  - *Heurística H2 (Coarse Filter)*: Verificação se o verbo *introduce* é ancestral do hash $h_j$ na árvore sintática gerada pelo spaCy.
  - *Heurística H3 (Fine Filter)*: Para casos sem o verbo *introduce*, validação de dependências semânticas e lista restritiva de stop-words (*was, been, seem, solved, fixed, try, trie, by, attempt, test*).
  - *Desduplicação*: Eliminação de forks de repositórios repetidos, mantendo o repositório canônico.
  - *Resultado Automatizado*: 3.585 commits candidatos.
* **Validação Manual dos Candidatos**:
  - 4 avaliadores (aluno de pós-graduação, docente, pesquisador júnior e pesquisador sênior).
  - Cada commit foi inspecionado independentemente por 2 avaliadores (total de 7.170 avaliações).
  - Critério conservador: Ausência de consenso ou marcação como "irrelevante" por um avaliador resultou em exclusão imediata.
  - Sobreviventes: 1.930 commits (55.6%) em 1.625 repositórios; apenas 212 (11.0%) referenciavam uma issue formal online.
* **Dataset Filtrado por Linguagem (Contexto Experimental Principal)** [Tabela III]:
  Focado nas 8 principais linguagens com maior representatividade: **C, Python, C++, JavaScript, Java, PHP, Ruby e C#**.
  - **Repositórios únicos**: 951
  - **oracle_all**: 1.115 commits fixadores (com ou sem issue).
  - **oracle_issues**: 129 commits fixadores (que possuem issue associada com data de abertura verificável).
  - **oracle_Jall**: 80 commits (subconjunto restrito a Java para rodar ferramentas que dependem de AST Java como RA-SZZ* e OpenSZZ).
  - **oracle_Jissues**: 10 commits (subconjunto Java com issue date).

---

## 8. Metodologia

O fluxo metodológico do estudo de avaliação e do PySZZ v2 é estruturado em:

```
[DADOS: GH Archive (19.6M commits)]
   │
[PRÉ-PROCESSAMENTO: spaCy NLP Trees (H1, H2, H3) + Deduplicação] ──> 3.585 commits
   │
[VALIDAÇÃO MANUAL: 4 Avaliadores Independentes (Critério Conservador)] ──> 1.930 commits
   │
[FILTRAGEM DE LINGUAGEM: Top-8 Linguagens (C, Py, C++, JS, Java, PHP, Ruby, C#)]
   ├── oracle_all (1.115 commits)
   └── oracle_issues (129 commits)
   │
[MÉTODO: Execução no PySZZ v2 de 9 Abordagens]
   ├── B-SZZ, AG-SZZ, MA-SZZ, L-SZZ, R-SZZ, RA-SZZ*
   └── Wrappers: SZZ@PYD (PyDriller), SZZ@UNL (Unleashed), SZZ@OPN (OpenSZZ)
   │
[VARIAÇÃO EXPERIMENTAL: Filtro de Data de Issue (Sem Data vs Com Data)]
   │
[MÉTRICAS: Precision, Recall, F1, Overlap (Jaccard Interseção), Exclusividade]
   │
[RESULTADOS & ANÁLISE QUALITATIVA: 311 casos onde todas as variantes falharam]
```

### Características Técnicas das Variantes Comparadas [Tabela IV]:
1. **B-SZZ**: Algoritmo canônico via `git blame`. Sem filtros de linha ou meta-changes.
2. **AG-SZZ**: Usa grafo de anotações; filtra mudanças cosméticas (espaços em branco, identação, comentários e quebras de linha).
3. **MA-SZZ**: Adiciona ao AG-SZZ a filtragem de *meta-changes* (commits de merge, criação/mudança de branches e alterações exclusivas de propriedades de arquivos/permissões).
4. **L-SZZ**: Baseado no MA-SZZ; aplica heurística de seleção *Largest* (seleciona o commit que alterou o maior número de linhas como o único BIC).
5. **R-SZZ**: Baseado no MA-SZZ; aplica heurística de seleção *Latest/Most Recent* (seleciona o commit temporalmente mais recente que tocou na linha como o único BIC).
6. **RA-SZZ***: Filtra refatorações de código Java utilizando `RefactoringMiner 2.0`.
7. **SZZ@PYD**: Wrapper da implementação do pacote PyDriller.
8. **SZZ@UNL**: Wrapper do SZZ Unleashed (implementa mapeamento de número de linha em Java).
9. **SZZ@OPN**: Wrapper do OpenSZZ.

---

## 9. Ferramentas

| Ferramenta | Versão Documentada | Finalidade | Configuração / Parâmetros |
| :--- | :--- | :--- | :--- |
| **PyDriller** | 1.15.2 | Mineração de repositórios Git em Python | Uso de `GitRepository` e extração de diffs |
| **GitPython** | 3.1.7 | Manipulação de Git no baixo nível | Execução de comandos `git blame -M -C` |
| **spaCy** | 2.x / 3.x | Processamento de linguagem natural | Parsing de árvores de dependência sintática (`doc.sents`) |
| **srcML** | Versão binária de sistema | Parsing sintático de código multi-linguagem | Mapeamento de comentários e AST para C, C++, C#, Java |
| **RefactoringMiner** | 2.0 | Detecção de refatorações em código Java | Utilizado pelo módulo `ra_szz.py` |
| **PyYAML** | 5.3.1 | Leitura de configurações declarativas | Arquivos em `conf/*.yml` |
| **Docker** | Dockerfile oficial | Empacotamento de ambiente reproduzível | Imagem base com Python 3 e srcML pré-instalados |

---

## 10. Algoritmos e Classificadores

* **Abordagem Algorítmica**: Heurísticas determinísticas baseadas em análise estática de repositórios versionados (não utiliza modelos de aprendizado de máquina supervisionados na identificação principal de BIC).
* **Parâmetros de Blame e Rastreamento** [Configuráveis em `conf/`]:
  - `max_change_size`: Limite de linhas alteradas para descartar commits massivos (default: 20 em MA-SZZ ou desativado).
  - `detect_move_within_file`: `-M` do `git blame` para rastrear linhas movidas dentro do mesmo arquivo.
  - `detect_move_from_other_files`: `-C` do `git blame` (opções: 1 = same commit, 2 = parent commit, 3 = any commit) para rastrear código copiado/movido entre arquivos distintos.
  - `timeout`: Limite de segurança de 1 hora por execução de blame para evitar loops infinitos em grafos cíclicos de commits.

---

## 11. Métricas

1. **Recall**:
   $$\text{Recall} = \frac{|\text{correct} \cap \text{identified}|}{|\text{correct}|}$$
2. **Precision**:
   $$\text{Precision} = \frac{|\text{correct} \cap \text{identified}|}{|\text{identified}|}$$
3. **F-Measure (F1)**:
   $$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
4. **Métrica de Sobreposição (Jaccard Intersect)**:
   $$\text{correct}_{v_i \cap v_j} = \frac{|\text{correct}_{v_i} \cap \text{correct}_{v_j}|}{|\text{correct}_{v_i} \cup \text{correct}_{v_j}|}$$
5. **Métrica de Exclusividade (Unique True Positives)**:
   $$\text{correct}_{v_i \setminus (\text{SZZ}_{\text{exp}} \setminus v_i)} = \frac{|\text{correct}_{v_i} \setminus \text{correct}_{(\text{SZZ}_{\text{exp}} \setminus v_i)}|}{|\text{correct}_{v_i} \cup \text{correct}_{(\text{SZZ}_{\text{exp}} \setminus v_i)}|}$$

---

## 12. Resultados

### Desempenho Geral das Variantes [Tabela V]:

#### Cenário 1: Sem Filtro de Data da Issue (`issue_date_filter: false`)

| Algoritmo | oracle_all: Recall | oracle_all: Precision | oracle_all: F1 | oracle_issue: Recall | oracle_issue: Precision | oracle_issue: F1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **B-SZZ** | 0.69 | 0.39 | 0.50 | 0.69 | 0.38 | 0.49 |
| **AG-SZZ** | 0.60 | 0.45 | 0.52 | 0.62 | 0.43 | 0.51 |
| **L-SZZ** | 0.45 | 0.52 | 0.48 | 0.43 | 0.49 | 0.46 |
| **R-SZZ** | 0.57 | **0.66** | **0.61** | 0.56 | **0.64** | **0.60** |
| **MA-SZZ** | 0.64 | 0.36 | 0.46 | 0.65 | 0.36 | 0.47 |
| **RA-SZZ\*** *(Java only)* | 0.45 | 0.35 | 0.39 | 0.40 | 0.57 | 0.47 |
| **SZZ@PYD** | 0.67 | 0.39 | 0.49 | 0.68 | 0.39 | 0.50 |
| **SZZ@UNL** | **0.72** | 0.09 | 0.16 | **0.72** | 0.06 | 0.12 |
| **SZZ@OPN** *(Java only)* | 0.19 | 0.32 | 0.24 | 0.10 | 0.50 | 0.17 |

#### Cenário 2: Com Filtro de Data da Issue (`issue_date_filter: true`)

| Algoritmo | oracle_all: Recall | oracle_all: Precision | oracle_all: F1 | oracle_issue: Recall | oracle_issue: Precision | oracle_issue: F1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **B-SZZ** | 0.69 | 0.42 | 0.53 | 0.69 | 0.39 | 0.50 |
| **AG-SZZ** | 0.60 | 0.49 | 0.54 | 0.62 | 0.44 | 0.52 |
| **L-SZZ** | 0.45 | 0.54 | 0.49 | 0.43 | 0.50 | 0.46 |
| **R-SZZ** | 0.57 | **0.73** | **0.64** | 0.56 | **0.67** | **0.61** |
| **MA-SZZ** | 0.64 | 0.39 | 0.48 | 0.65 | 0.37 | 0.47 |
| **RA-SZZ\*** *(Java only)* | 0.45 | 0.43 | 0.44 | 0.40 | 0.57 | 0.47 |
| **SZZ@PYD** | 0.67 | 0.42 | 0.52 | 0.68 | 0.41 | 0.51 |
| **SZZ@UNL** | **0.72** | 0.09 | 0.16 | **0.72** | 0.06 | 0.12 |
| **SZZ@OPN** *(Java only)* | 0.19 | 0.33 | 0.24 | 0.10 | 0.50 | 0.17 |

### Síntese dos Fatos Documentados:
1. **Campeão em Precisão**: **R-SZZ** é a variante mais precisa da literatura, atingindo até **73% de precisão** no `oracle_all` com filtro de data (e 66% sem data).
2. **Campeão em Recall com Colapso em Precisão**: **SZZ@UNL (SZZ Unleashed)** atinge o maior recall (72%), mas com precisão crítica entre **6% e 9%**. Os autores investigaram e descobriram que SZZ Unleashed gera outliers severos (ex.: 3 commits fixadores geraram 72 commits indutores apontados, dos quais apenas 3 eram verdadeiros).
3. **Filtro de Data da Issue**: Não altera o recall (como teoricamente esperado), mas traz aumentos consistentes de precisão entre +1% e +8% (especialmente para R-SZZ e RA-SZZ*).
4. **Sobreposição e Complementaridade**: 21 de 28 comparações entre variantes têm sobreposição $\ge 70\%$. Nenhuma variante, com exceção de SZZ@UNL (20 casos), encontrou commits corretos exclusivos que todas as outras perderam.

### Lições Aprendidas nos 311 Casos de Falha Unânime [Seção V-A]:
1. *A linha defeituosa nem sempre é alterada no fix*: Exemplo clássico em Java da adição de um `if (x != null)` para tratar NullPointerException; a linha que originou a leitura insegura não é deletada nem modificada, apenas recebe uma guarda ao redor. Blame tradicional falha 100% nesses casos.
2. *Sensibilidade a Reescritas de Histórico (Rebase e Reverts)*: Commits do tipo `git revert` enganam o SZZ, fazendo com que ele aponte o commit do revert como indutor em vez do commit que gerou o código original.
3. *Visão do Todo (The Big Picture)*: Commits onde linhas adicionadas corrigem o defeito enquanto linhas deletadas eram apenas refatorações secundárias emaranhadas.

---

## 13. Ameaças à Validade

* **Validade de Construção (Construct Validity)**:
  - Possibilidade de anotações incorretas em mensagens de commit. Mitigada pelo protocolo de revisão dupla com descarte obrigatório de qualquer caso com dúvida ou sem consenso.
  - Para atestar a maturidade dos 951 projetos minerados, os autores inspecionaram 123 projetos e constataram que 95% possuíam testes unitários e code reviews via PRs, e 75% possuíam pipelines de Integração Contínua (CI).
* **Validade Interna (Internal Validity)**:
  - Variações nas re-implementações das variantes. Os autores documentaram minuciosamente cada desvio na Tabela IV, mantendo as alterações restritas a otimizações de conformidade sintática.
* **Validade Externa (External Validity)**:
  - O oráculo representa um subconjunto de projetos onde desenvolvedores documentam explicitamente a causa raiz. Projetos de menor maturidade ou equipes que não registram commits indutores podem ter dinâmicas diferentes.

---

## 14. Artefatos Disponibilizados

* **Repositório GitHub**: `https://github.com/grosa1/pyszz_v2`
* **Código-Fonte**:
  - `main.py`: Ponto de entrada CLI multi-variante.
  - `szz/`: Módulos de todas as variantes (`b_szz.py`, `ag_szz.py`, `ma_szz.py`, `r_szz.py`, `l_szz.py`, `ra_szz.py`, `pd_szz.py`).
  - `conf/`: 32 arquivos YAML com matrizes de configuração para todas as combinações de filtros.
  - Scripts de teste e pós-filtragem: `start_example1.sh`, `start_example2.sh`, `start_example3.sh`, `postfilter_lszz.py`, `postfilter_rszz.py`.
* **Datasets e Pacote de Replicação**:
  - Figshare Archive DOI: `10.6084/m9.figshare.19586500`
  - Arquivos de teste embutidos no repositório: `test/repos_test.zip` e `test/bugfix_commits_test.json`.

---

## 15. Replicabilidade

* **Classificação**: **Diretamente replicável** (com alta maturidade de engenharia)
* **Justificativa**:
  O repositório inclui exemplos funcionais executáveis de ponta a ponta (`start_example1.sh`), pacotes de teste embutidos com mini-repositórios Git (`repos_test.zip`), Dockerfile funcional e configurações YAML claras.
  O único pré-requisito externo de sistema para variantes sintáticas é a ferramenta `srcML` no PATH do sistema.

---

## 16. Protocolo de Replicação Local

1. **Pré-requisitos**:
   - Python 3.8+ instalado.
   - `git` $\ge 2.23$.
   - `srcml` instalado no sistema (`sudo apt install srcml` ou download do binário em `srcml.org`).
2. **Ambiente**:
   - Sistema Operacional: Linux (Ubuntu/Debian) testado nativamente.
   - Processador: CPU multi-core (utiliza recursos nativos de `git blame`).
   - Memória RAM: $\ge 4$ GB.
3. **Dependências**:
   ```bash
   cd /home/artur-carvalho/mestrado/repos/02-pyszz-v2
   python3 -m venv venv
   source venv/bin/activate
   pip install --no-cache-dir -r requirements.txt
   ```
4. **Código Necessário**:
   - Repositório `repos/02-pyszz-v2` já clonado localmente.
5. **Dataset Necessário**:
   - Para teste local imediato: `test/bugfix_commits_test.json` e `test/repos_test.zip`.
   - Para replicação integral do paper: Dataset do Figshare (`10.6084/m9.figshare.19586500`).
6. **Como Obter os Dados**:
   - Os dados de teste e os 5 repositórios de prova de conceito já estão na pasta `test/`.
7. **Como Preparar os Dados**:
   - Descompactar os repositórios de teste:
     ```bash
     unzip test/repos_test.zip -d test/
     ```
8. **Como Executar o Experimento (Exemplo MA-SZZ)**:
   ```bash
   python3 main.py test/bugfix_commits_test.json conf/maszz.yml test/repos_test/
   ```
9. **Parâmetros**:
   - Definidos via arquivo YAML (`conf/maszz.yml` ou `conf/rszz.yml`):
     - `szz_name: "r"` ou `"ma"`
     - `issue_date_filter: false` ou `true`
     - `max_change_size: 20`
     - `detect_move_within_file: true`
     - `detect_move_from_other_files: 1`
10. **Configurações**:
    - Usar `conf/rszz.yml` para máxima precisão ou `conf/maszz.yml` para equilíbrio.
11. **Algoritmos**:
    - MA-SZZ, R-SZZ, AG-SZZ, B-SZZ, L-SZZ, RA-SZZ.
12. **Classificadores**:
    - N/A (Algoritmos determinísticos baseados em grafo de anotações e AST diffs).
13. **Métricas a Coletar**:
    - Precision, Recall, F1-Score contra os hashes esperados no JSON do oráculo.
14. **Resultados Esperados (sobre o Oracle All)**:
    - R-SZZ sem data: Recall 0.57, Precision 0.66, F1 0.61.
    - R-SZZ com data: Recall 0.57, Precision 0.73, F1 0.64.
15. **Critérios de Sucesso**:
    - Execução do script gerando arquivo de saída JSON contendo os commits indutores mapeados sem lançar exceções de timeout ou parsing.
16. **Problemas Conhecidos**:
    - `srcML` é obrigatório para suporte multi-linguagem a comentários.
    - Repositórios gigantescos podem acionar o timeout de 1 hora configurado em `szz/ma_szz.py#135`.
17. **Pontos que Exigirão Adaptação**:
    - Se executado fora de container Docker, garantir que o pacote `srcml` esteja instalado via repositório de pacotes da distribuição (`.deb`).

---

## 17. Gaps de Replicação

1. **Dependência Externa de Sistema (`srcml`)**: Não é um pacote Python (PyPI), requer instalação de binário C++ nativo no Linux para parsing de C/C++/Java/C#.
2. **Dependência de Repositórios Externos no Figshare**: O repositório Git traz testes unitários de prova de conceito, mas a replicação completa dos 1.115 commits requer o download do arquivo ZIP de repositórios arquivado no Figshare (que possui vários gigabytes).

---

## 18. Controle de Rastreabilidade

| Afirmação / Dado Documentado | Documento Fonte | Seção / Página | Evidência Textual no Artigo |
| :--- | :--- | :--- | :--- |
| **Definição da RQ Principal** | `02-pyszz-v2.pdf` | Seção IV, pág. 4 | "How do different variants of SZZ perform in identifying bug-inducing changes?" |
| **Volume Minerado no GH Archive** | `02-pyszz-v2.pdf` | Seção III-A, pág. 3 | "...mined the time period going from March 1st 2011 to April 30th 2020, extracting 19,603,736 commits..." |
| **Heurísticas NLP spaCy H1, H2, H3** | `02-pyszz-v2.pdf` | Seção III-A, pág. 3-4 | "H1: Exclude Commits Without Reference and Reverts... H2: Coarsely Filter... H3: Finely Filter..." |
| **Tamanho do Dataset (1.115 commits)** | `02-pyszz-v2.pdf` | Seção III-C, Tabela III, pág. 4 | "Total: 1,115 commits in 951 repositories (oracle_all); 129 in oracle_issues." |
| **R-SZZ como Campeão em Precisão** | `02-pyszz-v2.pdf` | Seção V, Tabela V, pág. 5-6 | "R-SZZ is the most precise on both oracles, achieving a 66% precision on oracle_all and 64% on oracle_issues... boosting to 73% with date filter." |
| **Colapso de Precisão do SZZ Unleashed** | `02-pyszz-v2.pdf` | Seção V, pág. 6 | "SZZ@UNL achieves a 72% recall... with, however, a precision of 9% and 6%... due to a set of outlier bug-fixing commits." |
| **Apenas 11% dos bugs têm issue pública** | `02-pyszz-v2.pdf` | Seção III-C, pág. 4 | "...only 212 of these (11.0%) mention the fixed issue. This indicates that SZZ implementations that rely on issue trackers can only be run on a minority of bug-fixing commits." |
| **3 Padrões de Falha do SZZ** | `02-pyszz-v2.pdf` | Seção V-A, pág. 7 | "1) The buggy line is not always impacted in the bug-fix; 2) SZZ is sensible to history rewritings (rebase/revert); 3) Looking at the big picture..." |
