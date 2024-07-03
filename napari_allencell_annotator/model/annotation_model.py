import json
from enum import Enum
from pathlib import Path
from typing import Optional, Any

from PyQt5.QtCore import QObject
from qtpy.QtCore import Signal

from napari_allencell_annotator.model.combo_key import ComboKey
from napari_allencell_annotator.model.key import Key
from napari_allencell_annotator.util.json_utils import JSONUtils



class AnnotatorModel(QObject):

    image_changed: Signal = Signal()
    at_least_one_file_added: Signal = Signal(bool)
    def __init__(self):
        super().__init__()
        self._annotation_keys: dict[str, Key] = {} # dict of annotation key names-Key objects containing information about that key,
                                                   # such as default value, type, options
        self._added_images: list[Path] = []  # List of paths of added images
        self._images_shuffled: bool = False  # Whether or not user has selected shuffle images


        # THE FOLLOWING FIELDS ONLY ARE NEEDED WHEN ANNOTATING STARTS AND ARE INITIALIZED AFTER STARTING.
        self._curr_img_index: int = None        # Current image being annotated's index, None by default (when annotations have not started)
        self._previous_img_index: Optional[int] = None  # index of previously viewed image, None by default
        self._created_annotations: Optional[dict[Path, list[Any]]] = None # annotations that have been crated. If annotating has not started, is None by default.
                                                         # dict of image path -> annotations
        self._csv_save_path: Optional[Path] = None

    def get_annotation_keys(self) -> dict[str, Key]:
        return self._annotation_keys

    def clear_annotation_keys(self) -> None:
        self._annotation_keys.clear()

    def set_annotation_keys(self, annotation_keys: dict[str, Key]) -> None:
        self._annotation_keys = annotation_keys

    def add_image(self, file_item: Path) -> None:
        self._added_images.append(file_item)
        if len(self._added_images) > 0:
            self.at_least_one_file_added.emit(True)


    def get_all_images(self) -> list[Path]:
        return self._added_images

    def get_image_at(self, idx: int) -> Path:
        return self._added_images[idx]

    def get_num_images(self) -> int:
        return len(self._added_images)

    def set_all_images(self, list_of_img: list[Path]) -> None:
        self._added_images = list_of_img

    def clear_all_images(self) -> None:
        self._added_images = []
        self.at_least_one_file_added.emit(False)

    def remove_image(self, item: Path) -> None:
        self._added_images.remove(item)
        if len(self._added_images) < 1:
            self.at_least_one_file_added.emit(False)

    def set_images_shuffled(self, shuffled: bool) -> None:
        self._images_shuffled = shuffled

    def is_images_shuffled(self) -> bool:
        return self._images_shuffled

    def get_curr_img_index(self) -> int:
        return self._curr_img_index

    def set_curr_img_index(self, idx: int) -> None:
        self._previous_img_index = self.get_curr_img_index() # store previous image index
        self._curr_img_index = idx
        self.image_changed.emit()


    def get_curr_img(self) -> Path:
        return self._added_images[self._curr_img_index]

    def get_annotations(self) -> dict[Path, list[Any]]:
        return self._created_annotations

    def add_annotation(self, file_path: Path, annotation: list[Any]):
        self._created_annotations[file_path] = annotation

    def set_annotations(self, annotations: dict[Path, list[Any]]) -> None:
        self._created_annotations = annotations

    def set_previous_image_index(self, idx: int) -> None:
        self._previous_img_index = idx

    def get_previous_image_index(self) -> int:
        return self._previous_img_index

    def set_csv_save_path(self, path: Path) -> None:
        self._csv_save_path = path

    def get_csv_save_path(self) -> Path:
        return self._csv_save_path
