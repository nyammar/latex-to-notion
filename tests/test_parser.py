"""Tests for LaTeX parser."""

import pytest
from latex2notion.parser import LaTeXParser, ASTNode, NodeType


class TestLaTeXParser:
    """Test cases for LaTeXParser."""
    
    def test_parse_section(self):
        """Test parsing section command"""
        parser = LaTeXParser()
        latex = "\\section{Introduction}"
        ast = parser.parse(latex)
        
        assert len(ast.children) == 1
        assert ast.children[0].node_type == NodeType.SECTION
        assert ast.children[0].content == "Introduction"
    
    def test_parse_subsection(self):
        """Test parsing subsection command"""
        parser = LaTeXParser()
        latex = "\\subsection{Details}"
        ast = parser.parse(latex)
        
        assert len(ast.children) == 1
        assert ast.children[0].node_type == NodeType.SUBSECTION
        assert ast.children[0].content == "Details"
    
    def test_parse_paragraph_with_text(self):
        """Test parsing paragraph with plain text"""
        parser = LaTeXParser()
        latex = "This is a paragraph."
        ast = parser.parse(latex)
        
        assert len(ast.children) > 0
        # Should have at least one paragraph node
    
    def test_parse_inline_math(self):
        """Test parsing inline math"""
        parser = LaTeXParser()
        latex = "The value is $x^2$."
        ast = parser.parse(latex)
        
        # Should find math node in paragraph
        found_math = False
        for child in ast.children:
            if child.node_type == NodeType.PARAGRAPH:
                for para_child in child.children:
                    if para_child.node_type == NodeType.MATH_INLINE:
                        found_math = True
                        assert "x^2" in para_child.content
        assert found_math
    
    def test_parse_display_math(self):
        """Test parsing display math"""
        parser = LaTeXParser()
        latex = "$$\\int_0^1 x dx$$"
        ast = parser.parse(latex)
        
        # Should find display math
        found_math = False
        for child in ast.children:
            if child.node_type == NodeType.PARAGRAPH:
                for para_child in child.children:
                    if para_child.node_type == NodeType.MATH_DISPLAY:
                        found_math = True
        assert found_math
    
    def test_parse_bold(self):
        """Test parsing bold text"""
        parser = LaTeXParser()
        latex = "This is \\textbf{bold} text."
        ast = parser.parse(latex)
        
        found_bold = False
        for child in ast.children:
            if child.node_type == NodeType.PARAGRAPH:
                for para_child in child.children:
                    if para_child.node_type == NodeType.BOLD:
                        found_bold = True
                        assert para_child.content == "bold"
        assert found_bold
    
    def test_parse_italic(self):
        """Test parsing italic text"""
        parser = LaTeXParser()
        latex = "This is \\textit{italic} text."
        ast = parser.parse(latex)
        
        found_italic = False
        for child in ast.children:
            if child.node_type == NodeType.PARAGRAPH:
                for para_child in child.children:
                    if para_child.node_type == NodeType.ITALIC:
                        found_italic = True
        assert found_italic
    
    def test_parse_itemize(self):
        """Test parsing itemize environment"""
        parser = LaTeXParser()
        latex = "\\begin{itemize}\n\\item First\n\\item Second\n\\end{itemize}"
        ast = parser.parse(latex)
        
        found_list = False
        for child in ast.children:
            if child.node_type == NodeType.LIST_ITEMIZE:
                found_list = True
                assert len(child.children) > 0
        assert found_list
    
    def test_parse_enumerate(self):
        """Test parsing enumerate environment"""
        parser = LaTeXParser()
        latex = "\\begin{enumerate}\n\\item First\n\\item Second\n\\end{enumerate}"
        ast = parser.parse(latex)
        
        found_list = False
        for child in ast.children:
            if child.node_type == NodeType.LIST_ENUMERATE:
                found_list = True
        assert found_list
    
    def test_parse_quote(self):
        """Test parsing quote environment"""
        parser = LaTeXParser()
        latex = "\\begin{quote}\nThis is a quote.\n\\end{quote}"
        ast = parser.parse(latex)
        
        found_quote = False
        for child in ast.children:
            if child.node_type == NodeType.QUOTE:
                found_quote = True
        assert found_quote
    
    def test_parse_verbatim(self):
        """Test parsing verbatim environment"""
        parser = LaTeXParser()
        latex = "\\begin{verbatim}\nprint('hello')\n\\end{verbatim}"
        ast = parser.parse(latex)
        
        found_verbatim = False
        for child in ast.children:
            if child.node_type == NodeType.VERBATIM:
                found_verbatim = True
        assert found_verbatim
    
    def test_parse_link(self):
        """Test parsing href link"""
        parser = LaTeXParser()
        latex = "Visit \\href{https://example.com}{Example}"
        ast = parser.parse(latex)
        
        found_link = False
        for child in ast.children:
            if child.node_type == NodeType.PARAGRAPH:
                for para_child in child.children:
                    if para_child.node_type == NodeType.LINK:
                        found_link = True
                        assert para_child.content == "Example"
                        assert para_child.attributes.get('url') == "https://example.com"
        assert found_link
    
    def test_parse_empty_document(self):
        """Test parsing empty document"""
        parser = LaTeXParser()
        latex = ""
        ast = parser.parse(latex)
        
        assert ast.node_type == NodeType.DOCUMENT
        assert len(ast.children) == 0
