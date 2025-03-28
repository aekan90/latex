import os
import re
import sys
from pathlib import Path

def tr_to_eng(text):
    """Convert Turkish characters to their ASCII equivalents."""
    tr_chars = {
        'ç': 'c', 'Ç': 'C',
        'ğ': 'g', 'Ğ': 'G',
        'ı': 'i', 'İ': 'I',
        'ö': 'o', 'Ö': 'O',
        'ş': 's', 'Ş': 'S',
        'ü': 'u', 'Ü': 'U',
    }
    for tr_char, eng_char in tr_chars.items():
        text = text.replace(tr_char, eng_char)
    return text

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def clean_filename(title):
    """Convert title to a valid filename."""
    # Convert Turkish characters to ASCII
    title = tr_to_eng(title)
    # Remove backticks and convert to lowercase
    title = title.replace('`', '').lower()
    # Remove special characters and replace spaces with underscores
    title = re.sub(r'[^\w\s-]', '', title)
    title = re.sub(r'[-\s]+', '_', title).strip('-_')
    return title

def split_markdown_file(input_file, output_dir):
    """Split markdown file into sections based on top-level headers."""
    ensure_directory_exists(output_dir)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {input_file}: {e}")
        return

    # Remove backticks at the start of lines
    content = re.sub(r'^\s*`', '', content, flags=re.MULTILINE)
    content = re.sub(r'`\s*$', '', content, flags=re.MULTILINE)
    
    # Split content by top-level headers
    sections = re.split(r'(?=^# )', content, flags=re.MULTILINE)
    
    # Remove empty sections
    sections = [s.strip() for s in sections if s.strip()]
    
    for i, section in enumerate(sections, 1):
        # Extract section title
        title_match = re.match(r'^# (.*?)(?:\n|$)', section)
        if title_match:
            title = title_match.group(1).strip()
            # Remove any remaining backticks from title
            title = title.replace('`', '')
        else:
            title = f"section_{i}"
        
        # Create filename
        filename = f"{i:02d}_{clean_filename(title)}.md"
        output_path = os.path.join(output_dir, filename)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(section.strip() + '\n')
            print(f"Created {filename}")
        except Exception as e:
            print(f"Error writing file {filename}: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python split_file.py <input_markdown_file> <output_directory>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist")
        sys.exit(1)
    
    split_markdown_file(input_file, output_dir)
    print("File splitting completed successfully!")

if __name__ == "__main__":
    main()
