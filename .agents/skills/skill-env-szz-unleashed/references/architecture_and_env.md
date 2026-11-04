# Arquitetura de Software e Diagnóstico de Ambiente — SZZ Unleashed (Pesquisa 3)

## 1. Diagrama dos 4 Subsistemas (`repos/03-szz-unleashed/`)

```
+-----------------------------------------------------------------------------------+
| SUBSISTEMA 1: fetch_jira_bugs/ (Python 3)                                         |
|  - fetch.py -> Jira REST API (JQL query) -> examples/data/issues/*.json           |
|  - git_log_to_array.py -> gitlog.json                                             |
|  - find_bug_fixes.py -> Regex matching (JENKINS-XXX) -> issue_list.json           |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| SUBSISTEMA 2: szz/ (Java 8/11 + Eclipse JGit 4.10.0)                              |
|  - Main.java: CLI Parser (-i issue_list.json -r repo -d depth)                    |
|  - parser/GitParser.java & GitParserThread.java: Multi-threaded JGit traversal    |
|  - graph/FileAnnotationGraph.java & AnnotationMap.java: Grafo de revisões         |
|  - diff/DiffingLines.java & SimplePartition.java: Hunk partitioning               |
|  - heuristics/DistanceIntroducerFinder.java: Williams & Spacco Line Mapping       |
|    usando info.debatty:java-string-similarity (Jaccard Distance)                  |
|  - Saída: results/fix_and_introducers_pairs.json                                  |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| SUBSISTEMA 3: data_assembler/ (Python 3 + code-maat 1.1)                          |
|  - assemble_code_churns.py (Ft1-Ft3)                                              |
|  - assemble_diffusion_features.py (Ft4-Ft7)                                       |
|  - assemble_purpose_features.py (Ft8)                                             |
|  - assemble_history_features.py & assemble_experience_features.py (Ft9-Ft13)      |
|  - assemble_coupling_features.py (Ft14-Ft16 via CodeMaat temporal coupling)       |
|  - assemble_labels.py -> Rotula commits presentes em fix_and_introducers_pairs    |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| SUBSISTEMA 4: model/ (Python 3 + scikit-learn + imbalanced-learn)                 |
|  - model.ini: Configuração de n_estimators=200, split (kfold|occ), sampler        |
|  - time_sensitive_split.py: Janelas deslizantes OCC (sgap=331, gap=73, egap=781)  |
|  - random_forest_wrapper.py & model.py: Treino, amostragem e métricas P, R, F1    |
+-----------------------------------------------------------------------------------+
```

## 2. Diagnóstico Crítico de Build Java (`szz/build.gradle`)

- **FatJar Pré-Compilado Disponível**: O repositório já inclui o binário pronto em [`examples/data/jars/szz_find_bug_introducers-0.1.jar`](file:///home/artur-carvalho/mestrado/repos/03-szz-unleashed/examples/data/jars/szz_find_bug_introducers-0.1.jar) (4,6 MB), que embute todas as bibliotecas (`org.eclipse.jgit`, `java-string-similarity`, `commons-cli`, `json-simple`, `slf4j`).
- **Caso seja necessário recompilar `szz/`**: O arquivo `szz/build.gradle` original declara `jcenter()` (descontinuado pela JFrog em 2021) e a diretiva `compile` (substituída por `implementation` no Gradle 7+). Para recompilar código Java modificado, substitua `jcenter()` por `mavenCentral()`.
