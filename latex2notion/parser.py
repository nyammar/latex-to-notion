"""
LaTeX Parser

Parses LaTeX syntax and builds an Abstract Syntax Tree (AST).
"""

import re
from typing import List, Dict, Any, Optional
from enum import Enum


class NodeType(Enum):
    """Types of AST nodes."""
    DOCUMENT = "document"
    SECTION = "section"
    SUBSECTION = "subsection"
    SUBSUBSECTION = "subsubsection"
    PARAGRAPH = "paragraph"
    MATH_INLINE = "math_inline"
    MATH_DISPLAY = "math_display"
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    LIST_ITEMIZE = "list_itemize"
    LIST_ENUMERATE = "list_enumerate"
    LIST_ITEM = "list_item"
    TABLE = "table"
    QUOTE = "quote"
    VERBATIM = "verbatim"
    CODE_BLOCK = "code_block"


class ASTNode:
    """Represents a node in the Abstract Syntax Tree."""
    
    def __init__(self, node_type: NodeType, content: Any = None, children: Optional[List['ASTNode']] = None, 
                 attributes: Optional[Dict[str, Any]] = None):
        self.node_type = node_type
        self.content = content
        self.children = children or []
        self.attributes = attributes or {}
    
    def __repr__(self):
        return f"ASTNode({self.node_type.value}, content={self.content}, children={len(self.children)})"


