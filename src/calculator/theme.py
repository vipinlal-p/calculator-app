from typing import Dict, Any

class ThemeManager:
    def __init__(self):
        self.themes = {
            "dark": {
                "main_bg": "#1E1E1E",
                "display_bg": "#1E1E1E",
                "display_fg": "white",
                "button_bg": "#333333",
                "button_fg": "white",
                "operator_bg": "#FF9500",
                "operator_fg": "white",
                "function_bg": "#AFAFAF",
                "function_fg": "black",
                "scientific_bg": "#505050",
                "scientific_fg": "white",
                "active_bg": "#666666",
            },
            "light": {
                "main_bg": "#F0F0F0",
                "display_bg": "#F0F0F0",
                "display_fg": "black",
                "button_bg": "#E0E0E0",
                "button_fg": "black",
                "operator_bg": "#FF9500",
                "operator_fg": "white",
                "function_bg": "#D4D4D2",
                "function_fg": "black",
                "scientific_bg": "#C0C0C0",
                "scientific_fg": "black",
                "active_bg": "#CCCCCC",
            },
        }
        self.current_theme = "dark"

    def get_theme(self) -> Dict[str, Any]:
        return self.themes[self.current_theme]

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
