"""
Utility functions for LaTeX to Notion conversion.
"""

from typing import Optional


def escape_markdown(text: str) -> str:
    """
    Escape special markdown characters.
    
    Args:
        text: Text to escape
        
    Returns:
        Escaped text
    """
    # Characters that need escaping in markdown
    special_chars = ['*', '_', '`', '[', ']', '(', ')', '#', '+', '-', '.', '!']
    result = text
    for char in special_chars:
        result = result.replace(char, f'\\{char}')
    return result


def clean_latex_text(text: str) -> str:
    """
    Clean LaTeX text by removing common artifacts.
    
    Args:
        text: LaTeX text to clean
        
    Returns:
        Cleaned text
    """
    # Remove LaTeX line breaks that are just spacing
    text = text.replace('\\\\', '\n')
    # Remove excessive whitespace
    text = ' '.join(text.split())
    return text
