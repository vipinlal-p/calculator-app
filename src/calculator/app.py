import tkinter as tk
from src.calculator.logic import CalculatorLogic
from src.calculator.ui import CalculatorUI, HistoryPanel
from src.calculator.history import History
from src.calculator.theme import ThemeManager

class Application:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.logic = CalculatorLogic()
        self.history = History()
        self.theme_manager = ThemeManager()
        self.ui = CalculatorUI(self.root, self.on_button_press, self.on_toggle_scientific, self.on_copy_to_clipboard, self.on_show_history, self.on_toggle_theme, self.theme_manager)

    def on_button_press(self, value: str):
        expression_before = self.logic.expression
        self.logic.on_button_press(value)
        self.ui.update_display(self.logic.get_display_text())

        if value == '=' and self.logic.result != "Error":
            self.history.add_entry(expression_before, self.logic.result)

    def on_toggle_scientific(self):
        # Placeholder for any logic to run when toggling scientific mode
        pass

    def on_copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.logic.get_display_text())

    def on_show_history(self):
        HistoryPanel(self.root, self.history.get_history(), self.on_clear_history, self.theme_manager)

    def on_clear_history(self):
        self.history.clear_history()

    def on_toggle_theme(self):
        self.theme_manager.toggle_theme()

    def run(self):
        self.root.mainloop()

def main():
    root = tk.Tk()
    app = Application(root)
    app.run()
