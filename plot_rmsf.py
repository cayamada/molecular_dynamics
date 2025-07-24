#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot RMSF for multiple GROMACS simulations using Seaborn.

This script reads multiple .xvg files containing RMSF data, combines them
into a single DataFrame, and plots them using seaborn with labeled curves.

Date: [2025-07-24]
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ========== USER CONFIGURATION ==========

# Folder containing the RMSF .xvg files
base_path = "../../rmsfs_500ns"  # Adjust as needed

# Expected filenames (rmsf_0.xvg, rmsf_1.xvg, ..., rmsf_4.xvg)
file_list = [os.path.join(base_path, f"rmsf_{i}.xvg") for i in range(5)]

# =========================================

def read_xvg(file_path):
    """
    Reads a GROMACS .xvg file and returns a DataFrame with columns:
    'Residue' and 'RMSF (nm)'.

    Parameters:
        file_path (str): Path to the .xvg file

    Returns:
        pd.DataFrame: DataFrame with parsed data
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Skip header lines starting with '#' or '@'
    data = [line.strip().split() for line in lines if not line.startswith(('@', '#'))]

    df = pd.DataFrame(data, columns=['Residue', 'RMSF (nm)'])
    df = df.astype(float)

    return df


# Store all dataframes
all_dfs = []

# Loop over each file, read and label it
for i, file in enumerate(file_list):
    if os.path.exists(file):
        df = read_xvg(file)
        df['Replicate'] = f'Replicate {i}'
        all_dfs.append(df)
    else:
        print(f"[Warning] File not found: {file}. Skipping...")

# Check if any data was loaded
if not all_dfs:
    raise FileNotFoundError("No RMSF files were found. Please check the path and filenames.")

# Combine all data into a single DataFrame
df_all = pd.concat(all_dfs, ignore_index=True)

# ========== PLOTTING ==========

# Use seaborn styling
sns.set(style="whitegrid")

# Create the plot
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=df_all,
    x='Residue',
    y='RMSF (nm)',
    hue='Replicate',
    palette='colorblind',
    linewidth=1
)

# Force x-axis to start at zero and end at residue 254 - depends on your protein size
plt.xlim(left=0, right=254)

# Axis labels and title
plt.title('5Y5R RMSF', fontsize=12, fontweight='bold')
plt.xlabel('Residue', labelpad=15)
plt.ylabel('RMSF (nm)', labelpad=15)

# Remove the legend title (e.g., "Replicate")
legend = plt.gca().get_legend()
if legend is not None:
    legend.set_title(None)

# Improve layout
plt.tight_layout()

# Save image as a PNG
plt.savefig('rmsf_500ns.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