class LaTeXParser:
    """Parses LaTeX syntax into an AST."""
    
    def __init__(self):
        # Patterns for LaTeX commands and environments
        self.patterns = {
            'section': re.compile(r'\\section\s*\{([^}]+)\}'),
            'subsection': re.compile(r'\\subsection\s*\{([^}]+)\}'),
            'subsubsection': re.compile(r'\\subsubsection\s*\{([^}]+)\}'),
            'textbf': re.compile(r'\\textbf\s*\{([^}]+)\}'),
            'textit': re.compile(r'\\textit\s*\{([^}]+)\}'),
            'texttt': re.compile(r'\\texttt\s*\{([^}]+)\}'),
            'href': re.compile(r'\\href\s*\{([^}]+)\}\s*\{([^}]+)\}'),
            'math_inline': re.compile(r'(?<!\$)\$(?!\$)([^$]+)\$(?!\$)'),
            'math_display': re.compile(r'\$\$([^$]+)\$\$'),
            'math_display_brackets': re.compile(r'\\\[(.*?)\\\]', re.DOTALL),
            'math_inline_parens': re.compile(r'\\\((.*?)\\\)', re.DOTALL),
            'begin_env': re.compile(r'\\begin\s*\{([^}]+)\}'),
            'end_env': re.compile(r'\\end\s*\{([^}]+)\}'),
            'item': re.compile(r'\\item\s*(.*)'),
        }
    
    def parse(self, latex_text: str) -> ASTNode:
        """
        Parse LaTeX text into an AST.
        
        Args:
            latex_text: The LaTeX source text
            
        Returns:
            Root ASTNode representing the document
        """
        root = ASTNode(NodeType.DOCUMENT)
        lines = latex_text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            # Check for section commands
            if match := self.patterns['section'].search(line):
                heading_text = match.group(1)
                root.children.append(ASTNode(NodeType.SECTION, content=heading_text))
                i += 1
                continue
            
            if match := self.patterns['subsection'].search(line):
                heading_text = match.group(1)
                root.children.append(ASTNode(NodeType.SUBSECTION, content=heading_text))
                i += 1
                continue
            
            if match := self.patterns['subsubsection'].search(line):
                heading_text = match.group(1)
                root.children.append(ASTNode(NodeType.SUBSUBSECTION, content=heading_text))
                i += 1
                continue
            
            # Check for environments
            begin_match = self.patterns['begin_env'].search(line)
            if begin_match:
                env_name = begin_match.group(1)
                env_node = self._parse_environment(latex_text, i, env_name, lines)
                if env_node:
                    root.children.append(env_node)
                    # Skip lines that were processed in the environment (including the \end line)
                    i = env_node.attributes.get('end_line', i + 1) + 1
                    continue
            
            # Parse paragraph content
            paragraph_node = self._parse_paragraph(line)
            if paragraph_node and paragraph_node.children:
                root.children.append(paragraph_node)
            
            i += 1
        
        return root
    
    def _parse_environment(self, full_text: str, start_line: int, env_name: str, lines: List[str]) -> Optional[ASTNode]:
        """Parse a LaTeX environment."""
        # Find the matching \end{env_name}
        depth = 1
        end_line = start_line + 1
        env_content_lines = []
        
        # Collect content until we find matching \end
        for i in range(start_line + 1, len(lines)):
            line = lines[i]
            if self.patterns['begin_env'].search(line):
                depth += 1
                env_content_lines.append(line)
            elif match := self.patterns['end_env'].search(line):
                if match.group(1) == env_name:
                    depth -= 1
                    if depth == 0:
                        end_line = i
                        break
                    else:
                        # Nested environment end, include it
                        env_content_lines.append(line)
                else:
                    # Different environment end, include it
                    env_content_lines.append(line)
            else:
                env_content_lines.append(line)
        
        env_content = '\n'.join(env_content_lines)
        
        # Map environment names to node types
        env_map = {
            'itemize': NodeType.LIST_ITEMIZE,
            'enumerate': NodeType.LIST_ENUMERATE,
            'quote': NodeType.QUOTE,
            'verbatim': NodeType.VERBATIM,
            'lstlisting': NodeType.CODE_BLOCK,
            'table': NodeType.TABLE,
            'tabular': NodeType.TABLE,
        }
        
        node_type = env_map.get(env_name, NodeType.PARAGRAPH)
        node = ASTNode(node_type, content=env_content)
        node.attributes['end_line'] = end_line
        node.attributes['env_name'] = env_name
        
        # Parse content based on environment type
        if env_name in ['itemize', 'enumerate']:
            node.children = self._parse_list_items(env_content)
        elif env_name in ['table', 'tabular']:
            node.children = self._parse_table(env_content)
        else:
            # For quote, verbatim, etc., store raw content
            node.content = env_content
        
        return node
    
    def _parse_list_items(self, content: str) -> List[ASTNode]:
        """Parse list items from environment content."""
        items = []
        # Find all \item commands
        lines = content.split('\n')
        current_item_content = []
        
        for line in lines:
            if match := self.patterns['item'].search(line):
                # Save previous item if exists
                if current_item_content:
                    item_text = '\n'.join(current_item_content).strip()
                    if item_text:
                        item_node = ASTNode(NodeType.LIST_ITEM)
                        # Parse the item content as a paragraph
                        para_node = self._parse_paragraph(item_text)
                        item_node.children = para_node.children if para_node else []
                        items.append(item_node)
                
                # Start new item
                item_text_after_item = match.group(1).strip() if match.group(1) else ""
                current_item_content = [item_text_after_item] if item_text_after_item else []
            else:
                # Continue current item
                if current_item_content is not None:
                    current_item_content.append(line)
        
        # Add last item
        if current_item_content:
            item_text = '\n'.join(current_item_content).strip()
            if item_text:
                item_node = ASTNode(NodeType.LIST_ITEM)
                para_node = self._parse_paragraph(item_text)
                item_node.children = para_node.children if para_node else []
                items.append(item_node)
        
        return items
    
    def _parse_table(self, content: str) -> List[ASTNode]:
        """Parse table content."""
        # Basic table parsing - extract rows
        rows = []
        # Look for table rows (lines with & separators)
        for line in content.split('\n'):
            if '&' in line and not line.strip().startswith('%'):
                # This is a table row
                cells = [cell.strip() for cell in line.split('&')]
                row_node = ASTNode(NodeType.TEXT, content=cells)
                rows.append(row_node)
        return rows
    
    def _parse_paragraph(self, text: str) -> ASTNode:
        """Parse a paragraph, handling inline commands and math."""
        para = ASTNode(NodeType.PARAGRAPH)
        
        # Process text with inline commands
        remaining = text
        last_pos = 0
        
        # Find all inline elements (math, commands) with their positions
        elements = []
        
        # Find math expressions first (they have priority)
        for match in self.patterns['math_display'].finditer(text):
            elements.append(('math_display', match.start(), match.end(), match.group(1)))
        for match in self.patterns['math_inline'].finditer(text):
            elements.append(('math_inline', match.start(), match.end(), match.group(1)))
        for match in self.patterns['math_display_brackets'].finditer(text):
            elements.append(('math_display', match.start(), match.end(), match.group(1)))
        for match in self.patterns['math_inline_parens'].finditer(text):
            elements.append(('math_inline', match.start(), match.end(), match.group(1)))
        
        # Find formatting commands
        for match in self.patterns['textbf'].finditer(text):
            elements.append(('textbf', match.start(), match.end(), match.group(1)))
        for match in self.patterns['textit'].finditer(text):
            elements.append(('textit', match.start(), match.end(), match.group(1)))
        for match in self.patterns['texttt'].finditer(text):
            elements.append(('code', match.start(), match.end(), match.group(1)))
        for match in self.patterns['href'].finditer(text):
            elements.append(('href', match.start(), match.end(), (match.group(1), match.group(2))))
        
        # Sort by position
        elements.sort(key=lambda x: x[1])
        
        # Build nodes in order
        pos = 0
        for elem_type, start, end, content in elements:
            # Add text before this element
            if start > pos:
                text_before = text[pos:start]
                if text_before.strip():
                    para.children.append(ASTNode(NodeType.TEXT, content=text_before))
            
            # Add the element
            if elem_type == 'math_inline':
                para.children.append(ASTNode(NodeType.MATH_INLINE, content=content))
            elif elem_type == 'math_display':
                para.children.append(ASTNode(NodeType.MATH_DISPLAY, content=content))
            elif elem_type == 'textbf':
                para.children.append(ASTNode(NodeType.BOLD, content=content))
            elif elem_type == 'textit':
                para.children.append(ASTNode(NodeType.ITALIC, content=content))
            elif elem_type == 'code':
                para.children.append(ASTNode(NodeType.CODE, content=content))
            elif elem_type == 'href':
                url, link_text = content
                para.children.append(ASTNode(NodeType.LINK, content=link_text, attributes={'url': url}))
            
            pos = end
        
        # Add remaining text
        if pos < len(text):
            remaining_text = text[pos:]
            if remaining_text.strip():
                para.children.append(ASTNode(NodeType.TEXT, content=remaining_text))
        
        # If no elements found, add whole text as text node
        if not para.children and text.strip():
            para.children.append(ASTNode(NodeType.TEXT, content=text))
        
        return para
