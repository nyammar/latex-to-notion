"""Tests for list handler."""

import pytest
from latex2notion.handlers.list_handler import ListHandler
from latex2notion.parser import ASTNode, NodeType


class TestListHandler:
    """Test cases for ListHandler."""
    
    def test_simple_bullet_list(self):
        """Test simple bullet list: \begin{itemize}...\end{itemize} → Markdown bullet list"""
        handler = ListHandler()
        node = ASTNode(NodeType.LIST_ITEMIZE)
        
        item1 = ASTNode(NodeType.LIST_ITEM)
        item1.children = [ASTNode(NodeType.PARAGRAPH, children=[ASTNode(NodeType.TEXT, content="Item 1")])]
        
        item2 = ASTNode(NodeType.LIST_ITEM)
        item2.children = [ASTNode(NodeType.PARAGRAPH, children=[ASTNode(NodeType.TEXT, content="Item 2")])]
        
        node.children = [item1, item2]
        
        result = handler.convert(node)
        assert "- Item 1" in result
        assert "- Item 2" in result
    
    def test_numbered_list(self):
        """Test numbered list: \begin{enumerate}...\end{enumerate} → Markdown numbered list"""
        handler = ListHandler()
        node = ASTNode(NodeType.LIST_ENUMERATE)
        
        item1 = ASTNode(NodeType.LIST_ITEM)
        item1.children = [ASTNode(NodeType.PARAGRAPH, children=[ASTNode(NodeType.TEXT, content="First")])]
        
        item2 = ASTNode(NodeType.LIST_ITEM)
        item2.children = [ASTNode(NodeType.PARAGRAPH, children=[ASTNode(NodeType.TEXT, content="Second")])]
        
        node.children = [item1, item2]
        
        result = handler.convert(node)
        assert "1. First" in result
        assert "1. Second" in result  # Markdown uses 1. for all items
    
    def test_nested_lists_2_levels(self):
        """Test nested lists (2 levels deep)"""
        handler = ListHandler()
        node = ASTNode(NodeType.LIST_ITEMIZE)
        
        item1 = ASTNode(NodeType.LIST_ITEM)
        item1.children = [ASTNode(NodeType.PARAGRAPH, children=[ASTNode(NodeType.TEXT, content="Outer")])]
        
        node.children = [item1]
        
        result = handler.convert(node, level=0)
        assert "- Outer" in result
        
        # Test nested level
        nested_result = handler.convert(node, level=1)
        assert "  - Outer" in nested_result  # Should have indentation
    
    def test_list_with_inline_formatting(self):
        """Test lists with inline formatting"""
        handler = ListHandler()
        node = ASTNode(NodeType.LIST_ITEMIZE)
        
        item1 = ASTNode(NodeType.LIST_ITEM)
        para = ASTNode(NodeType.PARAGRAPH)
        para.children = [
            ASTNode(NodeType.TEXT, content="Bold: "),
            ASTNode(NodeType.BOLD, content="bold text")
        ]
        item1.children = [para]
        
        node.children = [item1]
        
        result = handler.convert(node)
        assert "**bold text**" in result
    
    def test_list_with_math_expressions(self):
        """Test lists with math expressions"""
        handler = ListHandler()
        node = ASTNode(NodeType.LIST_ITEMIZE)
        
        item1 = ASTNode(NodeType.LIST_ITEM)
        para = ASTNode(NodeType.PARAGRAPH)
        para.children = [
            ASTNode(NodeType.TEXT, content="Value: "),
            ASTNode(NodeType.MATH_INLINE, content="x^2")
        ]
        item1.children = [para]
        
        node.children = [item1]
        
        result = handler.convert(node)
        assert "$$x^2$$" in result
    
    def test_mixed_nested_lists(self):
        """Test mixed nested lists (itemize within enumerate)"""
        handler = ListHandler()
        # This would require more complex structure, but we test the basic functionality
        enumerate_node = ASTNode(NodeType.LIST_ENUMERATE)
        item = ASTNode(NodeType.LIST_ITEM)
        item.children = [ASTNode(NodeType.PARAGRAPH, children=[ASTNode(NodeType.TEXT, content="Numbered")])]
        enumerate_node.children = [item]
        
        result = handler.convert(enumerate_node)
        assert "1. Numbered" in result
    
    def test_empty_list(self):
        """Test empty list"""
        handler = ListHandler()
        node = ASTNode(NodeType.LIST_ITEMIZE)
        node.children = []
        
        result = handler.convert(node)
        assert result == ""
    
    def test_is_list_node(self):
        """Test is_list_node method"""
        handler = ListHandler()
        itemize = ASTNode(NodeType.LIST_ITEMIZE)
        enumerate = ASTNode(NodeType.LIST_ENUMERATE)
        paragraph = ASTNode(NodeType.PARAGRAPH)
        
        assert handler.is_list_node(itemize) is True
        assert handler.is_list_node(enumerate) is True
        assert handler.is_list_node(paragraph) is False
