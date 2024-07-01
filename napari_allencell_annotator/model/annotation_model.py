import json
from pathlib import Path

from napari_allencell_annotator.model.annotation_keys import AnnotationKeys
from napari_allencell_annotator.model.combo_key import ComboKey
from napari_allencell_annotator.model.key import Key
from napari_allencell_annotator.util.json_utils import JSONUtils


class AnnotationModel:

    def __init__(self):
        self._annotation_keys: dict[str, Key] = AnnotationKeys()

    def get_annotation_keys(self) -> dict[str, Key]:
        return self._annotation_keys

    def clear_annotation_keys(self) -> None:
        self._annotation_keys.clear()

    def set_annotation_keys(self, annotation_keys: dict[str, Key]) -> None:
        self._annotation_keys = annotation_keys