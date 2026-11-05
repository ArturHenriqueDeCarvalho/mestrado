"""
Replicação e Auditoria Empírica do Dataset SZZ-TSE (10 Projetos Apache)
Validação dos 126.526 commits e análise da distribuição dos 4 rótulos SZZ:
- buggy_B2: B-SZZ clássico (Sliwerski et al., 2005)
- buggy_AG: AG-SZZ baseado em anotações (Kim et al., 2006)
- buggy_MA: MA-SZZ baseado em meta-informações (da Costa et al., 2017)
- buggy_RA: RA-SZZ filtrado por refatoração com RefactoringMiner (Neto et al., 2018)
"""

import os
import glob
import json
import pandas as pd
import numpy as np

DATA_DIR = '/home/artur-carvalho/mestrado/repos/04-szz-tse/szz-tse/data_results/data_csvs'
OUTPUT_DIR = '/home/artur-carvalho/mestrado/experiments/01-szz-tse'

os.makedirs(OUTPUT_DIR, exist_ok=True)

files = sorted(glob.glob(os.path.join(DATA_DIR, '*.csv')))
szz_variants = ['buggy_B2', 'buggy_AG', 'buggy_MA', 'buggy_RA']

project_summaries = []
all_dfs = []

for filepath in files:
    project_name = os.path.basename(filepath).replace('.csv', '')
    df = pd.read_csv(filepath)
    df['project'] = project_name
    all_dfs.append(df)
    
    total = len(df)
    row = {
        'project': project_name,
        'total_commits': total
    }
    
    for v in szz_variants:
        count = int((df[v] == 'buggy').sum())
        ratio = float(count / total) if total > 0 else 0.0
        row[f'{v}_count'] = count
        row[f'{v}_ratio'] = round(ratio, 4)
        
    project_summaries.append(row)

# Consolidado Apache (Total 10 projetos)
total_df = pd.concat(all_dfs, ignore_index=True)
grand_total = len(total_df)

total_row = {
    'project': 'TOTAL_APACHE',
    'total_commits': grand_total
}

for v in szz_variants:
    count = int((total_df[v] == 'buggy').sum())
    ratio = float(count / grand_total)
    total_row[f'{v}_count'] = count
    total_row[f'{v}_ratio'] = round(ratio, 4)

project_summaries.append(total_row)

summary_df = pd.DataFrame(project_summaries)
summary_csv_path = os.path.join(OUTPUT_DIR, 'apache_10_projects_szz_summary.csv')
summary_df.to_csv(summary_csv_path, index=False)

# Auditoria de Mislabeled Changes (Ruído de Rotulagem frente ao Baseline RA-SZZ)
# Conforme Fan et al. (IEEE TSE 2019/2021)
mislabeled_stats = {
    'total_commits_auditados': grand_total,
    'b2_vs_ra': {
        'b2_total_buggy': int((total_df['buggy_B2'] == 'buggy').sum()),
        'ra_total_buggy': int((total_df['buggy_RA'] == 'buggy').sum()),
        'mislabeled_as_buggy_by_b2': int(((total_df['buggy_B2'] == 'buggy') & (total_df['buggy_RA'] == 'clean')).sum()),
        'mislabeled_ratio': round(float(((total_df['buggy_B2'] == 'buggy') & (total_df['buggy_RA'] == 'clean')).sum()) / grand_total, 4)
    },
    'ag_vs_ra': {
        'ag_total_buggy': int((total_df['buggy_AG'] == 'buggy').sum()),
        'ra_total_buggy': int((total_df['buggy_RA'] == 'buggy').sum()),
        'mislabeled_as_buggy_by_ag': int(((total_df['buggy_AG'] == 'buggy') & (total_df['buggy_RA'] == 'clean')).sum()),
        'mislabeled_ratio': round(float(((total_df['buggy_AG'] == 'buggy') & (total_df['buggy_RA'] == 'clean')).sum()) / grand_total, 4)
    },
    'ma_vs_ra': {
        'ma_total_buggy': int((total_df['buggy_MA'] == 'buggy').sum()),
        'ra_total_buggy': int((total_df['buggy_RA'] == 'buggy').sum()),
        'mislabeled_as_buggy_by_ma': int(((total_df['buggy_MA'] == 'buggy') & (total_df['buggy_RA'] == 'clean')).sum()),
        'mislabeled_ratio': round(float(((total_df['buggy_MA'] == 'buggy') & (total_df['buggy_RA'] == 'clean')).sum()) / grand_total, 4)
    }
}

audit_json_path = os.path.join(OUTPUT_DIR, 'szz_tse_replication_audit.json')
with open(audit_json_path, 'w', encoding='utf-8') as f:
    json.dump(mislabeled_stats, f, indent=2, ensure_ascii=False)

print("=" * 80)
print(f"[REPLICAÇÃO SZZ-TSE] Auditoria concluída em {len(files)} projetos Apache.")
print(f"Total de commits analisados: {grand_total:,}")
print("=" * 80)
print(summary_df.to_string(index=False))
print("-" * 80)
print("Ruído de Rotulagem frente ao Baseline RA-SZZ (Refactoring-Aware):")
print(f"- B-SZZ  marcou {mislabeled_stats['b2_vs_ra']['b2_total_buggy']:,} como buggy ({mislabeled_stats['b2_vs_ra']['mislabeled_as_buggy_by_b2']:,} eram falso ruído por refatoração: {mislabeled_stats['b2_vs_ra']['mislabeled_ratio']:.2%}).")
print(f"- AG-SZZ marcou {mislabeled_stats['ag_vs_ra']['ag_total_buggy']:,} como buggy ({mislabeled_stats['ag_vs_ra']['mislabeled_as_buggy_by_ag']:,} eram falso ruído por refatoração: {mislabeled_stats['ag_vs_ra']['mislabeled_ratio']:.2%}).")
print(f"- MA-SZZ marcou {mislabeled_stats['ma_vs_ra']['ma_total_buggy']:,} como buggy ({mislabeled_stats['ma_vs_ra']['mislabeled_as_buggy_by_ma']:,} eram falso ruído por refatoração: {mislabeled_stats['ma_vs_ra']['mislabeled_ratio']:.2%}).")
print(f"- RA-SZZ totalizou {mislabeled_stats['b2_vs_ra']['ra_total_buggy']:,} commits genuínos indutores de defeito.")
print(f"\nResultados persistidos em: {OUTPUT_DIR}")
print("=" * 80)
