from pathlib import Path
from napari_allencell_annotator.constants.constants import SUPPORTED_FILE_TYPES


class FileUtils:

    @staticmethod
    def select_only_valid_files(file_list: list[Path]) -> list[Path]:
        return [file for file in file_list if not file.name.startswith(".") and file.is_file()]

    @staticmethod
    def is_supported(file_path: Path) -> bool:
        """
        Check if the provided file name is a supported file.

        This function checks if the file name extension is in
        the supported file types files.

        Parameters
        ----------
        file_path : Path
            Name of the file to check.

        Returns
        -------
        bool
            True if the file is supported.
        """
        if file_path is None:
            return False
        extension: str = file_path.suffix
        if extension in SUPPORTED_FILE_TYPES:
            return True
        else:
            return False

    @staticmethod
    def get_files_in_dir(dir_path: Path) -> list[Path]:
        return list(dir_path.glob('*.*'))
