from typing import Dict, List
from napari_allencell_annotator.widgets.file_item import FileItem
from pathlib import Path


class ImagesModel:
    def __init__(self):
        self._files_dict: Dict[str, List[str]] = {}

    def get_files_dict(self) -> Dict[str, List[str]]:
        return self._files_dict

    def set_files_dict(self, files_dict: Dict[str, List[str]]) -> None:
        self._files_dict = files_dict

    def get_num_files(self) -> int:
        return len(self._files_dict)

    def remove_item(self, item: FileItem):
        del self._files_dict[item.file_path]

    def add_item(self, file):
        self._files_dict[file] = [self.get_name(file), ""]

    def get_name(self, file):
        """Return basename"""
        return Path(file).stem
