"""Tests for math handler."""

import pytest
from latex2notion.handlers.math_handler import MathHandler
from latex2notion.parser import ASTNode, NodeType


class TestMathHandler:
    """Test cases for MathHandler."""
    
    def test_inline_math(self):
        """Test inline math conversion: $x^2 + y^2$ → $$x^2 + y^2$$"""
        handler = MathHandler()
        node = ASTNode(NodeType.MATH_INLINE, content="x^2 + y^2")
        result = handler.convert(node)
        assert result == "$$x^2 + y^2$$"
    
    def test_display_math(self):
        """Test display math conversion: $$\int_0^1 x dx$$ → Notion math block"""
        handler = MathHandler()
        node = ASTNode(NodeType.MATH_DISPLAY, content="\\int_0^1 x dx")
        result = handler.convert(node)
        assert "$$" in result
        assert "\\int_0^1 x dx" in result
    
    def test_math_with_fractions(self):
        """Test math with fractions: $\frac{a}{b}$ → $$\frac{a}{b}$$"""
        handler = MathHandler()
        node = ASTNode(NodeType.MATH_INLINE, content="\\frac{a}{b}")
        result = handler.convert(node)
        assert result == "$$\\frac{a}{b}$$"
    
    def test_math_with_special_characters(self):
        """Test math with special characters and Greek letters"""
        handler = MathHandler()
        node = ASTNode(NodeType.MATH_INLINE, content="\\alpha + \\beta = \\gamma")
        result = handler.convert(node)
        assert result == "$$\\alpha + \\beta = \\gamma$$"
    
    def test_multiple_math_expressions(self):
        """Test multiple math expressions in one paragraph"""
        handler = MathHandler()
        node1 = ASTNode(NodeType.MATH_INLINE, content="x^2")
        node2 = ASTNode(NodeType.MATH_INLINE, content="y^2")
        result1 = handler.convert(node1)
        result2 = handler.convert(node2)
        assert result1 == "$$x^2$$"
        assert result2 == "$$y^2$$"
    
    def test_complex_math_expression(self):
        """Test complex math expression"""
        handler = MathHandler()
        node = ASTNode(NodeType.MATH_DISPLAY, content="\\sum_{i=1}^{n} x_i = \\frac{n(n+1)}{2}")
        result = handler.convert(node)
        assert "$$" in result
        assert "\\sum" in result
    
    def test_is_math_node(self):
        """Test is_math_node method"""
        handler = MathHandler()
        inline_node = ASTNode(NodeType.MATH_INLINE)
        display_node = ASTNode(NodeType.MATH_DISPLAY)
        text_node = ASTNode(NodeType.TEXT)
        
        assert handler.is_math_node(inline_node) is True
        assert handler.is_math_node(display_node) is True
        assert handler.is_math_node(text_node) is False
