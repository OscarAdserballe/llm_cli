#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import shutil

def create_latex_template(args):
    filename = args.filename.replace('.tex', '')
    
    script_dir = Path(__file__).parent.absolute()
    template_path = script_dir / 'template.tex'
    
    output_filename = f"{filename}.tex"
    
    # Check if file already exists and handle force flag
    if os.path.exists(output_filename):
        response = input(f"File {output_filename} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return
    
    try:
        # copy the template file
        shutil.copy2(template_path, output_filename)
        print(f"Successfully created {output_filename}")
        
        # Create figures directory if specified
        figures_dir = 'figures'
        if not os.path.exists(figures_dir):
            os.makedirs(figures_dir)
            print(f"Created {figures_dir}/ directory for your figures")
        
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
        print("Please ensure template.tex exists in the same directory as this script")
    except Exception as e:
        print(f"Error creating file: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Generate a LaTeX template file',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument('filename', help='Name of the LaTeX file to create')
    
    args = parser.parse_args()
    create_latex_template(args)

if __name__ == "__main__":
    main()