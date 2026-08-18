#!/usr/bin/env python3
"""
Example script demonstrating how to use latex2notion.
"""

from latex2notion import convert

# Example 1: Simple document with headings and text
latex_example_1 = """
\\section{Introduction}
This is an introduction paragraph with some \\textbf{bold} text.

\\subsection{Details}
Here's a subsection with inline math: $x^2 + y^2 = z^2$.
"""

print("Example 1: Simple Document")
print("=" * 50)
notion_output = convert(latex_example_1)
print(notion_output)
print("\n")

# Example 2: Document with lists and math
latex_example_2 = """
\\section{Mathematical Concepts}

\\begin{itemize}
\\item The Pythagorean theorem: $a^2 + b^2 = c^2$
\\item Euler's identity: $e^{i\\pi} + 1 = 0$
\\end{itemize}

Display math:
$$\\int_0^1 x^2 dx = \\frac{1}{3}$$
"""

print("Example 2: Lists and Math")
print("=" * 50)
notion_output = convert(latex_example_2)
print(notion_output)
print("\n")

# Example 3: Complete document with multiple features
latex_example_3 = """
\\section{Research Paper}

\\subsection{Abstract}
This paper presents important findings.

\\begin{quote}
This is an important note that will become a callout in Notion.
\\end{quote}

\\subsection{Methodology}
We used the following approach:

\\begin{enumerate}
\\item Data collection
\\item Analysis with $\\alpha = 0.05$
\\item Results interpretation
\\end{enumerate}

\\begin{verbatim}
def analyze_data():
    return results
\\end{verbatim}

Visit our website: \\href{https://example.com}{Example Site}
"""

print("Example 3: Complete Document")
print("=" * 50)
notion_output = convert(latex_example_3)
print(notion_output)
print("\n")

# Example 4: Reading from a file
print("Example 4: Reading from file (if example.tex exists)")
print("=" * 50)
try:
    with open('example.tex', 'r') as f:
        latex_from_file = f.read()
    notion_output = convert(latex_from_file)
    print(notion_output)
except FileNotFoundError:
    print("No example.tex file found. Create one to test file reading.")
