# Arquitetura de Software e Diagnóstico de Ambiente — PySZZ v2 (Pesquisa 2)

## 1. Hierarquia de Classes Orientada a Objetos (`repos/02-pyszz-v2/szz/`)

```
                            +-----------------------------+
                            |        AbstractSZZ          |
                            |  (szz/core/abstract_szz.py) |
                            +--------------+--------------+
                                           |
            +------------------------------+------------------------------+
            |                              |                              |
            v                              v                              v
   +-----------------+            +-----------------+            +-----------------+
   |     BaseSZZ     |            |      AGSZZ      |            |  PyDrillerSZZ   |
   |  (szz/b_szz.py) |            | (szz/ag_szz.py) |            |  (szz/pd_szz.py)|
   +-----------------+            +--------+--------+            +-----------------+
                                           |
                                           v
                                  +-----------------+
                                  |      MASZZ      |
                                  | (szz/ma_szz.py) |
                                  +--------+--------+
                                           |
       +-----------------+-----------------+-----------------+-----------------+
       |                 |                 |                 |                 |
       v                 v                 v                 v                 v
+-------------+   +-------------+   +-------------+   +-------------+   +-------------+
|    LSZZ     |   |    RSZZ     |   |    RASZZ    |   |    ASZZ     |   |    DFSZZ    |
| (l_szz.py)  |   | (r_szz.py)  |   | (ra_szz.py) |   |(aszz/a_szz) |   |(dfszz/df_szz|
+-------------+   +-------------+   +-------------+   +-------------+   +-------------+
```

## 2. Módulos transversais e Utilitários (`szz/common/` & `szz/core/`)

- `szz/core/comment_parser.py` & `szz/common/srcml_wrapper.py`: Invoca `srcml` para converter código-fonte (C, C++, C#, Java) em AST XML e identificar intervalos de linhas de comentários, podando-os antes do `git blame`.
- `szz/common/issue_date.py`: Função `parse_issue_date(commit)` que extrai e normaliza o timestamp de abertura da issue quando `issue_date_filter: true` no arquivo YAML de `conf/`.
- `szz/common/revert_commits.py`: Detecta commits de `git revert` e redireciona o blame para o commit anterior ao revert.
- `tools/RefactoringMiner-2.0/bin/RefactoringMiner`: Executável Java embutido invocado por `RASZZ` para detectar refatorações em commits Java.
- `postfilter.py`, `postfilter_lszz.py`, `postfilter_rszz.py`: Scripts de pós-processamento sobre os JSONs de saída em `out/`.

## 3. Esquema dos Arquivos de Configuração (`conf/*.yml`)

- `szz_name`: Identificador da variante (`b`, `ag`, `ma`, `l`, `r`, `ra`, `pd`, `a`, `df`).
- `max_change_size`: Número máximo de linhas modificadas por commit (ex.: `20`).
- `issue_date_filter`: `true` | `false`.
- `detect_move_within_file`: `true` | `false` (`git blame -M`).
- `detect_move_from_other_files`: `1` (`-C`), `2` (`-C -C`), `3` (`-C -C -C`).
- `ignore_revs_file_path`: Caminho para lista de hashes de formatação em massa (`.git-blame-ignore-revs`).
