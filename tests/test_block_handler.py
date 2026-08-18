"""Tests for block handler."""

import pytest
from latex2notion.handlers.block_handler import BlockHandler
from latex2notion.parser import ASTNode, NodeType


class TestBlockHandler:
    """Test cases for BlockHandler."""
    
    def test_section_heading(self):
        """Test section heading: \section{Introduction} → # Introduction"""
        handler = BlockHandler()
        node = ASTNode(NodeType.SECTION, content="Introduction")
        result = handler.convert_heading(node)
        assert result == "# Introduction"
    
    def test_subsection_heading(self):
        """Test subsection heading: \subsection{Details} → ## Details"""
        handler = BlockHandler()
        node = ASTNode(NodeType.SUBSECTION, content="Details")
        result = handler.convert_heading(node)
        assert result == "## Details"
    
    def test_subsubsection_heading(self):
        """Test subsubsection heading"""
        handler = BlockHandler()
        node = ASTNode(NodeType.SUBSUBSECTION, content="Subdetails")
        result = handler.convert_heading(node)
        assert result == "### Subdetails"
    
    def test_quote_environment(self):
        """Test quote environment: \begin{quote}...\end{quote} → Notion callout"""
        handler = BlockHandler()
        node = ASTNode(NodeType.QUOTE, content="This is a quote")
        result = handler.convert_quote(node)
        assert result.startswith("> 💡")
        assert "This is a quote" in result
    
    def test_code_block(self):
        """Test code blocks: \begin{verbatim}...\end{verbatim} → Notion code block"""
        handler = BlockHandler()
        node = ASTNode(NodeType.VERBATIM, content="print('hello')")
        result = handler.convert_code_block(node)
        assert result.startswith("```")
        assert result.endswith("```")
        assert "print('hello')" in result
    
    def test_paragraph_with_text(self):
        """Test paragraph conversion with plain text"""
        handler = BlockHandler()
        from latex2notion.handlers.inline_handler import InlineHandler
        inline_handler = InlineHandler()
        
        node = ASTNode(NodeType.PARAGRAPH)
        node.children = [ASTNode(NodeType.TEXT, content="This is a paragraph")]
        result = handler.convert_paragraph(node, inline_handler)
        assert result == "This is a paragraph"
    
    def test_paragraph_with_bold(self):
        """Test paragraph with bold text"""
        handler = BlockHandler()
        from latex2notion.handlers.inline_handler import InlineHandler
        inline_handler = InlineHandler()
        
        node = ASTNode(NodeType.PARAGRAPH)
        node.children = [ASTNode(NodeType.BOLD, content="bold text")]
        result = handler.convert_paragraph(node, inline_handler)
        assert result == "**bold text**"
    
    def test_paragraph_with_italic(self):
        """Test paragraph with italic text"""
        handler = BlockHandler()
        from latex2notion.handlers.inline_handler import InlineHandler
        inline_handler = InlineHandler()
        
        node = ASTNode(NodeType.PARAGRAPH)
        node.children = [ASTNode(NodeType.ITALIC, content="italic text")]
        result = handler.convert_paragraph(node, inline_handler)
        assert result == "*italic text*"
    
    def test_paragraph_with_math(self):
        """Test paragraph with inline math"""
        handler = BlockHandler()
        from latex2notion.handlers.inline_handler import InlineHandler
        inline_handler = InlineHandler()
        
        node = ASTNode(NodeType.PARAGRAPH)
        math_node = ASTNode(NodeType.MATH_INLINE, content="x^2")
        node.children = [ASTNode(NodeType.TEXT, content="The value is "), math_node]
        result = handler.convert_paragraph(node, inline_handler)
        assert "$$x^2$$" in result
    
    def test_multiple_heading_levels(self):
        """Test multiple heading levels in sequence"""
        handler = BlockHandler()
        section = ASTNode(NodeType.SECTION, content="Section 1")
        subsection = ASTNode(NodeType.SUBSECTION, content="Subsection 1.1")
        
        assert handler.convert_heading(section) == "# Section 1"
        assert handler.convert_heading(subsection) == "## Subsection 1.1"
    
    def test_is_heading(self):
        """Test is_heading method"""
        handler = BlockHandler()
        section = ASTNode(NodeType.SECTION)
        subsection = ASTNode(NodeType.SUBSECTION)
        paragraph = ASTNode(NodeType.PARAGRAPH)
        
        assert handler.is_heading(section) is True
        assert handler.is_heading(subsection) is True
        assert handler.is_heading(paragraph) is False
    
    def test_is_block_environment(self):
        """Test is_block_environment method"""
        handler = BlockHandler()
        quote = ASTNode(NodeType.QUOTE)
        verbatim = ASTNode(NodeType.VERBATIM)
        paragraph = ASTNode(NodeType.PARAGRAPH)
        
        assert handler.is_block_environment(quote) is True
        assert handler.is_block_environment(verbatim) is True
        assert handler.is_block_environment(paragraph) is False
