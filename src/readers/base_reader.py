from abc import ABC, abstractmethod
from pathlib import Path


class BaseReader(ABC):
    def __init__(self, filepath: Path) -> None:
        if not filepath.exists():
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        self.filepath = filepath

    @abstractmethod
    def read(self): ...
