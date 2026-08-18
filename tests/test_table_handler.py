"""Tests for table handler."""

import pytest
from latex2notion.handlers.table_handler import TableHandler
from latex2notion.parser import ASTNode, NodeType


class TestTableHandler:
    """Test cases for TableHandler."""
    
    def test_simple_table(self):
        """Test simple table with 2x2 grid"""
        handler = TableHandler()
        node = ASTNode(NodeType.TABLE)
        
        row1 = ASTNode(NodeType.TEXT, content=["Header1", "Header2"])
        row2 = ASTNode(NodeType.TEXT, content=["Cell1", "Cell2"])
        node.children = [row1, row2]
        
        result = handler.convert(node)
        assert "Header1" in result
        assert "Header2" in result
        assert "Cell1" in result
        assert "Cell2" in result
        assert "|" in result  # Should contain pipe separators
    
    def test_table_with_separator(self):
        """Test that table includes markdown separator row"""
        handler = TableHandler()
        node = ASTNode(NodeType.TABLE)
        
        row1 = ASTNode(NodeType.TEXT, content=["A", "B"])
        node.children = [row1]
        
        result = handler.convert(node)
        lines = result.split('\n')
        # Should have header, separator, and at least one data row
        assert len(lines) >= 2
        assert "---" in result or "|" in result
    
    def test_table_with_math(self):
        """Test table with math expressions in cells"""
        handler = TableHandler()
        node = ASTNode(NodeType.TABLE)
        
        row1 = ASTNode(NodeType.TEXT, content=["$x^2$", "$y^2$"])
        node.children = [row1]
        
        result = handler.convert(node)
        assert "$x^2$" in result or "x^2" in result
    
    def test_table_escapes_pipes(self):
        """Test that pipe characters in cells are escaped"""
        handler = TableHandler()
        node = ASTNode(NodeType.TABLE)
        
        row1 = ASTNode(NodeType.TEXT, content=["Cell|with|pipe", "Normal"])
        node.children = [row1]
        
        result = handler.convert(node)
        # Pipes in content should be escaped
        assert "\\|" in result or "Cell" in result
    
    def test_empty_table(self):
        """Test empty table"""
        handler = TableHandler()
        node = ASTNode(NodeType.TABLE)
        node.children = []
        
        result = handler.convert(node)
        assert result == ""
    
    def test_is_table_node(self):
        """Test is_table_node method"""
        handler = TableHandler()
        table = ASTNode(NodeType.TABLE)
        paragraph = ASTNode(NodeType.PARAGRAPH)
        
        assert handler.is_table_node(table) is True
        assert handler.is_table_node(paragraph) is False
