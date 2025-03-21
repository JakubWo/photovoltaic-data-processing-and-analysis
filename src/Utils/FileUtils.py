import os

from pathlib import Path

class FileUtils:
    @staticmethod
    def get_absolute_path(filename: str) -> str:
        return str(Path(__file__).resolve().parent.parent.parent) + FileUtils.get_path(filename)

    @staticmethod
    def get_path(path: str) -> str:
        return path.replace('/', os.sep)

