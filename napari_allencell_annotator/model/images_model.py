from typing import Dict, List
from napari_allencell_annotator.widgets.file_item import FileItem
from pathlib import Path


class ImagesModel:
    """
    A class used to manage image files for annotation.

    Attributes
    ----------
    _files_dict: Dict[str, List[str]]
        A dictionary of file path -> [File Name, FMS]
        stores file order in insertion order of keys

    Methods
    -------
    get_files_dict() -> Dict[str, List[str]]
        Returns the dictionary of all image files.
    set_files_dict(files_dict: Dict[str, List[str]])
        Sets the dictionary to a new value.
    get_num_files() -> int
        Returns the number of files in the dictionary.
    remove_item(item: FileItem)
        Removes an item from the dictionary.
    add_item(file: str)
        Adds an item to the dictionary.
    get_name(file: str) -> str
        Returns the basename of a file.
    """

    def __init__(self):
        self._files_dict: Dict[str, List[str]] = {}

    def get_files_dict(self) -> Dict[str, List[str]]:
        """
        Return the dictionary of all image files.

        Returns
        -------
        Dict[str, List[str]]
            The dictionary of files. path -> [File Name, FMS]
        """
        return self._files_dict

    def set_files_dict(self, files_dict: Dict[str, List[str]]) -> None:
        """
        Set the dictionary to a new value.
        """
        self._files_dict = files_dict

    def get_num_files(self) -> int:
        """
        Return the number of files in the dictionary.

        Returns
        -------
        int
            The size of the dictionary
        """
        return len(self._files_dict)

    def remove_item(self, item: FileItem) -> None:
        """
        Remove an item from the dictionary.
        """
        del self._files_dict[item.file_path]

    def add_item(self, file: str) -> None:
        """
        Add an item to the dictionary.
        """
        self._files_dict[file] = [self.get_name(file), ""]

    def get_name(self, file: str) -> str:
        """
        Return the basename of a file.

        Returns
        -------
        str
            basename
        """
        return Path(file).stem
