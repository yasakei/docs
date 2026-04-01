"""
Custom Markdown extension to support GitHub-style admonitions.
Converts >[!TYPE] syntax to standard admonition syntax.
"""

import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class GitHubAdmonitionPreprocessor(Preprocessor):
    """Convert GitHub-style admonitions to standard admonition syntax."""
    
    # Pattern to match GitHub-style admonitions
    GITHUB_ADMONITION_RE = re.compile(
        r'^(\s*)>\s*\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT|NOTE)\]\s*(.*)$',
        re.IGNORECASE | re.MULTILINE
    )
    
    # Map GitHub types to standard admonition types
    TYPE_MAP = {
        'note': 'note',
        'tip': 'tip', 
        'warning': 'warning',
        'caution': 'danger',
        'important': 'warning',
    }
    
    def run(self, lines):
        new_lines = []
        in_admonition = False
        admonition_type = 'note'
        
        for line in lines:
            match = self.GITHUB_ADMONITION_RE.match(line)
            if match:
                indent = match.group(1)
                admonition_type = self.TYPE_MAP.get(match.group(2).lower(), 'note')
                content = match.group(3).strip()
                
                # Start admonition
                new_lines.append(f"{indent}!!! {admonition_type}")
                if content:
                    new_lines.append(f"{indent}    {content}")
                in_admonition = True
            elif in_admonition and line.startswith('>'):
                # Continue admonition content
                content = line[1:].strip()
                if content:
                    new_lines.append(f"    {content}")
            else:
                in_admonition = False
                new_lines.append(line)
        
        return new_lines


class GitHubAdmonitionExtension(Extension):
    """GitHub-style admonition extension."""
    
    def extendMarkdown(self, md):
        md.preprocessors.register(
            GitHubAdmonitionPreprocessor(md), 
            'github_admonition', 
            105
        )


def makeExtension(**kwargs):
    return GitHubAdmonitionExtension(**kwargs)
