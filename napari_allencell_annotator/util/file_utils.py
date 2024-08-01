import os.path
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
        return [
            file
            for file in file_list
            if not file.name.startswith(".") and file.is_file() and FileUtils.is_supported(file)
        ]

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

    @staticmethod
    def is_ome_zarr(path: Path):
        if path.name.endswith(".ome.zarr") or len(list(path.glob("*.ome.zarr"))) != 0:
            return True
        else:
            return False

    @staticmethod
    def select_only_ome_zarr(path_list: List[Path]) -> List[Path]:
        valid_dirs = [path for path in path_list if not path.name.startswith(".") and os.path.isdir(path)]

        ome_zarr_dirs = []
        for valid_dir in valid_dirs:
            if valid_dir.name.endswith(".ome.zarr"):
                ome_zarr_dirs.append(valid_dir)
            else:
                ome_zarr_files: List[Path] = list(valid_dir.glob("*.zarr"))
                ome_zarr_dirs += ome_zarr_files

        return ome_zarr_dirs

    @staticmethod
    def select_valid_images(path_list: List[Path]):
        return FileUtils.select_only_valid_files(path_list) + FileUtils.select_only_ome_zarr(path_list)
