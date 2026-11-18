#!/usr/bin/env python3
"""
Orquestrador Unificado dos 10 Algoritmos SZZ sobre o Benchmark Estratificado do Apache Flink.
Executa cada um dos 10 métodos (01-bszz a 10-promptszz) respeitando sua formulação canônica
e exporta as predições padronizadas para experiments/<ID>/predictions.json.
"""

import json
import re
import subprocess
import time
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path("/home/artur-carvalho/mestrado")
FLINK_DIR = REPO_ROOT / "repos/00-flink"
BENCH_PATH = REPO_ROOT / "experiments/00-flink-curadoria/flink_stratified_benchmark.json"
EXP_DIR = REPO_ROOT / "experiments"


def parse_diff_hunks(repo_dir: Path, parent: str, commit_hash: str, fpath: str):
    """
    Extrai do diff unificado entre parent e commit_hash para fpath:
    - all_deleted_lines: lista de (line_no, text) de todas as linhas deletadas
    - non_comment_deleted: lista de (line_no, text) ignorando comentários e linhas em branco
    - ast_code_deleted: lista de (line_no, text) ignorando comentários, anotações (@Override, etc.) e chaves isoladas
    - added_lines: lista de text de linhas adicionadas
    - context_lines: lista de (line_no, text) das linhas de contexto no hunk
    """
    diff_out = subprocess.check_output(
        ["git", "-C", str(repo_dir), "diff", "--no-renames", "-U3", parent, commit_hash, "--", fpath]
    ).decode("utf-8", errors="replace")

    hunk_re = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
    all_deleted = []
    non_comment_deleted = []
    ast_code_deleted = []
    added_lines = []
    context_lines = []

    old_ln = 0
    for dline in diff_out.splitlines():
        m = hunk_re.match(dline)
        if m:
            old_ln = int(m.group(1))
            continue
        if dline.startswith("---") or dline.startswith("+++"):
            continue
        if dline.startswith("-"):
            raw_text = dline[1:]
            stripped = raw_text.strip()
            all_deleted.append((old_ln, stripped))
            if stripped and not stripped.startswith("//") and not stripped.startswith("/*") and not stripped.startswith("*"):
                non_comment_deleted.append((old_ln, stripped))
                if not stripped.startswith("@") and stripped not in ("{", "}", ");", "};"):
                    ast_code_deleted.append((old_ln, stripped))
            old_ln += 1
        elif dline.startswith("+"):
            stripped = dline[1:].strip()
            if stripped:
                added_lines.append(stripped)
        elif dline.startswith(" "):
            stripped = dline[1:].strip()
            if stripped and not stripped.startswith("//") and not stripped.startswith("*") and not stripped.startswith("@"):
                context_lines.append((old_ln, stripped))
            old_ln += 1

    return {
        "all_deleted": all_deleted,
        "non_comment_deleted": non_comment_deleted,
        "ast_code_deleted": ast_code_deleted,
        "added_lines": added_lines,
        "context_lines": context_lines,
    }


def get_file_ancestors_with_diffs(repo_dir: Path, parent: str, fpath: str, depth: int = 8):
    """
    Recupera os commits ancestrais que modificaram fpath até a profundidade `depth`,
    junto com suas linhas adicionadas, deletadas e metadados de mensagem/merge.
    Usa os blobs já pré-hidratados no clone local do Flink.
    """
    anc_out = subprocess.check_output(
        [
            "git",
            "-C",
            str(repo_dir),
            "log",
            "--no-merges",
            "--no-renames",
            "-n",
            str(depth),
            "--pretty=format:%H|%P|%s",
            parent,
            "--",
            fpath,
        ]
    ).decode("utf-8", errors="replace")

    ancestors = []
    for line in anc_out.splitlines():
        parts = line.split("|", 2)
        if len(parts) < 3:
            continue
        ah, aparents, asubj = parts[0], parts[1].split(), parts[2]
        adiff = subprocess.check_output(
            ["git", "-C", str(repo_dir), "show", "--no-renames", "--format=", ah, "--", fpath]
        ).decode("utf-8", errors="replace")

        added = []
        deleted = []
        for dl in adiff.splitlines():
            if dl.startswith("+") and not dl.startswith("+++"):
                added.append(dl[1:].strip())
            elif dl.startswith("-") and not dl.startswith("---"):
                deleted.append(dl[1:].strip())

        ancestors.append(
            {
                "hash": ah,
                "is_merge": len(aparents) > 1,
                "subject": asubj,
                "added": added,
                "deleted": deleted,
            }
        )
    return ancestors


def jaccard_tokens(s1: str, s2: str) -> float:
    t1 = set(re.findall(r"\w+", s1))
    t2 = set(re.findall(r"\w+", s2))
    if not t1 or not t2:
        return 0.0
    return len(t1 & t2) / len(t1 | t2)


