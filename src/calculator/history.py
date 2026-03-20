from typing import List, Tuple

class History:
    def __init__(self):
        self._history: List[Tuple[str, str]] = []

    def add_entry(self, expression: str, result: str):
        self._history.append((expression, result))

    def get_history(self) -> List[Tuple[str, str]]:
        return self._history

    def clear_history(self):
        self._history.clear()
