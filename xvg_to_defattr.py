import os

# ================= USER CONFIGURATION =================
base_path = "../../rmsfs_500ns"  # Directory where your RMSF .xvg files are located
chain_id = "A"                   # Chain ID (not used in .defattr files but useful if needed)
file_list = [os.path.join(base_path, f"rmsf_{i}.xvg") for i in range(5)]
# ======================================================

def parse_xvg(file_path):
    """
    Parse a GROMACS RMSF .xvg file, skipping header lines and extracting residue numbers and RMSF values.
    
    Parameters:
        file_path (str): Path to the .xvg file to be parsed.
        
    Returns:
        residues (list of int): List of residue indices.
        values (list of float): List of RMSF values corresponding to residues.
    """
    residues = []
    values = []
    with open(file_path, 'r') as f:
        for line in f:
            # Skip lines starting with '#' or '@' (GROMACS metadata lines)
            if line.startswith(('@', '#')):
                continue
            parts = line.strip().split()
            # Ensure line has at least two columns (residue index and RMSF value)
            if len(parts) >= 2:
                residues.append(int(float(parts[0])))  # Convert residue number to int
                values.append(float(parts[1]))          # Convert RMSF value to float
    return residues, values

def write_defattr(residues, values, output_path):
    """
    Write a ChimeraX .defattr attribute file using the residue numbers and RMSF values.
    This format is compatible with ChimeraX's new 'open' command for attributes.
    
    Parameters:
        residues (list of int): List of residue indices.
        values (list of float): List of RMSF values.
        output_path (str): Path where the .defattr file will be saved.
    """
    with open(output_path, 'w') as f:
        # Write the attribute header
        f.write("attribute: rmsf_value\n")
        f.write("recipient: residues\n")
        # Write each residue number and its RMSF value line by line
        for r, v in zip(residues, values):
            f.write(f"\t:{r}\t{v:.4f}\n")  # Format values with 4 decimal places
    print(f"[OK] Written: {output_path}")

# ================= MAIN PROCESSING LOOP =================
for xvg_file in file_list:
    # Check if the .xvg file exists before processing
    if os.path.exists(xvg_file):
        # Define the output filename by replacing .xvg extension with .defattr
        output_file = os.path.splitext(xvg_file)[0] + ".defattr"
        # Parse the input .xvg file
        residues, values = parse_xvg(xvg_file)
        # Write the parsed data to a .defattr ChimeraX attribute file
        write_defattr(residues, values, output_file)
    else:
        print(f"[Warning] File not found: {xvg_file}")
