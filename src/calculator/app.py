import tkinter as tk
import platform
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except (ImportError, AttributeError):
    pass

from src.calculator.logic import CalculatorLogic
from src.calculator.ui import CalculatorUI, HistoryPanel
from src.calculator.history import History
from src.calculator.theme import ThemeManager

class Application:
    """The main application class for the calculator."""
    def __init__(self, root: tk.Tk):
        """
        Initializes the application.

        Args:
            root: The root Tkinter window.
        """
        self.root = root
        self.logic = CalculatorLogic()
        self.history = History()
        self.theme_manager = ThemeManager()
        self.ui = CalculatorUI(self.root, self.on_button_press, self.on_toggle_scientific, self.on_copy_to_clipboard, self.on_show_history, self.on_toggle_theme, self.theme_manager)

    def on_button_press(self, value: str):
        """
        Handles a button press event from the UI.

        Args:
            value: The value of the button that was pressed.
        """
        expression_before = self.logic.expression
        self.logic.on_button_press(value)
        self.ui.update_display(self.logic.get_display_text())

        if value == '=' and self.logic.result != "Error":
            self.history.add_entry(expression_before, self.logic.result)

    def on_toggle_scientific(self):
        """Handles the event to toggle scientific mode."""
        pass

    def on_copy_to_clipboard(self):
        """Handles the event to copy the display text to the clipboard."""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.logic.get_display_text())

    def on_show_history(self):
        """Handles the event to show the history panel."""
        HistoryPanel(self.root, self.history.get_history(), self.on_clear_history, self.theme_manager)

    def on_clear_history(self):
        """Handles the event to clear the calculation history."""
        self.history.clear_history()

    def on_toggle_theme(self):
        """Handles the event to toggle the theme."""
        self.theme_manager.toggle_theme()

    def run(self):
        """Runs the main application loop."""
        self.root.mainloop()

def main():
    """The main entry point for the application."""
    root = tk.Tk()
    app = Application(root)
    app.run()
