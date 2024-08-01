import os
from pathlib import Path

from qtpy.QtWidgets import QFileDialog
from napari_allencell_annotator.util.file_utils import FileUtils


class OmeZarrDirectoryOrFileDialog(QFileDialog):
    def __init__(self):
        super().__init__()
        self.setOption(QFileDialog.DontUseNativeDialog)
        self.setFileMode(QFileDialog.Directory)
        self.currentChanged.connect(self._selected)
        self.setNameFilter("Directories and files (*)")

    def _selected(self, name: str) -> None:
        """
        Called whenever the user selects a new option in the File Dialog menu.
        """
        path: Path = Path(name)
        if os.path.isdir(path) and FileUtils.is_ome_zarr(path):
            self.setFileMode(QFileDialog.Directory)
            self.setNameFilter("Directories and files (*)")
        else:
            self.setFileMode(QFileDialog.ExistingFiles)
