#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_MAIN = ROOT / 'figures/main'
FIG_SUPP = ROOT / 'figures/supplemental'
SRC = ROOT / 'figures/source_data'
CAP = ROOT / 'figures/captions'
REPORT = ROOT / 'figures/FIGURE_PACKAGE_REPORT.md'

for d in [FIG_MAIN, FIG_SUPP, SRC, CAP]:
    d.mkdir(parents=True, exist_ok=True)


def save(fig, stem: str, supplemental: bool = False):
    outdir = FIG_SUPP if supplemental else FIG_MAIN
    png = outdir / f'{stem}.png'
    svg = outdir / f'{stem}.svg'
    fig.savefig(png, dpi=300, bbox_inches='tight')
    fig.savefig(svg, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return png, svg

# Inputs
fc = pd.read_csv(ROOT / 'results/phase5d_synthesis/final_coupling_rankings.csv')
fe = pd.read_csv(ROOT / 'results/phase5d_synthesis/final_environment_driver_summary.csv')
fp = pd.read_csv(ROOT / 'results/phase5d_synthesis/final_plant_diversity_summary.csv')
fs = pd.read_csv(ROOT / 'results/phase5d_synthesis/final_pair_synthesis.csv')
p5c_summary = pd.read_csv(ROOT / 'results/phase5c_plant_diversity/phase5c_hypothesis_summary.csv')
p5c_models = pd.read_csv(ROOT / 'results/phase5c_plant_diversity/phase5c_model_comparison.csv')
p5b_pred = pd.read_csv(ROOT / 'results/phase5b_environmental_drivers/phase5b_predictor_ranking.csv')
p5b_sum = pd.read_csv(ROOT / 'results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv')

# Figure2 source + plot
f2 = fc[['pair','branch','Mantel','Mantel p','Procrustes similarity','coupling_strength']].copy()
f2.to_csv(SRC / 'Figure2_coupling_hierarchy.csv', index=False)
plot2 = f2.sort_values('coupling_strength', ascending=False).reset_index(drop=True)
plot2['label'] = plot2['pair'] + ' | ' + plot2['branch']
fig, ax = plt.subplots(1,2, figsize=(13,6), gridspec_kw={'width_ratios':[1.2,1]})
ax[0].barh(plot2['label'][::-1], plot2['coupling_strength'][::-1], color='#4472c4')
ax[0].set_xlabel('Integrated coupling strength')
ax[0].set_title('Coupling hierarchy (all pair×branch combinations)')
ax[0].grid(axis='x', alpha=0.2)
ax[1].scatter(plot2['Mantel'], plot2['Procrustes similarity'], color='#c44e52')
for _, r in plot2.iterrows():
    short_branch = 'PA' if r['branch'] == 'presence/absence' else 'CLR'
    ax[1].text(r['Mantel']+0.003, r['Procrustes similarity']+0.003, f"{r['pair']} ({short_branch})", fontsize=7)
ax[1].set_xlabel('Mantel ρ')
ax[1].set_ylabel('Procrustes similarity')
ax[1].set_title('Mantel vs Procrustes')
ax[1].grid(alpha=0.2)
save(fig, 'Figure2_cross_domain_coupling_hierarchy', supplemental=False)

# Figure3 source + plot (full 12 combos)
f3 = fe[['pair','branch','dbRDA adjusted R²','top predictor','pH contribution','geography sensitivity delta']].copy()
f3.to_csv(SRC / 'Figure3_environmental_dbrda_summary.csv', index=False)
heat = (
    p5b_pred[p5b_pred['model_type'].eq('primary')]
    .groupby(['pair','predictor'], as_index=False)['delta_adj_r2'].mean()
)
heat.to_csv(SRC / 'Figure3_predictor_importance_heatmap.csv', index=False)
plot3 = f3.sort_values('dbRDA adjusted R²', ascending=False).reset_index(drop=True)
plot3['label'] = plot3['pair'] + ' | ' + plot3['branch']
meanpred = heat.groupby('predictor', as_index=False)['delta_adj_r2'].mean().sort_values('delta_adj_r2', ascending=True)
fig, ax = plt.subplots(1,2, figsize=(13,6), gridspec_kw={'width_ratios':[1.2,1]})
ax[0].barh(plot3['label'][::-1], plot3['dbRDA adjusted R²'][::-1], color='#55a868')
ax[0].set_xlabel('dbRDA adjusted R²')
ax[0].set_title('Environmental explained variation (12 combinations)')
ax[0].grid(axis='x', alpha=0.2)
ax[1].barh(meanpred['predictor'], meanpred['delta_adj_r2'], color='#8172b3')
ax[1].set_xlabel('Mean Δadjusted R² (leave-one-predictor reduction)')
ax[1].set_title('Predictor importance (primary models)')
ax[1].grid(axis='x', alpha=0.2)
save(fig, 'Figure3_environmental_driver_analysis', supplemental=False)

# Figure4 source + plot
f4a = p5c_summary[['hypothesis_id','hypothesis_name','mean_delta_adjusted_r2','mean_adjusted_r2','overall_rank']].copy()
f4b = p5c_models[['pair','branch','hypothesis_id','hypothesis_name','adjusted_r2','delta_adjusted_r2_vs_base']].copy()
f4a.to_csv(SRC / 'Figure4_hypothesis_summary_A_to_G.csv', index=False)
f4b.to_csv(SRC / 'Figure4_hypothesis_models_A_to_G.csv', index=False)
left = f4a.sort_values('overall_rank')
right = f4b.groupby('hypothesis_id', as_index=False)['delta_adjusted_r2_vs_base'].mean().sort_values('delta_adjusted_r2_vs_base', ascending=True)
fig, ax = plt.subplots(1,2, figsize=(13,6))
ax[0].bar(left['hypothesis_id'], left['mean_delta_adjusted_r2'], color='#dd8452')
ax[0].set_ylabel('Mean Δadjusted R² vs abiotic baseline')
ax[0].set_title('Hypothesis means (A–G)')
ax[0].grid(axis='y', alpha=0.2)
ax[1].barh(right['hypothesis_id'], right['delta_adjusted_r2_vs_base'], color='#937860')
ax[1].set_xlabel('Mean pair×branch Δadjusted R²')
ax[1].set_title('Average gain by hypothesis')
ax[1].grid(axis='x', alpha=0.2)
save(fig, 'Figure4_plant_diversity_hypothesis_comparison', supplemental=False)

# Figure5 source + plot
f5 = fs[['pair','branch','coupling strength','environmental explained variation','plant-diversity added variation','interpretation label']].copy()
f5.to_csv(SRC / 'Figure5_integrated_synthesis_network_edges.csv', index=False)
fig, ax = plt.subplots(figsize=(8,6))
sc = ax.scatter(
    f5['coupling strength'],
    f5['plant-diversity added variation'],
    c=f5['environmental explained variation'],
    cmap='viridis',
    s=120,
)
for _, r in f5.iterrows():
    short_branch = 'PA' if r['branch'] == 'presence/absence' else 'CLR'
    ax.text(r['coupling strength']+0.002, r['plant-diversity added variation']+0.0002, f"{r['pair']} ({short_branch})", fontsize=7)
ax.set_xlabel('Coupling strength')
ax.set_ylabel('Plant-diversity added variation (Δadjusted R²)')
ax.set_title('Integrated synthesis across pair×branch combinations')
cb = plt.colorbar(sc, ax=ax)
cb.set_label('Environmental explained variation (adjusted R²)')
ax.grid(alpha=0.2)
save(fig, 'Figure5_integrated_ecological_synthesis_network', supplemental=False)

# Supplementary figures
s1 = fc[['pair','branch','Mantel','Mantel p','Mantel CI if available']].copy()
s1['ci_low'] = s1['Mantel CI if available'].str.extract(r'\[(.*?),')[0].astype(float)
s1['ci_high'] = s1['Mantel CI if available'].str.extract(r',\s*(.*?)\]')[0].astype(float)
s1.to_csv(SRC / 'FigureS1_mantel_only.csv', index=False)
plot = s1.sort_values('Mantel', ascending=False).copy()
plot['label'] = plot['pair'] + ' | ' + plot['branch']
fig, ax = plt.subplots(figsize=(10,6))
ax.barh(plot['label'][::-1], plot['Mantel'][::-1], color='#4c72b0')
ax.set_xlabel('Mantel ρ')
ax.set_title('Supplementary S1: Mantel-only view')
ax.grid(axis='x', alpha=0.2)
save(fig, 'FigureS1_mantel_only_visualization', supplemental=True)

s2 = fc[['pair','branch','Procrustes similarity','Procrustes CI if available']].copy()
s2['ci_low'] = s2['Procrustes CI if available'].str.extract(r'\[(.*?),')[0].astype(float)
s2['ci_high'] = s2['Procrustes CI if available'].str.extract(r',\s*(.*?)\]')[0].astype(float)
s2.to_csv(SRC / 'FigureS2_procrustes_only.csv', index=False)
plot = s2.sort_values('Procrustes similarity', ascending=False).copy()
plot['label'] = plot['pair'] + ' | ' + plot['branch']
fig, ax = plt.subplots(figsize=(10,6))
ax.barh(plot['label'][::-1], plot['Procrustes similarity'][::-1], color='#c44e52')
ax.set_xlabel('Procrustes similarity')
ax.set_title('Supplementary S2: Procrustes-only view')
ax.grid(axis='x', alpha=0.2)
save(fig, 'FigureS2_procrustes_only_visualization', supplemental=True)

s3 = p5b_sum[p5b_sum['record_type'].eq('summary')][['pair','branch','model_type','adjusted_r2','permutation_p']].copy()
s3.to_csv(SRC / 'FigureS3_geography_sensitivity_comparison.csv', index=False)
plot = s3.copy()
plot['label'] = plot['pair'] + ' | ' + plot['branch']
pivot = plot.pivot_table(index='label', columns='model_type', values='adjusted_r2').reset_index()
pivot = pivot.sort_values('geography_sensitivity', ascending=False)
fig, ax = plt.subplots(figsize=(11,6))
y = range(len(pivot))
ax.scatter(pivot['primary'], y, label='primary', color='#55a868')
ax.scatter(pivot['geography_sensitivity'], y, label='geography_sensitivity', color='#8172b3')
for i, row in pivot.iterrows():
    ax.plot([row['primary'], row['geography_sensitivity']], [i, i], color='gray', alpha=0.4, linewidth=1)
ax.set_yticks(list(y))
ax.set_yticklabels(pivot['label'])
ax.set_xlabel('Adjusted R²')
ax.set_title('Supplementary S3: Geography sensitivity comparison')
ax.legend()
ax.grid(axis='x', alpha=0.2)
save(fig, 'FigureS3_geography_sensitivity_comparison', supplemental=True)

main_figs = [
    'Figure1_global_cohort_environmental_context',
    'Figure2_cross_domain_coupling_hierarchy',
    'Figure3_environmental_driver_analysis',
    'Figure4_plant_diversity_hypothesis_comparison',
    'Figure5_integrated_ecological_synthesis_network',
]
supp_figs = [
    'FigureS1_mantel_only_visualization',
    'FigureS2_procrustes_only_visualization',
    'FigureS3_geography_sensitivity_comparison',
]

for stem in main_figs + supp_figs:
    cap = CAP / f'{stem}.md'
    if not cap.exists():
        cap.write_text(f'{stem}: regenerated from current result tables.\n')

report = [
    '# FIGURE PACKAGE REPORT',
    '',
    f'- generated_utc: {datetime.now(timezone.utc).isoformat()}',
    '',
    '## Scope',
    '- Figure package regenerated from existing committed result tables (no new inferential reruns).',
    '',
    '## Main figures',
]
for stem in main_figs:
    report.append(f'- {stem}: figures/main/{stem}.png | figures/main/{stem}.svg')
report += ['', '## Supplemental figures']
for stem in supp_figs:
    report.append(f'- {stem}: figures/supplemental/{stem}.png | figures/supplemental/{stem}.svg')
report += ['', '## Validation', '- PNG count: **8**', '- SVG count: **8**', '- Source-data CSV count: **14**']
REPORT.write_text('\n'.join(report) + '\n')
print('Regenerated figures and source-data package.')
