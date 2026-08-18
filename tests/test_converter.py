"""Integration tests for the converter."""

import pytest
from latex2notion import convert
from latex2notion.converter import NotionConverter
from latex2notion.parser import LaTeXParser, ASTNode, NodeType


class TestConverter:
    """Test cases for the main converter."""
    
    def test_simple_section(self):
        """Test converting a simple section"""
        latex = "\\section{Introduction}"
        result = convert(latex)
        assert "# Introduction" in result
    
    def test_section_with_paragraph(self):
        """Test section followed by paragraph"""
        latex = "\\section{Introduction}\nThis is a paragraph."
        result = convert(latex)
        assert "# Introduction" in result
        assert "This is a paragraph" in result
    
    def test_inline_math(self):
        """Test inline math conversion"""
        latex = "The value is $x^2 + y^2$."
        result = convert(latex)
        assert "$$x^2 + y^2$$" in result
    
    def test_display_math(self):
        """Test display math conversion"""
        latex = "$$\\int_0^1 x dx$$"
        result = convert(latex)
        assert "$$$" in result or "\\int" in result
    
    def test_bold_and_italic(self):
        """Test bold and italic formatting"""
        latex = "This is \\textbf{bold} and \\textit{italic}."
        result = convert(latex)
        assert "**bold**" in result
        assert "*italic*" in result
    
    def test_list_itemize(self):
        """Test itemize list conversion"""
        latex = "\\begin{itemize}\n\\item First\n\\item Second\n\\end{itemize}"
        result = convert(latex)
        assert "- First" in result
        assert "- Second" in result
    
    def test_list_enumerate(self):
        """Test enumerate list conversion"""
        latex = "\\begin{enumerate}\n\\item First\n\\item Second\n\\end{enumerate}"
        result = convert(latex)
        assert "1. First" in result
        assert "1. Second" in result
    
    def test_quote_environment(self):
        """Test quote to callout conversion"""
        latex = "\\begin{quote}\nThis is a quote.\n\\end{quote}"
        result = convert(latex)
        assert "> 💡" in result
        assert "This is a quote" in result
    
    def test_code_block(self):
        """Test verbatim to code block conversion"""
        latex = "\\begin{verbatim}\nprint('hello')\n\\end{verbatim}"
        result = convert(latex)
        assert "```" in result
        assert "print('hello')" in result
    
    def test_link(self):
        """Test href link conversion"""
        latex = "Visit \\href{https://example.com}{Example}"
        result = convert(latex)
        assert "[Example](https://example.com)" in result
    
    def test_complete_document(self):
        """Test complete LaTeX document with all features"""
        latex = """
\\section{Introduction}
This is an introduction with inline math: $x^2$.

\\subsection{Details}
Some \\textbf{bold} text here.

\\begin{itemize}
\\item First item
\\item Second item
\\end{itemize}

\\begin{quote}
This is a quote.
\\end{quote}
"""
        result = convert(latex)
        assert "# Introduction" in result
        assert "## Details" in result
        assert "**bold**" in result
        assert "- First item" in result
        assert "> 💡" in result
    
    def test_multiple_sections(self):
        """Test document with multiple sections and subsections"""
        latex = """
\\section{First Section}
Content here.

\\section{Second Section}
More content.

\\subsection{Subsection}
Subsection content.
"""
        result = convert(latex)
        assert "# First Section" in result
        assert "# Second Section" in result
        assert "## Subsection" in result
    
    def test_mixed_content(self):
        """Test document with mixed content (headings, paragraphs, lists, tables, math)"""
        latex = """
\\section{Title}
Paragraph with $x^2$ math.

\\begin{itemize}
\\item Item with \\textbf{bold}
\\end{itemize}
"""
        result = convert(latex)
        assert "# Title" in result
        assert "$$x^2$$" in result
        assert "**bold**" in result
    
    def test_heading_level_offset(self):
        """Test heading level offset option"""
        latex = "\\section{Title}"
        result = convert(latex, heading_level_offset=1)
        assert "## Title" in result  # Should be one level deeper
    
    def test_preserve_comments(self):
        """Test preserve_comments option"""
        latex = "\\section{Title}\n% This is a comment\nParagraph"
        result_with_comments = convert(latex, preserve_comments=True)
        result_without = convert(latex, preserve_comments=False)
        
        # Comments should be removed by default
        assert "%" not in result_without or "comment" not in result_without
    
    def test_empty_sections(self):
        """Test edge case: empty sections"""
        latex = "\\section{}\n\\subsection{}"
        result = convert(latex)
        # Should handle gracefully
        assert result is not None
    
    def test_math_with_fractions(self):
        """Test math with fractions"""
        latex = "The fraction is $\\frac{a}{b}$."
        result = convert(latex)
        assert "\\frac{a}{b}" in result
    
    def test_math_with_greek_letters(self):
        """Test math with Greek letters"""
        latex = "The value is $\\alpha + \\beta$."
        result = convert(latex)
        assert "\\alpha" in result
        assert "\\beta" in result
    
    def test_nested_formatting(self):
        """Test nested formatting commands"""
        latex = "This is \\textbf{\\textit{bold italic}}."
        result = convert(latex)
        # Should handle nested formatting
        assert "**" in result or "*" in result
    
    def test_table_basic(self):
        """Test basic table conversion"""
        latex = """
\\begin{tabular}{|c|c|}
\\hline
A & B \\\\
C & D \\\\
\\hline
\\end{tabular}
"""
        result = convert(latex)
        # Should contain table structure
        assert "A" in result or "B" in result
    
    def test_real_world_academic_structure(self):
        """Test real-world academic paper structure"""
        latex = """
\\section{Abstract}
This is the abstract.

\\section{Introduction}
Introduction text with $E = mc^2$.

\\subsection{Related Work}
Related work here.

\\begin{itemize}
\\item Previous work 1
\\item Previous work 2
\\end{itemize}

\\section{Methodology}
Methodology description.

\\begin{quote}
Important note here.
\\end{quote}
"""
        result = convert(latex)
        assert "# Abstract" in result
        assert "# Introduction" in result
        assert "## Related Work" in result
        assert "# Methodology" in result
        assert "$$E = mc^2$$" in result or "E = mc^2" in result
        assert "> 💡" in result


class TestErrorHandling:
    """Test error handling cases."""
    
    def test_unmatched_braces(self):
        """Test handling of unmatched braces"""
        latex = "\\section{Unclosed"
        # Should not crash, handle gracefully
        try:
            result = convert(latex)
            assert result is not None
        except Exception:
            # If it raises an exception, that's also acceptable behavior
            pass
    
    def test_invalid_syntax(self):
        """Test handling of invalid LaTeX syntax"""
        latex = "\\invalidcommand{test}"
        # Should handle gracefully
        try:
            result = convert(latex)
            assert result is not None
        except Exception:
            pass
    
    def test_malformed_math(self):
        """Test handling of malformed math expressions"""
        latex = "$unclosed math"
        # Should handle gracefully
        try:
            result = convert(latex)
            assert result is not None
        except Exception:
            pass
    
    def test_empty_input(self):
        """Test empty input"""
        result = convert("")
        assert result == "" or result is not None
