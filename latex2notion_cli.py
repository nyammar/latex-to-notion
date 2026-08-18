#!/usr/bin/env python3
"""
Command-line interface for latex2notion converter.

Usage:
    python3 latex2notion_cli.py <input.tex> [output.md]
    
If output file is not specified, output is printed to stdout.
"""

import sys
from latex2notion import convert


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 latex2notion_cli.py <input.tex> [output.md]")
        print("\nExamples:")
        print("  python3 latex2notion_cli.py document.tex")
        print("  python3 latex2notion_cli.py document.tex output.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            latex_content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        notion_content = convert(latex_content)
    except Exception as e:
        print(f"Error converting LaTeX: {e}", file=sys.stderr)
        sys.exit(1)
    
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(notion_content)
            print(f"✓ Converted {input_file} to {output_file}")
        except Exception as e:
            print(f"Error writing file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(notion_content)


if __name__ == '__main__':
    main()
