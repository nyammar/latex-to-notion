"""
Table Handler

Converts LaTeX tables to Notion markdown table format.
"""

from latex2notion.parser import ASTNode, NodeType


class TableHandler:
    """Handles conversion of LaTeX tables."""
    
    def convert(self, node: ASTNode) -> str:
        """
        Convert table node to Notion markdown table format.
        
        Args:
            node: ASTNode with NodeType.TABLE containing table rows
            
        Returns:
            Notion-compatible markdown table
        """
        if not node.children:
            return ""
        
        rows = []
        for row_node in node.children:
            if isinstance(row_node.content, list):
                # Row content is a list of cells
                cells = row_node.content
                # Escape pipe characters in cells
                escaped_cells = [str(cell).replace('|', '\\|') for cell in cells]
                rows.append('| ' + ' | '.join(escaped_cells) + ' |')
        
        if not rows:
            return ""
        
        # Add header separator (required for markdown tables)
        if len(rows) > 0:
            num_cols = len(rows[0].split('|')) - 2  # Subtract 2 for leading/trailing empty strings
            separator = '| ' + ' | '.join(['---'] * num_cols) + ' |'
            rows.insert(1, separator)
        
        return '\n'.join(rows)
    
    def is_table_node(self, node: ASTNode) -> bool:
        """Check if node is a table."""
        return node.node_type == NodeType.TABLE
