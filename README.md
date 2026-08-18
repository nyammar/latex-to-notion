# LaTeX to Notion Converter

A Python library that converts LaTeX documents to Notion-compatible format. The converter parses LaTeX syntax and outputs text that can be directly pasted into Notion, preserving structure, formatting, and mathematical notation.

## Features

- **Headings**: Converts `\section`, `\subsection`, `\subsubsection` to Notion headings
- **Math**: Supports inline math (`$...$`) and display math (`$$...$$`) using KaTeX-compatible syntax
- **Formatting**: Converts `\textbf`, `\textit`, `\texttt` to markdown formatting
- **Lists**: Supports both `itemize` (bullet) and `enumerate` (numbered) lists with nesting
- **Tables**: Converts LaTeX `tabular` and `table` environments to markdown tables
- **Code Blocks**: Converts `verbatim` and `lstlisting` environments to code blocks
- **Callouts**: Converts `quote` environments to Notion callouts
- **Links**: Converts `\href{url}{text}` to markdown links

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

## GUI Application

A graphical user interface is available for easy conversion:

```bash
python3 latex2notion_gui.py
```

**Features:**
- Split-pane view: LaTeX input on the left, Notion output on the right
- Open `.tex` files from disk
- Save output to `.md` or `.txt` files
- Auto-convert as you type (optional)
- Copy output to clipboard
- Keyboard shortcuts (Ctrl+O to open, Ctrl+S to save, etc.)

## Installation

First, install the package in development mode:

```bash
pip install -e .
```

Or install with development dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

### Basic Usage (Python Library)

The simplest way to use the converter is to import the `convert` function:

```python
from latex2notion import convert

latex_text = """
\\section{Introduction}
This is a paragraph with inline math: $x^2 + y^2 = z^2$.

\\subsection{Details}
Some \\textbf{bold} and \\textit{italic} text.
"""

notion_text = convert(latex_text)
print(notion_text)
```

### Running the Example Script

A complete example script is provided:

```bash
python3 example.py
```

This will demonstrate various conversion examples.

### Converting a LaTeX File

You can read a LaTeX file and convert it:

```python
from latex2notion import convert

# Read LaTeX from file
with open('document.tex', 'r') as f:
    latex_content = f.read()

# Convert to Notion format
notion_content = convert(latex_content)

# Save or print the result
print(notion_content)
# Or save to file:
# with open('notion_output.md', 'w') as f:
#     f.write(notion_content)
```

### With Options

```python
notion_text = convert(
    latex_string,
    math_mode='katex',  # Ensure KaTeX compatibility (default)
    heading_level_offset=0,  # Adjust heading levels (0 = no change)
    preserve_comments=False  # Remove LaTeX comments (default: False)
)

# Example: Shift all headings down by one level
notion_text = convert(latex_string, heading_level_offset=1)
# \section becomes ## instead of #
```

### Command Line Usage (Simple Script)

You can create a simple CLI script. Create a file `latex2notion_cli.py`:

```python
#!/usr/bin/env python3
import sys
from latex2notion import convert

if len(sys.argv) < 2:
    print("Usage: python3 latex2notion_cli.py <input.tex> [output.md]")
    sys.exit(1)

input_file = sys.argv[1]
with open(input_file, 'r') as f:
    latex_content = f.read()

notion_content = convert(latex_content)

if len(sys.argv) >= 3:
    output_file = sys.argv[2]
    with open(output_file, 'w') as f:
        f.write(notion_content)
    print(f"Converted {input_file} to {output_file}")
else:
    print(notion_content)
```

Then use it:

```bash
python3 latex2notion_cli.py example.tex output.md
# Or just print to stdout:
python3 latex2notion_cli.py example.tex
```

## Supported LaTeX Features

### Headings
- `\section{Title}` → `# Title`
- `\subsection{Title}` → `## Title`
- `\subsubsection{Title}` → `### Title`

### Math
- Inline: `$x^2$` → `$$x^2$$`
- Display: `$$\int_0^1 x dx$$` → Block math
- Also supports `\(...\)` and `\[...\]` syntax

### Formatting
- `\textbf{text}` → `**text**`
- `\textit{text}` → `*text*`
- `\texttt{text}` → `` `text` ``
- `\href{url}{text}` → `[text](url)`

### Lists
- `\begin{itemize}...\end{itemize}` → Bullet lists
- `\begin{enumerate}...\end{enumerate}` → Numbered lists
- Supports nested lists

### Tables
- `\begin{tabular}...\end{tabular}` → Markdown tables
- `\begin{table}...\end{table}` → Markdown tables

### Code Blocks
- `\begin{verbatim}...\end{verbatim}` → Code blocks
- `\begin{lstlisting}...\end{lstlisting}` → Code blocks

### Callouts
- `\begin{quote}...\end{quote}` → Notion callouts

## Testing

Run tests with pytest:

```bash
pytest
```

With coverage:

```bash
pytest --cov=latex2notion
```

## Limitations

- Notion uses KaTeX for math rendering, which supports most LaTeX math but not all commands
- Some LaTeX features may not have direct Notion equivalents
- Complex LaTeX environments may require manual adjustment
- Custom LaTeX commands are not supported

## License

Licensed under the [MIT License](LICENSE).
