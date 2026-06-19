import os
from pathlib import Path

class PersonaLoader:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)

    def _read_file(self, filename: str) -> str:
        filepath = self.config_dir / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def load_soul(self) -> str:
        return self._read_file("SOUL.md")

    def load_empathy(self) -> str:
        return self._read_file("EMPATHY.md")

    def load_rational(self) -> str:
        return self._read_file("RATIONAL.md")
