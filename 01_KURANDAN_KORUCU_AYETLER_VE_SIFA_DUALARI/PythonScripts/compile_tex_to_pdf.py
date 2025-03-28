import os
import sys
import shutil
import subprocess
from pathlib import Path

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def compile_latex_to_pdf(tex_file, project_dir):
    """Compile LaTeX file to PDF using xelatex."""
    # Convert paths to absolute paths
    tex_file = os.path.abspath(tex_file)
    project_dir = os.path.abspath(project_dir)
    
    # Get directories
    tex_dir = os.path.dirname(tex_file)
    pdf_dir = os.path.join(project_dir, 'TexDosyalari', 'PdfFiles')
    temp_dir = os.path.join(project_dir, 'TexDosyalari', 'TempFiles')
    
    # Ensure directories exist
    for directory in [pdf_dir, temp_dir]:
        ensure_directory_exists(directory)
    
    # Get base name without extension
    base_name = os.path.splitext(os.path.basename(tex_file))[0]
    
    try:
        # Run xelatex twice to resolve references
        for _ in range(2):
            result = subprocess.run([
                'xelatex',
                '-interaction=nonstopmode',
                f'-output-directory={temp_dir}',
                tex_file
            ], capture_output=True, text=True, cwd=tex_dir)
            
            if result.returncode != 0:
                print("Error during LaTeX compilation:")
                print(result.stdout)
                print(result.stderr)
                return False
        
        # Move PDF to output directory
        pdf_file = os.path.join(temp_dir, f"{base_name}.pdf")
        if os.path.exists(pdf_file):
            output_pdf = os.path.join(pdf_dir, f"{base_name}.pdf")
            shutil.move(pdf_file, output_pdf)
            print(f"Created PDF file: {output_pdf}")
        else:
            print("PDF file was not created")
            return False
        
        # Clean up temporary files
        for ext in ['.aux', '.log', '.out', '.toc']:
            temp_file = os.path.join(temp_dir, base_name + ext)
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        return True
        
    except Exception as e:
        print(f"Error during compilation: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python compile_tex_to_pdf.py <tex_file> <project_directory>")
        sys.exit(1)
    
    tex_file = sys.argv[1]
    project_dir = sys.argv[2]
    
    if not os.path.exists(tex_file):
        print(f"Error: LaTeX file {tex_file} does not exist")
        sys.exit(1)
    
    success = compile_latex_to_pdf(tex_file, project_dir)
    if success:
        print("PDF compilation completed successfully!")
    else:
        print("PDF compilation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
