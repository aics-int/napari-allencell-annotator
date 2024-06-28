from pathlib import Path


class FileUtils:

    @staticmethod
    def select_only_valid_files(file_list: list[Path]) -> list[Path]:
        return [file for file in file_list if not file.name.startswith(".") and file.is_file()]
