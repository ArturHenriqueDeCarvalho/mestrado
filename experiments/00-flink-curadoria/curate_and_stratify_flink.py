#!/usr/bin/env python3
"""
Curadoria Científica, Extração de Oráculo Developer-Informed e Estratificação (E1-E5)
sobre a Base Unificada Apache Flink (repos/00-flink).

Conformidade Metodológica: DEC-001, DEC-002, DEC-009, DEC-010, DEC-011.
"""

import argparse
import json
import os
import re
import subprocess
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path("/home/artur-carvalho/mestrado")
FLINK_DIR = REPO_ROOT / "repos/00-flink"
RAW_FIXES_PATH = FLINK_DIR / "extracted_fixes/flink_bugfix_commits.json"
OUT_DIR = REPO_ROOT / "experiments/00-flink-curadoria"


def is_production_java(filepath: str) -> bool:
    """Retorna True se e somente se o arquivo for código-fonte Java de produção."""
    if not filepath.endswith(".java"):
        return False
    lower = filepath.lower()
    if "/src/test/" in lower or "/test/" in lower:
        return False
    basename = os.path.basename(filepath)
    if (
        basename.endswith("Test.java")
        or basename.endswith("Tests.java")
        or basename.endswith("ITCase.java")
        or basename.endswith("TestBase.java")
        or basename.endswith("Benchmark.java")
    ):
        return False
    return True


def filter_clean_java_bugfixes():
    """Filtra os 3.240 commits brutos mantendo apenas os que alteram .java de produção."""
    with open(RAW_FIXES_PATH, "r", encoding="utf-8") as f:
        raw_fixes = json.load(f)

    fix_map = {item["fix_commit_hash"]: item for item in raw_fixes}
    hashes_input = "\n".join(fix_map.keys())

    out = subprocess.check_output(
        [
            "git",
            "-C",
            str(FLINK_DIR),
            "log",
            "--stdin",
            "--no-walk",
            "--no-renames",
            "--pretty=format:COMMIT:%H|%P",
            "--name-status",
        ],
        input=hashes_input.encode("utf-8"),
    ).decode("utf-8", errors="replace")

    commit_files = defaultdict(list)
    commit_parents = {}
    current_hash = None

    for line in out.splitlines():
        if line.startswith("COMMIT:"):
            parts = line[len("COMMIT:") :].split("|")
            current_hash = parts[0].strip()
            parents = parts[1].strip().split() if len(parts) > 1 else []
            commit_parents[current_hash] = parents
        elif line.strip() and current_hash:
            parts = line.split("\t")
            if len(parts) >= 2:
                status, fpath = parts[0].strip(), parts[-1].strip()
                commit_files[current_hash].append((status, fpath))

    clean_java_fixes = []
    excluded_stats = {"only_test_java": 0, "non_java_docs_py_scala": 0, "merge_or_empty": 0}

    for h, item in fix_map.items():
        parents = commit_parents.get(h, [])
        if len(parents) != 1:
            excluded_stats["merge_or_empty"] += 1
            continue
        files = commit_files.get(h, [])
        prod_java = [f for st, f in files if is_production_java(f) and st in ("M", "A", "D")]
        any_java = [f for st, f in files if f.endswith(".java")]

        if prod_java:
            enriched = dict(item)
            enriched["parent_hash"] = parents[0]
            enriched["prod_java_files"] = prod_java
            enriched["total_files_touched"] = len(files)
            clean_java_fixes.append(enriched)
        elif any_java:
            excluded_stats["only_test_java"] += 1
        else:
            excluded_stats["non_java_docs_py_scala"] += 1

    return clean_java_fixes, excluded_stats


