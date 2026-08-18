"""
Block Handler

Handles conversion of block-level elements (headings, paragraphs, callouts, code blocks).
"""

from latex2notion.parser import ASTNode, NodeType


class BlockHandler:
    """Handles conversion of block-level elements."""
    
    def convert_heading(self, node: ASTNode) -> str:
        """Convert section node to Notion heading."""
        if node.node_type == NodeType.SECTION:
            return f"# {node.content}"
        elif node.node_type == NodeType.SUBSECTION:
            return f"## {node.content}"
        elif node.node_type == NodeType.SUBSUBSECTION:
            return f"### {node.content}"
        return ""
    
    def convert_quote(self, node: ASTNode) -> str:
        """Convert quote environment to Notion callout."""
        # Notion callout format: > 💡 Callout text
        content = node.content.strip() if isinstance(node.content, str) else ""
        return f"> 💡 {content}"
    
    def convert_code_block(self, node: ASTNode) -> str:
        """Convert verbatim/lstlisting to Notion code block."""
        content = node.content.strip() if isinstance(node.content, str) else ""
        # Notion code block format: ```language\ncode\n```
        return f"```\n{content}\n```"
    
    def convert_paragraph(self, node: ASTNode, inline_handler) -> str:
        """
        Convert paragraph node to Notion format.
        
        Args:
            node: Paragraph ASTNode
            inline_handler: InlineHandler instance for processing inline content
            
        Returns:
            Notion-compatible paragraph text
        """
        if not node.children:
            return ""
        
        parts = []
        for child in node.children:
            if child.node_type == NodeType.TEXT:
                parts.append(child.content)
            elif child.node_type == NodeType.BOLD:
                parts.append(f"**{child.content}**")
            elif child.node_type == NodeType.ITALIC:
                parts.append(f"*{child.content}*")
            elif child.node_type == NodeType.CODE:
                parts.append(f"`{child.content}`")
            elif child.node_type == NodeType.LINK:
                url = child.attributes.get('url', '')
                parts.append(f"[{child.content}]({url})")
            elif child.node_type in [NodeType.MATH_INLINE, NodeType.MATH_DISPLAY]:
                from latex2notion.handlers.math_handler import MathHandler
                math_handler = MathHandler()
                parts.append(math_handler.convert(child))
        
        return ''.join(parts)
    
    def is_heading(self, node: ASTNode) -> bool:
        """Check if node is a heading."""
        return node.node_type in [NodeType.SECTION, NodeType.SUBSECTION, NodeType.SUBSUBSECTION]
    
    def is_block_environment(self, node: ASTNode) -> bool:
        """Check if node is a block environment."""
        return node.node_type in [NodeType.QUOTE, NodeType.VERBATIM, NodeType.CODE_BLOCK]
