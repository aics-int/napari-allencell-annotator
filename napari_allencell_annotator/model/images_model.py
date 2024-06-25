from typing import Dict, List


class ImagesModel:
    def __init__(self):
        self._files_dict: Dict[str, List[str]] = {}

    def get_files_dict(self) -> Dict[str, List[str]]:
        return self._files_dict

    def set_files_dict(self, files_dict: Dict[str, List[str]]) -> None:
        self._files_dict = files_dict

    def get_num_files(self) -> int:
        return len(self.get_files_dict())
