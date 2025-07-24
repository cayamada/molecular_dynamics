#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot RMSF for a specific residue region from multiple GROMACS simulations.

This script reads .xvg files with RMSF data, selects a specific residue
range (e.g., 100–150), and plots it using Seaborn.

Date: [2025-07-24]
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ========== USER CONFIGURATION ==========

# Folder containing the RMSF .xvg files
base_path = "../../rmsfs_500ns"  # Adjust this as needed

# Expected filenames (rmsf_0.xvg, rmsf_1.xvg, ..., rmsf_4.xvg)
file_list = [os.path.join(base_path, f"rmsf_{i}.xvg") for i in range(6)]

# Residue range to plot
res_start = 100
res_end = 150

# ========== FUNCTION ==========

def read_xvg(file_path):
    """
    Reads a GROMACS .xvg file and returns a DataFrame with columns:
    'Residue' and 'RMSF (nm)'.

    Parameters:
        file_path (str): Path to the .xvg file

    Returns:
        pd.DataFrame: Parsed data
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Skip lines starting with '#' or '@'
    data = [line.strip().split() for line in lines if not line.startswith(('@', '#'))]

    df = pd.DataFrame(data, columns=['Residue', 'RMSF (nm)'])
    df = df.astype(float)
    return df

# ========== DATA LOADING ==========

all_dfs = []

for i, file in enumerate(file_list):
    if os.path.exists(file):
        df = read_xvg(file)
        df['Replicate'] = f'Replicate {i}'
        all_dfs.append(df)
    else:
        print(f"[Warning] File not found: {file}. Skipping...")

if not all_dfs:
    raise FileNotFoundError("No RMSF files found.")

# Combine and filter the DataFrame by residue range
df_all = pd.concat(all_dfs, ignore_index=True)
df_all['Residue'] = df_all['Residue'].astype(float)
df_all = df_all[(df_all['Residue'] >= res_start) & (df_all['Residue'] <= res_end)]

# ========== PLOTTING ==========

sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=df_all,
    x='Residue',
    y='RMSF (nm)',
    hue='Replicate',
    palette='colorblind',
    linewidth=1
)

plt.title(f'5Y5R RMSF, Residues {res_start}-{res_end}', fontsize=12, fontweight='bold')
plt.xlabel('Residue', labelpad=15)
plt.ylabel('RMSF (nm)', labelpad=15)

ax = plt.gca()

# Set major ticks every 5 residues
ax.set_xticks(range(int(res_start), int(res_end) + 1, 5))

# Minor ticks every 1 residue (no labels)
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.tick_params(axis='x', which='minor', length=3, color='gray', labelsize=0)
ax.grid(True, which='minor', linestyle=':', linewidth=0.5, color='lightgray')

legend = ax.get_legend()
if legend is not None:
    legend.set_title(None)

plt.tight_layout()
plt.savefig(f"rmsf_region_{res_start}_{res_end}.png", dpi=300, bbox_inches='tight')
plt.show()