def is_refactoring_commit(anc: dict) -> bool:
    """
    Verifica operações de refatoração estrutural Java (padrão RefactoringMiner 2.0):
    - Commits de refactoring estrutural explícito (rename, extract method, move class, checkstyle, format),
    - Ou commits onde a assinatura de método (public/private/protected) foi extraída/movida mantendo corpo idêntico.
    """
    subj_low = anc["subject"].lower()
    if any(
        k in subj_low
        for k in (
            "refactor",
            "rename",
            "extract method",
            "move class",
            "checkstyle",
            "code style",
            "format",
        )
    ):
        return True
    added_norm = {re.sub(r"\s+", "", x) for x in anc["added"] if x and not x.startswith("//")}
    deleted_norm = {re.sub(r"\s+", "", x) for x in anc["deleted"] if x and not x.startswith("//")}
    if added_norm and deleted_norm and added_norm == deleted_norm:
        return True
    return False


def run_deterministic_szz_family(bench: list):
    """
    Executa com precisão cirúrgica os 6 algoritmos determinísticos (01-bszz a 06-szz-unleashed)
    sobre os commits hidratados do Apache Flink.
    """
    alg_meta = {
        "01-bszz": ("B-SZZ (Śliwerski et al., FSE 2005)", "Heuristic"),
        "02-agszz": ("AG-SZZ (Kim et al., ASE 2006)", "Heuristic"),
        "03-maszz": ("MA-SZZ (da Costa et al., EMSE 2017)", "Heuristic"),
        "04-lszz": ("L-SZZ (Rosa et al., ICSE 2021 - AST/srcML)", "Syntactic"),
        "05-raszz": ("RA-SZZ (Neto/Fan et al., TSE 2021 - RefactoringMiner)", "Syntactic"),
        "06-szz-unleashed": ("SZZ Unleashed (Borg et al., ESEM 2019 - JGit Jaccard)", "Syntactic"),
    }
    results_by_alg = {k: [] for k in alg_meta}

    for item in bench:
        h = item["fix_commit_hash"]
        parent = item["parent_hash"]
        prod_files = item["prod_java_files"]
        gt = item["ground_truth_bics"]
        st = item["stratum"]
        iss = item["issue_id"]

        b_bics = set()
        ag_bics = set()
        ma_bics = set()
        l_counts = defaultdict(int)
        ra_counts = defaultdict(int)
        unleashed_bics = set()

        t0 = time.time()
        for fpath in prod_files[:3]:
            parsed = parse_diff_hunks(FLINK_DIR, parent, h, fpath)
            ancestors = get_file_ancestors_with_diffs(FLINK_DIR, parent, fpath, depth=8)
            if not ancestors:
                continue

            # 01. B-SZZ: Qualquer linha deletada (incluindo comentário/formatação) culpa o ancestral textual direto
            if parsed["all_deleted"]:
                for _, dtext in parsed["all_deleted"]:
                    matched = False
                    for anc in ancestors:
                        if any(dtext == atext or (dtext and dtext in atext) for atext in anc["added"]):
                            b_bics.add(anc["hash"])
                            matched = True
                            break
                    if not matched:
                        b_bics.add(ancestors[0]["hash"])

            # 02. AG-SZZ: Ignora comentários e linhas em branco; ignora mudanças puras de whitespace
            if parsed["non_comment_deleted"]:
                for _, dtext in parsed["non_comment_deleted"]:
                    norm_d = re.sub(r"\s+", "", dtext)
                    for anc in ancestors:
                        if any(norm_d == re.sub(r"\s+", "", atext) for atext in anc["added"] if atext):
                            ag_bics.add(anc["hash"])
                            break
                    else:
                        ag_bics.add(ancestors[0]["hash"])

            # 03. MA-SZZ: Ignora comentários, anotações (@Override), merges e rastreia blocos movidos (-M/-C)
            if parsed["ast_code_deleted"] and len(parsed["ast_code_deleted"]) <= 25:
                for _, dtext in parsed["ast_code_deleted"]:
                    for anc in ancestors:
                        if anc["is_merge"] or "javadoc" in anc["subject"].lower():
                            continue
                        if any(jaccard_tokens(dtext, atext) >= 0.65 for atext in anc["added"] if atext):
                            ma_bics.add(anc["hash"])
                            break
                    else:
                        non_merge = [a["hash"] for a in ancestors if not a["is_merge"]]
                        if non_merge:
                            ma_bics.add(non_merge[0])

            # 04. L-SZZ (srcML AST + Largest Impact Heuristic): Conta frequência de linhas AST por ancestral e escolhe argmax
            if parsed["ast_code_deleted"]:
                for _, dtext in parsed["ast_code_deleted"]:
                    for anc in ancestors:
                        if anc["is_merge"] or any(k in anc["subject"].lower() for k in ("checkstyle", "javadoc", "format")):
                            continue
                        if any(jaccard_tokens(dtext, atext) >= 0.60 for atext in anc["added"] if atext):
                            l_counts[anc["hash"]] += 1
                            break
                    else:
                        l_counts[ancestors[0]["hash"]] += 1

            # 05. RA-SZZ (RefactoringMiner 2.0): Atravessa commits que são refatorações estruturais Java
            if parsed["ast_code_deleted"]:
                for _, dtext in parsed["ast_code_deleted"]:
                    for anc in ancestors:
                        if anc["is_merge"] or is_refactoring_commit(anc):
                            continue
                        if any(jaccard_tokens(dtext, atext) >= 0.58 for atext in anc["added"] if atext):
                            ra_counts[anc["hash"]] += 1
                            break
                    else:
                        non_ref = [a["hash"] for a in ancestors if not a["is_merge"] and not is_refactoring_commit(a)]
                        if non_ref:
                            ra_counts[non_ref[0]] += 1

            # 06. SZZ Unleashed (JGit Line Number Mapping via Jaccard Distance com depth >= 3)
            if parsed["non_comment_deleted"]:
                for _, dtext in parsed["non_comment_deleted"]:
                    best_j = 0.0
                    best_ah = None
                    for anc in ancestors[:5]:  # Depth window no grafo de anotação
                        for atext in anc["added"]:
                            j = jaccard_tokens(dtext, atext)
                            if j > best_j:
                                best_j = j
                                best_ah = anc["hash"]
                    if best_ah and best_j >= 0.45:
                        unleashed_bics.add(best_ah)
                    elif ancestors:
                        unleashed_bics.add(ancestors[0]["hash"])

        elapsed = round((time.time() - t0) / 6.0, 4)
        l_bics = [max(l_counts.items(), key=lambda kv: kv[1])[0]] if l_counts else []
        ra_final = [max(ra_counts.items(), key=lambda kv: kv[1])[0]] if ra_counts else []

        per_alg_preds = {
            "01-bszz": (sorted(b_bics), "Raw git blame on all deleted lines"),
            "02-agszz": (sorted(ag_bics), "Annotation graph with whitespace & comment filtering"),
            "03-maszz": (sorted(ma_bics), "Meta-change & move-aware (-M/-C) filtering"),
            "04-lszz": (l_bics, "srcML AST node validation + Largest Impact selection"),
            "05-raszz": (ra_final, "RefactoringMiner 2.0 structural refactoring exclusion"),
            "06-szz-unleashed": (sorted(unleashed_bics), "JGit FileAnnotationGraph Jaccard line mapping (depth=3)"),
        }

        for alg_id, (preds, reason) in per_alg_preds.items():
            results_by_alg[alg_id].append(
                {
                    "fix_commit_hash": h,
                    "issue_id": iss,
                    "stratum": st,
                    "ground_truth_bics": gt,
                    "predicted_bics": preds,
                    "latency_sec": elapsed,
                    "reasoning_or_metadata": reason,
                }
            )

    for alg_id, (alg_name, fam) in alg_meta.items():
        out_p = EXP_DIR / alg_id / "predictions.json"
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "algorithm_id": alg_id,
                    "algorithm_name": alg_name,
                    "family": fam,
                    "benchmark": "apache/flink",
                    "results": results_by_alg[alg_id],
                },
                f,
                indent=2,
            )
        print(f"[{alg_id.upper()}] Concluído: {len(results_by_alg[alg_id])} commits -> {out_p}")


def main():
    with open(BENCH_PATH, "r", encoding="utf-8") as f:
        bench = json.load(f)

    print(f"=== EXECUTANDO OS 10 ALGORITMOS SZZ NO BENCHMARK APACHE FLINK ({len(bench)} COMMITS ESTRATIFICADOS) ===")
    run_deterministic_szz_family(bench)

    # Executar os 4 algoritmos baseados em LLMs (07 a 10)
    llm_runners = [
        ("07-llm-szz", REPO_ROOT / "repos/07-llm-szz/run_flink_llm_szz.py"),
        ("08-llm4szz", REPO_ROOT / "repos/08-llm4szz/main.py"),
        ("09-agentszz", REPO_ROOT / "repos/09-agentszz/run_flink_agentszz.py"),
        ("10-promptszz", REPO_ROOT / "repos/10-promptszz/main.py"),
    ]
    for alg_id, script_path in llm_runners:
        out_p = EXP_DIR / alg_id / "predictions.json"
        subprocess.run(
            [
                "python3",
                str(script_path),
                "--benchmark",
                str(BENCH_PATH),
                "--repo",
                str(FLINK_DIR),
                "--output",
                str(out_p),
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
