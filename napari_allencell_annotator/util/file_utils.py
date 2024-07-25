import random
from pathlib import Path
from napari_allencell_annotator.constants.constants import SUPPORTED_FILE_TYPES
from typing import List


class FileUtils:
    """
    Handles file and directory related functions.
    """

    @staticmethod
    def select_only_valid_files(file_list: list[Path]) -> list[Path]:
        """
        Return a list of paths to files that are not hidden.

        Parameters
        ----------
        file_list: list[Path]
            A list of paths
        """
        valid_files: List[Path] = []
        for file in file_list:
            if not file.name.startswith("."):
                # get files
                if file.is_file():
                    valid_files.append(file)
                # get zarr file
                elif file.is_dir() and file.name.endswith(".zarr"):
                    valid_files.append(file)
                # get zarr inside the directory
                else:
                    dir_zarr_files: List[Path] = list(file.glob("*.zarr"))
                    valid_files += dir_zarr_files

        return valid_files

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
        extension: str = file_path.suffix
        return extension in SUPPORTED_FILE_TYPES

    @staticmethod
    def get_sorted_dirs_and_files_in_dir(dir_path: Path) -> list[Path]:
        """
        Return a sorted list of paths to files in a directory.

        Parameters
        ----------
        dir_path: list[Path]
            The path to a directory
        """

        return sorted(list(dir_path.glob("*")))

    @staticmethod
    def shuffle_file_list(files: list[Path]) -> list[Path]:
        shuffled_list = files.copy()
        random.shuffle(shuffled_list)
        return shuffled_list

    @staticmethod
    def get_file_name(path: Path):
        if path.suffix == ".zarr":
            return path.parent.stem
        else:
            return path.name

