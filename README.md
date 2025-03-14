# GFF File Generator

This script processes `.pt` files to generate GFF3 files with annotations. The input files are expected to have data blocks in groups of three lines that contain:
1. A header line (prefixed with `>`).
2. A DNA sequence line (prefixed with `$`).
3. A comma-separated list of numeric values (prefixed with `#`).

The script reads these blocks, extracts information, and creates a GFF file with:
- A sequence region declaration.
- Gene and CDS features covering the entire sequence.
- Region features for consecutive numeric values that are greater than or equal to 1.

## Features

- **Graphical Directory Selection:** Uses Tkinter to let the user choose input and output directories.
- **Automated File Processing:** Iterates over all `.pt` files in the input directory.
- **GFF3 Output:** Produces a GFF file with proper annotations for genes, CDS, and regions.

## Prerequisites

- Python 3.x
- Tkinter (usually comes with Python, but ensure it is installed for your platform)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/gff-file-generator.git
   cd gff-file-generator
