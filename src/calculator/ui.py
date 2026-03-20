import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Tuple
from src.calculator.theme import ThemeManager

class HistoryPanel(tk.Toplevel):
    def __init__(self, master, history: List[Tuple[str, str]], on_clear_history: Callable[[], None], theme_manager: ThemeManager):
        super().__init__(master)
        self.title("History")
        self.geometry("300x400")
        theme = theme_manager.get_theme()
        self.configure(background=theme["main_bg"])

        self.history = history
        self.on_clear_history = on_clear_history

        self.listbox = tk.Listbox(self, background=theme["main_bg"], foreground=theme["display_fg"], selectbackground=theme["active_bg"])
        self.listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        for expression, result in self.history:
            self.listbox.insert(tk.END, f"{expression} = {result}")

        clear_button = ttk.Button(self, text="Clear History", command=self.clear_history, style='Function.TButton')
        clear_button.pack(pady=10)

    def clear_history(self):
        self.on_clear_history()
        self.listbox.delete(0, tk.END)


class CalculatorUI:
    def __init__(self, root: tk.Tk, on_button_press: Callable[[str], None], on_toggle_scientific: Callable[[], None], on_copy_to_clipboard: Callable[[], None], on_show_history: Callable[[], None], on_toggle_theme: Callable[[], None], theme_manager: ThemeManager):
        self.root = root
        self.on_button_press = on_button_press
        self.on_toggle_scientific = on_toggle_scientific
        self.on_copy_to_clipboard = on_copy_to_clipboard
        self.on_show_history = on_show_history
        self.on_toggle_theme = on_toggle_theme
        self.theme_manager = theme_manager
        self.scientific_mode = False
        
        self.root.title("Calculator")
        self.root.geometry("400x600")
        self.root.resizable(True, True)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        
        self.display_var = tk.StringVar(value="0")
        self._create_display()

        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=10, pady=10)
        
        self.scientific_buttons_frame = ttk.Frame(self.main_frame)
        
        self._create_buttons()
        self._create_scientific_buttons()
        self._configure_styles()


    def _configure_styles(self):
        theme = self.theme_manager.get_theme()
        self.root.configure(background=theme["main_bg"])
        self.main_frame.configure(style='Main.TFrame')
        self.buttons_frame.configure(style='Main.TFrame')
        self.scientific_buttons_frame.configure(style='Main.TFrame')

        self.style.configure('Main.TFrame', background=theme["main_bg"])
        self.style.configure('Display.TLabel', background=theme["display_bg"], foreground=theme["display_fg"], font=('Helvetica', 48, 'bold'))
        self.style.configure('TButton', font=('Helvetica', 18), borderwidth=0, focuscolor=theme["main_bg"])
        self.style.map('TButton', background=[('active', theme["active_bg"])])
        
        self.style.configure('Digit.TButton', background=theme["button_bg"], foreground=theme["button_fg"])
        self.style.configure('Operator.TButton', background=theme["operator_bg"], foreground=theme["operator_fg"])
        self.style.configure('Function.TButton', background=theme["function_bg"], foreground=theme["function_fg"])
        self.style.configure('Scientific.TButton', background=theme["scientific_bg"], foreground=theme["scientific_fg"])

    def _create_display(self):
        display_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        display_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=20)
        
        self.display_label = ttk.Label(display_frame, textvariable=self.display_var, anchor='e', style='Display.TLabel')
        self.display_label.pack(expand=True, fill=tk.BOTH)

    def _create_buttons(self):
        button_layout = [
            ('Sci', 'Function.TButton'), ('Theme', 'Function.TButton'), ('AC', 'Function.TButton'), ('+/-', 'Function.TButton'), ('%', 'Function.TButton'), ('÷', 'Operator.TButton'),
            ('7', 'Digit.TButton'), ('8', 'Digit.TButton'), ('9', 'Digit.TButton'), ('x', 'Operator.TButton'),
            ('4', 'Digit.TButton'), ('5', 'Digit.TButton'), ('6', 'Digit.TButton'), ('-', 'Operator.TButton'),
            ('1', 'Digit.TButton'), ('2', 'Digit.TButton'), ('3', 'Digit.TButton'), ('+', 'Operator.TButton'),
            ('0', 'Digit.TButton'), ('.', 'Digit.TButton'), ('=', 'Operator.TButton'), ('Copy', 'Function.TButton'),
            ('History', 'Function.TButton')
        ]
        
        num_cols = 4
        # Clear existing buttons before creating new ones
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        for i, (text, style) in enumerate(button_layout):
            row = i // num_cols
            col = i % num_cols
            
            if text == 'Sci':
                button = ttk.Button(self.buttons_frame, text=text, style=style, command=self.toggle_scientific_mode)
            elif text == 'Copy':
                button = ttk.Button(self.buttons_frame, text=text, style=style, command=self.on_copy_to_clipboard)
            elif text == 'History':
                button = ttk.Button(self.buttons_frame, text=text, style=style, command=self.on_show_history)
            elif text == 'Theme':
                button = ttk.Button(self.buttons_frame, text=text, style=style, command=self.toggle_theme)
            else:
                button = ttk.Button(self.buttons_frame, text=text, style=style, command=lambda t=text: self.on_button_press(t))
            
            button.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
            
            if text == '0':
                button.grid(columnspan=2, sticky='nsew')
                self.buttons_frame.grid_columnconfigure(col + 1, weight=1)
            elif text == '=':
                 button.grid(row=row, column=col+1, sticky='nsew', padx=5, pady=5)

        for i in range(6):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(num_cols):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

    def _create_scientific_buttons(self):
        button_layout = [
            ('sin', 'Scientific.TButton'), ('cos', 'Scientific.TButton'), ('tan', 'Scientific.TButton'),
            ('log', 'Scientific.TButton'), ('ln', 'Scientific.TButton'), ('^', 'Scientific.TButton'),
            ('√', 'Scientific.TButton'), ('(', 'Scientific.TButton'), (')', 'Scientific.TButton'),
            ('MC', 'Scientific.TButton'), ('MR', 'Scientific.TButton'), ('M+', 'Scientific.TButton'), 
            ('M-', 'Scientific.TButton'),
        ]

        num_cols = 3
        for widget in self.scientific_buttons_frame.winfo_children():
            widget.destroy()

        for i, (text, style) in enumerate(button_layout):
            row = i // num_cols
            col = i % num_cols
            button = ttk.Button(self.scientific_buttons_frame, text=text, style=style, command=lambda t=text: self.on_button_press(t))
            button.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

        for i in range(5):
            self.scientific_buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(num_cols):
            self.scientific_buttons_frame.grid_columnconfigure(i, weight=1)

    def toggle_scientific_mode(self):
        self.scientific_mode = not self.scientific_mode
        if self.scientific_mode:
            self.scientific_buttons_frame.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT, padx=10, pady=10)
            self.root.geometry("600x600")
        else:
            self.scientific_buttons_frame.pack_forget()
            self.root.geometry("400x600")
        self.on_toggle_scientific()

    def toggle_theme(self):
        self.on_toggle_theme()
        self._configure_styles()
        self._create_buttons()
        self._create_scientific_buttons()

    def update_display(self, text: str):
        self.display_var.set(text)


