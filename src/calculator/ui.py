import tkinter as tk
from tkinter import ttk, font
import platform
from typing import Callable, List, Tuple
from src.calculator.theme import ThemeManager

class HistoryPanel(tk.Toplevel):
    """A Toplevel window to display the calculation history."""
    def __init__(self, master, history: List[Tuple[str, str]], on_clear_history: Callable[[], None], theme_manager: ThemeManager):
        super().__init__(master)
        self.title("History")
        self.geometry("300x400")
        theme = theme_manager.get_theme()
        self.configure(background=theme["main_bg"])

        self.history = history
        self.on_clear_history = on_clear_history

        self.listbox = tk.Listbox(self, background=theme["main_bg"], foreground=theme["display_fg"], selectbackground=theme["active_bg"], borderwidth=0, highlightthickness=0)
        self.listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        for expression, result in self.history:
            self.listbox.insert(tk.END, f"{expression} = {result}")

        clear_button = ttk.Button(self, text="Clear History", command=self.clear_history, style='Function.TButton')
        clear_button.pack(pady=10, padx=10, fill=tk.X)

class CalculatorUI:
    """The main UI class for the calculator."""
    def __init__(self, root: tk.Tk, on_button_press: Callable[[str], None], on_toggle_scientific: Callable[[], None], on_copy_to_clipboard: Callable[[], None], on_show_history: Callable[[], None], on_toggle_theme: Callable[[], None], theme_manager: ThemeManager):
        self.root = root
        self.on_button_press = on_button_press
        self.on_toggle_scientific = on_toggle_scientific
        self.on_copy_to_clipboard = on_copy_to_clipboard
        self.on_show_history = on_show_history
        self.on_toggle_theme = on_toggle_theme
        self.theme_manager = theme_manager
        self.scientific_mode = False

        self._setup_fonts()
        
        self.root.title("Calculator")
        self.root.geometry("400x550")
        self.root.minsize(320, 500)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        self.display_var = tk.StringVar(value="0")
        self._create_display()
        
        self.buttons_container = ttk.Frame(self.main_frame, style='Main.TFrame')
        self.buttons_container.pack(expand=True, fill=tk.BOTH)

        self.buttons_frame = ttk.Frame(self.buttons_container, style='Main.TFrame')
        self.buttons_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(10, 5), pady=10)

        self.scientific_buttons_frame = ttk.Frame(self.buttons_container, style='Main.TFrame')

        self._create_buttons()
        self._create_scientific_buttons()
        self._configure_styles()

    def _setup_fonts(self):
        """Sets up platform-specific fonts."""
        system = platform.system()
        if system == "Windows":
            self.display_font_family = "Segoe UI"
            self.button_font_family = "Segoe UI"
        elif system == "Darwin": # macOS
            self.display_font_family = "Helvetica Neue"
            self.button_font_family = "Helvetica Neue"
        else: # Linux and others
            self.display_font_family = "DejaVu Sans"
            self.button_font_family = "DejaVu Sans"

    def _get_font_size(self, base_size: int) -> int:
        """Calculates font size based on DPI scaling."""
        scaling_factor = self.root.tk.call('tk', 'scaling')
        return int(base_size * scaling_factor)

    def _configure_styles(self):
        """Configures the styles for the UI elements based on the current theme."""
        theme = self.theme_manager.get_theme()
        
        display_font_size = self._get_font_size(48)
        button_font_size = self._get_font_size(16)
        
        self.root.configure(background=theme["main_bg"])
        self.main_frame.configure(style='Main.TFrame')
        self.buttons_container.configure(style='Main.TFrame')
        self.buttons_frame.configure(style='Main.TFrame')
        self.scientific_buttons_frame.configure(style='Main.TFrame')

        self.style.configure('Main.TFrame', background=theme["main_bg"])
        self.style.configure('Display.TLabel', background=theme["display_bg"], foreground=theme["display_fg"], font=(self.display_font_family, display_font_size, 'bold'))
        self.style.configure('TButton', font=(self.button_font_family, button_font_size), borderwidth=0, focuscolor=theme["main_bg"])
        self.style.map('TButton', background=[('active', theme["active_bg"])])
        
        self.style.configure('Digit.TButton', background=theme["button_bg"], foreground=theme["button_fg"])
        self.style.configure('Operator.TButton', background=theme["operator_bg"], foreground=theme["operator_fg"])
        self.style.configure('Function.TButton', background=theme["function_bg"], foreground=theme["function_fg"])
        self.style.configure('Scientific.TButton', background=theme["scientific_bg"], foreground=theme["scientific_fg"])

    def _create_display(self):
        """Creates the display area."""
        display_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        display_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=(20, 10))
        
        self.display_label = ttk.Label(display_frame, textvariable=self.display_var, anchor='e', style='Display.TLabel')
        self.display_label.pack(expand=True, fill=tk.BOTH)

    def _create_buttons(self):
        """Creates the standard calculator buttons."""
        button_layout = [
            ('Sci', 0, 0, 'Function.TButton'), ('Theme', 0, 1, 'Function.TButton'), ('AC', 0, 2, 'Function.TButton'), ('%', 0, 3, 'Function.TButton'), ('÷', 0, 4, 'Operator.TButton'),
            ('7', 1, 0, 'Digit.TButton'), ('8', 1, 1, 'Digit.TButton'), ('9', 1, 2, 'Digit.TButton'), ('x', 1, 4, 'Operator.TButton'),
            ('4', 2, 0, 'Digit.TButton'), ('5', 2, 1, 'Digit.TButton'), ('6', 2, 2, 'Digit.TButton'), ('-', 2, 4, 'Operator.TButton'),
            ('1', 3, 0, 'Digit.TButton'), ('2', 3, 1, 'Digit.TButton'), ('3', 3, 2, 'Digit.TButton'), ('+', 3, 4, 'Operator.TButton'),
            ('0', 4, 0, 'Digit.TButton', 2), ('.', 4, 2, 'Digit.TButton'), ('=', 4, 4, 'Operator.TButton')
        ]
        
        callbacks = {
            'Sci': self.toggle_scientific_mode,
            'Theme': self.toggle_theme,
            'Copy': self.on_copy_to_clipboard,
            'History': self.on_show_history
        }

        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        for item in button_layout:
            text, row, col, style = item[:4]
            colspan = item[4] if len(item) > 4 else 1

            cmd = callbacks.get(text, lambda t=text: self.on_button_press(t))
            button = ttk.Button(self.buttons_frame, text=text, style=style, command=cmd)
            button.grid(row=row, column=col, columnspan=colspan, sticky='nsew', padx=5, pady=5)

        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

    def _create_scientific_buttons(self):
        """Creates the scientific calculator buttons."""
        button_layout = [
            ('sin', 'Scientific.TButton'), ('cos', 'Scientific.TButton'), ('tan', 'Scientific.TButton'),
            ('log', 'Scientific.TButton'), ('ln', 'Scientific.TButton'), ('^', 'Scientific.TButton'),
            ('√', 'Scientific.TButton'), ('(', 'Scientific.TButton'), (')', 'Scientific.TButton'),
            ('MC', 'Scientific.TButton'), ('MR', 'Scientific.TButton'), ('M+', 'Scientific.TButton'), ('M-', 'Scientific.TButton'),
            ('Copy', 'Function.TButton'), ('History', 'Function.TButton')
        ]
        
        num_cols = 3
        for widget in self.scientific_buttons_frame.winfo_children():
            widget.destroy()

        for i, (text, style) in enumerate(button_layout):
            row = i // num_cols
            col = i % num_cols
            
            cmd = self.on_copy_to_clipboard if text == 'Copy' else self.on_show_history if text == 'History' else lambda t=text: self.on_button_press(t)
            button = ttk.Button(self.scientific_buttons_frame, text=text, style=style, command=cmd)
            button.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

        for i in range(5):
            self.scientific_buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(num_cols):
            self.scientific_buttons_frame.grid_columnconfigure(i, weight=1)
            
    def toggle_scientific_mode(self):
        """Toggles the scientific mode."""
        self.scientific_mode = not self.scientific_mode
        if self.scientific_mode:
            self.scientific_buttons_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=(5, 10), pady=10)
        else:
            self.scientific_buttons_frame.pack_forget()
        self.on_toggle_scientific()

    def toggle_theme(self):
        """Toggles the theme and reconfigures the styles."""
        self.on_toggle_theme()
        self._configure_styles()

    def update_display(self, text: str):
        """Updates the display with the given text."""
        self.display_var.set(text)


