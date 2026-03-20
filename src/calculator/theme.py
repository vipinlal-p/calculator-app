from typing import Dict, Any

class ThemeManager:
    def __init__(self):
        self.themes = {
            "dark": {
                "main_bg": "#2E2E2E",
                "display_bg": "#2E2E2E",
                "display_fg": "#FFFFFF",
                "button_bg": "#4F4F4F",
                "button_fg": "#FFFFFF",
                "operator_bg": "#FF9F0A",
                "operator_fg": "#FFFFFF",
                "function_bg": "#D4D4D2",
                "function_fg": "#000000",
                "scientific_bg": "#6E6E6E",
                "scientific_fg": "#FFFFFF",
                "active_bg": "#8E8E8E",
            },
            "light": {
                "main_bg": "#FFFFFF",
                "display_bg": "#FFFFFF",
                "display_fg": "#000000",
                "button_bg": "#F2F2F2",
                "button_fg": "#000000",
                "operator_bg": "#FF9F0A",
                "operator_fg": "#FFFFFF",
                "function_bg": "#E0E0E0",
                "function_fg": "#000000",
                "scientific_bg": "#D0D0D0",
                "scientific_fg": "#000000",
                "active_bg": "#EAEAEA",
            },
        }
        self.current_theme = "dark"

    def get_theme(self) -> Dict[str, Any]:
        return self.themes[self.current_theme]

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
