#!/usr/bin/env python3
"""
GUI Application for LaTeX to Notion Converter

A graphical interface with:
- Left panel: LaTeX input
- Right panel: Notion output
- File operations: Open .tex files, Save output
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sys
import os

# Add the latex2notion directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'latex2notion'))
from latex2notion import convert


class LaTeX2NotionGUI:
    """Main GUI application class."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("LaTeX to Notion Converter")
        self.root.geometry("1200x700")
        self.root.minsize(800, 500)
        
        # Current file path
        self.current_file = None
        
        # Auto-convert on text change (with debounce)
        self.auto_convert_var = tk.BooleanVar(value=True)
        self.convert_timer = None
        
        # Create UI
        self.create_menu()
        self.create_widgets()
    
    def create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open LaTeX File...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Output...", command=self.save_output, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Clear All", command=self.clear_all, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Convert", command=self.convert_text, accelerator="Ctrl+R")
        edit_menu.add_checkbutton(label="Auto-convert", variable=self.auto_convert_var)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_output())
        self.root.bind('<Control-n>', lambda e: self.clear_all())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-r>', lambda e: self.convert_text())
    
    def create_widgets(self):
        """Create main widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(toolbar, text="Open File", command=self.open_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Convert", command=self.convert_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Save Output", command=self.save_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Auto-convert checkbox
        ttk.Checkbutton(toolbar, text="Auto-convert", variable=self.auto_convert_var).pack(side=tk.LEFT, padx=20)
        
        # Status label
        self.status_label = ttk.Label(toolbar, text="Ready", foreground="green")
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Paned window for split view
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Left panel - LaTeX Input
        left_frame = ttk.Frame(paned, padding="5")
        paned.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="LaTeX Input", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        # Input text area with scrollbar
        input_frame = ttk.Frame(left_frame)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            font=("Courier", 11),
            undo=True
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        self.input_text.bind('<KeyRelease>', self.on_input_change)
        self.input_text.bind('<Button-1>', self.on_input_change)
        
        # Right panel - Notion Output
        right_frame = ttk.Frame(paned, padding="5")
        paned.add(right_frame, weight=1)
        
        ttk.Label(right_frame, text="Notion Output", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        # Output text area with scrollbar
        output_frame = ttk.Frame(right_frame)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Courier", 11),
            state=tk.DISABLED,
            bg="#f5f5f5"
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Copy button for output
        copy_frame = ttk.Frame(right_frame)
        copy_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(copy_frame, text="Copy to Clipboard", command=self.copy_output).pack(side=tk.LEFT)
        
        # Load sample text
        self.load_sample()
    
    def on_input_change(self, event=None):
        """Handle input text changes with auto-convert."""
        if self.auto_convert_var.get():
            # Cancel previous timer
            if self.convert_timer:
                self.root.after_cancel(self.convert_timer)
            
            # Schedule conversion after 500ms of no typing
            self.convert_timer = self.root.after(500, self.convert_text)
    
    def convert_text(self):
        """Convert LaTeX to Notion format."""
        latex_input = self.input_text.get("1.0", tk.END).strip()
        
        if not latex_input:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.config(state=tk.DISABLED)
            self.update_status("No input to convert", "orange")
            return
        
        try:
            notion_output = convert(latex_input)
            
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", notion_output)
            self.output_text.config(state=tk.DISABLED)
            
            self.update_status("Conversion successful", "green")
        except Exception as e:
            error_msg = f"Conversion error: {str(e)}"
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", error_msg)
            self.output_text.config(state=tk.DISABLED)
            self.update_status("Conversion failed", "red")
            messagebox.showerror("Conversion Error", f"An error occurred:\n{str(e)}")
    
    def open_file(self):
        """Open a LaTeX file."""
        file_path = filedialog.askopenfilename(
            title="Open LaTeX File",
            filetypes=[
                ("LaTeX files", "*.tex"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
            initialdir=os.getcwd()
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", content)
                self.current_file = file_path
                self.update_status(f"Opened: {os.path.basename(file_path)}", "green")
                
                # Auto-convert if enabled
                if self.auto_convert_var.get():
                    self.convert_text()
            except Exception as e:
                messagebox.showerror("File Error", f"Could not open file:\n{str(e)}")
                self.update_status("File open failed", "red")
    
    def save_output(self):
        """Save the output to a file."""
        output_content = self.output_text.get("1.0", tk.END).strip()
        
        if not output_content:
            messagebox.showwarning("No Content", "There is no output to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Notion Output",
            defaultextension=".md",
            filetypes=[
                ("Markdown files", "*.md"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
            initialdir=os.getcwd()
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(output_content)
                
                self.update_status(f"Saved: {os.path.basename(file_path)}", "green")
                messagebox.showinfo("Success", f"Output saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file:\n{str(e)}")
                self.update_status("Save failed", "red")
    
    def copy_output(self):
        """Copy output to clipboard."""
        output_content = self.output_text.get("1.0", tk.END).strip()
        
        if not output_content:
            messagebox.showwarning("No Content", "There is no output to copy.")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(output_content)
        self.update_status("Copied to clipboard", "green")
    
    def clear_all(self):
        """Clear both input and output."""
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all text?"):
            self.input_text.delete("1.0", tk.END)
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.config(state=tk.DISABLED)
            self.current_file = None
            self.update_status("Cleared", "blue")
    
    def update_status(self, message, color="black"):
        """Update status label."""
        self.status_label.config(text=message, foreground=color)
        # Clear status after 3 seconds
        self.root.after(3000, lambda: self.status_label.config(text="Ready", foreground="green"))
    
    def load_sample(self):
        """Load sample LaTeX text."""
        sample = """\\section{Introduction}
This is a sample LaTeX document. You can edit this text or open a .tex file.

\\subsection{Mathematical Expressions}
Here's some inline math: $E = mc^2$ and $x^2 + y^2 = z^2$.

Display math:
$$\\int_0^1 x dx = \\frac{1}{2}$$

\\subsection{Formatting}
This text has \\textbf{bold}, \\textit{italic}, and \\texttt{code} formatting.

\\subsection{Lists}
\\begin{itemize}
\\item First bullet point
\\item Second bullet point with \\textbf{bold text}
\\item Third point with math: $f(x) = x^2$
\\end{itemize}

\\begin{enumerate}
\\item First numbered item
\\item Second numbered item
\\end{enumerate}

\\subsection{Code Block}
\\begin{verbatim}
def hello_world():
    print("Hello, World!")
    return True
\\end{verbatim}

\\subsection{Quote}
\\begin{quote}
This is a quote that will become a callout in Notion.
\\end{quote}

\\subsection{Links}
Visit \\href{https://www.example.com}{Example Website} for more information.
"""
        self.input_text.insert("1.0", sample)
        if self.auto_convert_var.get():
            self.convert_text()
    
    def show_about(self):
        """Show about dialog."""
        about_text = """LaTeX to Notion Converter

A GUI application for converting LaTeX documents to Notion-compatible format.

Features:
• Split-pane view for input and output
• Open .tex files
• Save output to .md files
• Auto-convert on typing
• Copy to clipboard

Version: 0.1.0
"""
        messagebox.showinfo("About", about_text)


def main():
    """Main entry point."""
    root = tk.Tk()
    app = LaTeX2NotionGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
