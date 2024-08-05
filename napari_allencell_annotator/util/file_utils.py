import random
from pathlib import Path
from napari_allencell_annotator.constants.constants import SUPPORTED_FILE_TYPES


class FileUtils:
    """
    Handles file and directory related functions.
    """

    @staticmethod
    def select_valid_images(file_list: list[Path]) -> list[Path]:
        """
        Return a list of paths to files that are not hidden and is either a valid image file or a valid zarr image.

        Parameters
        ----------
        file_list: list[Path]
            A list of paths
        """
        valid_files: list[Path] = []
        for file in file_list:
            # is not hidden
            if not file.name.startswith("."):
                # all supported files including raw zarr
                if FileUtils.is_supported(file):
                    valid_files.append(file)
                # if zarr outer folder was selected instead
                elif FileUtils._is_outer_zarr(file):
                    valid_files.append(FileUtils._get_raw_zarr_from_outer_dir(file))

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
        """
        Shuffles the file list.

        Parameters
        ----------
        files: list[Path]
            A file list to be shuffled

        Returns
        -------
        list[Path]
            The shuffled file list
        """
        shuffled_list = files.copy()
        random.shuffle(shuffled_list)
        return shuffled_list

    @staticmethod
    def get_file_name(path: Path) -> str:
        """
        Return the parent file name for zarr. Otherwise, return the file name.

        Parameters
        ----------
        path: Path
            The path to an image file
        """
        if path.suffix == ".zarr":
            return path.parent.stem
        else:
            return path.name

    @staticmethod
    def _is_outer_zarr(path: Path) -> bool:
        """
        Return whether a given path is the outer directory of a raw zarr.

        Parameters
        ----------
        path: Path
            The path to a directory
        """
        if list(path.glob("*.zarr")):
            return True
        else:
            return False

    @staticmethod
    def _get_raw_zarr_from_outer_dir(path: Path) -> Path:
        """
        Returns the path to the raw zarr in a given directory

        Parameters
        ----------
        path: Path
            The path to an outer zarr directory
        """
        return path.glob("*.zarr").__next__()