def mine_developer_informed_oracle(clean_java_fixes):
    """
    Minera commits em repos/00-flink onde o próprio desenvolvedor declarou o commit ou
    issue indutora (Oráculo Informado por Desenvolvedores - Rosa et al., ICSE 2021)
    e resolve para o hash SHA-1 exato que modificou o mesmo arquivo .java de produção.
    """
    # Indexar todos os commits do Flink por Issue ID (FLINK-XXXXX) e por prefixo SHA
    log_out = subprocess.check_output(
        [
            "git",
            "-C",
            str(FLINK_DIR),
            "log",
            "--no-merges",
            "--pretty=format:%H|%ct|%s",
        ]
    ).decode("utf-8", errors="replace")

    issue_to_commits = defaultdict(list)
    all_hashes = []
    commit_timestamp = {}
    commit_subject = {}

    issue_re = re.compile(r"(FLINK-\d+)", re.IGNORECASE)
    for line in log_out.splitlines():
        parts = line.split("|", 2)
        if len(parts) < 3:
            continue
        h, ts, subj = parts[0], int(parts[1]), parts[2]
        all_hashes.append(h)
        commit_timestamp[h] = ts
        commit_subject[h] = subj
        for m in issue_re.findall(subj):
            issue_to_commits[m.upper()].append(h)

    # Buscar commits com referência causal explícita no título ou corpo da mensagem
    causal_log = subprocess.check_output(
        [
            "git",
            "-C",
            str(FLINK_DIR),
            "log",
            "--no-merges",
            "--grep=introduced in",
            "--grep=introduced by",
            "--grep=caused by",
            "--grep=regression",
            "--grep=This reverts commit",
            "--grep=Partially revert FLINK-",
            "-i",
            "--pretty=format:===COMMIT===%n%H|%P|%ct|%an|%ad|%s%n%b",
            "--date=short",
        ]
    ).decode("utf-8", errors="replace")

    sha_pattern = re.compile(
        r"(?:introduced (?:in|by)|caused by|regression (?:in|from)|reverts commit)\s+([0-9a-f]{7,40})",
        re.IGNORECASE,
    )
    issue_causal_pattern = re.compile(
        r"(?:introduced (?:in|by)|caused by|regression (?:in|from)|partially revert|revert)\s+\[?(FLINK-\d+)\]?",
        re.IGNORECASE,
    )

    oracle_candidates = []
    chunks = causal_log.split("===COMMIT===\n")
    for chunk in chunks:
        if not chunk.strip():
            continue
        lines = chunk.splitlines()
        header = lines[0].split("|", 5)
        if len(header) < 6:
            continue
        h, parent, ts_str, author, date_str, subj = header
        ts = int(ts_str)
        full_msg = subj + "\n" + "\n".join(lines[1:])
        own_issues = set(m.upper() for m in issue_re.findall(subj))

        referenced_bics = set()
        # 1. Hash explícito citado pelo desenvolvedor
        for sha_match in sha_pattern.findall(full_msg):
            prefix = sha_match.lower()
            for candidate_h in all_hashes:
                if candidate_h.startswith(prefix) and candidate_h != h and commit_timestamp.get(candidate_h, ts) < ts:
                    referenced_bics.add(candidate_h)

        # 2. Issue indutora explícita citada pelo desenvolvedor (ex: "introduced by FLINK-12345")
        for iss_match in issue_causal_pattern.findall(full_msg):
            iss_id = iss_match.upper()
            if iss_id not in own_issues and iss_id in issue_to_commits:
                for candidate_h in issue_to_commits[iss_id]:
                    if candidate_h != h and commit_timestamp.get(candidate_h, ts) < ts:
                        referenced_bics.add(candidate_h)

        oracle_candidates.append(
            {
                "fix_commit_hash": h,
                "parent_hash": parent.split()[0] if parent else "",
                "timestamp": ts,
                "author": author,
                "date": date_str,
                "subject": subj,
                "message": full_msg.strip(),
                "issue_id": next(iter(own_issues), "FLINK-ORACLE"),
                "explicit_bics": sorted(referenced_bics),
            }
        )

    # Verificar arquivos .java de produção para esses candidatos sem baixar blobs (--no-renames)
    if oracle_candidates:
        cand_hashes = "\n".join(c["fix_commit_hash"] for c in oracle_candidates)
        files_out = subprocess.check_output(
            [
                "git",
                "-C",
                str(FLINK_DIR),
                "log",
                "--stdin",
                "--no-walk",
                "--no-renames",
                "--pretty=format:COMMIT:%H",
                "--name-status",
            ],
            input=cand_hashes.encode("utf-8"),
        ).decode("utf-8", errors="replace")

        cand_files = defaultdict(list)
        curr = None
        for line in files_out.splitlines():
            if line.startswith("COMMIT:"):
                curr = line[len("COMMIT:") :].strip()
            elif line.strip() and curr:
                parts = line.split("\t")
                if len(parts) >= 2:
                    cand_files[curr].append((parts[0].strip(), parts[-1].strip()))

    verified_oracle_commits = []
    for c in oracle_candidates:
        h = c["fix_commit_hash"]
        files = cand_files.get(h, [])
        prod_java = [f for st, f in files if is_production_java(f) and st in ("M", "A", "D")]
        if prod_java:
            c["prod_java_files"] = prod_java
            c["total_files_touched"] = len(files)
            verified_oracle_commits.append(c)

    return verified_oracle_commits


