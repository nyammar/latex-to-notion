"""
Inline Handler

Handles conversion of inline formatting (bold, italic, code, links).
"""

from latex2notion.parser import ASTNode, NodeType


class InlineHandler:
    """Handles conversion of inline formatting."""
    
    def convert(self, node: ASTNode) -> str:
        """
        Convert inline formatting node to Notion format.
        
        Args:
            node: ASTNode with inline formatting type
            
        Returns:
            Notion-compatible formatted text
        """
        if node.node_type == NodeType.BOLD:
            return f"**{node.content}**"
        elif node.node_type == NodeType.ITALIC:
            return f"*{node.content}*"
        elif node.node_type == NodeType.CODE:
            return f"`{node.content}`"
        elif node.node_type == NodeType.LINK:
            url = node.attributes.get('url', '')
            return f"[{node.content}]({url})"
        elif node.node_type == NodeType.TEXT:
            return node.content
        else:
            return ""
    
    def is_inline_node(self, node: ASTNode) -> bool:
        """Check if node is an inline formatting node."""
        return node.node_type in [NodeType.BOLD, NodeType.ITALIC, NodeType.CODE, NodeType.LINK, NodeType.TEXT]
