"""
Replicação e Teste de Execução das Variantes SZZ do Framework PySZZ v2
Base: Rosa et al. (ICSE 2021 / JSS 2023)
Variantes avaliadas: B-SZZ, AG-SZZ, MA-SZZ, L-SZZ
Utiliza os repositórios reais e bugfix commits empacotados em repos/02-pyszz-v2/test/
"""

import os
import sys
import glob
import json
import shutil
import zipfile
import subprocess
import pandas as pd

REPO_DIR = '/home/artur-carvalho/mestrado/repos/02-pyszz-v2'
OUTPUT_DIR = '/home/artur-carvalho/mestrado/experiments/02-pyszz-v2'
PYTHON_BIN = os.path.join(REPO_DIR, '.venv-pyszz-v2/bin/python')

os.makedirs(OUTPUT_DIR, exist_ok=True)
TEST_DIR = os.path.join(REPO_DIR, 'test')
WORKDIR = os.path.join(OUTPUT_DIR, 'workspace_test')
os.makedirs(WORKDIR, exist_ok=True)

# 1. Descompactar repositório de teste
zip_path = os.path.join(TEST_DIR, 'repos_test.zip')
print(f"[1/4] Descompactando {zip_path}...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(WORKDIR)

repos_path = os.path.join(WORKDIR, 'repos_test')
bugfix_json = os.path.join(TEST_DIR, 'bugfix_commits_test.json')

with open(bugfix_json, 'r') as f:
    input_cases = json.load(f)

print(f"[2/4] Casos de teste carregados: {len(input_cases)} commits de correção de bugs.")

# 2. Executar as variantes SZZ nativas
configs = [
    ('B-SZZ', os.path.join(REPO_DIR, 'conf/bszz.yml'), 'bszz'),
    ('AG-SZZ', os.path.join(REPO_DIR, 'conf/agszz.yml'), 'agszz'),
    ('MA-SZZ', os.path.join(REPO_DIR, 'conf/maszz.yml'), 'maszz'),
    ('L-SZZ', os.path.join(REPO_DIR, 'conf/lszz.yml'), 'lszz')
]

results_summary = []
pyszz_out_dir = os.path.join(REPO_DIR, 'out')
shutil.rmtree(pyszz_out_dir, ignore_errors=True)

for name, conf_path, prefix in configs:
    print(f"[3/4] Executando variante {name}...")
    run_cmd = [
        PYTHON_BIN,
        os.path.join(REPO_DIR, 'main.py'),
        bugfix_json,
        conf_path,
        repos_path
    ]
    
    p = subprocess.run(run_cmd, cwd=REPO_DIR, capture_output=True, text=True)
    if p.returncode != 0:
        print(f"Erro ao executar {name}:\n{p.stderr}")
        continue
        
    # O PySZZ gera arquivos no formato out/bic_<prefix>_<timestamp>.json
    matching_files = sorted(glob.glob(os.path.join(pyszz_out_dir, f'bic_{prefix}_*.json')))
    if matching_files:
        latest_file = matching_files[-1]
        with open(latest_file, 'r') as f:
            pairs = json.load(f)
            
        # Salvar cópia específica da variante no diretório de experimentos
        var_out_path = os.path.join(OUTPUT_DIR, f'pyszz_{prefix}_pairs.json')
        shutil.copy(latest_file, var_out_path)
        
        # Calcular estatísticas
        total_fixes = len(pairs)
        total_introducers = sum(len(entry.get('inducing_commit_hash', [])) for entry in pairs)
        avg_introducers = total_introducers / total_fixes if total_fixes > 0 else 0
        
        results_summary.append({
            'variant': name,
            'bugfix_commits': total_fixes,
            'total_inducing_commits': total_introducers,
            'avg_inducing_per_fix': round(avg_introducers, 2),
            'status': 'SUCCESS'
        })
    else:
        results_summary.append({
            'variant': name,
            'bugfix_commits': len(input_cases),
            'total_inducing_commits': 0,
            'avg_inducing_per_fix': 0,
            'status': 'NO_OUTPUT'
        })

# 3. Consolidar e Salvar Relatório
df_summary = pd.DataFrame(results_summary)
csv_path = os.path.join(OUTPUT_DIR, 'pyszz_v2_replication_summary.csv')
df_summary.to_csv(csv_path, index=False)

# Limpeza da pasta de trabalho temporária
shutil.rmtree(WORKDIR, ignore_errors=True)

print("=" * 70)
print("[REPLICAÇÃO PYSZZ V2] Execução concluída com sucesso!")
print("=" * 70)
print(df_summary.to_string(index=False))
print(f"\nResultados persistidos em: {OUTPUT_DIR}")
print("=" * 70)
