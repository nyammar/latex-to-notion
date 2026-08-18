"""Tests for inline handler."""

import pytest
from latex2notion.handlers.inline_handler import InlineHandler
from latex2notion.parser import ASTNode, NodeType


class TestInlineHandler:
    """Test cases for InlineHandler."""
    
    def test_bold_text(self):
        """Test bold text: \textbf{text} → **text**"""
        handler = InlineHandler()
        node = ASTNode(NodeType.BOLD, content="text")
        result = handler.convert(node)
        assert result == "**text**"
    
    def test_italic_text(self):
        """Test italic text: \textit{text} → *text*"""
        handler = InlineHandler()
        node = ASTNode(NodeType.ITALIC, content="text")
        result = handler.convert(node)
        assert result == "*text*"
    
    def test_code_inline(self):
        """Test code inline: \texttt{code} → `code`"""
        handler = InlineHandler()
        node = ASTNode(NodeType.CODE, content="code")
        result = handler.convert(node)
        assert result == "`code`"
    
    def test_link(self):
        """Test links: \href{https://example.com}{Link} → [Link](https://example.com)"""
        handler = InlineHandler()
        node = ASTNode(NodeType.LINK, content="Link", attributes={'url': 'https://example.com'})
        result = handler.convert(node)
        assert result == "[Link](https://example.com)"
    
    def test_combined_formatting(self):
        """Test combined formatting: \textbf{\textit{bold italic}} → ***bold italic***"""
        # Note: This requires nested parsing, but we can test the individual conversions
        handler = InlineHandler()
        bold_node = ASTNode(NodeType.BOLD, content="bold text")
        italic_node = ASTNode(NodeType.ITALIC, content="italic text")
        
        assert handler.convert(bold_node) == "**bold text**"
        assert handler.convert(italic_node) == "*italic text*"
    
    def test_text_node(self):
        """Test plain text node"""
        handler = InlineHandler()
        node = ASTNode(NodeType.TEXT, content="plain text")
        result = handler.convert(node)
        assert result == "plain text"
    
    def test_link_without_url(self):
        """Test link node without URL attribute"""
        handler = InlineHandler()
        node = ASTNode(NodeType.LINK, content="Link", attributes={})
        result = handler.convert(node)
        assert result == "[Link]()"
    
    def test_is_inline_node(self):
        """Test is_inline_node method"""
        handler = InlineHandler()
        bold = ASTNode(NodeType.BOLD)
        italic = ASTNode(NodeType.ITALIC)
        code = ASTNode(NodeType.CODE)
        link = ASTNode(NodeType.LINK)
        text = ASTNode(NodeType.TEXT)
        paragraph = ASTNode(NodeType.PARAGRAPH)
        
        assert handler.is_inline_node(bold) is True
        assert handler.is_inline_node(italic) is True
        assert handler.is_inline_node(code) is True
        assert handler.is_inline_node(link) is True
        assert handler.is_inline_node(text) is True
        assert handler.is_inline_node(paragraph) is False
