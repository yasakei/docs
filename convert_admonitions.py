#!/usr/bin/env python3
"""
Preprocess markdown files to convert GitHub-style admonitions to Material format.
Run this before mkdocs build.
"""

import os
import re
import sys

# GitHub admonition pattern
GITHUB_ADMONITION_RE = re.compile(
    r'^(\s*)>\s*\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)\]\s*$',
    re.IGNORECASE
)

# Map GitHub types to Material types
TYPE_MAP = {
    'NOTE': 'note',
    'TIP': 'tip',
    'WARNING': 'warning',
    'CAUTION': 'danger',
    'IMPORTANT': 'warning',
}

def process_file(filepath):
    """Convert GitHub admonitions in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        match = GITHUB_ADMONITION_RE.match(line)
        
        if match:
            admonition_type = TYPE_MAP.get(match.group(2).upper(), 'note')
            indent = match.group(1)
            
            # Add admonition start
            new_lines.append(f'{indent}!!! {admonition_type}')
            
            # Process following lines that are part of the blockquote
            i += 1
            first_content = True
            while i < len(lines) and lines[i].startswith('>'):
                content_line = lines[i][1:] if lines[i].startswith('>') else lines[i]
                if content_line and not GITHUB_ADMONITION_RE.match(lines[i]):
                    if first_content:
                        new_lines.append(f'{indent}    {content_line.strip()}')
                        first_content = False
                    else:
                        new_lines.append(f'{indent}    {content_line.strip()}')
                elif GITHUB_ADMONITION_RE.match(lines[i]):
                    # Nested admonition - go back and process it
                    i -= 1
                    break
                i += 1
            continue
        else:
            new_lines.append(line)
        
        i += 1
    
    new_content = '\n'.join(new_lines)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Converted: {filepath}")
        return True
    return False

def main():
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else 'docs'
    count = 0
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    count += 1
    
    print(f"Processed {count} files with GitHub admonitions")

if __name__ == '__main__':
    main()
