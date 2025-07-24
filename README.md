# molecular_dynamics
Python scripts for analyzing Molecular Dynamics (MD) simulations using GROMACS output: RMSD, RMSF (full and region-specific), and ChimeraX visualization attributes.

# MD Analysis Scripts (GROMACS + ChimeraX)

This repository contains Python scripts to assist in the post-processing and visualization of Molecular Dynamics (MD) simulations performed with **GROMACS**. These tools are tailored to compute and plot **RMSD**, **RMSF**, extract **region-specific RMSF**, and convert RMSF data to ChimeraX-compatible `.defattr` files for structure coloring.

## Features

- **RMSD Plotting**: Parse and plot RMSD from `.xvg` files.
- **RMSF Plotting**: Visualize full RMSF profiles from trajectory analysis.
- **Region-Specific RMSF**: Extract and plot RMSF values for selected residue ranges.
- **ChimeraX Attribute Files**: Convert RMSF values into `.defattr` files for coloring molecular structures by flexibility.

---

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `plot_rmsd.py` | Plot RMSD over time from a GROMACS `.xvg` file. |
| `plot_rmsf.py` | Plot RMSF for the entire protein based on residue data. |
| `plot_rmsf_region.py` | Extract and plot RMSF values for a specific residue range. |
| `xvg_to_defattr.py` | Convert RMSF `.xvg` files to ChimeraX `.defattr` format. |

---

## Requirements

These scripts require Python 3 and the following packages:

```bash
matplotlib
pandas
seaborn
````
---

## ChimeraX
ChimeraX .defattr files can be loaded with:

````
open structure.pdb
open "C:/path/to/rmsf_0.defattr"
cartoon byattribute rmsf_value
color byattribute rmsf_value palette white:red
````

