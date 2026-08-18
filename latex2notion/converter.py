"""
Main Converter

Orchestrates the conversion from LaTeX AST to Notion format.
"""

from typing import Optional
from latex2notion.parser import LaTeXParser, ASTNode, NodeType
from latex2notion.handlers.math_handler import MathHandler
from latex2notion.handlers.block_handler import BlockHandler
from latex2notion.handlers.inline_handler import InlineHandler
from latex2notion.handlers.table_handler import TableHandler
from latex2notion.handlers.list_handler import ListHandler


def convert(latex_string: str, math_mode: str = 'katex', 
            heading_level_offset: int = 0, preserve_comments: bool = False) -> str:
    """
    Convert LaTeX string to Notion-compatible format.
    
    Args:
        latex_string: The LaTeX source text
        math_mode: Math rendering mode (default: 'katex' for Notion compatibility)
        heading_level_offset: Offset to adjust heading levels (default: 0)
        preserve_comments: Whether to preserve LaTeX comments (default: False)
        
    Returns:
        Notion-compatible text that can be pasted into Notion
    """
    # Remove comments if not preserving
    if not preserve_comments:
        import re
        latex_string = re.sub(r'%.*$', '', latex_string, flags=re.MULTILINE)
    
    # Parse LaTeX
    parser = LaTeXParser()
    ast = parser.parse(latex_string)
    
    # Convert AST to Notion format
    converter = NotionConverter(
        math_mode=math_mode,
        heading_level_offset=heading_level_offset
    )
    
    return converter.convert(ast)


class NotionConverter:
    """Converts LaTeX AST to Notion format."""
    
    def __init__(self, math_mode: str = 'katex', heading_level_offset: int = 0):
        self.math_mode = math_mode
        self.heading_level_offset = heading_level_offset
        self.math_handler = MathHandler()
        self.block_handler = BlockHandler()
        self.inline_handler = InlineHandler()
        self.table_handler = TableHandler()
        self.list_handler = ListHandler()
    
    def convert(self, ast: ASTNode) -> str:
        """Convert AST to Notion format."""
        if ast.node_type != NodeType.DOCUMENT:
            return ""
        
        blocks = []
        for child in ast.children:
            block = self._convert_node(child)
            if block:
                blocks.append(block)
        
        return '\n\n'.join(blocks)
    
    def _convert_node(self, node: ASTNode) -> str:
        """Convert a single AST node to Notion format."""
        # Headings
        if self.block_handler.is_heading(node):
            heading = self.block_handler.convert_heading(node)
            # Apply heading level offset
            if self.heading_level_offset != 0:
                heading = self._adjust_heading_level(heading, self.heading_level_offset)
            return heading
        
        # Lists
        if self.list_handler.is_list_node(node):
            return self.list_handler.convert(node)
        
        # Tables
        if self.table_handler.is_table_node(node):
            return self.table_handler.convert(node)
        
        # Block environments
        if self.block_handler.is_block_environment(node):
            if node.node_type == NodeType.QUOTE:
                return self.block_handler.convert_quote(node)
            elif node.node_type in [NodeType.VERBATIM, NodeType.CODE_BLOCK]:
                return self.block_handler.convert_code_block(node)
        
        # Paragraphs
        if node.node_type == NodeType.PARAGRAPH:
            return self.block_handler.convert_paragraph(node, self.inline_handler)
        
        # Math (standalone)
        if self.math_handler.is_math_node(node):
            return self.math_handler.convert(node)
        
        # Default: return empty string
        return ""
    
    def _adjust_heading_level(self, heading: str, offset: int) -> str:
        """Adjust heading level by offset."""
        if not heading.startswith('#'):
            return heading
        
        # Count current level
        level = 0
        for char in heading:
            if char == '#':
                level += 1
            else:
                break
        
        # Apply offset
        new_level = max(1, min(6, level + offset))
        rest = heading[level:].lstrip()
        
        return '#' * new_level + ' ' + rest
