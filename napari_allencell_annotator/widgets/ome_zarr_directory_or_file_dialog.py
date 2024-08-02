import os
from pathlib import Path

from PyQt5.QtWidgets import QListView, QAbstractItemView, QTreeView
from qtpy.QtWidgets import QFileDialog
from napari_allencell_annotator.util.file_utils import FileUtils


class OmeZarrDirectoryOrFileDialog(QFileDialog):
    def __init__(self):
        super().__init__()
        self.currentChanged.connect(self._selected)
        self.setFileMode(QFileDialog.Directory)
        self.setNameFilter("Directories and files (*)")
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.findChild(QListView, "listView").setSelectionMode(QAbstractItemView.ExtendedSelection)

        f_tree_view = self.findChild(QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def _selected(self, name: str) -> None:
        """
        Called whenever the user selects a new option in the File Dialog menu.
        """
        path: Path = Path(name)
        if os.path.isdir(path) and FileUtils.is_ome_zarr(path):
            self.setFileMode(QFileDialog.Directory)
            self.setNameFilter("Directories and files (*)")
            self.setOption(QFileDialog.DontUseNativeDialog, True)
            self.findChild(QListView, "listView").setSelectionMode(QAbstractItemView.ExtendedSelection)

            f_tree_view = self.findChild(QTreeView)
            if f_tree_view:
                f_tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        else:
            self.setFileMode(QFileDialog.ExistingFiles)

    def accept(self):
        self.setFileMode(QFileDialog.Directory)

        super().accept()
