import os
import re
import sys
from pathlib import Path

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def clean_filename(filename):
    """Convert filename to a valid LaTeX filename."""
    # Remove extension and clean
    base = os.path.splitext(filename)[0]
    clean = re.sub(r'[^\w\s-]', '', base)
    clean = re.sub(r'[-\s]+', '_', clean).strip('-_')
    return clean.lower()

def create_latex_header():
    """Create LaTeX document header with necessary packages."""
    return r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}

\geometry{margin=2.5cm}
\setlength{\parindent}{0pt}
\setlength{\parskip}{1em}

\begin{document}
"""

def create_latex_footer():
    """Create LaTeX document footer."""
    return r"""
\end{document}
"""

def convert_arabic_text(text):
    """Convert Arabic text blocks to LaTeX format."""
    def replace_arabic(match):
        arabic = match.group(1)
        return f"\\begin{{arab}}\n{arabic}\n\\end{{arab}}"
    
    # Find Arabic text blocks (assuming they're between specific markers)
    text = re.sub(r'`([^`]*[\u0600-\u06FF][^`]*)`', replace_arabic, text)
    return text

def convert_markdown_to_latex(content):
    """Convert markdown content to LaTeX format."""
    # Remove backticks at start/end of lines
    content = re.sub(r'^\s*`|`\s*$', '', content, flags=re.MULTILINE)
    
    # Convert headers
    content = re.sub(r'^# (.*?)$', r'\\section{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.*?)$', r'\\subsection{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.*?)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^#### (.*?)$', r'\\paragraph{\1}', content, flags=re.MULTILINE)
    
    # Convert italic text
    content = re.sub(r'_([^_]+)_', r'\\textit{\1}', content)
    
    # Convert bold text
    content = re.sub(r'\*\*([^*]+)\*\*', r'\\textbf{\1}', content)
    
    # Convert Arabic text and transliterations
    content = convert_arabic_text(content)
    
    # Convert lists
    content = re.sub(r'^\s*- ', r'\\item ', content, flags=re.MULTILINE)
    content = re.sub(r'((?:^\s*\\item .*?\n)+)', r'\\begin{itemize}\n\1\\end{itemize}\n', content, flags=re.MULTILINE)
    
    # Handle special characters
    content = content.replace('%', '\\%')
    content = content.replace('&', '\\&')
    content = content.replace('#', '\\#')
    content = content.replace('_', '\\_')
    
    return content

def process_markdown_file(input_file, project_dir):
    """Process a single markdown file and convert it to LaTeX."""
    # Create output directories if they don't exist
    tex_dir = os.path.join(project_dir, 'TexDosyalari', 'Bolumler')
    pdf_dir = os.path.join(project_dir, 'TexDosyalari', 'PdfFiles')
    temp_dir = os.path.join(project_dir, 'TexDosyalari', 'TempFiles')
    
    for directory in [tex_dir, pdf_dir, temp_dir]:
        ensure_directory_exists(directory)
    
    # Read markdown content
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {input_file}: {e}")
        return
    
    # Convert content to LaTeX
    latex_content = convert_markdown_to_latex(content)
    
    # Create complete LaTeX document
    full_document = create_latex_header() + latex_content + create_latex_footer()
    
    # Generate output filename
    base_name = clean_filename(os.path.basename(input_file))
    tex_file = os.path.join(tex_dir, f"{base_name}.tex")
    
    # Write LaTeX file
    try:
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(full_document)
        print(f"Created LaTeX file: {tex_file}")
    except Exception as e:
        print(f"Error writing file {tex_file}: {e}")
        return
    
    return tex_file

def main():
    if len(sys.argv) != 3:
        print("Usage: python md_to_tex.py <input_markdown_file> <project_directory>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    project_dir = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist")
        sys.exit(1)
    
    tex_file = process_markdown_file(input_file, project_dir)
    if tex_file:
        print("Conversion completed successfully!")

if __name__ == "__main__":
    main()
