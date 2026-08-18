"""
List Handler

Converts LaTeX lists (itemize, enumerate) to Notion markdown lists.
"""

from latex2notion.parser import ASTNode, NodeType


class ListHandler:
    """Handles conversion of LaTeX lists."""
    
    def convert(self, node: ASTNode, level: int = 0) -> str:
        """
        Convert list node to Notion markdown list format.
        
        Args:
            node: ASTNode with NodeType.LIST_ITEMIZE or NodeType.LIST_ENUMERATE
            level: Nesting level (0-based)
            
        Returns:
            Notion-compatible markdown list
        """
        if not node.children:
            return ""
        
        items = []
        indent = '  ' * level
        
        is_ordered = node.node_type == NodeType.LIST_ENUMERATE
        
        for item_node in node.children:
            if item_node.node_type == NodeType.LIST_ITEM:
                # Process item content
                item_text = self._process_item_content(item_node)
                
                if is_ordered:
                    # Numbered list (Notion uses 1. format)
                    items.append(f"{indent}1. {item_text}")
                else:
                    # Bullet list
                    items.append(f"{indent}- {item_text}")
        
        return '\n'.join(items)
    
    def _process_item_content(self, item_node: ASTNode) -> str:
        """Process the content of a list item."""
        if not item_node.children:
            return ""
        
        parts = []
        for child in item_node.children:
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
            elif child.node_type == NodeType.PARAGRAPH:
                # Process paragraph children
                for para_child in child.children:
                    parts.append(self._convert_inline_node(para_child))
        
        return ''.join(parts)
    
    def _convert_inline_node(self, node: ASTNode) -> str:
        """Convert an inline node to text."""
        if node.node_type == NodeType.TEXT:
            return node.content
        elif node.node_type == NodeType.BOLD:
            return f"**{node.content}**"
        elif node.node_type == NodeType.ITALIC:
            return f"*{node.content}*"
        elif node.node_type == NodeType.CODE:
            return f"`{node.content}`"
        elif node.node_type == NodeType.LINK:
            url = node.attributes.get('url', '')
            return f"[{node.content}]({url})"
        elif node.node_type in [NodeType.MATH_INLINE, NodeType.MATH_DISPLAY]:
            from latex2notion.handlers.math_handler import MathHandler
            math_handler = MathHandler()
            return math_handler.convert(node)
        else:
            return ""
    
    def is_list_node(self, node: ASTNode) -> bool:
        """Check if node is a list."""
        return node.node_type in [NodeType.LIST_ITEMIZE, NodeType.LIST_ENUMERATE]
