#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Jung Soo Kim (Arkhenomia Institute) <https://orcid.org/0009-0006-5140-0604>
# SPDX-License-Identifier: CC-BY-NC-4.0 AND LicenseRef-Arkhenomia-Governance-v2.2.0
# ==============================================================================
# Author & Institute: Jung Soo Kim (ORCID: 0009-0006-5140-0604) / Arkhenomia Institute
# License           : CC BY-NC 4.0 (Commercial licensing administered by Arkhenetics; see LICENSE.txt)
# Canonical Repo    : https://github.com/arkhenomia/arkheion
# Dataset Archive   : https://huggingface.co/datasets/arkhenomia/arkheion
# Official Websites : https://arkhenomia.org | https://arkhenetics.com
# ------------------------------------------------------------------------------
# Commercial use, corporate R&D, in-house enterprise deployment, AI knowledge
# distillation, surrogate model training, automated scraping/corpus ingestion,
# OS kernel/hardware/firmware porting (ZINN / Ark-ZPF), network state-index
# synchronization/congestion-control protocol implementation, and high-risk or
# non-peaceful applications are strictly prohibited without a separate written
# commercial license agreement executed with the Author or Arkhenetics. All
# patent rights are expressly reserved; no patent or commercial rights are
# granted by implication. Governed by the latest LICENSE.txt (Policy v2.2.0+).
# ==============================================================================

"""
2026 Grand Unified Framework - Part 1 (v1.5 Canonical Release)
Module: Source_Code_2_Figure1_Visualization.py
Reads 'Data_1_Euler_Inviscid_Limit_DNS.csv' and generates the academic plot.
"""

import pandas as pd
import matplotlib.pyplot as plt

def main():
    # 1. Load the clean CSV file directly
    file_path = 'Data_1_Euler_Inviscid_Limit_DNS.csv'
    try:
        df = pd.read_csv(file_path, comment='#')
    except FileNotFoundError:
        print(f"Error: Cannot find '{file_path}'. Please ensure the CSV file is in the same directory.")
        return

    # Rename columns for easier access
    df.columns = ['t', 'Baseline_no_TZT', 'TZT_augmented']
    
    # Ensure data is numeric
    df = df.apply(pd.to_numeric, errors='coerce').dropna()

    # 2. Extract key stats automatically
    max_baseline = df['Baseline_no_TZT'].max()
    t_max_baseline = df.loc[df['Baseline_no_TZT'].idxmax(), 't']
    
    max_tzt = df['TZT_augmented'].max()
    t_max_tzt = df.loc[df['TZT_augmented'].idxmax(), 't']
    final_tzt = df['TZT_augmented'].iloc[-1]

    # 3. Set up academic plot style
    plt.style.use('default')
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 12,
        'axes.linewidth': 1.2,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12,
        'legend.frameon': True,
        'legend.edgecolor': 'black',
        'figure.figsize': (10, 6),
        'figure.dpi': 300
    })

    fig, ax = plt.subplots()

    # 4. Plot lines
    ax.plot(df['t'], df['Baseline_no_TZT'], label='Baseline Euler (Standard NS, no TZT)', 
            color='#1f77b4', linewidth=2.5, zorder=3)
    ax.plot(df['t'], df['TZT_augmented'], label='TZT-Augmented (0-Point Core)', 
            color='#ff7f0e', linewidth=2.5, zorder=3)

    # 5. Highlight peaks with annotations
    # Baseline Peak
    ax.scatter(t_max_baseline, max_baseline, color='red', s=60, zorder=4)
    ax.annotate(f'Blow-up Peak\nMax |$\\omega$| = {max_baseline:.2f}', 
                xy=(t_max_baseline, max_baseline), xytext=(t_max_baseline-35, max_baseline-3),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5), 
                fontsize=11, fontweight='bold')

    # TZT Bounded Peak
    ax.scatter(t_max_tzt, max_tzt, color='green', s=60, zorder=4)
    ax.annotate(f'TZT Bounded Peak\nMax |$\\omega$| = {max_tzt:.2f}', 
                xy=(t_max_tzt, max_tzt), xytext=(t_max_tzt+15, max_tzt+2),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5), 
                fontsize=11, fontweight='bold')

    # 6. Grid and styling
    ax.grid(True, linestyle='--', alpha=0.6, zorder=0)
    ax.set_xlabel('Simulation Time Steps ($t$)')
    ax.set_ylabel('Maximum Vorticity ($\\max |\\omega|$)')
    ax.set_title('Geometric Cancellation of Euler Singularity via TZT Framework\n(Re=10,000, N=32 Limits)', 
                 fontweight='bold', pad=15)
    ax.legend(loc='upper left')

    # 7. Save figure and output stats
    plot_path = 'TZT_Euler_Stabilization_PRL.png'
    plt.tight_layout()
    plt.savefig(plot_path)
    
    print("=== H.U.G.G.E.R DNS Validation Stats ===")
    print(f"Max Baseline : {max_baseline:.2f} at t={t_max_baseline}")
    print(f"Max TZT      : {max_tzt:.2f} at t={t_max_tzt}")
    print(f"Final TZT    : {final_tzt:.2f} at t={df['t'].iloc[-1]}")
    print(f"Plot successfully saved to '{plot_path}'")
    
    plt.show()

if __name__ == "__main__":
    main()