import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_dir_if_not_exists(dir_path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def compile_tex_to_pdf(tex_file_path, output_dir):
    """Compile TEX file to PDF using XeLaTeX."""
    try:
        # Create output directory if it doesn't exist
        create_dir_if_not_exists(output_dir)
        
        # Get the base name of the tex file (without extension)
        base_name = os.path.splitext(os.path.basename(tex_file_path))[0]
        
        # Change to the directory containing the tex file
        os.chdir(os.path.dirname(tex_file_path))
        
        # Run xelatex twice to resolve references
        for _ in range(2):
            subprocess.run([
                'xelatex',
                '-interaction=nonstopmode',
                '-output-directory=' + output_dir,
                tex_file_path
            ], check=True)
        
        print(f"Successfully compiled {tex_file_path} to PDF")
        
    except subprocess.CalledProcessError as e:
        print(f"Error compiling {tex_file_path}: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python compile_tex_to_pdf.py <tex_file> <project_directory>")
        sys.exit(1)
    
    tex_file = sys.argv[1]
    project_dir = sys.argv[2]
    
    if not os.path.exists(tex_file):
        print(f"Error: LaTeX file {tex_file} does not exist")
        sys.exit(1)
    
    compile_tex_to_pdf(tex_file, project_dir)

if __name__ == "__main__":
    main()
