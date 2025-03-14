import os
import tkinter as tk
from tkinter import filedialog

def create_gff_from_file(file_path: str, output_directory: str) -> None:
    """
    Process a .pt file to generate a GFF file with gene, CDS, and region annotations.
    
    The input file is expected to be formatted in blocks of three lines:
      1. Header line starting with '>' (e.g., ">chromosome1")
      2. DNA sequence line starting with '$' (e.g., "$ACTG...")
      3. Comma-separated values line starting with '#' (e.g., "#0,1,1,0,...")
    
    The function extracts the header, DNA sequence, and region information, then writes
    the annotations in GFF3 format to an output file in the given directory.
    
    Args:
        file_path (str): Full path to the input file.
        output_directory (str): Directory where the output GFF file will be saved.
    """
    print(f"Processing file: {file_path}")
    
    # Read the entire content of the file
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    # Split the content into lines
    lines = file_content.split('\n')
    
    # Initialize the GFF content with the header specifying GFF version 3
    gff_content = "##gff-version 3\n"
    
    # Process lines in groups of three
    for i in range(0, len(lines), 3):
        # Ensure there are at least three lines in the current block
        if i + 2 < len(lines):
            # Extract and clean the header, DNA sequence, and comma-separated region values
            header = lines[i].strip().lstrip('>')
            dna_sequence = lines[i+1].strip().lstrip('$')
            comma_values = lines[i+2].strip().lstrip('#').split(',')
            
            # Add sequence region information to the GFF content
            seq_length = len(dna_sequence)
            gff_content += f"##sequence-region {header} 1 {seq_length}\n"
            
            # Add gene and CDS features covering the whole sequence
            gene_id = f"gene{i//3}"
            cds_id = f"cds{i//3}"
            gff_content += (
                f"{header}\t.\tgene\t1\t{seq_length}\t.\t+\t.\tID={gene_id};Name=ExampleGene\n"
            )
            gff_content += (
                f"{header}\t.\tCDS\t1\t{seq_length}\t.\t+\t0\tID={cds_id};Parent={gene_id};Name=ExampleCDS\n"
            )
            
            # Detect regions with consecutive values >= 1 from the comma-separated values
            start = None
            end = None
            for j, value in enumerate(comma_values):
                try:
                    # Convert value to integer for comparison
                    int_value = int(value)
                except ValueError:
                    # If conversion fails, skip this value
                    continue

                if int_value >= 1:
                    # Start a new region if not already started
                    if start is None:
                        start = j + 1  # converting to 1-indexed position
                    end = j + 1
                else:
                    # When a region ends, if a region was active, output it
                    if start is not None:
                        gff_content += (
                            f"{header}\t.\tregion\t{start}\t{end}\t.\t+\t.\t"
                            f"ID=region{start};Name=Region{start};color=0,0,255\n"
                        )
                        start = None
                        end = None
            
            # If the file ends with an active region, add it
            if start is not None:
                gff_content += (
                    f"{header}\t.\tregion\t{start}\t{end}\t.\t+\t.\t"
                    f"ID=region{start};Name=Region{start};color=0,0,255\n"
                )
    
    # Construct the output file path by replacing the .pt extension with a descriptive suffix
    output_file_name = os.path.basename(file_path).replace('.pt', '_with_consecutive_regions.gff')
    output_file_path = os.path.join(output_directory, output_file_name)
    
    # Write the generated GFF content to the output file
    with open(output_file_path, 'w') as gff_file:
        gff_file.write(gff_content)
    
    print(f"The GFF file has been created successfully: {output_file_path}")

def select_directory(prompt: str) -> str:
    """
    Open a dialog for the user to select a directory.
    
    Args:
        prompt (str): The title message for the directory selection dialog.
    
    Returns:
        str: The path of the selected directory.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    directory_path = filedialog.askdirectory(title=prompt)
    return directory_path

def main():
    """
    Main function to handle directory selection and file processing.
    
    It prompts the user to select the input and output directories,
    then processes all .pt files found in the input directory.
    """
    # Get user input for directories via file dialog
    input_directory_path = select_directory("Select the input directory")
    output_directory_path = select_directory("Select the output directory")
    
    print(f"Input directory: {input_directory_path}")
    print(f"Output directory: {output_directory_path}")
    
    # Loop through files in the input directory, processing those ending with .pt
    for filename in os.listdir(input_directory_path):
        if filename.endswith('.pt'):
            print(f"Found file: {filename}")
            create_gff_from_file(os.path.join(input_directory_path, filename), output_directory_path)

if __name__ == "__main__":
    main()