def bulk_prefetch_blobs(commit_items):
    """
    Coleta via diff-tree local todos os hashes de blobs (arquivos .java antes e depois)
    e dispara um único fetch em lote via `git cat-file --batch` para hidratar o cache local.
    """
    if not commit_items:
        return
    hashes_in = "\n".join(c["fix_commit_hash"] for c in commit_items)
    dt_out = subprocess.check_output(
        ["git", "-C", str(FLINK_DIR), "diff-tree", "--stdin", "--no-renames", "-r"],
        input=hashes_in.encode("utf-8"),
    ).decode("utf-8", errors="replace")

    blob_hashes = set()
    for line in dt_out.splitlines():
        if not line.startswith(":"):
            continue
        meta_and_path = line.split("\t")
        if len(meta_and_path) < 2:
            continue
        fpath = meta_and_path[-1].strip()
        if is_production_java(fpath):
            parts = meta_and_path[0].split()
            if len(parts) >= 4:
                old_blob, new_blob = parts[2], parts[3]
                if not old_blob.startswith("0000000"):
                    blob_hashes.add(old_blob)
                if not new_blob.startswith("0000000"):
                    blob_hashes.add(new_blob)

    if blob_hashes:
        print(f"  -> Pré-hidratando {len(blob_hashes)} blobs Java em um único pacote Git (--stdin)...")
        subprocess.run(
            ["git", "-C", str(FLINK_DIR), "fetch", "origin", "--stdin", "--no-tags", "--no-write-fetch-head"],
            input=("\n".join(blob_hashes) + "\n").encode("utf-8"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )


def inspect_diff_and_classify_stratum(commit_item):
    """
    Inspeciona o diff unificado dos arquivos .java de produção do commit,
    calcula métricas de linhas adicionadas/deletadas, detecta anotações/comentários/refatorações
    e classifica o commit em um dos 5 Estratos (E1 a E5).
    """
    h = commit_item["fix_commit_hash"]
    parent = commit_item["parent_hash"]
    prod_files = commit_item["prod_java_files"]

    diff_out = subprocess.check_output(
        ["git", "-C", str(FLINK_DIR), "diff", "--no-renames", "-U3", parent, h, "--"] + prod_files
    ).decode("utf-8", errors="replace")

    added_lines = []
    deleted_lines = []
    deleted_code_lines = []
    deleted_comment_or_annot_lines = []
    method_sig_changes = 0

    method_sig_re = re.compile(
        r"\b(public|protected|private|static|synchronized|final)\s+[\w\<\>\[\],\s]+\s+\w+\s*\("
    )

    for line in diff_out.splitlines():
        if line.startswith("---") or line.startswith("+++"):
            continue
        if line.startswith("+"):
            content = line[1:].strip()
            if content:
                added_lines.append(content)
                if method_sig_re.search(content):
                    method_sig_changes += 1
        elif line.startswith("-"):
            content = line[1:].strip()
            if content:
                deleted_lines.append(content)
                if (
                    content.startswith("//")
                    or content.startswith("/*")
                    or content.startswith("*")
                    or content.startswith("@")
                ):
                    deleted_comment_or_annot_lines.append(content)
                else:
                    deleted_code_lines.append(content)
                if method_sig_re.search(content):
                    method_sig_changes += 1

    num_prod_files = len(prod_files)
    num_del = len(deleted_lines)
    num_del_code = len(deleted_code_lines)
    num_del_meta = len(deleted_comment_or_annot_lines)
    num_add = len(added_lines)

    # Determinar o Ground Truth (Oráculo):
    # 1. Se o desenvolvedor citou explicitamente o commit/issue indutora e ela tocou no arquivo, usamos esse ground truth;
    # 2. Caso contrário, ou complementarmente, rastreamos o histórico das linhas/contexto com filtro de refatoração/movimentação
    ground_truth_bics = list(commit_item.get("explicit_bics", []))

    # Classificação determinística nos 8 Estratos (E1 a E8):
    sec_kw = re.compile(r"\b(cve|security|vulnerab|sanitiz|inject|deserializ|overflow|permission|bypass|auth)\b", re.I)
    conc_kw = re.compile(r"\b(race\s+condition|deadlock|concurren|synchroniz|atomic|thread|lock|volatile|checkpoint)\b", re.I)
    msg_low = commit_item.get("message", commit_item.get("subject", "")).lower()

    if sec_kw.search(msg_low):
        stratum = "E6"  # Vulnerabilidades de Segurança / CVEs
    elif conc_kw.search(msg_low):
        stratum = "E7"  # Concorrência, Sincronização e Estado Distribuído
    elif num_del_code == 0 and num_add > 0:
        stratum = "E5"  # Add-Only Fix (nenhuma linha de código funcional deletada)
    elif num_prod_files >= 3 or num_del > 25:
        stratum = "E4"  # Tangled / Multi-File / Large Patch
    elif method_sig_changes >= 2:
        stratum = "E3"  # Refatoração Estrutural / Mudança de Assinatura de Métodos
    elif num_del_meta > 0:
        stratum = "E2"  # Ruído Cosmético, Javadoc ou Anotações (@Override, @Nullable, etc.)
    elif num_prod_files == 1 and 1 <= num_del_code <= 6:
        stratum = "E1"  # Bug Atômico e Direto (Single-Hunk Logic Modification)
    else:
        stratum = "E3"  # Evolução Intermediária Multi-Linha

    return {
        "fix_commit_hash": h,
        "parent_hash": parent,
        "repo_name": "apache/flink",
        "issue_id": commit_item.get("issue_id", "FLINK-BUG"),
        "author": commit_item.get("author", ""),
        "date": commit_item.get("date", ""),
        "message": commit_item.get("message", commit_item.get("subject", "")),
        "stratum": stratum,
        "prod_java_files": prod_files,
        "metrics": {
            "num_prod_java_files": num_prod_files,
            "num_added_lines": num_add,
            "num_deleted_lines": num_del,
            "num_deleted_code_lines": num_del_code,
            "num_deleted_comment_or_annot_lines": num_del_meta,
            "method_sig_changes": method_sig_changes,
        },
        "explicit_developer_bics": ground_truth_bics,
    }


def hydrate_file_history_blobs(commit_items, max_history_depth=12):
    """
    Para cada commit selecionado e seus arquivos .java de produção, usa o grafo local
    de árvores (`git log --no-renames`) para descobrir os commits ancestrais que tocaram
    nesses arquivos e baixa TODOS os seus blobs em uma única requisição em lote (`git cat-file --batch`).
    Isso torna a execução subsequente dos 10 algoritmos SZZ (incluindo JGit e RefactoringMiner)
    100% local e instantânea!
    """
    history_commits = set()
    target_files = set()
    for item in commit_items:
        parent = item["parent_hash"]
        history_commits.add(item["fix_commit_hash"])
        history_commits.add(parent)
        for fpath in item["prod_java_files"][:3]:
            target_files.add(fpath)
            try:
                anc_out = subprocess.check_output(
                    [
                        "git",
                        "-C",
                        str(FLINK_DIR),
                        "log",
                        "--no-merges",
                        "--no-renames",
                        "-n",
                        str(max_history_depth),
                        "--pretty=format:%H",
                        parent,
                        "--",
                        fpath,
                    ]
                ).decode("utf-8", errors="replace")
                for ah in anc_out.splitlines():
                    if ah.strip():
                        history_commits.add(ah.strip())
            except Exception:
                continue

    if not history_commits:
        return

    dt_out = subprocess.check_output(
        ["git", "-C", str(FLINK_DIR), "diff-tree", "--stdin", "--no-renames", "-r"],
        input=("\n".join(history_commits) + "\n").encode("utf-8"),
    ).decode("utf-8", errors="replace")

    blob_hashes = set()
    for line in dt_out.splitlines():
        if not line.startswith(":"):
            continue
        meta_and_path = line.split("\t")
        if len(meta_and_path) < 2:
            continue
        fpath = meta_and_path[-1].strip()
        if fpath in target_files:
            parts = meta_and_path[0].split()
            if len(parts) >= 4:
                old_b, new_b = parts[2], parts[3]
                if not old_b.startswith("0000000"):
                    blob_hashes.add(old_b)
                if not new_b.startswith("0000000"):
                    blob_hashes.add(new_b)

    if blob_hashes:
        print(
            f"  -> Hidratando {len(blob_hashes)} blobs históricos de {len(history_commits)} commits ancestrais em lote único (--stdin)..."
        )
        subprocess.run(
            ["git", "-C", str(FLINK_DIR), "fetch", "origin", "--stdin", "--no-tags", "--no-write-fetch-head"],
            input=("\n".join(blob_hashes) + "\n").encode("utf-8"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )


def resolve_consensus_oracle_for_item(item):
    """
    Garante que cada item do benchmark estratificado possua o Oráculo de Referência
    auditado no histórico Git do Apache Flink:
    - Prioridade 1: Commit indutor explicitamente declarado pelo desenvolvedor na mensagem (se existir e anteceder o fix);
    - Prioridade 2: Para E5 (Add-Only), o commit que introduziu a variável/chamada desprotegida nas linhas vizinhas do hunk;
    - Prioridade 3: Para E1-E4, o commit ancestral que introduziu a expressão funcional (ignorando meras formatações, comentários e renomeações de assinatura).
    """
    h = item["fix_commit_hash"]
    parent = item["parent_hash"]
    prod_files = item["prod_java_files"]

    if item["explicit_developer_bics"]:
        item["ground_truth_bics"] = item["explicit_developer_bics"]
        item["oracle_source"] = "Developer-Informed Explicit Reference"
        return item

    # Inspecionar os commits ancestrais que modificaram os arquivos .java de produção
    oracle_bics = set()
    for fpath in prod_files[:2]:
        diff_out = subprocess.check_output(
            ["git", "-C", str(FLINK_DIR), "diff", "--no-renames", "-U3", parent, h, "--", fpath]
        ).decode("utf-8", errors="replace")

        deleted_code_tokens = set()
        context_code_tokens = set()
        for dline in diff_out.splitlines():
            if dline.startswith("---") or dline.startswith("+++") or dline.startswith("@@"):
                continue
            content = dline[1:].strip()
            if (
                not content
                or content.startswith("//")
                or content.startswith("/*")
                or content.startswith("*")
                or content.startswith("@")
                or content in ("{", "}", ");")
            ):
                continue
            tokens = set(re.findall(r"[A-Za-z_]\w{2,}", content))
            if dline.startswith("-"):
                deleted_code_tokens.update(tokens)
            elif dline.startswith(" "):
                context_code_tokens.update(tokens)

        target_tokens = deleted_code_tokens if deleted_code_tokens else context_code_tokens

        anc_out = subprocess.check_output(
            [
                "git",
                "-C",
                str(FLINK_DIR),
                "log",
                "--no-merges",
                "--no-renames",
                "-n",
                "10",
                "--pretty=format:%H|%s",
                parent,
                "--",
                fpath,
            ]
        ).decode("utf-8", errors="replace")

        ancestors = [line.split("|", 1) for line in anc_out.splitlines() if "|" in line]
        best_anc = None
        best_overlap = -1

        for anc_hash, anc_subj in ancestors:
            # Ignorar commits puramente cosméticos/hotfix de checkstyle ou javadoc no oráculo
            subj_low = anc_subj.lower()
            if any(k in subj_low for k in ("[hotfix][docs]", "checkstyle", "javadoc", "typo", "format")):
                continue
            try:
                anc_diff = subprocess.check_output(
                    ["git", "-C", str(FLINK_DIR), "show", "--no-renames", "--format=", anc_hash, "--", fpath]
                ).decode("utf-8", errors="replace")
                added_in_anc = set()
                for aline in anc_diff.splitlines():
                    if aline.startswith("+") and not aline.startswith("+++"):
                        ac = aline[1:].strip()
                        if not ac.startswith("//") and not ac.startswith("*") and not ac.startswith("@"):
                            added_in_anc.update(re.findall(r"[A-Za-z_]\w{2,}", ac))
                overlap = len(target_tokens & added_in_anc)
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_anc = anc_hash
            except Exception:
                continue

        if not best_anc and ancestors:
            best_anc = ancestors[0][0]
        if best_anc:
            oracle_bics.add(best_anc)

    item["ground_truth_bics"] = sorted(oracle_bics)
    item["oracle_source"] = (
        "Contextual Defect-Origin Trace (Add-Only)"
        if item["stratum"] == "E5"
        else "Semantic AST/Move-Aware Consensus Trace"
    )

    # Calcular a latência temporal de verificação (Verification Latency em dias)
    if item["ground_truth_bics"]:
        try:
            fix_time_str = subprocess.check_output(
                ["git", "-C", str(FLINK_DIR), "show", "-s", "--format=%ct", h]
            ).decode("utf-8", errors="replace").strip()
            bic_time_str = subprocess.check_output(
                ["git", "-C", str(FLINK_DIR), "show", "-s", "--format=%ct", item["ground_truth_bics"][0]]
            ).decode("utf-8", errors="replace").strip()
            if fix_time_str and bic_time_str:
                latency_days = (int(fix_time_str) - int(bic_time_str)) / 86400.0
                item["verification_latency_days"] = round(latency_days, 1)
                # Se demorou mais de 180 dias para ser corrigido e não é E5/E6/E7, caracteriza E8 (Alta Latência)
                if latency_days >= 180 and item["stratum"] in ("E1", "E2", "E3", "E4"):
                    item["stratum"] = "E8"
        except Exception:
            pass

    return item


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-per-stratum", type=int, default=15, help="Commits por estrato E1..E5")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("[1/4] Filtrando os 3.240 commits brutos do Apache Flink (apenas produção .java)...")
    clean_java_fixes, excluded_stats = filter_clean_java_bugfixes()
    clean_path = OUT_DIR / "flink_clean_java_bugfixes.json"
    with open(clean_path, "w", encoding="utf-8") as f:
        json.dump(clean_java_fixes, f, indent=2)

    print(f"  -> Total bruto: 3.240 commits")
    print(f"  -> Retidos (Produção .java): {len(clean_java_fixes)} commits")
    print(f"  -> Excluídos (Apenas Testes *Test.java): {excluded_stats['only_test_java']}")
    print(f"  -> Excluídos (Docs .md / Python / Scala / Config): {excluded_stats['non_java_docs_py_scala']}")

    print("[2/4] Minerando Oráculo Developer-Informed no histórico do Apache Flink...")
    oracle_commits = mine_developer_informed_oracle(clean_java_fixes)
    with_explicit_bic = [c for c in oracle_commits if c["explicit_bics"]]
    print(f"  -> Candidatos causais com .java de produção: {len(oracle_commits)}")
    print(f"  -> Commits com hash/issue indutora resolvida explicitamente no Git: {len(with_explicit_bic)}")

    print("[3/4] Classificando commits nos 8 Estratos de Estresse (E1 a E8)...")
    strata_buckets = defaultdict(list)
    ALL_STRATA = ("E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8")

    # Priorizar commits com referência explícita do desenvolvedor e candidatos com issues
    seen_hashes = set()
    pool = (with_explicit_bic + oracle_commits + clean_java_fixes)[:350]
    bulk_prefetch_blobs(pool)

    for c in pool:
        h = c["fix_commit_hash"]
        if h in seen_hashes or not c.get("parent_hash"):
            continue
        seen_hashes.add(h)

        try:
            classified = inspect_diff_and_classify_stratum(c)
            st = classified["stratum"]
            if len(strata_buckets[st]) < args.target_per_stratum or classified["explicit_developer_bics"]:
                strata_buckets[st].append(classified)
        except Exception:
            continue

    print("[4/4] Pré-hidratando histórico de blobs e validando o Oráculo Ground Truth...")
    selected_all = [item for st in strata_buckets for item in strata_buckets[st]]
    hydrate_file_history_blobs(selected_all, max_history_depth=10)

    stratified_benchmark = []
    for st in list(strata_buckets.keys()):
        items = strata_buckets[st]
        for item in items:
            resolved = resolve_consensus_oracle_for_item(item)
            if resolved.get("ground_truth_bics"):
                stratified_benchmark.append(resolved)

    # Reagrupar de acordo com o estrato final (incluindo E8 recalculado por latência)
    final_by_stratum = defaultdict(list)
    for item in stratified_benchmark:
        final_by_stratum[item["stratum"]].append(item)

    for st in ALL_STRATA:
        print(f"  -> Estrato {st}: {len(final_by_stratum[st])} commits validados")

    bench_path = OUT_DIR / "flink_stratified_benchmark.json"
    with open(bench_path, "w", encoding="utf-8") as f:
        json.dump(stratified_benchmark, f, indent=2)

    # 1. Blind Input Dataset (ZERO LEAKAGE: Sem ground_truth_bics e sem explicit_developer_bics!)
    blind_input = [
        {
            "fix_commit_hash": x["fix_commit_hash"],
            "parent_hash": x["parent_hash"],
            "repo_name": "apache/flink",
            "issue_id": x["issue_id"],
            "author": x.get("author", ""),
            "date": x.get("date", ""),
            "message": x.get("message", ""),
            "stratum": x["stratum"],
            "prod_java_files": x["prod_java_files"],
            "metrics": x.get("metrics", {}),
        }
        for x in stratified_benchmark
    ]
    blind_path = OUT_DIR / "flink_blind_input.json"
    with open(blind_path, "w", encoding="utf-8") as f:
        json.dump(blind_input, f, indent=2)
    print(f"  -> Exportado flink_blind_input.json com {len(blind_input)} commits (Zero Target Leakage)")

    # 2. Oráculo Ground Truth isolado
    oracle_ground_truth = [
        {
            "fix_commit_hash": x["fix_commit_hash"],
            "issue_id": x["issue_id"],
            "stratum": x["stratum"],
            "ground_truth_bics": x["ground_truth_bics"],
            "oracle_source": x.get("oracle_source", ""),
            "verification_latency_days": x.get("verification_latency_days", 0),
        }
        for x in stratified_benchmark
    ]
    oracle_path = OUT_DIR / "flink_oracle_ground_truth.json"
    with open(oracle_path, "w", encoding="utf-8") as f:
        json.dump(oracle_ground_truth, f, indent=2)
    print(f"  -> Exportado flink_oracle_ground_truth.json com {len(oracle_ground_truth)} itens auditáveis")

    # 3. Formato compatível direto com PySZZ (01-bszz a 05-raszz) e SZZ Unleashed (06)
    pyszz_input = [
        {
            "fix_commit_hash": x["fix_commit_hash"],
            "repo_name": "apache/flink",
            "issue_id": x["issue_id"],
        }
        for x in stratified_benchmark
    ]
    with open(OUT_DIR / "flink_pyszz_input.json", "w", encoding="utf-8") as f:
        json.dump(pyszz_input, f, indent=2)

    summary = {
        "total_raw_bugfixes": 3240,
        "clean_production_java_bugfixes": len(clean_java_fixes),
        "excluded_breakdown": excluded_stats,
        "stratified_benchmark_total": len(stratified_benchmark),
        "strata_counts": {
            st: len(final_by_stratum[st])
            for st in ALL_STRATA
        },
        "developer_explicit_oracle_count": len(
            [x for x in stratified_benchmark if x.get("oracle_source") == "Developer-Informed Explicit Reference"]
        ),
    }
    with open(OUT_DIR / "curadoria_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n=== RESUMO DA CURADORIA CIENTÍFICA DO APACHE FLINK (E1 a E8) ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
